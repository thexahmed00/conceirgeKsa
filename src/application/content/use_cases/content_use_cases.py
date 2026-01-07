"""Content use cases - Banners and Cities."""

from src.domain.content.repository.banner_repository import BannerRepository
from src.domain.content.repository.city_repository import CityRepository
from src.application.content.dto.content_dto import (
    BannerDTO,
    BannerListResponseDTO,
    CityDTO,
    CityListResponseDTO,
)


class ListBannersUseCase:
    """Use case for listing banners."""

    def __init__(self, banner_repository: BannerRepository):
        self.banner_repository = banner_repository

    async def execute(self) -> BannerListResponseDTO:
        """Execute the use case."""
        banners = await self.banner_repository.find_all(active_only=True)
        
        banner_dtos = [
            BannerDTO(
                id=banner.banner_id,
                title=banner.title,
                image_url=banner.image_url,
                description=banner.description,
                link_url=banner.link_url,
                display_order=banner.display_order,
                is_active=banner.is_active,
                created_at=banner.created_at,
                updated_at=banner.updated_at,
            )
            for banner in banners
        ]
        
        return BannerListResponseDTO(banners=banner_dtos, total=len(banner_dtos))


class ListCitiesUseCase:
    """Use case for listing cities."""

    def __init__(self, city_repository: CityRepository):
        self.city_repository = city_repository

    async def execute(self) -> CityListResponseDTO:
        """Execute the use case."""
        cities = await self.city_repository.find_all(active_only=True)
        
        city_dtos = [
            CityDTO(
                id=city.city_id,
                name=city.name,
                name_ar=city.name_ar,
                country=city.country,
                display_order=city.display_order,
                is_active=city.is_active,
                created_at=city.created_at,
                updated_at=city.updated_at,
            )
            for city in cities
        ]
        
        return CityListResponseDTO(cities=city_dtos, total=len(city_dtos))
