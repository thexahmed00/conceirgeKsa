# AJLA Concierge Platform - AI Development Guidelines

## Tech Stack & Architecture

- **Backend**: FastAPI (Python) with Clean Architecture + Domain-Driven Design (DDD)
- **Database**: PostgreSQL
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
- **Persistence**: PostgreSQL session management, SQLAlchemy ORM models
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
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255),
  tier INT DEFAULT 5000,  -- 5000, 25000, 100000
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Requests
CREATE TABLE requests (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id),
  type VARCHAR(50) NOT NULL CHECK (type IN ('travel', 'dining', 'events', 'shopping')),
  description TEXT,
  status VARCHAR(50) NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'assigned', 'in_progress', 'fulfilled')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversations (1:1 with Request)
CREATE TABLE conversations (
  id SERIAL PRIMARY KEY,
  request_id INT NOT NULL UNIQUE REFERENCES requests(id),
  user_id INT NOT NULL REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages
CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  conversation_id INT NOT NULL REFERENCES conversations(id),
  sender_id INT NOT NULL REFERENCES users(id),
  sender_type VARCHAR(50) NOT NULL CHECK (sender_type IN ('user', 'admin')),
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

- PostgreSQL supports UTF-8 by default (full Unicode/Arabic support)
- Add indexes on `user_id`, `conversation_id`, `created_at` for query performance
- Use `CREATE INDEX` for optimal query performance
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
psycopg2-binary==2.9.9
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

## Microservices Migration Path

The current **monolithic architecture is designed for easy decomposition into microservices**. Here's how to break it down:

### Service Boundaries (Natural Split Points)

1. **User Service** (`/src/domain/user` + `/src/application/user`)
   - Handles: User registration, authentication, profile management
   - Database: Separate `users` database
   - APIs: `/api/v1/auth/`, `/api/v1/users/`
   - Owns: JWT token validation, user permissions

2. **Request Service** (`/src/domain/request` + `/src/application/request`)
   - Handles: Concierge request creation, tracking, status updates
   - Database: Separate `requests` database
   - APIs: `/api/v1/requests/`
   - Publishes: `RequestSubmitted`, `RequestStatusChanged` events

3. **Conversation Service** (`/src/domain/conversation` + `/src/application/conversation`)
   - Handles: Real-time chat, message persistence, conversation history
   - Database: Separate `conversations` database
   - WebSocket: `/ws/chat/{conversation_id}`
   - HTTP: `/api/v1/conversations/`, `/api/v1/messages/`
   - Consumes: User events (for validation)

4. **Notification Service** (future, separate repo)
   - Handles: Email, SMS, WhatsApp, push notifications
   - Events: Listens to `RequestSubmitted`, `MessageCreated` events
   - No database needed (or minimal audit log)

5. **Booking Service** (`/src/domain/booking` - separate when admin features added)
   - Handles: Booking creation, invoicing, payments
   - Database: Separate `bookings` database
   - Consumes: Request service events

### Migration Strategy

**Phase 1 (Current):** Monolith with clear domain boundaries
- One FastAPI app, one MySQL database
- Domain layer separation enables easy extraction
- Events published locally via in-memory event bus

**Phase 2 (Microservices v1):** Extract User & Request Services
```
Monolith → 3 Services:
- API Gateway (FastAPI) - routes requests
- User Service (FastAPI) - independent deployment
- Request Service (FastAPI) - independent deployment
- Conversation Service (stays in main monolith temporarily)
```

**Phase 3 (Microservices v2):** Extract Conversation & Notification
```
5 Services + Event Bus:
- User Service
- Request Service  
- Conversation Service (WebSocket-enabled)
- Notification Service
- Booking Service (when ready)
```

### Inter-Service Communication

**Synchronous (REST/gRPC):**
- User Service → validates JWT tokens for other services
- Request Service → creates Conversation via REST
- Booking Service → reads from Request Service

**Asynchronous (Event Bus):**
- Replace in-memory event bus with **RabbitMQ/Kafka**
- Events: `UserCreated`, `RequestSubmitted`, `MessageCreated`, `BookingConfirmed`
- Services subscribe to relevant events

**Example Event Flow:**
```
Request Service publishes: RequestSubmitted
  ↓
Notification Service listens: Sends admin notification
Conversation Service listens: Creates conversation + first message
Analytics Service listens: Records metrics
```

### Code Extraction Steps

1. **Extract User Service:**
   - Copy `/src/domain/user/`, `/src/application/user/`
   - Create new `user-service/` repo with its own `main.py`
   - Add PostgreSQL/MySQL for users table
   - Expose `/api/v1/auth/`, `/api/v1/users/` endpoints
   - Publish `UserCreated`, `UserAuthenticated` events

2. **Extract Request Service:**
   - Copy `/src/domain/request/`, `/src/application/request/`
   - Create new `request-service/` repo
   - Depends on User Service (calls `/api/v1/users/{user_id}`)
   - Calls Conversation Service to create conversations
   - Publishes `RequestSubmitted`, `RequestStatusChanged` events

3. **Extract Conversation Service:**
   - Copy `/src/domain/conversation/`, `/src/application/conversation/`
   - Create new `conversation-service/` repo (WebSocket-enabled)
   - Depends on User Service (JWT validation)
   - Publishes `MessageCreated` events

### Shared Components Between Services

**Packages to Create** (`shared-lib/`):
- `event-bus/` - Base event classes, publisher/subscriber interfaces
- `auth/` - JWT utilities, token validation
- `exceptions/` - Standard domain exceptions
- `value-objects/` - Shared `UserId`, `RequestId`, `MessageId` value objects
- `logger/` - Centralized logging configuration

Each service imports from `shared-lib` to maintain consistency.

### Database Strategy

**Per-Service Database:**
```
User Service → PostgreSQL: users, user_profiles
Request Service → PostgreSQL: requests, request_items
Conversation Service → PostgreSQL: conversations, messages
Booking Service → PostgreSQL: bookings, invoices
```

**Shared Database (Read-Only Cache):**
- Redis for user sessions, JWT blacklist, conversation metadata
- Elasticsearch for message search and analytics

### API Gateway Pattern

Single entry point for clients:
```
Client → API Gateway (port 8000)
         ↓
         Route /api/v1/auth/* → User Service (8001)
         Route /api/v1/requests/* → Request Service (8002)
         Route /api/v1/conversations/* → Conversation Service (8003)
         Route /ws/chat/* → Conversation Service (8003)
```

Use **Kong**, **AWS API Gateway**, or **FastAPI reverse proxy** as gateway.

### Deployment Evolution

**Current (Single container):**
```
docker run -p 8000:8000 ajla-api
```

**Microservices (Docker Compose):**
```
services:
  api-gateway: FastAPI port 8000
  user-service: FastAPI port 8001
  request-service: FastAPI port 8002
  conversation-service: FastAPI port 8003
  event-bus: RabbitMQ port 5672
  mysql: MySQL port 3306
  redis: Redis port 6379
```

**Production (Kubernetes):**
```
k8s:
  - deployment: api-gateway (replicas: 3)
  - deployment: user-service (replicas: 2)
  - deployment: request-service (replicas: 2)
  - deployment: conversation-service (replicas: 3)  # High traffic
  - statefulset: MySQL
  - statefulset: RabbitMQ
  - statefulset: Redis
  - ingress: Route HTTP/WebSocket
```

### Why This Architecture Works for Microservices

✅ **Clean Separation:** Each domain is isolated, minimal coupling
✅ **Independent Scaling:** Conversation Service (WebSocket) scaled separately
✅ **Database per Service:** No shared schema, true isolation
✅ **Event-Driven:** Services communicate via events, not direct calls
✅ **Testability:** Each service can be tested independently
✅ **Language-Agnostic:** Could rewrite Notification Service in Node.js/Go later
✅ **Gradual Migration:** Extract one service at a time, keep rest monolithic

### Recommended Timeline

- **Month 1-2 (MVP):** Monolith, focus on core features
- **Month 3-4:** Identify bottlenecks, extract User Service
- **Month 5-6:** Extract Request Service
- **Month 7-8:** Extract Conversation Service (highest complexity)
- **Month 9+:** Add Notification, Booking, Admin services as needed
