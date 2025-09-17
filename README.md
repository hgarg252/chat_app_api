# 💬 Chat App API

A backend service for a real-time chat application built with **FastAPI**, **WebSockets**, **JWT Authentication**, and **SQLAlchemy**.  
This API enables user authentication, message persistence, and live chat communication through WebSocket connections.  

---

## 🚀 Features

- User registration & authentication with JWT  
- Real-time messaging via WebSockets  
- Message persistence using a relational database  
- REST endpoints for users and messages  
- Secure connection handling with token-based authentication  
- Interactive API docs (Swagger & ReDoc)  

---

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – API framework  
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM  
- [PostgreSQL](https://www.postgresql.org/) (or SQLite for dev) – Database  
- [JWT (python-jose)](https://python-jose.readthedocs.io/) – Authentication  
- [Uvicorn](https://www.uvicorn.org/) – ASGI server  

---

## 📂 Project Structure

chat_app_api/

│── auth.py # JWT authentication logic

│── database.py # Database models & session

│── main.py # App entry point

│── models.py # SQLAlchemy models

│── routers/
  │ ├── users.py # User endpoints

  │ ├── messages.py # Message endpoints

  │ └── websockets.py # WebSocket handlers

│── schemas.py # Pydantic models

│── requirements.txt # Dependencies

│── README.md # Project documentation

yaml
Copy code

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/chat_app_api.git
cd chat_app_api
2. Create & activate a virtual environment
bash
Copy code
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
🔑 Environment Variables
Create a .env file in the project root:

ini
Copy code
DATABASE_URL=postgresql://user:password@localhost/chatdb
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
🗄️ Database Setup
PostgreSQL
bash
Copy code
createdb chatdb
SQLite (for development)
ini
Copy code
DATABASE_URL=sqlite:///./chat.db
▶️ Running the Server
bash
Copy code
uvicorn main:app --reload
API Docs available at:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

🔐 Authentication
Register a new user → /auth/register

Get a JWT token → /auth/token

Use Authorization: Bearer <token> in request headers

💬 WebSockets Usage
Connection URL

ruby
Copy code
ws://127.0.0.1:8000/websockets/chat/{room_id}
Headers

json
Copy code
{
  "Authorization": "Bearer <your-jwt-token>"
}
Example (JavaScript)

javascript
Copy code
const socket = new WebSocket("ws://127.0.0.1:8000/websockets/chat/1");

socket.onopen = () => {
  console.log("Connected");
  socket.send(JSON.stringify({ message: "Hello World!" }));
};

socket.onmessage = (event) => {
  console.log("New message:", event.data);
};
📮 Example REST Requests
Register
http
Copy code
POST /auth/register
Content-Type: application/json

{
  "username": "alice",
  "email": "alice@example.com",
  "password": "1234"
}
Login
http
Copy code
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=alice@example.com&password=1234
Response

json
Copy code
{
  "access_token": "your.jwt.token",
  "token_type": "bearer"
}
🧪 Testing
Run tests with:

bash
Copy code
pytest
📦 Deployment
For production:

bash
Copy code
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Can be deployed on:

Docker

Heroku

Railway / Render

AWS / GCP / Azure

📜 License
This project is licensed under the MIT License.
