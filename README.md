# Travel API

A **Travel API** built using Flask, supporting multiple microservices for user management, destination management, and authentication. The system utilizes **JWT tokens** for secure communication and role-based access control.

## Overview

The **Travel API** is a set of independent microservices that allow users to:
1. Register, authenticate, and manage user profiles.
2. Manage travel destinations (list, delete).
3. Ensure role-based access control using JWT tokens.

### Microservices:
- **Auth Service**: Manages JWT token generation and validation, including role-based access checks.
- **User Service**: Manages user registration, login, and profile management.
- **Destination Service**: Manages travel destinations (list, delete).
- **API Gateway**: Routes incoming requests to appropriate microservices.

---

## Architecture

The application follows a **microservice architecture** with the following services:
1. **Auth Service**: Handles authentication and role-based access control.
2. **User Service**: Manages user details and login functionality.
3. **Destination Service**: Manages travel destinations (CRUD operations).
4. **API Gateway**: A single entry point that routes requests to the appropriate service.

Each service communicates independently with others through HTTP calls, ensuring modularity and scalability.

---

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/zas03ia/Microservice_based_destination_app.git
```

### Step 2: Set up the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install the dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Before running the application, configure the environment variables:

## env
An example env file is provided.

## Running the Application

To run the **Travel API** services:

1. **Start the Auth Service**:
   ```bash
   FLASK_APP=auth_service.app FLASK_ENV=development flask run --port 5003
   ```

2. **Start the User Service**:
   ```bash
   FLASK_APP=user_service.app FLASK_ENV=development flask run --port 5002
   ```

3. **Start the Destination Service**:
   ```bash
   FLASK_APP=destination_service.app FLASK_ENV=development flask run --port 5001
   ```

4. **Start the API Gateway**:
   ```bash
   FLASK_APP=gateway.app FLASK_ENV=development flask run --port 5000
   ```

---

## Usage

### Authentication Service

- **POST /auth/login**: Authenticate a user and receive a JWT token.
  - Body:
    ```json
    {
        "email": "user@example.com",
        "password": "password123"
    }
    ```

- **POST /auth/validate-role**: Check if the current user has the required role (`Admin` or `User`).
  - Body:
    ```json
    {
        "role": "Admin"
    }
    ```

### User Service

- **POST /users/register**: Register a new user.
  - Body:
    ```json
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "role": "Admin"
    }
    ```

- **POST /users/login**: User login (returns JWT token).
  - Body:
    ```json
    {
        "email": "john.doe@example.com",
        "password": "password123"
    }
    ```

- **GET /users/profile**: Get user profile information (requires JWT token).

### Destination Service

- **GET /destinations**: Retrieve a list of all travel destinations.

- **DELETE /destinations/{destination_id}**: Delete a specific travel destination (Admin-only, requires JWT token).

### API Gateway

The **API Gateway** is the entry point for all incoming requests. It will route the request to the appropriate microservice.

- **GET /destinations**: Routes to the **Destination Service**.
- **DELETE /destinations/{destination_id}**: Routes to the **Destination Service**.
- **POST /users/login**: Routes to the **User Service**.
- **POST /users/register**: Routes to the **User Service**.

---

## Testing

You can run unit and integration tests for each service to ensure everything works as expected. Each microservice includes a `/tests` directory containing test cases.

To run the tests for the services, use:

```bash
coverage run -m unittest
coverage report
```

---

## Swagger Documentation

All services have integrated Swagger documentation via **Flasgger**.

- **Auth Service Swagger**: [http://localhost:5003/apidocs](http://localhost:5003/apidocs)
- **User Service Swagger**: [http://localhost:5002/apidocs](http://localhost:5002/apidocs)
- **Destination Service Swagger**: [http://localhost:5001/apidocs](http://localhost:5001/apidocs)
- **API Gateway Swagger**: [http://localhost:5000/docs/desatination](http://localhost:5000/docs/destination), [http://localhost:5000/docs/user](http://localhost:5000/docs/user), [http://localhost:5000/docs/auth](http://localhost:5000/docs/auth)

---

## Dependencies

- **Flask**: Web framework for building microservices.
- **Flask-JWT-Extended**: JWT token management for authentication and authorization.
- **Flask-Swagger-UI & Flasgger**: API documentation using Swagger.
- **requests**: HTTP requests for inter-service communication.
- **python-decouple**: To manage environment variables.

