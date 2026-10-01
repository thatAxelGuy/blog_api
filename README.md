# Masterblog API

A simple blog application built with **Flask**, **JavaScript**, and **JSON**.

The project consists of a Flask REST API backend and a JavaScript frontend that allows users to view, create, update, and delete blog posts.

## Features

* View all blog posts
* Create new blog posts
* Update existing blog posts
* Delete blog posts
* Search posts
* Sort posts by title, content, author, or date
* Pagination with page and limit parameters
* Swagger API documentation
* Persistent storage using a JSON file
* Frontend connected to the Flask API using JavaScript Fetch
* CORS support for communication between frontend and backend

## Project Structure

```text
masterblog/
├── app.py
├── posts.json
├── requirements.txt
├── static/
│   ├── blog.json
│   ├── main.js
│   └── styles.css
└── templates/
    └── index.html
```

## Requirements

* Python 3
* Flask
* Flask-CORS

## Installation

Clone the repository and move into the project directory.

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Using uv

If you use `uv`, you can install the dependencies with:

```bash
uv pip install -r requirements.txt
```

## Running the Backend

Start the Flask API:

```bash
python app.py
```

The API will run on:

```text
http://127.0.0.1:5002
```

## Running the Frontend

The frontend runs separately from the Flask API.

Start the frontend server on port 5001 and open:

```text
http://127.0.0.1:5001
```

The frontend uses the API base URL:

```text
http://127.0.0.1:5002/api
```

## Swagger Documentation

Interactive API documentation is available at:

```text
http://127.0.0.1:5002/api/docs
```

The Swagger documentation describes the available API endpoints and allows them to be tested directly from the browser.

## API Endpoints

### Get Posts

```http
GET /api/posts
```

Supports pagination:

```http
GET /api/posts?page=1&limit=5
```

Supports sorting:

```http
GET /api/posts?sort=date&direction=desc
```

### Create a Post

```http
POST /api/posts
```

Example request:

```json
{
    "title": "My New Post",
    "content": "This is my new blog post.",
    "author": "Axel",
    "date": "2026-10-01"
}
```

### Update a Post

```http
PUT /api/posts/{id}
```

### Delete a Post

```http
DELETE /api/posts/{id}
```

### Search Posts

```http
GET /api/posts/search?search=Flask
```

Pagination can also be used with search:

```http
GET /api/posts/search?search=Flask&page=1&limit=5
```

## Data Storage

Blog posts are stored in `posts.json`.

Each post contains:

```json
{
    "id": 1,
    "title": "My First Flask API",
    "content": "Today I built my first API using Flask.",
    "author": "Axel",
    "date": "2026-01-01"
}
```

## Frontend

The frontend is built with HTML, CSS, and vanilla JavaScript.

JavaScript uses the browser's `fetch()` function to communicate with the Flask API.

The frontend supports:

* Loading posts
* Creating posts
* Deleting posts
* Pagination
* Displaying authors and dates
* Remembering the API base URL using browser local storage

## Learning Goals

This project was built to practice:

* Building REST APIs with Flask
* Working with HTTP methods
* Handling JSON data
* Using query parameters
* Pagination
* CRUD operations
* Connecting JavaScript to a Python backend
* Using Fetch API
* Working with Swagger/OpenAPI
* Managing project dependencies

## License

This project is licensed under the MIT License.

See the LICENSE file for the full license text.
