"""Content API endpoints - Banners and Cities."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.content.dto.content_dto import (
    BannerListResponseDTO,
    BannerDTO,
    BannerCreateDTO,
    BannerUpdateDTO,
    CityListResponseDTO,
)
from src.application.content.use_cases.content_use_cases import (
    ListBannersUseCase,
    ListCitiesUseCase,
    CreateBannerUseCase,
    UpdateBannerUseCase,
    DeleteBannerUseCase,
)
from src.infrastructure.web.dependencies import (
    get_current_admin_user,
    get_list_banners_use_case,
    get_list_cities_use_case,
    get_create_banner_use_case,
    get_update_banner_use_case,
    get_delete_banner_use_case,
)
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/content",
    tags=["content"],
)


@router.get("/banners", response_model=BannerListResponseDTO, summary="Get all active banners")
async def list_banners(
    use_case: ListBannersUseCase = Depends(get_list_banners_use_case),
) -> BannerListResponseDTO:
    """
    Get all active promotional banners.
    
    Returns banners ordered by display_order.
    """
    return await use_case.execute()


@router.get("/cities", response_model=CityListResponseDTO, summary="Get all active cities")
async def list_cities(
    use_case: ListCitiesUseCase = Depends(get_list_cities_use_case),
) -> CityListResponseDTO:
    """
    Get all active cities/locations.
    
    Returns cities ordered by display_order and name.
    """
    return await use_case.execute()


# Admin Banner Endpoints
@router.post("/admin/banners", response_model=BannerDTO, status_code=status.HTTP_201_CREATED, summary="Create a new banner")
async def create_banner(
    banner_data: BannerCreateDTO,
    admin_id: int = Depends(get_current_admin_user),
    use_case: CreateBannerUseCase = Depends(get_create_banner_use_case),
) -> BannerDTO:
    """
    Create a new promotional banner.
    
    **Admin only endpoint**
    
    - **title**: Text that appears on the banner image
    - **image_url**: URL to the banner image
    - **description**: Optional additional description
    - **link_url**: Optional deep link or URL when banner is tapped
    - **display_order**: Order for displaying multiple banners (lower first)
    - **is_active**: Whether the banner should be displayed to users
    
    Returns the created banner with its ID.
    """
    logger.info(f"Admin {admin_id} creating new banner: {banner_data.title}")
    return await use_case.execute(banner_data)


@router.put("/admin/banners/{banner_id}", response_model=BannerDTO, summary="Update an existing banner")
async def update_banner(
    banner_id: int,
    banner_data: BannerUpdateDTO,
    admin_id: int = Depends(get_current_admin_user),
    use_case: UpdateBannerUseCase = Depends(get_update_banner_use_case),
) -> BannerDTO:
    """
    Update an existing promotional banner.
    
    **Admin only endpoint**
    
    All fields are optional - only provided fields will be updated.
    
    Returns the updated banner.
    """
    logger.info(f"Admin {admin_id} updating banner {banner_id}")
    return await use_case.execute(banner_id, banner_data)


@router.delete("/admin/banners/{banner_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a banner")
async def delete_banner(
    banner_id: int,
    admin_id: int = Depends(get_current_admin_user),
    use_case: DeleteBannerUseCase = Depends(get_delete_banner_use_case),
) -> None:
    """
    Delete a promotional banner.
    
    **Admin only endpoint**
    
    Permanently removes the banner from the system.
    """
    logger.info(f"Admin {admin_id} deleting banner {banner_id}")
    await use_case.execute(banner_id)
