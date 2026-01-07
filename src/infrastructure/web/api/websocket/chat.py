"""WebSocket chat endpoint."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.web.api.websocket.connection_manager import manager
from src.infrastructure.web.dependencies import get_db
from src.infrastructure.auth.jwt_handler import get_token_claims
from src.infrastructure.persistence.repositories.conversation_repository import ConversationRepository
from src.infrastructure.persistence.repositories.user_repository import PostgreSQLUserRepository
from src.application.notification.services.notification_service import NotificationService
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
    # WebSocket Real-Time Chat Endpoint
    
    ## Connection URL
    ```
    ws://localhost:8000/ws/chat/{conversation_id}?token={jwt_token}
    ```
    
    ## Authentication
    - Pass JWT token as query parameter: `?token=YOUR_JWT_TOKEN`
    - Get JWT from: `POST /api/v1/auth/login`
    - Token is validated on connection
    
    ## Access Control
    - **Regular Users**: Can only connect to their own conversations
    - **Admins** (`is_admin=true`): Can connect to any conversation
    
    ## Message Flow
    
    ### 1. Client Connects
    ```javascript
    const ws = new WebSocket('ws://localhost:8000/ws/chat/2?token=eyJhbGci...');
    
    ws.onopen = () => {
      console.log('Connected!');
    };
    ```
    
    **Server Response:**
    ```json
    {
      "type": "connected",
      "conversation_id": 2,
      "user_type": "user",
      "message": "Connected to chat as user"
    }
    ```
    
    ### 2. Send Message (Client → Server)
    ```javascript
    ws.send(JSON.stringify({
      "content": "Hello! Can you help me book a table?"
    }));
    ```
    
    ### 3. Receive Messages (Server → Client)
    **Broadcast to all connected clients (user + admin):**
    ```json
    {
      "type": "message",
      "id": 123,
      "conversation_id": 2,
      "sender_id": 9,
      "sender_type": "user",
      "content": "Hello! Can you help me book a table?",
      "created_at": "2025-12-23T16:45:30.123456"
    }
    ```
    
    **Admin reply (all clients receive):**
    ```json
    {
      "type": "message",
      "id": 124,
      "conversation_id": 2,
      "sender_id": 1,
      "sender_type": "admin",
      "content": "Of course! Which restaurant would you prefer?",
      "created_at": "2025-12-23T16:46:15.789012"
    }
    ```
    
    ### 4. Handle Incoming Messages
    ```javascript
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      switch(data.type) {
        case 'connected':
          console.log('Connection established:', data.message);
          break;
        
        case 'message':
          // Display message in chat UI
          if (data.sender_type === 'admin') {
            displayAdminMessage(data.content, data.created_at);
          } else {
            displayUserMessage(data.content, data.created_at);
          }
          break;
        
        case 'error':
          console.error('Error:', data.message);
          break;
      }
    };
    ```
    
    ### 5. Handle Disconnection
    ```javascript
    ws.onclose = (event) => {
      console.log('Disconnected:', event.code);
      // Attempt reconnection if needed
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    ```
    
    ## Error Responses
    
    ### Invalid/Expired Token (Code: 4001)
    ```json
    {
      "type": "error",
      "message": "Invalid or expired token"
    }
    ```
    
    ### Conversation Not Found (Code: 4004)
    ```json
    {
      "type": "error",
      "message": "Conversation not found"
    }
    ```
    
    ### Access Denied (Code: 4003)
    ```json
    {
      "type": "error",
      "message": "Access denied to this conversation"
    }
    ```
    
    ### Empty Message Content
    ```json
    {
      "type": "error",
      "message": "Message content cannot be empty"
    }
    ```
    
    ## Complete Frontend Example
    
    ```javascript
    class ChatClient {
      constructor(conversationId, token) {
        this.conversationId = conversationId;
        this.token = token;
        this.ws = null;
      }
      
      connect() {
        const url = `ws://localhost:8000/ws/chat/${this.conversationId}?token=${this.token}`;
        this.ws = new WebSocket(url);
        
        this.ws.onopen = () => {
          console.log('✅ Connected to chat');
        };
        
        this.ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          this.handleMessage(data);
        };
        
        this.ws.onerror = (error) => {
          console.error('❌ WebSocket error:', error);
        };
        
        this.ws.onclose = (event) => {
          console.log('🔌 Disconnected:', event.code);
          // Reconnect after 3 seconds
          setTimeout(() => this.connect(), 3000);
        };
      }
      
      sendMessage(content) {
        if (this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(JSON.stringify({ content }));
        } else {
          console.error('WebSocket not connected');
        }
      }
      
      handleMessage(data) {
        switch(data.type) {
          case 'connected':
            console.log('Connected as:', data.user_type);
            break;
          
          case 'message':
            this.displayMessage(data);
            break;
          
          case 'error':
            alert('Error: ' + data.message);
            break;
        }
      }
      
      displayMessage(msg) {
        const messageDiv = document.createElement('div');
        messageDiv.className = msg.sender_type === 'admin' ? 'admin-message' : 'user-message';
        messageDiv.innerHTML = `
          <strong>${msg.sender_type}</strong>: ${msg.content}
          <small>${new Date(msg.created_at).toLocaleTimeString()}</small>
        `;
        document.getElementById('chat-messages').appendChild(messageDiv);
      }
      
      disconnect() {
        if (this.ws) {
          this.ws.close();
        }
      }
    }
    
    // Usage
    const chat = new ChatClient(2, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...');
    chat.connect();
    
    // Send message
    document.getElementById('send-btn').onclick = () => {
      const input = document.getElementById('message-input');
      chat.sendMessage(input.value);
      input.value = '';
    };
    ```
    
    ## React Example
    
    ```javascript
    import { useEffect, useState, useRef } from 'react';
    
    function ChatComponent({ conversationId, token }) {
      const [messages, setMessages] = useState([]);
      const [inputValue, setInputValue] = useState('');
      const wsRef = useRef(null);
      
      useEffect(() => {
        const ws = new WebSocket(
          `ws://localhost:8000/ws/chat/${conversationId}?token=${token}`
        );
        
        ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          if (data.type === 'message') {
            setMessages(prev => [...prev, data]);
          }
        };
        
        wsRef.current = ws;
        
        return () => ws.close();
      }, [conversationId, token]);
      
      const sendMessage = () => {
        if (wsRef.current && inputValue.trim()) {
          wsRef.current.send(JSON.stringify({ content: inputValue }));
          setInputValue('');
        }
      };
      
      return (
        <div className="chat-container">
          <div className="messages">
            {messages.map((msg) => (
              <div key={msg.id} className={`message ${msg.sender_type}`}>
                <strong>{msg.sender_type}:</strong> {msg.content}
              </div>
            ))}
          </div>
          <input 
            value={inputValue} 
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      );
    }
    ```
    
    ## Testing with Postman/Thunder Client
    
    1. Create WebSocket request
    2. URL: `ws://localhost:8000/ws/chat/2?token=YOUR_JWT`
    3. Connect
    4. Send: `{"content": "Test message"}`
    5. Observe broadcasted response
    
    ## Notes
    - All messages are persisted to database before broadcasting
    - Both user and admin receive all messages in real-time
    - Connection auto-closes on invalid token or access denial
    - Messages are ordered by `created_at` timestamp
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
                
                # Send notification to the other party (if user sends, notify admin; if admin sends, notify user)
                try:
                    user_repo = PostgreSQLUserRepository(db)
                    notification_service = NotificationService(db)
                    
                    if sender_type == "user":
                        # User sent message - notify admins (skip for now, can be enhanced later)
                        pass
                    else:
                        # Admin sent message - notify the conversation's user
                        sender = user_repo.find_by_id(user_id)
                        sender_name = sender.full_name if sender and sender.full_name else "Support Team"
                        
                        notification_service.notify_message_received(
                            user_id=conversation.user_id,
                            conversation_id=conversation_id,
                            sender_name=sender_name,
                        )
                except Exception as e:
                    # Don't fail message sending if notification fails
                    logger.error(f"Failed to send message notification: {e}")
                
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
