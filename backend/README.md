# 📋 Task Manager – FastAPI + JWT + SQLite

A full-stack Task Manager web application built for the **Weboin Technologies** Python Developer Intern assessment.

🌐 **Live Demo**: https://task-manager-gpbu.onrender.com  
📖 **API Docs**: https://task-manager-gpbu.onrender.com/docs  
🐙 **GitHub**: https://github.com/Kadershahib/task-manager

---

## 📌 Project Overview

A simple Task Manager where users can register, login, and manage their personal tasks. Built with FastAPI backend, JWT authentication, SQLite database, and a plain HTML/CSS/JS frontend.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Database | SQLite + SQLAlchemy ORM |
| Validation | Pydantic |
| Testing | pytest, httpx |
| Frontend | HTML + CSS + JavaScript |
| Deployment | Render |

---

## 📁 Project Structure

```
task-manager/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── core/
│   │   └── security.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   └── models.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── schemas/
│   │   └── schemas.py
│   └── tests/
│       └── test_api.py
├── frontend/
│   └── index.html
└── README.md
```

---

## ⚙️ How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/Kadershahib/task-manager.git
cd task-manager
```

### 2. Create virtual environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
copy .env.example .env
```

### 5. Run the server
```bash
python -m uvicorn main:app --reload
```

Open **http://localhost:8000** in your browser.  
API docs at **http://localhost:8000/docs**

---

## 🔐 Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | JWT signing secret | `changeme-super-secret-key` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry in minutes | `30` |
| `DATABASE_URL` | SQLAlchemy DB URL | `sqlite:///./taskmanager.db` |

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register new user |
| POST | `/login` | Login and get JWT token |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks (paginated + filterable) |
| GET | `/tasks/{id}` | Get single task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

---

## 🚀 Deployment

Deployed on **Render.com**

- **Live URL**: https://task-manager-gpbu.onrender.com
- **API Docs**: https://task-manager-gpbu.onrender.com/docs

---

*Built for Weboin Technologies Python Developer Intern Assessment*
