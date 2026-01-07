"""Request use cases - application layer orchestration."""

from typing import List
from src.domain.request.entities.request import Request
from src.domain.conversation.entities.conversation import Conversation
from src.domain.request.repository.request_repository import RequestRepository
from src.domain.conversation.repository.conversation_repository import ConversationRepository
from src.domain.service.repository.service_vendor_repository import ServiceVendorRepository
from src.application.request.dto.request_dto import RequestCreateDTO, RequestResponseDTO
from src.domain.shared.exceptions import AccessDeniedError, ResourceNotFoundError


class SubmitRequestUseCase:
    """Submit a new concierge request (creates request + conversation + first message)."""
    
    def __init__(
        self,
        request_repo: RequestRepository,
        conversation_repo: ConversationRepository,
        vendor_repo: ServiceVendorRepository,
        notification_service=None,
        user_repo=None,
    ):
        self.request_repo = request_repo
        self.conversation_repo = conversation_repo
        self.vendor_repo = vendor_repo
        self.notification_service = notification_service
        self.user_repo = user_repo
    
    def execute(self, dto: RequestCreateDTO, user_id: int) -> RequestResponseDTO:
        # 1. Look up vendor to get category and title
        vendor = self.vendor_repo.find_by_id(dto.vendor_id)
        if not vendor:
            raise ResourceNotFoundError(f"Vendor {dto.vendor_id} not found")
        
        # Derive title from vendor name, category_slug from vendor's category
        title = vendor.name
        category_slug = vendor.category_slug
        
        # 2. Create request entity (validates business rules)
        request = Request.create(
            user_id=user_id,
            title=title,
            category_slug=category_slug,
            description=dto.description,
            vendor_id=dto.vendor_id,
        )
        
        # 3. Save request
        saved_request = self.request_repo.save(request)
        
        # 4. Create conversation linked to request
        conversation = Conversation.create(
            request_id=saved_request.request_id,
            user_id=user_id,
        )
        saved_conversation = self.conversation_repo.save(conversation)
        
        # 5. Add first message (the request description)
        first_message = saved_conversation.add_message(
            sender_id=user_id,
            sender_type="user",
            content=dto.description,
        )
        self.conversation_repo.add_message(first_message)
        
        # 6. Notify all admins about new request
        if self.notification_service and self.user_repo:
            try:
                # Get user name for notification
                user = self.user_repo.find_by_id(user_id)
                user_name = f"{user.first_name} {user.last_name}" if user else None
                
                # Get all admin users
                admins = self.user_repo.find_all_admins()
                for admin in admins:
                    self.notification_service.notify_new_request(
                        admin_user_id=admin.user_id,
                        request_id=saved_request.request_id,
                        request_title=title,
                        user_name=user_name,
                    )
            except Exception:
                # Don't fail request submission if notification fails
                pass
        
        # 7. Return response
        return RequestResponseDTO(
            id=saved_request.request_id,
            user_id=saved_request.user_id,
            title=saved_request.title,
            category_slug=saved_request.category_slug,
            description=saved_request.description,
            status=saved_request.status,
            vendor_id=saved_request.vendor_id,
            vendor_name=vendor.name,
            conversation_id=saved_conversation.conversation_id,
            created_at=saved_request.created_at,
            updated_at=saved_request.updated_at,
        )


class GetRequestUseCase:
    """Get a single request by ID."""
    
    def __init__(self, request_repo: RequestRepository, conversation_repo: ConversationRepository):
        self.request_repo = request_repo
        self.conversation_repo = conversation_repo
    
    def execute(self, request_id: int, user_id: int) -> RequestResponseDTO:
        request = self.request_repo.find_by_id(request_id)
        
        if not request:
            raise ResourceNotFoundError(f"Request {request_id} not found")
        
        # Check ownership
        if request.user_id != user_id:
            raise AccessDeniedError("You don't have access to this request")
        
        # Get conversation ID
        conversation = self.conversation_repo.find_by_request_id(request_id)
        
        return RequestResponseDTO(
            id=request.request_id,
            user_id=request.user_id,
            title=request.title,
            category_slug=request.category_slug,
            description=request.description,
            status=request.status,
            vendor_id=request.vendor_id,
            conversation_id=conversation.conversation_id if conversation else None,
            created_at=request.created_at,
            updated_at=request.updated_at,
        )


class ListUserRequestsUseCase:
    """List all requests for a user."""
    
    def __init__(self, request_repo: RequestRepository):
        self.request_repo = request_repo
    
    def execute(self, user_id: int, skip: int = 0, limit: int = 20) -> List[RequestResponseDTO]:
        requests = self.request_repo.find_by_user_id(user_id, skip, limit)
        
        return [
            RequestResponseDTO(
                id=r.request_id,
                user_id=r.user_id,
                title=r.title,
                category_slug=r.category_slug,
                description=r.description,
                status=r.status,
                vendor_id=r.vendor_id,
                conversation_id=None,  # Optimize: don't fetch conversation for list
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in requests
        ]
