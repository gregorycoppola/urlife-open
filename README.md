# urlife-open

**urlife-open** is an open-source Python library that implements a unified graph-relational data model for core digital structures: folders, documents, spreadsheets, and project plans.

These structures—called **functional data structures**—serve essential roles in organizing and executing user tasks. Despite their diverse appearances, they share a common underlying logic: they consist of identifiable entities (files, paragraphs, cells, tasks) connected by typed relationships (containment, sequence, dependency). `urlife-common` expresses this logic in a consistent, extensible, and queryable graph-relational format.

## What It Implements

The `urlife-common` package provides:

- **Core Node Types**: Schema definitions for nodes representing:
  - Folders and files (with containment edges)
  - Hierarchical documents (sections, paragraphs, sentences, etc.)
  - Spreadsheet cells and formulas (with cell-to-cell dependency edges)
  - Project plans (goals, options, plans, inputs, outputs)

- **Typed Edges**: Explicit relationship types such as:
  - `CHILD_OF`, `FOLLOWS`, `DEPENDS_ON`, `LINKS_TO`, etc.

- **Graph-Relational API**: A unified model for creating, traversing, and querying node-based data, using a graph-native or relational backend.

- **Validation and Serialization**: Pydantic-based schemas for type-checking, storage, and API communication.

- **Extensibility**: The system is modular, allowing you to define new node types or edge labels for your domain-specific applications.

This package forms the foundation for apps that manage personal knowledge, project planning, semantic documents, and other structured information — all within a single cohesive graph model.

## Implementation Details


### 📦 Features

- **Graph-relational data model** for:
  - Folder structures (tree or DAG)
  - Hierarchical documents (sections, paragraphs, etc.)
  - Spreadsheet-like cells with dependency graphs
  - Project plans with goals, options, plans, inputs, and outputs

