"""Service domain repository interfaces."""

from src.domain.service.repository.service_category_repository import ServiceCategoryRepository
from src.domain.service.repository.service_subcategory_repository import ServiceSubcategoryRepository
from src.domain.service.repository.service_vendor_repository import ServiceVendorRepository
from src.domain.service.repository.vendor_image_repository import VendorImageRepository

__all__ = ["ServiceCategoryRepository", "ServiceSubcategoryRepository", "ServiceVendorRepository", "VendorImageRepository"]
