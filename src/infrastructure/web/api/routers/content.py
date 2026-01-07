"""Content API endpoints - Banners and Cities."""

from fastapi import APIRouter, Depends

from src.application.content.dto.content_dto import (
    BannerListResponseDTO,
    CityListResponseDTO,
)
from src.application.content.use_cases.content_use_cases import (
    ListBannersUseCase,
    ListCitiesUseCase,
)
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/content",
    tags=["content"],
)


# Dependency injection functions
async def get_list_banners_use_case() -> ListBannersUseCase:
    """Get list banners use case."""
    from src.infrastructure.persistence.database import get_db
    from src.infrastructure.persistence.repositories.banner_repository import PostgreSQLBannerRepository
    
    db = next(get_db())
    banner_repo = PostgreSQLBannerRepository(db)
    return ListBannersUseCase(banner_repo)


async def get_list_cities_use_case() -> ListCitiesUseCase:
    """Get list cities use case."""
    from src.infrastructure.persistence.database import get_db
    from src.infrastructure.persistence.repositories.city_repository import PostgreSQLCityRepository
    
    db = next(get_db())
    city_repo = PostgreSQLCityRepository(db)
    return ListCitiesUseCase(city_repo)


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
