
### Project Name
Diplom work
# Project Overview

## Technology Stack

- **Programming Language**: Python
- **Web Framework**: FastAPI
- **Architecture**: Clean Architecture

## Key Components

1. **FastAPI Framework**: The project is built using the FastAPI framework, providing a fast and modern approach to building APIs with Python.

2. **Clean Architecture**: The architecture follows the principles of Clean Architecture, emphasizing separation of concerns and maintainability.

3. **Redis Caching**: Redis is used for caching, providing fast and efficient storage for frequently accessed data. This enhances performance by reducing redundant database queries.

4. **Celery for Background Tasks**: Celery is employed for handling asynchronous tasks, improving responsiveness by offloading time-consuming operations to background workers.

5. **Celery Beat for Scheduled Tasks**: Celery Beat extends Celery by adding support for periodic tasks. It's utilized for scheduling daily tasks, such as fetching and storing a random Hadith of the day in Redis.

6. **Wasabi for Image Storage**: Wasabi technology is employed for storing images securely in the cloud. This choice provides a scalable and cost-effective solution for handling image storage.


### Project Structure

```plaintext
/project1
|-- docker-compose.yml
|-- Dockerfile
|-- logs
|-- README.md
|-- requirements.txt
|-- /src
|   |-- config
|   |-- constants.py
|   |-- controller
|   |-- dependencies.py
|   |-- exceptions
|   |-- __init__.py
|   |-- main.py
|   |-- model
|   |-- __pycache__
|   |-- redis.py
|   |-- repository
|   |-- responses.py
|   |-- schema
|   |-- script
|   |-- service
|   |-- utils
|   |-- worker.py
```

### Components

- **config:** Description of the configuration files
- **constants.py:** Description of constant values used in the project
- **controller:** Description of controllers handling requests
- **dependencies.py:** Description of external dependencies and packages
- **exceptions:** Description of custom exceptions
- **main.py:** Description of the main application entry point
- **model:** Description of data models used in the project
- **redis.py:** Description of Redis-related functionality
- **repository:** Description of data access and storage
- **responses.py:** Description of response handling
- **schema:** Description of data validation schemas
- **script:** Description of any scripts used in the project
- **service:** Description of business logic and services
- **utils:** Description of utility functions
- **worker.py:** Description of background celery processes

### Running the Project

#### Step 1: Clone the Project

```bash
git clone git@github.com:raqazhet/sajda_task.git
```

#### Step 2: Navigate to the Project Directory

```bash
cd sajda_task
```

#### Step 3: Create a `.env` File

Create a `.env` file in the project root directory and add the following variables.

```bash
touch .env
```

```plaintext
JWT_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
REFRESH_TOKEN_EXPIRES_HOURS=

# MongoDB
MONGO_USERNAME=
MONGO_PASSWORD=
MONGO_HOST=

# Redis
REDIS_PORT=
REDIS_HOST=
REDIS_DB=
REDIS_PASSWORD=

# AWS Connection
AWS_ENDPOIN_URL=
AWS_ACCESS_KEY_ID=
AWS_SECRET_KEY=
AWS_BUCKET_NAME=
```

#### Step 4: Build and Run Docker Containers

```bash
docker-compose up
```

#### Step 5: Access Swagger Documentation

Open your web browser and navigate to:

```
http://localhost:7777/docs
```


Here's a template for documenting the controllers:

### Controllers

# Authentication API Documentation in auth.py

## Overview

The `auth.py` file contains API endpoints related to user authentication, including user registration and login.

## API Endpoints

### Sign-Up - Create User

- **Endpoint**: `/v1/auth/sign-up`
- **Method**: `POST`
- **Response Model**: `dict`
- **Description**: Creates a new user in the system.
- **Parameters**:
  - `user_data`: The data for the new user in `UserCreate` model format in the request body.
  - `service`: The `UserService` dependency obtained through the `get_user_service` function.

- **Example request**:
```json
{
  "email": "qazaq@gmail.com",
  "firstname": "Qazaq",
  "lastname": "Style",
  "password": "QR_@911216",
  "phone_number": "+7707888888888",
  "region": "QAZAQ"
}
```

#### Code Explanation

- `create_user`: Service function that handles the logic for creating a new user in the database.

### Sign-In - User Login
For testing purposes, a default user with the following credentials can be used:
- **Endpoint**: `/v1/auth/sing-in`
- **Method**: `POST`
- **Responses**:
  - `200 OK`: Successful authentication.
  - `401 Unauthorized`: Invalid credentials.
- **Response Model**: `dict`
- **Description**: Authenticates a user and returns an authentication token.
- **Parameters**:
  - `form_data`: The OAuth2PasswordRequestForm containing the username and password in the request body.
  - `service`: The `UserService` dependency obtained through the `get_user_service` function.

- **Example request**:
```json
{
  "username": "admin@example.com",
  "password": "admin"
}
```

#### Code Explanation

- `sing_in_logic`: Service function that handles the logic for user authentication and returns an authentication token.



Certainly! Here's the documentation for your Ayah Router:

# Ayah API Documentation in ayah_router.py

## Overview

The `ayah.py` file contains API endpoints related to managing Ayah data, including creation, retrieval, and deletion.


### Create Ayah

- **Endpoint**: `/v1/ayah/`
- **Method**: `POST`
- **Response Model**: `dict`
- **Description**: Creates a new Ayah in the system.
- **Parameters**:
  - `ayah_data`: The data for the new Ayah in `AyahCreate` model format in the request body.
  - `current_user`: The current authenticated user obtained through the `get_current_user` dependency.
  - `service`: The `AyahService` dependency obtained through the `get_ayah_service` function.

