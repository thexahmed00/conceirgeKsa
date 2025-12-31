"""Admin Services API endpoints - vendor management."""

from fastapi import APIRouter, Depends, status, Query, HTTPException, Response

from src.application.service.dto.service_dto import (
    VendorCreateDTO,
    VendorUpdateDTO,
    VendorDetailDTO,
    VendorListResponseDTO,
    ImageCreateDTO,
    ImageReorderDTO,
    VendorImageDTO,
    ServiceCategoryResponseDTO,
    ServiceCategoryCreateDTO,
    ServiceCategoryUpdateDTO,
)
from src.application.service.use_cases.admin_vendor_use_cases import (
    CreateVendorUseCase,
    UpdateVendorUseCase,
    DeleteVendorUseCase,
)
from src.application.service.use_cases.vendor_image_use_cases import (
    AddVendorImageUseCase,
    DeleteVendorImageUseCase,
    ReorderVendorImagesUseCase,
)
from src.application.service.use_cases.service_vendor_use_cases import (
    ListVendorsByCategoryUseCase,
    GetVendorDetailUseCase,
)
from src.infrastructure.web.dependencies import (
    get_current_admin_user,
    get_create_vendor_use_case,
    get_update_vendor_use_case,
    get_delete_vendor_use_case,
    get_add_vendor_image_use_case,
    get_delete_vendor_image_use_case,
    get_reorder_vendor_images_use_case,
    get_list_vendors_by_category_use_case,
    get_vendor_detail_use_case,
    get_create_category_use_case,
    get_update_category_use_case,
    get_service_category_repository,
)
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/admin/services",
    tags=["admin-services"],
)


# =============================================================================
# Vendor CRUD
# =============================================================================

@router.post("/vendors", response_model=VendorDetailDTO, status_code=status.HTTP_201_CREATED)
def create_vendor(
    dto: VendorCreateDTO,
    admin_id: int = Depends(get_current_admin_user),
    use_case: CreateVendorUseCase = Depends(get_create_vendor_use_case),
) -> VendorDetailDTO:
    """
    Create a new vendor.
    
    Admin only. Creates a vendor under the specified category.
    """
    result = use_case.execute(dto)
    logger.info(f"Vendor created: id={result.id}, name={result.name}, by admin={admin_id}")
    return result


