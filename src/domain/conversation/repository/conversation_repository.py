"""Conversation repository interface (domain layer)."""

from __future__ import annotations

from typing import List, Optional, Protocol

from src.domain.conversation.entities.conversation import Conversation, Message


class ConversationRepository(Protocol):
    def save(self, conversation: Conversation) -> Conversation:
        ...

    def find_by_id(self, conversation_id: int) -> Optional[Conversation]:
        ...

    def find_by_request_id(self, request_id: int) -> Optional[Conversation]:
        ...

    def find_by_user_id(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Conversation]:
        ...

    def find_all(self, skip: int = 0, limit: int = 20) -> List[Conversation]:
        ...

    def count_all(self) -> int:
        ...

    def add_message(self, message: Message) -> Message:
        ...

    def get_messages(self, conversation_id: int, skip: int = 0, limit: int = 50) -> List[Message]:
        ...