- **Example request**:
```json
{
  "surah_title": "sura title",
  "surah_ayah": "1:12",
  "arabic_text": "text of arabic",
  "languages": [
    {
      "transcript": "Субханаллах",
      "translate_text": "Алла тағала кемшіліктен пәк",
      "lang": "QAZ"
    }
  ]
}
```

#### Code Explanation

- Validates the user's role, allowing only users with the role "admin" to create Ayahs.
- `create_ayah`: Service function that handles the logic for creating a new Ayah in the database.

### Get Ayah by ID

- **Endpoint**: `/ayah/{id}`
- **Method**: `GET`
- **Response Model**: `dict`
- **Description**: Retrieves information about a specific Ayah by its ID.
- **Parameters**:
  - `id`: The ID of the Ayah to retrieve.
  - `service`: The `AyahService` dependency obtained through the `get_ayah_service` function.

- **Example Response**:
```json
{
  "result": {
    "id": "12345",
    "surah_title": "surah title",
    "surah_ayah": "1:12",
    "arabic_text": "text of arabic",
    "languages": [
      {
        "transcript": "Субханаллах",
        "translate_text": "Алла тағала кемшіліктен пәк",
        "lang": "QAZ"
      }
    ],
    "created": 1645948800,
    "updated": 1645948800,
    "hijri_time": 1645948800
  }
}
```

#### Code Explanation

- Checks the Redis cache for the Ayah data and returns it if found to optimize response time.
- `get_ayah_by_id`: Service function that fetches the Ayah by its ID.

### Get All Ayahs

- **Endpoint**: `/ayah/`
- **Method**: `GET`
- **Response Model**: `Page[AyahSchema]`
- **Description**: Retrieves a paginated list of all Ayahs in the system.
- **Parameters**:
  - `service`: The `AyahService` dependency obtained through the `get_ayah_service` function.

- **Example Response**:
```json
{
  "items": [
    {
      "id": "12345",
      "surah_title": "surah title",
      "surah_ayah": "1:12",
      "arabic_text": "text of arabic",
      "languages": [
        {
          "transcript": "Субханаллах",
          "translate_text": "Алла тағала кемшіліктен пәк",
          "lang": "QAZ"
        }
      ],
      "created": 1645948800,
      "updated": 1645948800,
      "hijri_time": 1645948800
    }
  ]
}
```

#### Code Explanation

- `get_all_ayahs`: Service function that fetches all Ayahs.

### Delete Ayah by ID

- **Endpoint**: `/ayah/{id}`
- **Method**: `DELETE`
- **Response Model**: `dict`
- **Description**: Deletes a specific Ayah by its ID.
- **Parameters**:
  - `id`: The ID of the Ayah to delete.
  - `current_user`: The current authenticated user obtained through the `get_current_user` dependency.
  - `service`: The `AyahService` dependency obtained through the `get_ayah_service` function.

- **Example request**:
```shell
localhost:7777/ayah/12345
```

#### Code Explanation

- Validates the user's role, allowing only users with the role "admin" to delete Ayahs.
- `delete_ayah_by_id`: Service function that deletes the Ayah



# CRUD operations

Let's document the CRUD operations for the remaining files `hadith.py`, `dhikr.py`, `like.py`, and `user.py`. We'll focus on one API endpoint from each file, similar to the `get_hadith_of_the_day` endpoint:

### Get Hadith of the Day

- **Endpoint**: `/v1/hadith/random/hadith`
- **Method**: `GET`
- **Response Model**: `dict`
- **Description**: Retrieves the Hadith of the day.
- **Parameters**:
  - None

- **Example Response**:
```json
{
  "result": "Hadith data of the day"
}
```
#### Code Explanation

- Retrieves the Hadith of the day from the cache (Redis) using the current date.
- Raises an exception if the Hadith data is not found, indicating a potential Celery Beat error.


# Celery Beat Workflow for [Hadith,ayah,dhikr,image] of the Day

## Overview

The system utilizes Celery Beat to perform a daily task of selecting a random Hadith and storing it in Redis. This process ensures that users can quickly retrieve the Hadith of the day without querying the database each time.

## Workflow

1. **Scheduled Task**: Celery Beat is configured to execute a scheduled task daily.

2. **Select Random Hadith**: The scheduled task triggers a function that selects a random Hadith from the collection.

3. **Cache Key Generation**: The system generates a unique cache key using the current date in the format `f"{date.today().isoformat()}_hadith"`.

4. **Store in Redis**: The selected random Hadith is then stored in Redis under the generated cache key.

5. **Expiration Time**: The cached Hadith data is set to expire after 24 hours to ensure that a new random Hadith is selected the next day.

## Code Implementation

The following code snippet in `./src/worker.py` showcases the implementation of the Celery Beat 


# Image Storage with Wasabi Technology

## Overview

The system employs Wasabi technology for efficient and scalable image storage. Wasabi is a cloud storage service known for its cost-effectiveness, performance, and durability. It provides secure and reliable storage solutions, allowing the system to store and retrieve images seamlessly.

## Image Storage Workflow

1. **Wasabi Account Setup**: Users need to set up a Wasabi account to access the cloud storage service.

2. **Integration with FastAPI**: The system integrates Wasabi storage into the FastAPI application to facilitate image storage and retrieval.

3. **Upload Images**: When users upload images through the application, the system utilizes Wasabi APIs to store the images securely in the cloud.

4. **Image URLs**: Wasabi provides unique URLs for each stored image, enabling easy retrieval and rendering in the application.

5. **Cost-Effective Storage**: Wasabi offers competitive pricing, and the free trial period allows users to experience the benefits without initial costs.

## Code Implementation
The following code snippet in `./src/controller/file.py` 


