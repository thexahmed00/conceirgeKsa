"""FastAPI dependencies."""

from src.infrastructure.web.dependencies.injection import (
	get_conversation_repository,
	get_conversation_use_case,
	get_authenticate_user_use_case,
	get_create_user_use_case,
	get_current_user,
	get_db,
	get_list_all_conversations_use_case,
	get_list_user_conversations_use_case,
	get_list_user_requests_use_case,
	get_optional_user,
	get_request_repository,
	get_request_use_case,
	get_send_message_use_case,
	get_submit_request_use_case,
	get_user_repository,
	get_user_use_case,
)

__all__ = [
	"get_db",
	"get_current_user",
	"get_optional_user",
	"get_user_repository",
	"get_create_user_use_case",
	"get_authenticate_user_use_case",
	"get_user_use_case",
	"get_request_repository",
	"get_conversation_repository",
	"get_submit_request_use_case",
	"get_request_use_case",
	"get_list_user_requests_use_case",
	"get_conversation_use_case",
	"get_send_message_use_case",
	"get_list_user_conversations_use_case",
	"get_list_all_conversations_use_case",
]
