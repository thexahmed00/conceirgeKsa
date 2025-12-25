"""Services API endpoints - user-facing service discovery."""

from fastapi import APIRouter, Depends, Query, Response

from src.application.service.dto.service_dto import (
    ServiceCategoryListResponseDTO,
    VendorListResponseDTO,
    VendorDetailDTO,
    VendorImageDTO,
)
from src.application.service.use_cases.service_category_use_cases import ListCategoriesUseCase
from src.application.service.use_cases.service_vendor_use_cases import (
    ListVendorsByCategoryUseCase,
    GetVendorDetailUseCase,
)
from src.application.service.use_cases.vendor_image_use_cases import GetVendorImageUseCase
from src.infrastructure.web.dependencies import (
    get_list_categories_use_case,
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


@router.get("/categories/{category_slug}/vendors", response_model=VendorListResponseDTO)
def list_vendors_by_category(
    category_slug: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    use_case: ListVendorsByCategoryUseCase = Depends(get_list_vendors_by_category_use_case),
) -> VendorListResponseDTO:
    """
    List vendors for a specific category (public endpoint).
    
    Provides thumbnail and basic info for list view.
    """
    return use_case.execute(
        category_slug=category_slug,
        skip=skip,
        limit=limit,
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
