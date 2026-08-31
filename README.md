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

```text
PS C:\Users\Nkanyiso\Desktop\task-api> curl.exe -i http://localhost:8000/tasks/1
date: Thu, 20 Aug 2026 10:06:04 GMT
server: uvicorn
content-length: 40
content-type: application/json
{"id":1,"title":"Buy milk","done":false}
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

---

## 🐳 Update: Now Running on Postgres in Docker (Assignment 3)

This version takes the architecture further. Instead of talking to SQLite
directly from inside my route functions, I split the code into three
layers — routes, a service, and a repository — and then proved the whole
point of doing that: swapping SQLite for a real Postgres database, running
in Docker, changed exactly one file.

### Why I restructured into layers first

Before touching Postgres, I rebuilt the API as `app_v3/`, splitting it into:

- **`main.py`** — the FastAPI routes. Their only job is handling the HTTP
  request/response and picking the right status code.
- **`service.py`** — validation and business rules (empty title checks,
  deciding what a 404 vs 400 should look like).
- **`repositories/`** — the only layer allowed to know how data is actually
  stored. `base.py` defines the contract every repository must follow;
  `memory_repository.py` and `postgres_repository.py` are two different
  implementations of that same contract.

The rule I was proving: the routes and the service are never allowed to
know what kind of storage is underneath them. They only know they can ask
a repository to get/create/update/delete a task.

### The actual proof

When I swapped from the in-memory repository to the Postgres one, this is
the entire diff in `main.py`:

```diff
- from app_v3.repositories.memory_repository import InMemoryTaskRepository
+ from app_v3.repositories.postgres_repository import PostgresTaskRepository

- repository = InMemoryTaskRepository()
+ repository = PostgresTaskRepository()
```

Nothing in `service.py` changed. Nothing in the routes changed. Nothing in
`models.py` changed. One import, one line — and the entire API started
reading and writing real Postgres instead of a Python list.

### Why Docker

Docker lets me run a full Postgres server without installing Postgres
directly on my machine, managing a service, or worrying about version
conflicts. The whole database — server, config, everything — lives inside
one container, defined by one file (`docker-compose.yml`), and anyone who
clones this repo can bring the exact same database up with one command.

### How to run it

```bash
git clone https://github.com/MianoCloudSec/flyrank-internship.git
cd flyrank-internship
cp .env.example .env
docker compose up -d
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install fastapi uvicorn psycopg2-binary python-dotenv
uvicorn app_v3.main:app --reload --port 8002
```

The first time `docker compose up` runs, Postgres starts fresh, and my
`app_v3/db/init.sql` script runs automatically — creating the `tasks` table
and inserting 3 seed tasks, but only that first time.

### The `.env` file

Real credentials live in `.env`, which is gitignored and never pushed to
GitHub. A `.env.example` file with the same variable names (but safe
placeholder values) is committed instead, so anyone cloning this repo knows
exactly what to fill in.

### A real problem I hit — and how I diagnosed it

My first attempt at connecting my FastAPI app to Postgres failed with:
psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed:
FATAL: password authentication failed for user "taskuser"

The confusing part: I could connect fine using `psql` directly inside the
container, so I assumed my password was correct. Turns out that had
nothing to do with it — that connection was going through a "trust"
authentication path that skips password checking entirely, so it never
actually proved my password worked over the network.

The real cause: I already had a **separate, native Postgres installed
directly on Windows**, running as a background service, sitting on port
5432 — completely unrelated to Docker. My Python app was connecting to
*that* one instead of my container, and that native install had never
heard of a user called `taskuser`.

I confirmed this with:

```powershell
netstat -ano | findstr :5432
tasklist /FI "PID eq <the PID that showed up>"
```

which showed two separate processes both listening on port 5432 — one was
`postgres.exe` (the native Windows service), the other was Docker's own
backend process.

**The fix**: instead of touching the native install, I remapped Docker's
Postgres to a different port on my host machine — `5433` instead of
`5432` — in both `docker-compose.yml` and `.env`. Postgres inside the
container is still running normally on its usual port 5432; only the
*outside-facing* port changed.

### Proving persistence — across an app restart AND a container restart

The assignment specifically wanted persistence proven across both restarts,
not just one. I did this:

1. Created a task, updated another, deleted a third — through the running API.
2. Stopped my FastAPI server (`Ctrl+C`).
3. Restarted the actual Postgres container: `docker compose restart`.
4. Started my FastAPI server again.
5. Called `GET /tasks`.

Every change was still there — the created task, the update, and the
deletion all held, with no data reverting. That's the real difference
between this version and Assignment 1: restarting isn't just "the app
comes back up," it's "the app comes back up and nothing was lost, even
when the database container itself restarted too."

### What changed vs. what didn't (all three versions)

| | `app.py` (A1) | `app_v2.py` (A2) | `app_v3/` (A3) |
|---|---|---|---|
| Storage | Python list in RAM | SQLite file | Postgres in Docker |
| Survives app restart? | ❌ | ✅ | ✅ |
| Survives container restart? | N/A | N/A | ✅ |
| Code structure | One flat file | One flat file | Routes / service / repository |
| Swapping storage requires | — | Rewriting the whole file | Changing 2 lines in `main.py` |

---

## 🔐 Update: Secure Auth with Supabase (Assignment 4)

Every previous version of this API was wide open — anyone who knew the URL
could read, create, update, or delete data. This version adds real
authentication: user accounts, login sessions, and routes that only work
if you can prove who you are.

### The trust triangle

This assignment introduced a pattern I hadn't built before — three parties
involved in every authenticated request instead of just two:

1. **Client → Supabase**: the client sends an email/password directly to
   Supabase, which is my Identity Provider (IdP).
2. **Supabase → Client**: if the credentials are valid, Supabase hands back
   a JWT (JSON Web Token) — a signed, verifiable "pass."
3. **Client → My server**: the client attaches that JWT to future requests,
   inside an `Authorization: Bearer <token>` header.
4. **My server → Supabase**: when a protected route is hit, my server asks
   Supabase to verify the token is real, unexpired, and untampered.

My server never sees or stores a single password. That job belongs
entirely to Supabase — password hashing, breach protection, and session
security are all handled by a dedicated identity provider instead of code
I wrote myself.

### Why I didn't build this myself

Rolling your own authentication means correctly implementing password
hashing, defending against credential-stuffing and brute-force attacks,
and taking on real legal/reputational risk if it's ever done wrong. A
service like Supabase has already solved that problem correctly, at scale
— so instead of reinventing it, my server's only job is verifying a token
Supabase already vouches for.

### Architecture

Built in `app_v4/`, following the same layered instinct as the Postgres
assignment:

- **`client.py`** — creates and exports a single shared Supabase client,
  built from `SUPABASE_URL` and `SUPABASE_KEY` in `.env`.
- **`models.py`** — the `AuthCredentials` shape (email + password) used by
  signup and login.
- **`dependencies.py`** — `get_current_user`, a reusable FastAPI
  dependency. It extracts and verifies the bearer token, and is the
  *only* place token-checking logic exists in the whole project.
- **`main.py`** — the actual routes. Protected routes don't contain any
  verification logic themselves — they just declare
  `Depends(get_current_user)` and trust it to guard the door.

### Endpoints

| Method | Path                  | Requires Auth? | Description                          |
|--------|-----------------------|:--------------:|---------------------------------------|
| POST   | `/auth/signup`        | ❌              | Create a new user account             |
| POST   | `/auth/login`         | ❌              | Authenticate and receive a JWT        |
| POST   | `/auth/logout`        | ✅              | End the current session               |
| GET    | `/public/info`        | ❌              | Public, unauthenticated data          |
| GET    | `/protected/profile`  | ✅              | Read the logged-in user's own profile |

### How to run it

```bash
git clone https://github.com/MianoCloudSec/flyrank-internship.git
cd flyrank-internship
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install fastapi uvicorn supabase python-dotenv
```

Then add your own Supabase project's values to `.env` (see
`.env.example` for the required keys):
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key


Start the server:

```bash
uvicorn app_v4.main:app --reload --port 8003
```

Docs and the Authorize button live at `http://localhost:8003/docs`.

