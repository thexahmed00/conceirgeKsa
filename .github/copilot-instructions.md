# AJLA Concierge Platform - AI Development Guidelines

## Tech Stack & Architecture

- **Backend**: FastAPI (Python) with Clean Architecture + Domain-Driven Design (DDD)
- **Database**: MySQL
- **Authentication**: JWT (Basic)
- **Phase**: MVP focused on backend + real-time chat communication
- **Chat**: WebSocket-based real-time messaging (async support via FastAPI)

## Project Overview

**AJLA** is a premium lifestyle concierge platform enabling users to request and book luxury services (travel, dining, events) through an intuitive app interface, with a specialized admin portal for concierge agents to manage requests and vendor partnerships.

## Architecture Layers

### MVP Scope - Core Components Only

#### 1. User Layer (Client-side features for MVP)
- **Authentication**: User registration and login
- **Request Submission**: Submit concierge requests
- **Real-time Chat**: Live messaging with concierge agents
- **Conversation History**: View full chat history

#### 2. Backend System Layer
- **User Management**: Registration, login, profile retrieval
- **Request Persistence**: Save incoming requests to database
- **Conversation System**: Create conversations and persist messages
- **Real-time Chat**: WebSocket server for live messaging
- **Status Updates**: Track request states (New → In Progress → Fulfilled)

#### 3. Admin/Concierge Layer (Post-MVP)
- Request queue, vendor search, assignment logic, analytics

*Note: Admin functionality deferred to Phase 2*

## Architecture Patterns (Clean Architecture + DDD)

### Domain Layer (`/src/domain`)
- **Entities**: `User`, `Request`, `Conversation`, `Message`, `Booking` - encapsulate business rules
- **Value Objects**: `UserId`, `RequestId`, `MessageContent`, `Money` - immutable domain concepts
- **Aggregates**: Root entities that maintain consistency (e.g., `Conversation` aggregate contains `Message` value objects)
- **Repository Interfaces**: Define data access contracts (`UserRepository`, `ConversationRepository`)
- **Domain Events**: `UserCreated`, `RequestSubmitted`, `MessageCreated` - capture state changes
- **Domain Services**: Pure business logic (`RequestAssignmentService`, `NotificationService` - NO infrastructure dependencies)

### Application Layer (`/src/application`)
- **Use Cases**: Command handlers that coordinate domain entities and repositories
  - `SubmitRequestUseCase`: Validates user input, creates `Request` aggregate, publishes `RequestSubmitted` event
  - `SendMessageUseCase`: Creates `Message`, updates `Conversation`, triggers notifications
  - `CreateBookingUseCase`: Creates `Booking` after admin confirmation
- **DTOs**: Data transfer objects for API contracts (separate from domain entities)
- **NO business logic here** - orchestrates domain layer only

### Infrastructure Layer (`/src/infrastructure`)
- **Repository Implementations**: SQLAlchemy-based concrete implementations
- **Web Layer**: FastAPI routers, WebSocket handlers, middleware
  - JWT middleware for authentication
  - Error handling middleware (convert domain exceptions to HTTP responses)
  - WebSocket connection manager for real-time chat
- **Persistence**: MySQL session management, SQLAlchemy ORM models
- **Auth**: JWT token generation/validation, password hashing (bcrypt)

### Dependency Injection
- Use FastAPI's `Depends()` for injecting repositories, use cases, and services
- Example: `@router.post("/requests") def submit_request(use_case: SubmitRequestUseCase = Depends(get_submit_request_use_case))`

## MVP Scope (Phase 1)

**Focus ONLY on core backend + chat, no admin UI yet:**

### User Requests API
- `POST /api/v1/requests` - Submit concierge request (creates `Request` + `Conversation` + first `Message`)
- `GET /api/v1/requests/{request_id}` - Get request details
- `GET /api/v1/requests` - List user's requests (paginated)

### Chat/Messaging API
- `WebSocket /ws/chat/{conversation_id}` - Real-time messaging
- `GET /api/v1/conversations/{conversation_id}` - Get conversation history
- `POST /api/v1/messages` - Send message (fallback HTTP endpoint)

### Authentication API
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - JWT token generation
- `POST /api/v1/auth/refresh` - Token refresh

### User Profile API
- `GET /api/v1/users/me` - Current user profile
- `PUT /api/v1/users/me` - Update profile preferences

