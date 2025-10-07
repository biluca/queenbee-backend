# JWT Authentication Setup

## Overview

The backend now includes JWT (JSON Web Token) based authentication using `djangorestframework-simplejwt`. This provides secure, stateless authentication for your API.

## Installation & Setup

The following changes have been made to enable JWT authentication:

### 1. Dependencies Added
- `djangorestframework-simplejwt==5.3.0` added to requirements.txt

### 2. Django Settings Updates
- Added `rest_framework_simplejwt` to INSTALLED_APPS
- Added `authentication` app to INSTALLED_APPS
- Updated REST_FRAMEWORK settings with JWT authentication classes
- Added SIMPLE_JWT configuration with token lifetimes and settings

### 3. Authentication App Created
A new `authentication` app has been created with the following views:
- Login (JWT token generation)
- Token refresh
- Logout (token blacklisting)
- User registration
- User profile management

## API Endpoints

### Authentication Endpoints

#### 1. Login
**POST** `/api/auth/login/`

Request body:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": "",
    "is_staff": true,
    "is_superuser": true
  }
}
```

#### 2. Token Refresh
**POST** `/api/auth/token/refresh/`

Request body:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 3. Logout
**POST** `/api/auth/logout/`

Headers: `Authorization: Bearer <access_token>`

Request body:
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Response:
```json
{
  "message": "Successfully logged out"
}
```

#### 4. User Registration
**POST** `/api/auth/register/`

Request body:
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

Response:
```json
{
  "message": "User created successfully",
  "user": {
    "id": 2,
    "username": "newuser",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### User Profile Endpoints

#### 5. Get Profile
**GET** `/api/auth/profile/`

Headers: `Authorization: Bearer <access_token>`

Response:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "",
  "last_name": "",
  "is_staff": true,
  "is_superuser": true,
  "date_joined": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-15T15:45:00Z"
}
```

#### 6. Update Profile
**PUT/PATCH** `/api/auth/profile/update/`

Headers: `Authorization: Bearer <access_token>`

Request body:
```json
{
  "first_name": "Updated",
  "last_name": "Name",
  "email": "updated@example.com"
}
```

Response:
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "updated@example.com",
    "first_name": "Updated",
    "last_name": "Name"
  }
}
```

## How to Use Authentication

### 1. For Protected Endpoints
All API endpoints now require authentication by default. To access protected endpoints:

1. Login to get access token
2. Include the token in the Authorization header: `Authorization: Bearer <access_token>`

### 2. Token Lifetimes
- **Access Token**: 60 minutes
- **Refresh Token**: 7 days
- Refresh tokens are rotated on each refresh for security

### 3. Example Usage with curl

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Use token to access protected endpoint
curl -X GET http://localhost:8000/api/customers/ \
  -H "Authorization: Bearer <your_access_token>"
```

### 4. Example Usage with JavaScript/Fetch

```javascript
// Login
const loginResponse = await fetch('/api/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin123'
  })
});

const loginData = await loginResponse.json();
const accessToken = loginData.access;

// Use token for protected requests
const customersResponse = await fetch('/api/customers/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

## Testing the Authentication

### Using the provided test script:

1. Make sure the Django server is running: `python manage.py runserver`
2. Run the test script: `python test_auth.py`

### Manual Testing:

1. Start the Django server: `python manage.py runserver`
2. Use a tool like Postman, curl, or any HTTP client to test the endpoints above

## Security Features

- JWT tokens are signed with Django's SECRET_KEY
- Refresh tokens are blacklisted on logout
- Tokens are rotated on refresh for enhanced security
- Access tokens have short expiration times (60 minutes)
- All customer and appointment endpoints now require authentication

## Admin User

A superuser has been created for testing:
- **Username**: admin
- **Password**: admin123
- **Email**: admin@example.com

You can use these credentials to test the authentication system.

## Next Steps

The authentication system is now fully functional. You can:

1. Test all endpoints using the provided credentials
2. Create new users via the registration endpoint
3. Integrate this authentication with your frontend application
4. Customize user model or add additional fields as needed
5. Add role-based permissions if required