### Testing the full flow

```bash
# 1. Sign up
curl -i -X POST http://localhost:8003/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"yourpassword"}'

# 2. Log in, copy the access_token from the response
curl -i -X POST http://localhost:8003/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"yourpassword"}'

# 3. Use the token to access a protected route
curl -i http://localhost:8003/protected/profile \
  -H "Authorization: Bearer PASTE_YOUR_TOKEN_HERE"
```

Changing even one character of the token causes the last request to
correctly return `401 Invalid or expired token`.

### A real bug I hit: Supabase's free-tier email rate limit

Testing signup repeatedly (as I iterated on the code) burned through
Supabase's default email-sending quota fast, and I started getting
`"email rate limit exceeded"` errors that had nothing to do with my code.

**The fix**: I configured a custom SMTP provider (Resend, free tier) under
Supabase's Auth SMTP settings, using Resend's built-in test sender
(`onboarding@resend.dev`). That removes Supabase's default cap entirely.
One limitation worth knowing: that shared test sender only delivers to the
email address the Resend account itself was created with — fine for a
one-account practice project like this, not something you'd use in
production.

### Swagger UI with Bearer Auth

Configuring `HTTPBearer` as a FastAPI security scheme makes `/docs` show a
padlock next to every protected route, plus a green "Authorize" button
that lets you paste a token once and test every protected endpoint
directly from the browser — no curl needed.

![Swagger UI showing protected routes with lock icons](swagger4.png)

![Swagger UI after authorizing and testing a protected route](swagger2.png)

### What changed vs. every version before it

| | Assignments 1–3 | Assignment 4 |
|---|---|---|
| Who can access the API | Anyone with the URL | Only users who can prove their identity |
| Passwords | N/A | Never touched by my code — handled entirely by Supabase |
| Protecting a route | No concept of this | `Depends(get_current_user)` |
| Adding auth to a new route | N/A | One line: add the same dependency |
| Swagger UI | Open, no auth | Padlock icons + Authorize button for protected routes |