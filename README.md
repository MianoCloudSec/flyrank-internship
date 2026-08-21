# Task API

A small REST API I built as part of my W2 backend assignment.

The project is a simple task-management API that implements the four basic CRUD operations:

**Create → Read → Update → Delete**

I built it from scratch with FastAPI and tested each stage with `curl`, PowerShell and Swagger UI. There is intentionally no database at this stage. Tasks are stored in memory using a Python list, so restarting the server resets the data.

This project is part of my process of moving from learning backend concepts to actually building and testing them myself.

---

## 🛠️ Tech Stack

* **Python 3**
* **FastAPI** — API framework
* **Uvicorn** — ASGI server
* **Pydantic** — request/input validation
* **Swagger UI / OpenAPI** — automatically generated API documentation
* **Git & GitHub** — version control

---

## 🚀 What I Built

### API Endpoints

| Method   | Endpoint      | Description                       |
| -------- | ------------- | --------------------------------- |
| `GET`    | `/`           | Returns information about the API |
| `GET`    | `/health`     | Health check for the server       |
| `GET`    | `/tasks`      | Returns all tasks                 |
| `GET`    | `/tasks/{id}` | Returns a specific task           |
| `POST`   | `/tasks`      | Creates a new task                |
| `PUT`    | `/tasks/{id}` | Updates an existing task          |
| `DELETE` | `/tasks/{id}` | Deletes a task                    |

---

## 📋 Features

* REST API architecture
* Full CRUD functionality
* Automatic request validation
* HTTP status codes for successful and failed operations
* 404 handling for tasks that don't exist
* Health-check endpoint
* Interactive Swagger documentation
* In-memory data storage
* Tested endpoints using real HTTP requests

---

## 📁 Project Structure

```text
task-api/
│
├── app.py
├── README.md
└── swagger-screenshot.png
```

The main application is currently contained in `app.py`. I'm intentionally keeping the project simple at this stage before introducing a database and a larger application structure.

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/MianoCloudSec/flyrank-internship.git
```

### 2. Move into the project

```bash
cd flyrank-internship
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install fastapi uvicorn
```

### 6. Start the server

```bash
uvicorn app:app --reload --port 8000
```

The API will now be available at:

```text
http://localhost:8000
```

---

## 📖 Interactive API Documentation

FastAPI automatically generates interactive API documentation.

Once the server is running, open:

```text
http://localhost:8000/docs
```

From Swagger UI I can test the API directly from the browser using the **Try it out** functionality.

![Swagger UI](swagger-screenshot.png)

I used Swagger to test the complete CRUD cycle:

```text
Create → Read → Update → Delete
```

---

## 🧪 Example Request

A real request I made against the running API:

```text
GET /tasks/1
```

Response:

```json
{
  "id": 1,
  "title": "Buy milk",
  "done": false
}
```

The server returned:

```text
HTTP/1.1 200 OK
```

---

## 🔄 CRUD Example

### Create a task

```http
POST /tasks
```

Example JSON:

```json
{
  "title": "Learn FastAPI",
  "done": false
}
```

### Read tasks

```http
GET /tasks
```

### Update a task

```http
PUT /tasks/1
```

Example:

```json
{
  "title": "Learn FastAPI properly",
  "done": true
}
```

### Delete a task

```http
DELETE /tasks/1
```

---

## 💾 Why There Is No Database

This version intentionally uses an in-memory Python list instead of a database.

That means the data only exists while the application is running.

For example:

```text
Start server
     ↓
Create task
     ↓
Task exists in memory
     ↓
Stop server
     ↓
Memory is cleared
     ↓
Start server again
     ↓
Task is gone
```

I tested this deliberately by creating a task, stopping the server and starting it again. The task disappeared and the API returned to the original three starter tasks.

This isn't a bug in this stage of the project. It's demonstrating why persistence is necessary.

---

## 🧠 What I Learned

The biggest thing I took from this project was understanding the pattern behind backend endpoints.

Most of the operations follow a similar flow:

```text
Receive request
      ↓
Validate input
      ↓
Find the resource
      ↓
Check whether it exists
      ↓
Perform the operation
      ↓
Return the appropriate response
```

Once I understood that pattern in `GET /tasks/{id}`, I started seeing the same structure appear in `PUT` and `DELETE`.

Building it myself made CRUD make a lot more sense than simply reading about it.

I also got more comfortable with:

* HTTP methods
* HTTP status codes
* REST API structure
* Request validation
* Path parameters
* JSON requests and responses
* API documentation
* Testing APIs from the command line
* Understanding the difference between memory and persistent storage

---

## 🔬 Testing Approach

I didn't build the entire API and test it at the end.

I built it incrementally.

After adding each major piece, I tested it before moving forward using:

* `curl`
* PowerShell
* Swagger UI

This helped me catch problems early instead of building more functionality on top of broken code.

---

## 🔮 What's Next?

The next stage is introducing **real persistence**.

The plan is to move from:

```text
Python List
     ↓
Temporary in-memory storage
```

to:

```text
FastAPI
     ↓
Database
     ↓
Persistent data
```

From there, I can start looking at things like:

* SQLite/PostgreSQL
* Database models
* SQLAlchemy
* Authentication
* Better project structure
* Automated testing
* Docker
* API deployment

The goal isn't to jump straight into all of that. I want to understand each layer properly and build on what I've already done.

---

## 📌 Project Status

**Current stage:** W2 — Backend API / CRUD

**Status:** ✅ Completed

**Next:** Database persistence

---

## 👨🏽‍💻 Why I Built This

I'm using projects like this to move beyond just knowing what technologies are called and actually understand how they work by building with them.

This API is small, but the important part for me was building the whole thing myself, testing it, breaking things, fixing them and understanding why each part exists.

That's the approach I'm taking with my development work going forward:

> **Build it. Test it. Break it. Understand it. Improve it.**
