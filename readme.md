# DashOrder Project

## Overview  
DashOrder is a Django-based web application with a RESTful API for managing 
user orders. It supports JWT authentication, role-based permissions (Admin and Customer), and includes API documentation via Swagger.

---

## Features  
- Custom user model with roles (Admin, Customer)  
- CRUD operations on orders with permission control  
- JWT authentication (access and refresh tokens)  
- API documentation with Swagger & ReDoc  
- Database migrations and static files handling automated  
- Dockerized deployment with Docker Compose

---

## Environment Variables  
| Variable          | Description                          | Example                        |
|-------------------|------------------------------------|--------------------------------|
| SECRET_KEY        | Django secret key                   | secret_key               <br/> |
| DEBUG             | Debug mode (True/False)             | False                          |
| POSTGRES_DB       | Postgres database name              | db_name                        |
| POSTGRES_USER     | Postgres username                   | user                           |
| POSTGRES_PASSWORD | Postgres password                   | 12345                          |
| DB_HOST           | Database host (service name or IP) | db                             |
| DB_PORT           | Database port                      | 5432                           |
| ALLOWED_HOSTS     | Allowed hosts for Django            | 127.0.0.1,localhost,0.0.0.0    |

---

## Setup & Run

### Prerequisites  
- Docker & Docker Compose installed  
- Environment variables set in `.env` file

### Build and Run with Docker Compose  
```bash
docker-compose up --build
```
### Entrypoint script (entrypoint.sh)
- Applies database migrations

- Collects static files

- Starts the Django application


### API Authentication
- JWT tokens (access and refresh) via /api/token/ and /api/token/refresh/

- Use token in Authorization: Bearer <token> header for authenticated requests

### API Endpoints
| Endpoint            | Method | Description             | Permissions         |
| ------------------- | ------ | ----------------------- | ------------------- |
| `/api/orders/`      | GET    | List user orders        | Authenticated users |
| `/api/orders/`      | POST   | Create new order        | Authenticated users |
| `/api/orders/{id}/` | GET    | Retrieve specific order | Owner or Admin      |
| `/api/orders/{id}/` | PUT    | Update specific order   | Owner or Admin      |
| `/api/orders/{id}/` | DELETE | Delete specific order   | Owner or Admin      |


### API Documentation
- Swagger UI: /swagger/
- ReDoc: /redoc/

### Testing
To run tests, use Django’s test command:

```bash
docker-compose exec web pytest
```
### Install dependencies without Docker:

- pip install -r requirements.txt


### Project Structure Highlights
**account** app: Custom user model and permissions

**order** app: Order model, filters, serializers, and views

order/api/views.py: OrderViewSet with permissions and filters

JWT authentication using rest_framework_simplejwt

Swagger docs via drf_yasg

Dockerized environment with Dockerfile, docker-compose.yml, and entrypoint.sh