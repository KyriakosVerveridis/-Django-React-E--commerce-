# 🛒 WHITELABELSHOP - E-commerce API

[![API Docs](https://img.shields.io/badge/Swagger-API_Docs-blue?style=for-the-badge)](https://whitelabel-shop-2c8c21e0d0c0.herokuapp.com/api/docs/)

Backend infrastructure built with **Django 5.x** and **DRF**, deployed on **Heroku** with **AWS** integration.

## 🛠 Tech Stack
* **Framework:** Python 3.x / Django 5.x / DRF
* **Database:** PostgreSQL (AWS RDS)
* **Storage:** AWS S3 (Media & Static files via `boto3`)
* **Auth:** JWT (SimpleJWT)
* **API Docs:** Swagger UI (OpenAPI 3.0)
* **Testing:** Django TestCase / UnitTest

## 🚀 Architecture Highlights
* **S3 Persistence:** AWS S3 integration for media storage (required for Heroku's ephemeral filesystem).
* **Decoupled Database:** PostgreSQL hosted on AWS RDS for persistence and scalability.
* **Frontend-Ready:** Specifically configured for React/Redux consumption (CORS, JWT, structured JSON).
* **Core Logic:** Order processing logic with stock updates and data consistency handling.
* **Interactive Documentation:** Fully integrated Swagger UI for real-time API testing.
* **Docker Ready:** Containerized environment for consistent development.

## 🔗 Core Endpoints (Showcase)
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/users/login/` | JWT Token Generation | Public |
| `GET` | `/api/users/profile/` | User Profile Data | **JWT** |
| `GET` | `/api/products/` | Product List & Search | Public |
| `POST` | `/api/products/upload/` | Secure Media Upload to S3 | **Admin** |
| `POST` | `/api/orders/add/` | Order Logic & Stock Update | **JWT** |


## ⚙️ Local Setup
```bash
# 1. Clone the repository
git clone https://github.com/KyriakosVerveridis/-Django-React-E--commerce-.git

# 2. Enter directory
cd ./-Django-React-E--commerce-

# 3. Spin up the containers (Environment variables are handled via .env.dev)
docker-compose --env-file ./backend/.env.dev up --build

# 4. Run database migrations (inside the container)
docker-compose exec backend python manage.py migrate

# 5. Run Tests
docker-compose exec backend python manage.py test
```

## 👤 Author

**Kyriakos Ververidis** *Backend Python Developer* 📍 Greece (Open to Remote)

📧 [ververidiskyriakos@gmail.com](mailto:ververidiskyriakos@gmail.com)  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/kyriakos-ververidis/)

## 📝 License
This project is open-source and free to use for educational purposes. License: MIT License.