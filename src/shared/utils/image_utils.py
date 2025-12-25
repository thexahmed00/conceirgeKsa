"""Image utility functions for processing and validating images."""

import base64
from io import BytesIO
from typing import Tuple, Optional
from PIL import Image

from src.domain.shared.exceptions import ValidationError


# Constants
MAX_IMAGE_SIZE_BYTES = 8 * 1024 * 1024  # 8MB
MAX_DISH_IMAGE_SIZE_BYTES = 500 * 1024  # 500KB for dish/item images in metadata
THUMBNAIL_SIZE = (200, 200)
VALID_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]
MIME_TO_FORMAT = {
    "image/jpeg": "JPEG",
    "image/png": "PNG",
    "image/webp": "WEBP",
}


def validate_mime_type(mime_type: str) -> bool:
    """Check if mime type is supported."""
    return mime_type in VALID_MIME_TYPES


def validate_image_size(image_data: bytes, max_size: int = MAX_IMAGE_SIZE_BYTES) -> bool:
    """Check if image size is within limit."""
    return len(image_data) <= max_size


def decode_base64_image(base64_string: str) -> bytes:
    """
    Decode a base64 string to bytes.
    
    Handles both plain base64 and data URI format (data:image/jpeg;base64,...).
    
    Args:
        base64_string: Base64 encoded image string
    
    Returns:
        Decoded image bytes
    
    Raises:
        ValidationError: If decoding fails
    """
    try:
        # Handle data URI format
        if base64_string.startswith("data:"):
            # Format: data:image/jpeg;base64,/9j/4AAQ...
            header, encoded = base64_string.split(",", 1)
            return base64.b64decode(encoded)
        else:
            return base64.b64decode(base64_string)
    except Exception as e:
        raise ValidationError(f"Invalid base64 image data: {str(e)}")


def encode_base64_image(image_data: bytes) -> str:
    """Encode image bytes to base64 string."""
    return base64.b64encode(image_data).decode("utf-8")


def extract_mime_type_from_data_uri(data_uri: str) -> Optional[str]:
    """
    Extract mime type from data URI format.
    
    Args:
        data_uri: Data URI string (e.g., "data:image/jpeg;base64,...")
    
    Returns:
        Mime type string or None if not a data URI
    """
    if data_uri.startswith("data:"):
        try:
            header = data_uri.split(",")[0]
            mime_type = header.split(":")[1].split(";")[0]
            return mime_type
        except (IndexError, ValueError):
            return None
    return None


def generate_thumbnail(
    image_data: bytes,
    size: Tuple[int, int] = THUMBNAIL_SIZE,
    output_format: str = "JPEG",
) -> bytes:
    """
    Generate a thumbnail from image data.
    
    Args:
        image_data: Original image bytes
        size: Thumbnail dimensions (width, height)
        output_format: Output format (JPEG, PNG, WEBP)
    
    Returns:
        Thumbnail image bytes
    
    Raises:
        ValidationError: If image processing fails
    """
    try:
        # Open image from bytes
        image = Image.open(BytesIO(image_data))
        
        # Convert to RGB if necessary (for JPEG output)
        if output_format == "JPEG" and image.mode in ("RGBA", "P"):
            # Create white background
            background = Image.new("RGB", image.size, (255, 255, 255))
            if image.mode == "P":
                image = image.convert("RGBA")
            background.paste(image, mask=image.split()[3] if len(image.split()) == 4 else None)
            image = background
        elif output_format == "JPEG" and image.mode != "RGB":
            image = image.convert("RGB")
        
        # Create thumbnail (maintains aspect ratio)
        image.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save to bytes
        output = BytesIO()
        image.save(output, format=output_format, quality=85, optimize=True)
        return output.getvalue()
    
    except Exception as e:
        raise ValidationError(f"Failed to generate thumbnail: {str(e)}")


def process_image(
    base64_string: str,
    mime_type: Optional[str] = None,
    max_size: int = MAX_IMAGE_SIZE_BYTES,
    generate_thumb: bool = True,
) -> Tuple[bytes, Optional[bytes], str]:
    """
    Process a base64 image: decode, validate, and optionally generate thumbnail.
    
    Args:
        base64_string: Base64 encoded image
        mime_type: Optional mime type (extracted from data URI if not provided)
        max_size: Maximum allowed size in bytes
        generate_thumb: Whether to generate a thumbnail
    
    Returns:
        Tuple of (image_data, thumbnail_data, mime_type)
    
    Raises:
        ValidationError: If validation fails
    """
    # Extract mime type from data URI if not provided
    if mime_type is None:
        mime_type = extract_mime_type_from_data_uri(base64_string)
    
    # Default to JPEG if still not determined
    if mime_type is None:
        mime_type = "image/jpeg"
    
    # Validate mime type
    if not validate_mime_type(mime_type):
        raise ValidationError(
            f"Unsupported image type: {mime_type}. Supported types: {VALID_MIME_TYPES}"
        )
    
    # Decode base64
    image_data = decode_base64_image(base64_string)
    
    # Validate size
    if not validate_image_size(image_data, max_size):
        max_mb = max_size / (1024 * 1024)
        actual_mb = len(image_data) / (1024 * 1024)
        raise ValidationError(
            f"Image size ({actual_mb:.2f}MB) exceeds maximum of {max_mb:.2f}MB"
        )
    
    # Generate thumbnail
    thumbnail_data = None
    if generate_thumb:
        output_format = MIME_TO_FORMAT.get(mime_type, "JPEG")
        thumbnail_data = generate_thumbnail(image_data, output_format=output_format)
    
    return image_data, thumbnail_data, mime_type


def process_dish_image(base64_string: str, mime_type: Optional[str] = None) -> str:
    """
    Process a dish/item image for storage in JSONB metadata.
    
    Validates size (500KB limit) and returns the base64 string.
    Does not generate thumbnail since these are already small display images.
    
    Args:
        base64_string: Base64 encoded image
        mime_type: Optional mime type
    
    Returns:
        Validated base64 string (can be stored in JSONB)
    
    Raises:
        ValidationError: If validation fails
    """
    # Decode to check size
    image_data = decode_base64_image(base64_string)
    
    if not validate_image_size(image_data, MAX_DISH_IMAGE_SIZE_BYTES):
        max_kb = MAX_DISH_IMAGE_SIZE_BYTES / 1024
        actual_kb = len(image_data) / 1024
        raise ValidationError(
            f"Dish image size ({actual_kb:.0f}KB) exceeds maximum of {max_kb:.0f}KB"
        )
    
    # Extract or validate mime type
    extracted_mime = extract_mime_type_from_data_uri(base64_string)
    final_mime = mime_type or extracted_mime or "image/jpeg"
    
    if not validate_mime_type(final_mime):
        raise ValidationError(
            f"Unsupported image type: {final_mime}. Supported types: {VALID_MIME_TYPES}"
        )
    
    # Return original base64 (keeping data URI format if present)
    return base64_string


def get_image_dimensions(image_data: bytes) -> Tuple[int, int]:
    """
    Get image dimensions.
    
    Args:
        image_data: Image bytes
    
    Returns:
        Tuple of (width, height)
    """
    try:
        image = Image.open(BytesIO(image_data))
        return image.size
    except Exception:
        return (0, 0)
