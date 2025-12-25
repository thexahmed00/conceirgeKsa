"""WebSocket documentation endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/docs", tags=["WebSocket Documentation"])


class WebSocketDocs(BaseModel):
    """WebSocket endpoint documentation."""
    endpoint: str
    description: str
    connection_url: str
    authentication: dict
    send_format: dict
    receive_format: dict
    error_codes: dict
    examples: dict


@router.get(
    "/websocket-chat",
    response_model=WebSocketDocs,
    summary="📡 WebSocket Real-Time Chat Documentation",
    description="""
    # WebSocket Real-Time Chat Documentation
    
    This endpoint provides documentation for the WebSocket chat feature.
    WebSocket endpoints don't appear in Swagger UI, so use this guide to implement the chat feature.
    """
)
def get_websocket_chat_docs():
    """
    # WebSocket Real-Time Chat Documentation
    
    ## Connection URL
    ```
    ws://localhost:8000/ws/chat/{conversation_id}?token={jwt_token}
    ```
    
    ## Quick Start
    
    ### 1. Get JWT Token
    ```bash
    POST /api/v1/auth/login
    {
      "email": "user@example.com",
      "password": "password"
    }
    # Response: { "access_token": "eyJhbGci..." }
    ```
    
    ### 2. Connect to WebSocket
    ```javascript
    const ws = new WebSocket('ws://localhost:8000/ws/chat/2?token=eyJhbGci...');
    
    ws.onopen = () => console.log('✅ Connected');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('📨 Received:', data);
    };
    ```
    
    ### 3. Send Message
    ```javascript
    ws.send(JSON.stringify({
      "content": "Hello! Can you help me?"
    }));
    ```
    
    ### 4. Receive Messages (Auto-broadcast)
    ```json
    {
      "type": "message",
      "id": 123,
      "conversation_id": 2,
      "sender_id": 9,
      "sender_type": "user",
      "content": "Hello! Can you help me?",
      "created_at": "2025-12-23T16:45:30.123456"
    }
    ```
    
    ## Complete Implementation Examples Below ⬇️
    """
    return {
        "endpoint": "/ws/chat/{conversation_id}",
        "description": "Real-time bidirectional chat between users and admins",
        "connection_url": "ws://localhost:8000/ws/chat/{conversation_id}?token={jwt_token}",
        "authentication": {
            "method": "JWT token in query parameter",
            "parameter": "token",
            "get_token_from": "POST /api/v1/auth/login",
            "example": "ws://localhost:8000/ws/chat/2?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        },
        "send_format": {
            "description": "Send this JSON to the WebSocket",
            "schema": {
                "content": "string (required, min 1 character)"
            },
            "example": {
                "content": "Hello! Can you help me book a restaurant?"
            }
        },
        "receive_format": {
            "description": "You will receive these message types",
            "types": {
                "connected": {
                    "description": "Sent when connection is established",
                    "example": {
                        "type": "connected",
                        "conversation_id": 2,
                        "user_type": "user",
                        "message": "Connected to chat as user"
                    }
                },
                "message": {
                    "description": "Broadcast to all connected clients when anyone sends a message",
                    "example": {
                        "type": "message",
                        "id": 123,
                        "conversation_id": 2,
                        "sender_id": 9,
                        "sender_type": "user",
                        "content": "Hello! Can you help me?",
                        "created_at": "2025-12-23T16:45:30.123456"
                    }
                },
                "error": {
                    "description": "Sent when an error occurs",
                    "example": {
                        "type": "error",
                        "message": "Message content cannot be empty"
                    }
                }
            }
        },
        "error_codes": {
            "4001": "Invalid or expired token",
            "4003": "Access denied to this conversation",
            "4004": "Conversation not found"
        },
        "examples": {
            "vanilla_javascript": """
// Vanilla JavaScript Example
const conversationId = 2;
const token = 'eyJhbGci...'; // Get from login endpoint

const ws = new WebSocket(`ws://localhost:8000/ws/chat/${conversationId}?token=${token}`);

ws.onopen = () => {
  console.log('✅ Connected to chat');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'connected':
      console.log('Connection confirmed:', data.message);
      break;
    
    case 'message':
      // Display message in UI
      const isAdmin = data.sender_type === 'admin';
      displayMessage(data.content, isAdmin, data.created_at);
      break;
    
    case 'error':
      console.error('Error:', data.message);
      break;
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = (event) => {
  console.log('Disconnected:', event.code);
  // Reconnect logic here
};

// Send message
function sendMessage(content) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ content }));
  }
}

// Usage
sendMessage('Hello! I need help with my booking.');
""",
            "react": """
// React Hook Example
import { useEffect, useState, useRef } from 'react';

function useWebSocketChat(conversationId, token) {
  const [messages, setMessages] = useState([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null);
  
  useEffect(() => {
    const ws = new WebSocket(
      `ws://localhost:8000/ws/chat/${conversationId}?token=${token}`
    );
    
    ws.onopen = () => {
      setConnected(true);
      console.log('Connected');
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'message') {
        setMessages(prev => [...prev, data]);
      } else if (data.type === 'error') {
        console.error('Error:', data.message);
      }
    };
    
    ws.onclose = () => {
      setConnected(false);
      console.log('Disconnected');
    };
    
    wsRef.current = ws;
    
    return () => {
      ws.close();
    };
  }, [conversationId, token]);
  
  const sendMessage = (content) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ content }));
    }
  };
  
  return { messages, connected, sendMessage };
}

// Component Usage
function ChatComponent({ conversationId, token }) {
  const { messages, connected, sendMessage } = useWebSocketChat(conversationId, token);
  const [input, setInput] = useState('');
  
  const handleSend = () => {
    if (input.trim()) {
      sendMessage(input);
      setInput('');
    }
  };
  
  return (
    <div>
      <div className="status">
        {connected ? '🟢 Connected' : '🔴 Disconnected'}
      </div>
      <div className="messages">
        {messages.map(msg => (
          <div key={msg.id} className={msg.sender_type}>
            <strong>{msg.sender_type}:</strong> {msg.content}
            <small>{new Date(msg.created_at).toLocaleTimeString()}</small>
          </div>
        ))}
      </div>
      <input 
        value={input} 
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        placeholder="Type a message..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
""",
            "postman_testing": """
# Testing with Postman

1. Create a new WebSocket request
2. Enter URL: ws://localhost:8000/ws/chat/2?token=YOUR_JWT_TOKEN
3. Click "Connect"
4. In the message input, send:
   {
     "content": "Test message from Postman"
   }
5. Observe the response in the messages panel
6. Open another WebSocket connection (simulating admin) to see real-time broadcast
"""
        }
    }
