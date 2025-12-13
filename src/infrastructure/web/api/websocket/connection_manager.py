"""WebSocket connection manager for real-time chat."""

from typing import Dict, List
from fastapi import WebSocket
from src.shared.logger.config import get_logger

logger = get_logger(__name__)


class ConnectionManager:
    """Manages WebSocket connections per conversation."""
    
    def __init__(self):
        # {conversation_id: [websocket1, websocket2, ...]}
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, conversation_id: int) -> None:
        """Accept connection and add to conversation room."""
        await websocket.accept()
        
        if conversation_id not in self.active_connections:
            self.active_connections[conversation_id] = []
        
        self.active_connections[conversation_id].append(websocket)
        logger.info(f"WebSocket connected: conversation={conversation_id}")
    
    def disconnect(self, websocket: WebSocket, conversation_id: int) -> None:
        """Remove connection from conversation room."""
        if conversation_id in self.active_connections:
            if websocket in self.active_connections[conversation_id]:
                self.active_connections[conversation_id].remove(websocket)
            
            # Clean up empty rooms
            if not self.active_connections[conversation_id]:
                del self.active_connections[conversation_id]
        
        logger.info(f"WebSocket disconnected: conversation={conversation_id}")
    
    async def broadcast(self, conversation_id: int, message: dict) -> None:
        """Send message to all connections in a conversation."""
        if conversation_id not in self.active_connections:
            return
        
        disconnected = []
        for connection in self.active_connections[conversation_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send message: {e}")
                disconnected.append(connection)
        
        # Clean up dead connections
        for conn in disconnected:
            self.disconnect(conn, conversation_id)
    
    async def send_personal(self, websocket: WebSocket, message: dict) -> None:
        """Send message to a specific connection."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.warning(f"Failed to send personal message: {e}")


# Global connection manager instance
manager = ConnectionManager()
