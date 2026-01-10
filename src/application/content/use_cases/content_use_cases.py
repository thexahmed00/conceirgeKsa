"""Content use cases - Banners and Cities."""

from datetime import datetime
from src.domain.content.entities.banner import Banner
from src.domain.content.repository.banner_repository import BannerRepository
from src.domain.content.repository.city_repository import CityRepository
from src.domain.shared.exceptions import ResourceNotFoundError
from src.application.content.dto.content_dto import (
    BannerDTO,
    BannerListResponseDTO,
    BannerCreateDTO,
    BannerUpdateDTO,
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


class CreateBannerUseCase:
    """Admin use case for creating a banner."""

    def __init__(self, banner_repository: BannerRepository):
        self.banner_repository = banner_repository

    async def execute(self, dto: BannerCreateDTO) -> BannerDTO:
        """Create a new banner."""
        banner = Banner(
            banner_id=0,  # Temporary, will be set by DB
            title=dto.title,
            image_url=dto.image_url,
            description=dto.description,
            link_url=dto.link_url,
            display_order=dto.display_order,
            is_active=dto.is_active,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        saved_banner = await self.banner_repository.create(banner)
        
        return BannerDTO(
            id=saved_banner.banner_id,
            title=saved_banner.title,
            image_url=saved_banner.image_url,
            description=saved_banner.description,
            link_url=saved_banner.link_url,
            display_order=saved_banner.display_order,
            is_active=saved_banner.is_active,
            created_at=saved_banner.created_at,
            updated_at=saved_banner.updated_at,
        )


class UpdateBannerUseCase:
    """Admin use case for updating a banner."""

    def __init__(self, banner_repository: BannerRepository):
        self.banner_repository = banner_repository

    async def execute(self, banner_id: int, dto: BannerUpdateDTO) -> BannerDTO:
        """Update an existing banner."""
        banner = await self.banner_repository.find_by_id(banner_id)
        if not banner:
            raise ResourceNotFoundError(f"Banner {banner_id} not found")
        
        # Update only provided fields
        if dto.title is not None:
            banner.title = dto.title
        if dto.image_url is not None:
            banner.image_url = dto.image_url
        if dto.description is not None:
            banner.description = dto.description
        if dto.link_url is not None:
            banner.link_url = dto.link_url
        if dto.display_order is not None:
            banner.display_order = dto.display_order
        if dto.is_active is not None:
            banner.is_active = dto.is_active
        
        banner.updated_at = datetime.utcnow()
        
        updated_banner = await self.banner_repository.update(banner)
        
        return BannerDTO(
            id=updated_banner.banner_id,
            title=updated_banner.title,
            image_url=updated_banner.image_url,
            description=updated_banner.description,
            link_url=updated_banner.link_url,
            display_order=updated_banner.display_order,
            is_active=updated_banner.is_active,
            created_at=updated_banner.created_at,
            updated_at=updated_banner.updated_at,
        )


class DeleteBannerUseCase:
    """Admin use case for deleting a banner."""

    def __init__(self, banner_repository: BannerRepository):
        self.banner_repository = banner_repository

    async def execute(self, banner_id: int) -> bool:
        """Delete a banner."""
        banner = await self.banner_repository.find_by_id(banner_id)
        if not banner:
            raise ResourceNotFoundError(f"Banner {banner_id} not found")
        
        return await self.banner_repository.delete(banner_id)
