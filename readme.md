
 # Pet Shop App
 
 A FastAPI app for managing pets, featuring both public and administrator interfaces, built with asynchronous SQLAlchemy ORM and JWT-based authentication.

 <p style="text-align: center;">
  <img src=".github/logo.png" alt="Pet Shop Logo" width="350"/>
 </p>
 
 ## Table of Contents
 
 - [Features](#features)
 - [Tech Stack](#tech-stack)
 - [Installation](#installation)
 - [Configuration](#configuration)
 - [API Documentation](#api-documentation)
   - [Authentication](#authentication)
     - [Register](#register)
     - [Login](#login)
   - [Public Endpoints](#public-endpoints)
     - [Search Pets](#search-pets)
     - [Get Pet Details](#get-pet-details)
   - [Admin Endpoints](#admin-endpoints)
     - [Create Pet](#create-pet)
     - [Update Pet](#update-pet)
     - [Delete Pet](#delete-pet)
     - [Search Pets (Admin)](#search-pets-admin)
     - [Get Pet Details (Admin)](#get-pet-details-admin)
 
 ## Features
 
 - **Public API** (no authentication):
   - Search for pets by `type`, `name`, `breed`, `color`, `min_age`, and `max_age`
   - Retrieve pet details (excluding secret info)
 
 - **Admin API** (JWT Authentication required):
   - Create, update, and delete pets (with secret info)
   - Search pets including the `secret_info` field
   - Retrieve full pet details
 
 - **Authentication**:
   - User registration and login with bcrypt-hashed passwords
   - JWT Bearer tokens (HS256, configurable expiry)
 
 ## Tech Stack
 
 - **Python** 3.12+
 - **FastAPI** for building the API
 - **Uvicorn** as the ASGI server
 - **SQLAlchemy** (v2) Async ORM
 - **Pydantic** v2 for schema validation
 - **bcrypt** for password hashing
 - **PyJWT** for JWT token handling
 
 ## Installation
 
 1. **Clone the repository**  
    ```bash
    git clone https://github.com/your-org/pet-shop.git
    cd pet-shop
    ```
 
 2. **Create a virtual environment and install deps**  
    ```bash
    poetry install
    poetry shell
    ```
 
 3. **Run the server**  
    ```bash
    uvicorn main:app --reload
    ```


## Configuration
 
 Create a `.env` (if using vscode) file (or set environment variables) with:
 
 ```dotenv
 DB_URL=postgresql+asyncpg://@localhost:5432/petshop
JWT_SECRET_KEY=petshopsecret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
 ```
 
 - `DB_URL`: Database connection string
 - `SECRET_KEY`: Signing key for JWT tokens
 
 
 The API will be available at `http://127.0.0.1:8000`.
 
 ## API Documentation
 
 Once running, visit the interactive docs at `http://127.0.0.1:8000/docs`.
 
 ### Authentication
 
 #### Register
 
 ```http
 POST /auth/register
 Content-Type: application/json
 
 {
   "login": "admin",
   "password": "secret"
 }
 ```
 
 _Response:_
 
 ```json
 {
   "status": "success"
 }
 ```
 
 #### Login
 
 ```http
 POST /auth/login
 Content-Type: application/json
 
 {
   "login": "admin",
   "password": "secret"
 }
 ```
 
 _Response:_
 
 ```json
 {
   "access_token": "<jwt_token>",
   "token_type": "bearer"
 }
 ```
 
 ### Public Endpoints
 
 #### Search Pets
 
 ```http
 GET /pets/find?type=cat&min_age=1.0&max_age=5.0
 ```
 
 _Response:_
 
 ```json
 [
   {
     "id": 1,
     "type": "cat",
     "name": "Barsik",
     "breed": "Sfinks",
     "color": "black",
     "age": 3.0
   }
 ]
 ```
 
 #### Get Pet Details
 
 ```http
 GET /pets/details?pet_id=1
 ```
 
 _Response:_
 
 ```json
 {
   "id": 1,
   "type": "cat",
   "name": "Barsik",
   "breed": "Sfinks",
   "color": "black",
   "age": 3.0
 }
 ```
 
 ### Admin Endpoints
 
 _All admin routes require:_
 
 ```
 Authorization: Bearer <jwt_token>
 ```
 
 #### Create Pet
 
 ```http
 POST /admin/pets/
 Content-Type: application/json
 
 {
   "type": "dog",
   "name": "Buddy",
   "breed": "Labrador",
   "color": "yellow",
   "age": 3.5,
   "secret_info": "fake pedigree"
 }
 ```
 
 #### Update Pet
 
 ```http
 PUT /admin/pets/1
 Content-Type: application/json
 
 {
   "color": "chocolate",
   "secret_info": "smuggled"
 }
 ```
 
 #### Delete Pet
 
 ```http
 DELETE /admin/pets/1
 ```
 
 #### Search Pets (Admin)
 
 ```http
 GET /admin/pets/?secret_info=smuggled&breed=Labrador
 ```
 
 #### Get Pet Details (Admin)
 
 ```http
 GET /admin/pets/1
 ```


```text
▖  ▖▄▖▖ ▖▖▄▖▄▖▄▖
▛▖▞▌▌▌▌ ▌▌▙▖▙▘▙▖
▌▝ ▌▛▌▙▖▚▘▙▖▌▌▙▖
                
```