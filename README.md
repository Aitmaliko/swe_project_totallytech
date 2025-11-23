
# 🛒 B2B HandShake by TotallyTech

A scalable multi-platform system enabling seamless B2B interaction between suppliers and business clients (restaurants, hotels, cafés).  
The platform consists of:

- **Web Application** – Supplier management panel (Owner, Manager)
- **Mobile Application** – For Consumers and Sales Representatives
- **Backend API** – Central business logic and data layer

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Technologies](#technologies)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Quick Start – 5-Min Demo](#quick-start--5-min-demo)
- [Testing](#testing)
- [Roles & Permissions](#roles--permissions)
- [API Documentation](#api-documentation)
- [Docker](#docker)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Support](#support)
- [License](#license)
- [Contributing](#contributing)

---

## 🎯 About the Project

The B2B Supply Chain Management System provides a unified environment where **suppliers** and **business consumers** interact through product catalogs, link approvals, order workflows, chat communication, and complaint escalation.

### Core Capabilities

- Product management & inventory  
- Supplier–consumer link approval  
- Order placement & processing  
- Built-in chat  
- Multi-level complaint escalation  
- Staff hierarchy: **Owner → Manager → Sales**

---

## ⭐ Features

### Supplier Web Panel
- Full product catalog management  
- Staff management (Owner only)  
- Approve requests from businesses  
- Handle and process orders  
- Manage complaints  

### Mobile App (Consumer & Sales)
- Registration & login  
- Supplier link requests  
- Product catalog & ordering  
- Real-time chat  
- Complaint creation & resolution workflow  

---

## 🔧 Technologies

### Backend
- Python 3.10+  
- FastAPI  
- PostgreSQL  
- SQLAlchemy ORM  
- JWT authentication  
- Bcrypt  

### Web (Supplier Panel)
- React 18 + TypeScript  
- Vite  
- Zustand  
- Axios  
- TailwindCSS  

### Mobile (Flutter App)
- Flutter 3  
- Dart  
- Provider  
- Material Design 3  

---

## 🏗️ Architecture

```

┌─────────────────────────────────────────────────────────────┐
│                         BACKEND API                         │
│                    FastAPI + PostgreSQL                     │
│                          :8000                              │
└────────────────┬────────────────────────┬───────────────────┘
│                        │
┌────────▼─────────┐    ┌────────▼─────────┐
│   WEB (React)    │    │  MOBILE (Flutter)│
│       :5173      │    │   Android/iOS    │
│  Owner/Manager   │    │ Consumer/Sales   │
└──────────────────┘    └──────────────────┘

````

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
git clone <repo-url>
cd project
docker-compose up -d
docker-compose exec backend python seed_data.py
````

Access:

* Web: [http://localhost:5173](http://localhost:5173)
* API: [http://localhost:8000](http://localhost:8000)
* Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Option 2: Manual Setup

#### Backend

```bash
cd server
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
python seed_data.py
```

#### Web

```bash
cd web
npm install
npm run dev
```

#### Mobile

```bash
cd mobile
flutter pub get
flutter run
```

---

## ⚡ Quick Start – 5-Min Demo

See **QUICK_START.md** for:

* Preloaded accounts
* Seed data
* Testing scenarios
* Full guided walkthrough

---

## 🧪 Testing

### Pre-Loaded Accounts

#### Supplier 1 — Fresh Products Co.

| Role    | Email                                                         | Password    |
| ------- | ------------------------------------------------------------- | ----------- |
| Owner   | [owner1@freshproducts.kz](mailto:owner1@freshproducts.kz)     | password123 |
| Manager | [manager1@freshproducts.kz](mailto:manager1@freshproducts.kz) | password123 |
| Sales   | [sales1@freshproducts.kz](mailto:sales1@freshproducts.kz)     | password123 |

#### Supplier 2 — Meat & Dairy Ltd.

| Role    | Email                                                 | Password    |
| ------- | ----------------------------------------------------- | ----------- |
| Owner   | [owner2@meatdairy.kz](mailto:owner2@meatdairy.kz)     | password123 |
| Manager | [manager2@meatdairy.kz](mailto:manager2@meatdairy.kz) | password123 |
| Sales   | [sales2@meatdairy.kz](mailto:sales2@meatdairy.kz)     | password123 |

#### Consumers

| Type       | Email                                                   | Password    |
| ---------- | ------------------------------------------------------- | ----------- |
| Restaurant | [restaurant1@example.kz](mailto:restaurant1@example.kz) | password123 |
| Hotel      | [hotel1@example.kz](mailto:hotel1@example.kz)           | password123 |
| Cafe       | [cafe1@example.kz](mailto:cafe1@example.kz)             | password123 |

---

## 🔐 Roles & Permissions

### Owner

* Full access
* Staff management
* Link, order, product, and complaint control
* Company deactivation

### Manager

* Manage products
* Process orders
* Handle escalated complaints
* View links
* Cannot manage staff

### Sales Representative

* Approve link requests
* Process orders
* Chat with consumers
* Manage complaints (with escalation)

### Consumer

* Register via mobile
* Request supplier link
* Browse catalog
* Place orders
* Chat & create complaints

---

## 📚 API Documentation

Swagger UI:

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

Includes:

* Authentication
* Products
* Orders
* Links
* Complaints
* Messages

---

## 🐳 Docker

```bash
docker-compose up -d
docker-compose down
docker-compose logs -f backend
docker-compose restart backend
docker-compose exec backend python seed_data.py
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

## 📁 Project Structure

```
project/
├── server/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── config.py
│   ├── seed_data.py
│   ├── requirements.txt
│   ├── routers/
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── links.py
│   │   ├── complaints.py
│   │   └── messages.py
│   └── utils/
│       ├── security.py
│       └── permissions.py
│
├── web/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── api.ts
│   │   ├── store.ts
│   │   └── pages/
│   ├── package.json
│   └── vite.config.ts
│
├── mobile/
│   ├── lib/
│   │   ├── main.dart
│   │   ├── models/
│   │   ├── screens/
│   │   └── services/
│   └── pubspec.yaml
│
├── docker-compose.yml
├── README.md
└── TESTING.md
```

---

## 🔧 Configuration

### Backend `.env`

```env
DATABASE_URL=postgresql://user:password@localhost:5432/supply_chain
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Web (`api.ts`)

```ts
const API_BASE_URL = 'http://localhost:8000';
```

### Mobile (`api_service.dart`)

```dart
// Android emulator
static const String baseUrl = 'http://10.0.2.2:8000';
// iOS simulator
static const String baseUrl = 'http://localhost:8000';
// Real device
static const String baseUrl = 'http://<your-ip>:8000';
```

---

## 🐛 Troubleshooting

### Backend not starting

* Check PostgreSQL
* Recreate DB
* Run seed script

### Web cannot reach API

* Check CORS
* Ensure backend is running
* Verify API URL

### Mobile issues

* Use correct emulator IP
* For real devices use local IP

### 401 Unauthorized

* Clear localStorage
* Hard refresh
* Login again

## 🔥 BACKEND FIX GUIDE

If backend breaks, follow these exact steps:

1️⃣ Ensure .env is correct
DATABASE_URL=postgresql://postgres:<your-password>@localhost:5432/<your-db>

2️⃣ Rebuild virtual environment  
py -3.11 -m venv venv  
source venv/Scripts/activate

3️⃣ Upgrade pip + essentials  
python -m pip install --upgrade pip setuptools wheel

4️⃣ Install required packages  
pip install -r requirements.txt

5️⃣ Fix bcrypt issues (Windows)

If a bcrypt version mismatch or hashing error occurs:  
pip uninstall bcrypt -y  
pip install bcrypt==4.1.2  
pip install --force-reinstall passlib

This resolves:  
- JWT hashing errors  
- Password hashing issues  
- Passlib bcrypt incompatibility

- Also try running seed_data.py in separate terminal and by creating separate venv1 and insalling req.txt:
req.txt:
annotated-types==0.7.0
anyio==4.11.0
bcrypt==4.1.2
cffi==2.0.0
click==8.3.1
colorama==0.4.6
cryptography==46.0.3
dnspython==2.8.0
ecdsa==0.19.1
email-validator==2.3.0
fastapi==0.121.3
greenlet==3.2.4
h11==0.16.0
httptools==0.7.1
idna==3.11
passlib==1.7.4
psycopg2-binary==2.9.11
pyasn1==0.6.1
pycparser==2.23
pydantic==2.12.4
pydantic-settings==2.12.0
pydantic_core==2.41.5
python-dotenv==1.2.1
python-jose==3.5.0
PyYAML==6.0.3
rsa==4.9.1
six==1.17.0
sniffio==1.3.1
SQLAlchemy==2.0.44
starlette==0.50.0
typing-inspection==0.4.2
typing_extensions==4.15.0
uvicorn==0.38.0
watchfiles==1.1.1
websockets==15.0.1

---

## 📞 Support

* GitHub Issues
* [support@example.com](mailto:support@example.com)
* Documentation (Wiki)

---


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request
<div align="center">
Made with ❤️ by TotallyTech
</div>
```

