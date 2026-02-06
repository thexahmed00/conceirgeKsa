"""Services API endpoints - user-facing service discovery."""

from fastapi import APIRouter, Depends, Query, Response

from src.application.service.dto.service_dto import (
    ServiceCategoryListResponseDTO,
    ServiceSubcategoryListResponseDTO,
    VendorListResponseDTO,
    VendorDetailDTO,
    VendorImageDTO,
)
from src.application.service.use_cases.service_category_use_cases import ListCategoriesUseCase
from src.application.service.use_cases.service_subcategory_use_cases import ListSubcategoriesByCategoryUseCase
from src.application.service.use_cases.service_vendor_use_cases import (
    ListVendorsByCategoryUseCase,
    GetVendorDetailUseCase,
)
from src.application.service.use_cases.vendor_image_use_cases import GetVendorImageUseCase
from src.infrastructure.web.dependencies import (
    get_list_categories_use_case,
    get_list_subcategories_by_category_use_case,
    get_list_vendors_by_category_use_case,
    get_vendor_detail_use_case,
    get_vendor_image_use_case,
)
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/services",
    tags=["services"],
)


@router.get("/categories", response_model=ServiceCategoryListResponseDTO)
def list_categories(
    use_case: ListCategoriesUseCase = Depends(get_list_categories_use_case),
) -> ServiceCategoryListResponseDTO:
    """
    List all service categories.
    
    Returns categories like: restaurant, private_jet, flight, car, hotel, car_driver
    """
    return use_case.execute()


@router.get("/categories/{category_id}/subcategories", response_model=ServiceSubcategoryListResponseDTO)
def list_category_subcategories(
    category_id: int,
    use_case: ListSubcategoriesByCategoryUseCase = Depends(get_list_subcategories_by_category_use_case),
) -> ServiceSubcategoryListResponseDTO:
    """
    List all subcategories for a specific category.
    
    Example: Get all subcategories under the "restaurant" category
    (e.g., Italian, Chinese, Indian, etc.)
    """
    return use_case.execute(category_id)


# Support both: /categories/{category_slug}/vendors and /vendors (category optional)
from typing import Optional

@router.get(
    "/categories/{category_slug}/vendors",
    response_model=VendorListResponseDTO,
    summary="List Vendors (by Category or All)",
    description="List vendors for a specific category (or all if not provided). Provides thumbnail and basic info for list view. Supports filtering by city."
)
@router.get(
    "/vendors",
    response_model=VendorListResponseDTO,
    summary="List All Vendors",
    description="List all vendors. Provides thumbnail and basic info for list view. Supports filtering by city."
)
def list_vendors(
    category_slug: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    city: Optional[str] = Query(None, description="Filter vendors by city"),
    use_case: ListVendorsByCategoryUseCase = Depends(get_list_vendors_by_category_use_case),
) -> VendorListResponseDTO:
    """
    List all vendors, or filter by category if category_slug is provided. 
    Supports optional city filter to get vendors in a specific city.
    
    Query Parameters:
    - city: Optional city name to filter vendors (e.g., ?city=Riyadh)
    """
    return use_case.execute(
        category_slug=category_slug,
        skip=skip,
        limit=limit,
        city=city,
    )


@router.get("/vendors/{vendor_id}", response_model=VendorDetailDTO)
def get_vendor_detail(
    vendor_id: int,
    use_case: GetVendorDetailUseCase = Depends(get_vendor_detail_use_case),
) -> VendorDetailDTO:
    """
    Get full details for a specific vendor (public endpoint).
    
    Includes hero images, gallery images, and type-specific metadata
    (dishes for restaurants, rooms for hotels, etc.).
    """
    return use_case.execute(vendor_id)


@router.get("/images/{image_id}", response_model=VendorImageDTO)
def get_image(
    image_id: int,
    use_case: GetVendorImageUseCase = Depends(get_vendor_image_use_case),
) -> VendorImageDTO:
    """
    Get image info including URL.
    
    Returns image metadata with direct URL to the image.
    """
    return use_case.execute(image_id)
