# 🔐 SpeakBetter - Authentication Implementation

This document details the multi-user support and JWT-based authentication system implemented for SpeakBetter.

## 📌 Overview
To support multiple users and maintain progress (streaks and history), we use a secure token-based authentication system.

## 🏗️ Technical Stack
*   **Hash Algorithm:** BCrypt (for password storage).
*   **Token Type:** JSON Web Token (JWT).
*   **Library:** `PyJWT` (Python/FastAPI) and `localStorage` (React).

## 🔑 Authentication Endpoints
### 1. Register
*   **Endpoint:** `POST /auth/register`
*   **Description:** Creates a new user record in MongoDB.
*   **Request Body:**
    ```json
    {
      "name": "User Name",
      "email": "user@example.com",
      "password": "secure_password"
    }
    ```

### 2. Login
*   **Endpoint:** `POST /auth/login`
*   **Description:** Validates credentials and returns a JWT.
*   **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "secure_password"
    }
    ```
*   **Response:**
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
    }
    ```

## 🔒 Protected Route Middleware
All endpoints except `/auth` and `/ping` are protected. The FastAPI backend implements a dependency to:
1.  Extract the token from the `Authorization: Bearer <token>` header.
2.  Validate the token signature against the `JWT_SECRET`.
3.  Ensure the token has not expired.
4.  Extract the `user_id` and attach it to the request context.

## 🗄️ Database Integration (MongoDB)
### User Model
```python
class User(BaseModel):
    name: str
    email: str
    hashed_password: str
    streak: int = 0
    last_active: datetime = None
```

## 🎤 Frontend Integration (React)
1.  **Storage:** Store the token in `localStorage`.
2.  **Request Header:** Include the token in all API calls via an Axios interceptor or custom `fetch` wrapper.
3.  **State:** Use a global `AuthContext` to manage user state and login status.

## ⚠️ Security Considerations
*   **HTTPS:** Required in production (Render/Netlify handle this).
*   **Environment Variables:** `JWT_SECRET` must be kept secret and configured on the hosting platform.
*   **Token Expiration:** Set to 7 days for a balance between security and user convenience.