- **Type-aware node schemas** using [Pydantic](https://docs.pydantic.dev)
  - Each node carries structured key-value properties based on its type
  - Similar to MongoDB's flexible schema — backed by Redis JSON for now

- **User accounts and authentication**
  - JWT-based login and registration system
  - Multi-user support and per-user data isolation

- **FastAPI web server**
  - Runs with [Uvicorn](https://www.uvicorn.org/) for async performance
  - CRUD operations on graph-based data nodes
  - Designed for real-time and interactive use

- **CLI interface** using [Click](https://click.palletsprojects.com/)
  - Command-line tools for initializing users, folders, and node data

---

### 🧱 Storage Backend

- Uses **Redis** (via `redis.asyncio` and `rejson`) as a fast, JSON-serializable, schemaless backend
- Suitable for development and prototyping
- Could be swapped for PostgreSQL, MongoDB, or a native graph DB in production

Each node is stored as a JSON document keyed by ID. The node includes:
- `type`: (e.g. `FOLDER`, `PARAGRAPH`, `GOAL`)
- `extra_properties`: key-value store based on type schema
- `parent`: optional reference to a parent node, including edge label
- `children`: optionally tracked, with labeled edges

---

### 🔐 Authentication

- JWT-based authentication flow
- `register`, `login`, and `me` endpoints
- Each request is tied to a specific user’s Redis namespace


## Usage

### 📋 Register a New User

Use the `register` command to create a new user account by providing an email, password, and display name.

```bash
venv/bin/urlife register --email user@example.com --password mysecurepassword123 --name "Test User"
```

```
🔍 Registering new user...
📌 Server: http://localhost:8000
📌 Email: user@example.com
📌 Name: Test User

✅ Registration successful!
User ID: _sbhV-O9jr1vz_jDRd6qew
```

### 🔐 Log In as an Existing User

Use the `login` command to authenticate an existing user and retrieve a JWT access token. The token will be saved locally for use in subsequent authenticated requests.

```bash
venv/bin/urlife login --email user@example.com --password mysecurepassword123
```

```
✅ Login successful!
Access Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiX3NiaFYtTzlqcjF2el9qRFJkNnFldyIsImV4cCI6MTc1MjYyNzA1MH0.LDHpzI79jkrICILMC0ocsHmJW54LuaWNf6AYAeZiCpg
🔐 Token saved to /Users/greg/.urlife/token
```

### 👤 Check Current Authenticated User

Use the `whoami` command to display the identity of the currently authenticated user (based on the saved JWT token).

```bash
venv/bin/urlife whoami
```

```
👤 User ID: _sbhV-O9jr1vz_jDRd6qew
📧 Email: user@example.com
📛 Name: Test User
✅ Active: True
```

### Get Root Folder ID

Retrieve the ID of the root folder for the currently logged-in user.

```
venv % urlife get-root-folder-id
Getting root folder ID...
Root folder ID: "User"
```

### List Direct Children of a Folder

List the immediate contents of a folder by specifying its ID or name (e.g., `"User"` for the root folder). Displays each child's ID, name, and type.

```
venv % urlife list-folder-direct User
📁 Listing contents of folder: User

📦 Folder contents:
----------------------------------------------------------------------
🆔 e610ccba-8da4-42fa-879a-48e48e755141 | 📌 Inbox   | 📂 
🆔 7a36e3ee-660b-4fae-9a8f-df0a5e7b3fe6 | 📌 People  | 📂 
🆔 db1bf582-36c2-40c9-8191-3e472fa4a333 | 📌 Journal | 📂 
🆔 db96df08-0ce2-4389-83de-b73f9fbaf241 | 📌 Projects| 📂 
```

### List All Descendants of a Folder (Recursive)

Recursively list all folders contained within the specified folder and its subfolders. This is useful for getting a complete view of your folder hierarchy.

```
venv % urlife list-folder-recursive User
📂 Recursively listing contents of folder: User

📦 Recursive folder contents:
----------------------------------------------------------------------
🆔 8d5c3670-0446-4971-87f1-6f5c7c2ca69d | 📌 Home     | 📂 
🆔 abdfdd8e-a577-4502-9889-d2862155bd35 | 📌 Life     | 📂 
🆔 ae5a0255-27c0-477d-b87e-277ff3dbb1fd | 📌 Product  | 📂 
🆔 155c24b3-0a48-42b7-b588-420132ec5396 | 📌 Body     | 📂 
🆔 bd3c7432-498c-4991-9d9c-066067011854 | 📌 Money    | 📂 
🆔 db1bf582-36c2-40c9-8191-3e472fa4a333 | 📌 Journal  | 📂 
🆔 db96df08-0ce2-4389-83de-b73f9fbaf241 | 📌 Projects | 📂 
🆔 e610ccba-8da4-42fa-879a-48e48e755141 | 📌 Inbox    | 📂 
🆔 f25338aa-bca6-4ba0-8bde-9e227574b41b | 📌 Business | 📂 
🆔 7a36e3ee-660b-4fae-9a8f-df0a5e7b3fe6 | 📌 People   | 📂 
🆔 1f861d7e-4aee-4260-8e7e-05cddead5fdb | 📌 Social   | 📂 
```

### Create a Node in a Folder

Create a new node of a specified type and caption inside a given folder. This is useful for adding tasks, documents, goals, or other functional entities to your personal hierarchy.

```
venv % urlife create-node-in-folder --folder-id 8d5c3670-0446-4971-87f1-6f5c7c2ca69d --type GOAL --caption "Get Some Coffee"
✅ Node created: 55068763381ae4fd5a05a78b414d0cd7
```

### Read Node Details

Retrieve the full details of a specific node by its ID. This includes metadata like type, caption, status, flags, parent relationship, and creation time.

```
venv % urlife read-node 55068763381ae4fd5a05a78b414d0cd7
✅ Node Details
───────────────
ID:            55068763381ae4fd5a05a78b414d0cd7
Type:          GOAL
Caption:       Get Some Coffee
Status:        open
Priority:      low
Attention:     0
Flags:
  - Urgent         : False
  - Critical       : False
  - Needs Decision : False
  - Active         : False
Parent:        8d5c3670-0446-4971-87f1-6f5c7c2ca69d (edge: CHILD_OF)
Created At:    2025-07-16 00:37:34 UTC
```

### Update Node Checkbox

Update the value of a specific checkbox field for a given node. Useful for toggling flags like "Urgent", "Active", or "Needs Decision".

```
venv % urlife update-node-checkbox 55068763381ae4fd5a05a78b414d0cd7 Urgent true
✅ Checkbox 'Urgent' updated to True for node 55068763381ae4fd5a05a78b414d0cd7
```

### Search Nodes

Search for nodes of a given type under a specified root folder, using a fuzzy match against the node captions.

```
venv % urlife search-nodes --root-id User --object-type GOAL --query "Coffee"
Top 1 matches:
- [100] 55068763381ae4fd5a05a78b414d0cd7 | Get Some Coffee | GOAL | Created: 2025-07-16T00:37:34Z
```