### Core Models
```sql
-- Users
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255),
  tier INT DEFAULT 5000,  -- 5000, 25000, 100000
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Requests
CREATE TABLE requests (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL FOREIGN KEY,
  type ENUM('travel', 'dining', 'events', 'shopping'),
  description TEXT,
  status ENUM('new', 'assigned', 'in_progress', 'fulfilled') DEFAULT 'new',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Conversations (1:1 with Request)
CREATE TABLE conversations (
  id INT PRIMARY KEY AUTO_INCREMENT,
  request_id INT NOT NULL UNIQUE FOREIGN KEY,
  user_id INT NOT NULL FOREIGN KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages
CREATE TABLE messages (
  id INT PRIMARY KEY AUTO_INCREMENT,
  conversation_id INT NOT NULL FOREIGN KEY,
  sender_id INT NOT NULL FOREIGN KEY,
  sender_type ENUM('user', 'admin') NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Critical Implementation Patterns (MVP)

### Request Submission Flow
1. User calls `POST /api/v1/requests`
2. `SubmitRequestUseCase` validates input
3. Creates `Request` aggregate in database
4. Creates `Conversation` aggregate linked to `Request`
5. Creates first `Message` persisted to database
6. Publishes `RequestSubmitted` domain event
7. Event triggers notification (future: webhook to admin service)

### Real-time Chat via WebSocket
- Establish WebSocket connection: `WebSocket /ws/chat/{conversation_id}?token={jwt_token}`
- Validate JWT and check permission (user owns conversation)
- Use connection manager to track active clients
- Incoming message → validate → create `Message` aggregate → persist → broadcast to active WebSocket clients
- Fallback HTTP endpoint for message sending (reconnection resilience)

### JWT Authentication
- Token generation on login: `exp`, `user_id`, `email` claims
- Middleware validates token on each protected route
- WebSocket authentication via URL query parameter or header

### Error Handling
- Domain exceptions (`ValidationError`, `ResourceNotFound`) → HTTP 400/404
- Consistency: All errors return `{"detail": "error message"}` JSON

## Database Schema Considerations

- Use `CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci` for Arabic support
- Add indexes on `user_id`, `conversation_id`, `created_at` for query performance
- Timestamps: Store in UTC, convert on API response

## Development Workflow

1. **Define Domain First**: Create entity classes, value objects, repository interfaces
2. **Write Domain Tests**: Test business logic in isolation
3. **Implement Repositories**: SQLAlchemy implementations
4. **Build Use Cases**: Orchestrate domain + repositories
5. **Create API Endpoints**: FastAPI routers using dependencies
6. **Test Integration**: End-to-end tests for flows
7. **Add WebSocket**: Chat functionality with connection management

## Key Dependencies

```
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.0
mysql-connector-python==8.2.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.1
python-multipart==0.0.6
websockets==12.0
```

## Known Constraints & Edge Cases (MVP Phase)

- **WebSocket Reconnection**: Implement exponential backoff on client side
- **Message Ordering**: Use database `created_at` timestamp for consistent ordering
- **Concurrent Messages**: Database ensures FIFO via autoincrement ID
- **User Permissions**: Always verify `user_id` from JWT matches resource ownership
- **Database Connection**: Use connection pooling to handle concurrent WebSocket connections
- **Offline Messages**: Store messages immediately in DB before broadcasting (no in-memory queue)

## Recommended Project Structure

```
/src
  /domain              # Domain entities, value objects, aggregates (DDD core)
    /user
      /entities        # User, UserProfile aggregates
      /repository      # UserRepository interface
      /events          # UserCreated, UserUpdated domain events
    /request
      /entities        # Request, RequestItem aggregates
      /repository      # RequestRepository interface
      /events          # RequestSubmitted, RequestAssigned events
    /conversation
      /entities        # Conversation, Message aggregates
      /repository      # ConversationRepository interface
      /events          # MessageCreated, ConversationStarted events
      /services        # DomainService for business rules (no infrastructure)
    /booking
      /entities        # Booking aggregate
      /repository      # BookingRepository interface
      /events          # BookingConfirmed event
    /shared            # Shared value objects, exceptions, event bus
  
  /application         # Use cases, DTOs, orchestration layer
    /user
      /use_cases       # CreateUserUseCase, AuthenticateUserUseCase
      /dto             # UserCreateDTO, UserResponseDTO
    /request
      /use_cases       # SubmitRequestUseCase, GetRequestsUseCase
      /dto             # RequestCreateDTO, RequestResponseDTO
    /conversation
      /use_cases       # SendMessageUseCase, GetConversationUseCase
      /dto             # MessageDTO, ConversationDTO
    /booking
      /use_cases       # CreateBookingUseCase
      /dto             # BookingDTO

  /infrastructure      # Database, external services, repositories
    /persistence
      /mysql           # SQLAlchemy models, session management
      /repositories    # Repository implementations
    /web
      /api
        /routers       # FastAPI routes (/api/v1/users, /api/v1/requests, etc)
        /websocket     # WebSocket handlers for chat
        /middleware    # JWT auth middleware, error handling
        /dependencies  # FastAPI dependency injection (get_db, get_current_user)
    /auth              # JWT token generation, password hashing
    /services          # External API clients (payment, SMS, etc - future)

  /shared              # Shared utilities, exceptions, logging
    /exceptions        # CustomException, ValidationError
    /utils             # Decorators, helpers
    /logger            # Logging configuration

/tests
  /domain              # Unit tests for business logic
  /application         # Use case tests
  /api                 # Integration tests for endpoints
  /fixtures            # Test data, factories

/docs                  # API documentation (Swagger auto-generated)
/requirements.txt      # Python dependencies
/main.py              # FastAPI app initialization
```

## Development Priorities (MVP Phase)

1. **User Authentication**: Registration and JWT-based login
2. **Request Submission**: User creates requests with conversation/first message
3. **Real-time Chat**: WebSocket implementation for live messaging
4. **Message History**: Retrieve and display full conversation threads
5. **User Profile**: Profile retrieval and preference updates
6. **Error Handling**: Consistent error responses across all endpoints

## Known Constraints & Edge Cases (MVP Phase)

- **WebSocket Reconnection**: Implement exponential backoff on client side
- **Message Ordering**: Use database `created_at` timestamp for consistent ordering
- **Concurrent Messages**: Database ensures FIFO via autoincrement ID
- **User Permissions**: Always verify `user_id` from JWT matches resource ownership
- **Database Connection**: Use connection pooling to handle concurrent WebSocket connections
- **Offline Messages**: Store messages immediately in DB before broadcasting (no in-memory queue)

## Future Phases (Post-MVP)

- Admin panel and request assignment logic
- Vendor integration and availability APIs
- Multi-channel notifications (Email, SMS, WhatsApp)
- Booking and invoicing system
- Analytics and audit logging
- Localization (Arabic support)
