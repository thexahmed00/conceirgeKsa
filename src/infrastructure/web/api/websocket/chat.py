"""WebSocket chat endpoint."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.web.api.websocket.connection_manager import manager
from src.infrastructure.web.dependencies import get_db
from src.infrastructure.auth.jwt_handler import get_token_claims
from src.infrastructure.persistence.repositories.conversation_repository import ConversationRepository
from src.domain.conversation.entities.conversation import Message
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/chat/{conversation_id}")
async def websocket_chat(
    websocket: WebSocket,
    conversation_id: int,
    token: str = Query(..., description="JWT token for authentication"),
):
    """
    WebSocket endpoint for real-time chat.
    
    Connect: ws://localhost:8000/ws/chat/{conversation_id}?token={jwt_token}
    
    Send message format:
    {"content": "Hello!"}
    
    Receive message format:
    {"id": 1, "sender_id": 1, "sender_type": "user", "content": "Hello!", "created_at": "..."}
    
    Admin users can access any conversation. Regular users can only access their own.
    """
    # 1. Authenticate via JWT token
    claims = get_token_claims(token)
    if not claims or not claims.get("user_id"):
        await websocket.accept()
        await websocket.send_json({"type": "error", "message": "Invalid or expired token"})
        await websocket.close(code=4001)
        return
    
    user_id = claims["user_id"]
    is_admin = claims.get("is_admin", False)
    sender_type = "admin" if is_admin else "user"
    
    # 2. Get database session
    db: Session = next(get_db())
    
    try:
        # 3. Verify user has access to this conversation
        conversation_repo = ConversationRepository(db)
        conversation = conversation_repo.find_by_id(conversation_id)
        
        if not conversation:
            await websocket.accept()
            await websocket.send_json({"type": "error", "message": "Conversation not found"})
            await websocket.close(code=4004)
            return
        
        # Admin can access any conversation, regular users only their own
        if not is_admin and conversation.user_id != user_id:
            await websocket.accept()
            await websocket.send_json({"type": "error", "message": "Access denied to this conversation"})
            await websocket.close(code=4003)
            return
        
        # 4. Accept connection and add to room
        await manager.connect(websocket, conversation_id)
        
        # 5. Send connection confirmation
        await manager.send_personal(websocket, {
            "type": "connected",
            "conversation_id": conversation_id,
            "user_type": sender_type,
            "message": f"Connected to chat as {sender_type}"
        })
        
        # 6. Listen for messages
        while True:
            try:
                data = await websocket.receive_json()
                
                # Validate message content
                content = data.get("content", "").strip()
                if not content:
                    await manager.send_personal(websocket, {
                        "type": "error",
                        "message": "Message content cannot be empty"
                    })
                    continue
                
                # Create and save message (sender_type based on is_admin)
                message = Message.create(
                    conversation_id=conversation_id,
                    sender_id=user_id,
                    sender_type=sender_type,
                    content=content,
                )
                saved_message = conversation_repo.add_message(message)
                
                # Broadcast to all connected clients
                await manager.broadcast(conversation_id, {
                    "type": "message",
                    "id": saved_message.message_id,
                    "conversation_id": conversation_id,
                    "sender_id": saved_message.sender_id,
                    "sender_type": saved_message.sender_type,
                    "content": saved_message.content,
                    "created_at": saved_message.created_at.isoformat(),
                })
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                await manager.send_personal(websocket, {
                    "type": "error",
                    "message": "Failed to process message"
                })
    
    finally:
        manager.disconnect(websocket, conversation_id)
        db.close()