@router.get("/vendors", response_model=VendorListResponseDTO)
def list_all_vendors(
    category_slug: str = Query(None, description="Filter by category slug"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    admin_id: int = Depends(get_current_admin_user),
    use_case: ListVendorsByCategoryUseCase = Depends(get_list_vendors_by_category_use_case),
) -> VendorListResponseDTO:
    """
    List vendors (admin view).
    
    Optionally filter by category slug. Includes inactive vendors.
    """
    if category_slug:
        return use_case.execute(category_slug=category_slug, skip=skip, limit=limit)
    # If no category specified, we need a different use case
    # For now, require category_slug
    return VendorListResponseDTO(vendors=[], total=0, skip=skip, limit=limit)


@router.get("/vendors/{vendor_id}", response_model=VendorDetailDTO)
def get_vendor(
    vendor_id: int,
    admin_id: int = Depends(get_current_admin_user),
    use_case: GetVendorDetailUseCase = Depends(get_vendor_detail_use_case),
) -> VendorDetailDTO:
    """
    Get vendor details (admin view).
    """
    return use_case.execute(vendor_id)


@router.put("/vendors/{vendor_id}", response_model=VendorDetailDTO)
def update_vendor(
    vendor_id: int,
    dto: VendorUpdateDTO,
    admin_id: int = Depends(get_current_admin_user),
    use_case: UpdateVendorUseCase = Depends(get_update_vendor_use_case),
) -> VendorDetailDTO:
    """
    Update vendor details.
    
    Admin only. Update name, description, contact info, rating, metadata, or status.
    """
    result = use_case.execute(vendor_id, dto)
    logger.info(f"Vendor updated: id={vendor_id}, by admin={admin_id}")
    return result


@router.delete("/vendors/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor(
    vendor_id: int,
    hard_delete: bool = Query(False, description="Permanently delete (True) or deactivate (False)"),
    admin_id: int = Depends(get_current_admin_user),
    use_case: DeleteVendorUseCase = Depends(get_delete_vendor_use_case),
) -> None:
    """
    Delete or deactivate a vendor.
    
    By default, soft deletes (deactivates). Use hard_delete=true for permanent deletion.
    """
    use_case.execute(vendor_id, hard_delete=hard_delete)
    logger.info(f"Vendor {'deleted' if hard_delete else 'deactivated'}: id={vendor_id}, by admin={admin_id}")


# =============================================================================
# Vendor Images
# =============================================================================

@router.post("/vendors/{vendor_id}/images", response_model=VendorImageDTO, status_code=status.HTTP_201_CREATED)
def add_vendor_image(
    vendor_id: int,
    dto: ImageCreateDTO,
    admin_id: int = Depends(get_current_admin_user),
    use_case: AddVendorImageUseCase = Depends(get_add_vendor_image_use_case),
) -> VendorImageDTO:
    """
    Add an image to a vendor.
    
    Supports 'hero' (carousel) or 'gallery' image types.
    Max size: 8MB. Thumbnail is auto-generated.
    """
    result = use_case.execute(vendor_id, dto)
    logger.info(f"Image added to vendor {vendor_id}: id={result.id}, type={result.image_type}, by admin={admin_id}")
    return result


# =============================================================================
# Service Categories (admin)
# =============================================================================


@router.post("/categories", response_model=ServiceCategoryResponseDTO, status_code=status.HTTP_201_CREATED)
def create_category(
    dto: ServiceCategoryCreateDTO,
    admin_id: int = Depends(get_current_admin_user),
    use_case = Depends(get_create_category_use_case),
) -> ServiceCategoryResponseDTO:
    """Create a new service category (admin only)."""
    try:
        result = use_case.execute(dto)
    except ValueError as e:
        # Covers both invalid icon_url and duplicate slug (from repo)
        raise HTTPException(status_code=400, detail=str(e))

    logger.info(f"Category created: id={result.id}, slug={result.slug}, by admin={admin_id}")
    return result


@router.put("/categories/{category_id}", response_model=ServiceCategoryResponseDTO)
def update_category(
    category_id: int,
    dto: ServiceCategoryUpdateDTO,
    admin_id: int = Depends(get_current_admin_user),
    use_case = Depends(get_update_category_use_case),
) -> ServiceCategoryResponseDTO:
    """Update an existing service category (admin only)."""
    try:
        result = use_case.execute(category_id, dto)
    except ValueError:
        raise HTTPException(status_code=404, detail="Category not found")

    logger.info(f"Category updated: id={category_id}, by admin={admin_id}")
    return result



@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    admin_id: int = Depends(get_current_admin_user),
    category_repo = Depends(get_service_category_repository),
) -> Response:
    """Delete a service category (admin only). Returns 204 on success, 404 if not found."""
    success = category_repo.delete(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")

    logger.info(f"Category deleted: id={category_id}, by admin={admin_id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/vendors/{vendor_id}/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor_image(
    vendor_id: int,
    image_id: int,
    admin_id: int = Depends(get_current_admin_user),
    use_case: DeleteVendorImageUseCase = Depends(get_delete_vendor_image_use_case),
) -> None:
    """
    Delete an image from a vendor.
    """
    use_case.execute(vendor_id, image_id)
    logger.info(f"Image {image_id} deleted from vendor {vendor_id}, by admin={admin_id}")


@router.put("/vendors/{vendor_id}/images/{image_type}/reorder", status_code=status.HTTP_200_OK)
def reorder_vendor_images(
    vendor_id: int,
    image_type: str,
    dto: ImageReorderDTO,
    admin_id: int = Depends(get_current_admin_user),
    use_case: ReorderVendorImagesUseCase = Depends(get_reorder_vendor_images_use_case),
) -> dict:
    """
    Reorder images of a specific type.
    
    Pass image_type as 'hero' or 'gallery'.
    Provide image_ids in desired order.
    """
    success = use_case.execute(vendor_id, image_type, dto)
    logger.info(f"Images reordered for vendor {vendor_id}, type={image_type}, by admin={admin_id}")
    return {"success": success}
