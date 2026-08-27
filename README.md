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

A real, unedited request straight from my terminal — headers and all, exactly as it printed:

GET /tasks/1

Response:

{
  "id": 1,
  "title": "Buy milk",
  "done": false
}

The server returned:

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
  "title": "Learn FastAPI"
}
```

`done` isn't part of the request — my API always sets a new task's `done` to `false` on creation. You mark it complete afterward with a `PUT` request.

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

I tested this deliberately: I created a task, stopped the server with Ctrl+C, and started it again with the same command. The new task was gone, and `GET /tasks` returned only the original 3 starter tasks. That happens because the whole task list lives in RAM, not on disk — nothing was writing it anywhere permanent, so the fresh server process had nothing to read back.

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

##  Why I Built This

I'm using projects like this to move beyond just knowing what technologies are called and actually understand how they work by building with them.

This API is small, but the important part for me was building the whole thing myself, testing it, breaking things, fixing them and understanding why each part exists.

That's the approach I'm taking with my development work going forward:

> **Build it. Test it. Break it. Understand it. Improve it.**

---

## 🗄️ Update: Now Backed by a Real Database (Assignment 2)

The version above (`app.py`) stores tasks in a Python list — which means every
restart wipes the data clean. This next version, `app_v2.py`, replaces that
list with an actual SQLite database, so tasks now survive a restart. The API
itself didn't change at all — same endpoints, same request bodies, same
responses. Only what's underneath it changed.

### Why SQLite

I picked SQLite because it needs zero setup — no server to install, no
service to run in the background, nothing to configure. The whole database
is just one file sitting in my project folder. That made it the right tool
for this stage: I wanted to learn how an API talks to a real database
without also having to learn how to install and manage a full database
server at the same time. SQLite is also built directly into Python through
the `sqlite3` module, so I didn't even need to `pip install` anything extra
to use it.

### Where the database file lives

The database is a single file called `tasks.db`, created automatically the
first time `app_v2.py` runs, sitting right next to the code in the project
folder:

```text
task-api/
│
├── app.py                     ← Assignment 1: in-memory version
├── app_v2.py                  ← Assignment 2: SQLite-backed version
├── tasks.db                   ← created automatically on first run
├── README.md
├── swagger-screenshot.png
└── db-browser-screenshot.png
```

I'm not committing `tasks.db` itself to GitHub — it's runtime data, not
source code, and anyone who clones this repo gets a fresh, empty version
created automatically the first time they run the app.

### How to start the project

```bash
git clone https://github.com/MianoCloudSec/flyrank-internship.git
cd flyrank-internship
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install fastapi uvicorn
uvicorn app_v2:app --reload --port 8001
```

The first time this runs, `tasks.db` gets created automatically, the
`tasks` table gets created if it doesn't exist yet, and 3 example tasks get
inserted — but only that first time. Restart it as many times as you want
after that, and those 3 example tasks won't duplicate, because the app
checks if the table is empty before inserting anything.

The API is now available at `http://localhost:8001`, and the same
interactive docs are at `http://localhost:8001/docs`.

### Seeing the database directly

I used **DB Browser for SQLite** to open `tasks.db` and look at the raw
data, completely separately from my API code:

![DB Browser screenshot](db-browser-screenshot.png)

> ⚠️ **Gotcha I ran into:** DB Browser doesn't save your changes to the
> actual `.db` file the moment you run a query. It keeps them pending
> until you click the **"Write Changes"** button. I ran an `UPDATE` and a
> `DELETE`, checked my API right after, and the old data was still
> showing — which confused me for a bit. The fix was clicking
> **"Write Changes"** in DB Browser. The moment I did, my API immediately
> reflected the change, no restart needed.
>
> This is the exact same idea as `connection.commit()` in my Python code
> — nothing is actually saved to disk until you explicitly say so. DB
> Browser just has a button for it instead of a line of code. It's a
> good reminder that "I ran the query" and "I saved the change" aren't
> the same thing, in SQL or in code.

The interesting part of this stage was realizing that DB Browser and my API
are both just looking at the exact same file. Anything I change in one, the
other one sees too — but only after it's actually been committed to disk.

### One real SQL query I ran

```sql
DELETE FROM tasks WHERE done = 1;
```

This deletes every task where `done` equals 1 (true). I ran this manually
inside DB Browser, clicked "Write Changes," and then checked `GET /tasks`
in my terminal right afterward — the deleted tasks were already gone from
the API's response, with no code change and no server restart needed.
That's what proved to me that the API and the database aren't two separate
sources of truth — they're the same file, viewed two different ways.

### What changed vs. what didn't

| | Assignment 1 (`app.py`) | Assignment 2 (`app_v2.py`) |
|---|---|---|
| Storage | Python list in RAM | SQLite file (`tasks.db`) |
| Survives restart? | ❌ No | ✅ Yes |
| Endpoints | Same | Same |
| Request/response shape | Same | Same |
| How I find a task | `next()` search through a list | `SELECT ... WHERE id = ?` |
| How I add a task | `.append()` to a list | `INSERT INTO tasks ...` |
| How the id is generated | `max(ids) + 1` in Python | Auto-generated by SQLite (`INTEGER PRIMARY KEY`) |