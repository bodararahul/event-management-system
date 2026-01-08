# API Documentation

Complete API reference for the Event Management System.

## Base URL

```
http://localhost:8000/api
```

## Authentication

All endpoints (except registration and login) require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Response Format

All responses follow a consistent format:

### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error message",
  "errors": { ... }
}
```

---

## Authentication Endpoints

### Register User

**POST** `/api/auth/register/`

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "email": "user@example.com",
      "name": "John Doe",
      "role": "USER",
      "date_joined": "2024-01-01T00:00:00Z"
    }
  }
}
```

---

### Login

**POST** `/api/auth/login/`

Authenticate and receive JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": { ... },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
  }
}
```

---

### Logout

**POST** `/api/auth/logout/`

**Headers:**
- `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "refresh": "refresh_token_here"
}
```

**Response:** `200 OK`

---

### Get Profile

**GET** `/api/auth/profile/`

**Headers:**
- `Authorization: Bearer <access_token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Profile retrieved successfully",
  "data": {
    "email": "user@example.com",
    "name": "John Doe",
    "role": "USER",
    "date_joined": "2024-01-01T00:00:00Z"
  }
}
```

---

## Event Endpoints

### List Events

**GET** `/api/events/`

List all active events with optional filtering.

**Query Parameters:**
- `status` - Filter by status (UPCOMING, ONGOING, COMPLETED, CANCELLED)
- `location` - Filter by location
- `search` - Search in title and description
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10)

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Events retrieved successfully",
  "data": {
    "count": 10,
    "next": "http://localhost:8000/api/events/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "Tech Conference 2024",
        "description": "Annual technology conference",
        "location": "San Francisco",
        "start_date": "2024-06-01T09:00:00Z",
        "end_date": "2024-06-03T17:00:00Z",
        "capacity": 500,
        "status": "UPCOMING",
        "created_by": {
          "email": "organizer@example.com",
          "name": "Event Organizer"
        },
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

---

### Get Event Details

**GET** `/api/events/{id}/`

Get detailed information about a specific event.

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Event retrieved successfully",
  "data": {
    "id": 1,
    "title": "Tech Conference 2024",
    "description": "Annual technology conference",
    "location": "San Francisco",
    "start_date": "2024-06-01T09:00:00Z",
    "end_date": "2024-06-03T17:00:00Z",
    "capacity": 500,
    "status": "UPCOMING",
    "created_by": { ... },
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

---

### Create Event

**POST** `/api/events/`

Create a new event. Requires ADMIN or ORGANIZER role.

**Headers:**
- `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "title": "New Event",
  "description": "Event description",
  "location": "Event Location",
  "start_date": "2024-06-01T09:00:00Z",
  "end_date": "2024-06-01T17:00:00Z",
  "capacity": 100,
  "status": "UPCOMING"
}
```

**Response:** `201 Created`

---

### Update Event

**PUT/PATCH** `/api/events/{id}/`

Update an existing event. Requires ADMIN or ORGANIZER role.

**Headers:**
- `Authorization: Bearer <access_token>`

**Request Body:** (same as create, all fields optional for PATCH)

**Response:** `200 OK`

---

### Delete Event

**DELETE** `/api/events/{id}/`

Soft delete an event. Requires ADMIN role.

**Headers:**
- `Authorization: Bearer <access_token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Event deleted",
  "data": {}
}
```

---

## Registration Endpoints

### Register for Event

**POST** `/api/events/{id}/register/`

Register the authenticated user for an event.

**Headers:**
- `Authorization: Bearer <access_token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Successfully registered for event",
  "data": {
    "id": 1,
    "user": { ... },
    "event": { ... },
    "registered_at": "2024-01-01T00:00:00Z",
    "status": "ACTIVE"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Event capacity exceeded or already registered
- `404 Not Found` - Event not found

---

### Get My Registrations

**GET** `/api/registrations/`

Get all registrations for the authenticated user.

**Headers:**
- `Authorization: Bearer <access_token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Registrations retrieved successfully",
  "data": [
    {
      "id": 1,
      "event_title": "Tech Conference 2024",
      "event_location": "San Francisco",
      "event_start_date": "2024-06-01T09:00:00Z",
      "registered_at": "2024-01-01T00:00:00Z",
      "status": "ACTIVE"
    }
  ]
}
```

---

### Get All Registrations (Admin)

**GET** `/api/admin/registrations/`

Get all registrations across all users. Requires ADMIN role.

**Headers:**
- `Authorization: Bearer <access_token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "All registrations retrieved successfully",
  "data": [
    {
      "id": 1,
      "user": { ... },
      "event": { ... },
      "registered_at": "2024-01-01T00:00:00Z",
      "status": "ACTIVE"
    }
  ]
}
```

---

## Error Codes

- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Rate Limiting

Rate limiting is configured and ready. Adjust limits in settings as needed.

---

## Pagination

List endpoints support pagination with the following query parameters:
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10, max: 100)

---

## Filtering

Event list endpoint supports filtering:
- `status` - Filter by event status
- `location` - Filter by location (partial match)
- `search` - Search in title and description

Example:
```
GET /api/events/?status=UPCOMING&location=San Francisco&search=conference
```

