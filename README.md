# 🛒 WHITELABELSHOP - Django REST API & eCommerce Infrastructure
> **⚠️ Status: Work in Progress** > Core backend logic and authentication are completed. Currently integrating the final frontend features and PayPal API.

A professional-grade Backend API architecture built with Django REST Framework, designed to power scalable eCommerce applications. This project prioritizes robust server-side logic, secure JWT authentication, and complex database modeling, while providing a seamless integration point for dynamic Frontends like React.

🚀 Features

* **Advanced Backend API:** Built with Django REST Framework for seamless data flow.
* **JWT Authentication:** Secure user login and registration using JSON Web Tokens.
* **Complete Checkout Workflow:** Integrated shipping, payment methods, and order processing.
* **Media Management:** Image upload and processing with Pillow (AWS S3 ready).
* **Admin Dashboard:** Full control over product inventory, user accounts, and order fulfillment.
* **Product Interaction:** System for product reviews, ratings, and top-product carousels.

🛠️ Tech Stack

* **Backend:** Django 5.2.7 (Python 3.12), Django REST Framework
* **Database:** SQLite (Development) / PostgreSQL compatible
* **Security:** SimpleJWT (Authentication), CORS Headers
* **Dependencies:** pillow, django-storages, boto3, PyJWT
* **Frontend:** React, React-Bootstrap, Redux (Global State Management)

⚙️ Installation & Setup

1. Clone the repository
git clone https://github.com/KyriakosVerveridis/-Django-React-E--commerce-.git
cd ECOMMERCE

2. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux: source venv/bin/activate | Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

3. Frontend Setup
cd ../frontend
npm install
npm start

Access the app
Main Store: http://127.0.0.1:3000
API Root: http://127.0.0.1:8000/api/

🧠 Learning Outcomes

Through this project, I mastered how to:
* Design and implement **RESTful APIs** using Django.
* Transition business logic from **Express/Node.js to Python/Django**.
* Secure endpoints using **JWT Authentication** and custom permissions.
* Manage complex database relationships for **Orders and Inventory**.
* Connect a **React/Redux** frontend to a Django backend via Axios.
* Handle media file storage and cloud integration (AWS S3).

👤 Author

Kyriakos Ververidis 📍 Based in Greece 💬 Open to remote opportunities 📧 ververidiskyriakos@gmail.com 🔗 https://www.linkedin.com/in/kyriakos-ververidis-593a8561/

## 📝 License
This project is open-source and free to use for educational purposes. License: MIT License.