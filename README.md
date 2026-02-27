# 🛒 WHITELABELSHOP - E-commerce API

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge)](https://whitelabel-shop-2c8c21e0d0c0.herokuapp.com/api/products/)

Backend infrastructure built with **Django 5.x** and **DRF**, deployed on **Heroku** with **AWS** integration.

## 🛠 Tech Stack
* **Framework:** Python 3.x / Django 5.x / DRF
* **Database:** PostgreSQL (AWS RDS)
* **Storage:** AWS S3 (Media & Static files via `boto3`)
* **Auth:** JWT (SimpleJWT)
* **API Docs:** Swagger UI (OpenAPI 3.0) - *In Progress*

## 🚀 Architecture Highlights
* **S3 Persistence:** AWS S3 integration for media storage (required for Heroku's ephemeral filesystem).
* **Decoupled Database:** PostgreSQL hosted on AWS RDS for persistence and scalability.
* **Frontend-Ready:** Specifically configured for React/Redux consumption (CORS, JWT, structured JSON).
* **Core Logic:** Order processing logic with stock updates and data consistency handling.

## 🔗 Core Endpoints (Showcase)
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/users/login/` | JWT Token Generation | Public |
| `GET` | `/api/users/profile/` | User Profile Data | **JWT** |
| `GET` | `/api/products/` | Product List & Search | Public |
| `POST` | `/api/products/upload/` | Secure Media Upload to S3 | **Admin** |
| `POST` | `/api/orders/add/` | Order Logic & Stock Update | **JWT** |

> **🚧 Documentation Update:** **Swagger UI** integration is underway. Interactive API documentation will soon be accessible.

## ⚙️ Local Setup
```bash
# 1. Clone the repository
git clone https://github.com/KyriakosVerveridis/-Django-React-E--commerce-.git

# 2. Enter directory
cd -Django-React-E--commerce-/backend

# 3. Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Run
python manage.py migrate
python manage.py runserver

👤 Author

Kyriakos Ververidis
Backend Python Developer
Greece-Open to Remote
ververidiskyriakos@gmail.com|https://www.linkedin.com/in/kyriakos-ververidis/

## 📝 License
This project is open-source and free to use for educational purposes. License: MIT License.