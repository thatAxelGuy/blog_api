import json
import os
from datetime import date

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL = "/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL = "/static/blog.json"  # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Axel-Blog API"},  # (3) You can change this if you like
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(BASE_DIR, "posts.json")


def load_posts() -> list[dict]:
    try:
        with open(POSTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_posts(posts) -> bool:
    try:
        with open(POSTS_FILE, "w", encoding="utf-8") as file:
            json.dump(posts, file, indent=2, ensure_ascii=False)
    except OSError:
        return False

    return True


def _paginate(posts: list[dict], page: int, limit: int) -> list[dict]:
    start = (page - 1) * limit
    end = start + limit
    return posts[start:end]


@app.route("/api/posts", methods=["GET"])
def get_posts():
    sort_by = request.args.get("sort")
    direction = request.args.get("direction")
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=5, type=int)

    if page < 1 or limit < 1:
        return jsonify({"error": "Invalid page number or limit"}), 400

    posts = load_posts()

    if sort_by is None and direction is None:
        return jsonify(_paginate(posts, page, limit)), 200

    if sort_by is None or direction is None:
        return jsonify({"error": "Both sort and direction values required"}), 400

    if sort_by not in ["title", "content", "author", "date"]:
        return (
            jsonify({"error": "Sort can be 'title', 'content', 'author', or 'date'"}),
            400,
        )

    if direction not in ["asc", "desc"]:
        return jsonify({"error": "Direction can only be 'asc' or 'desc'"}), 400

    if sort_by and direction:
        posts = sorted(
            posts,
            key=lambda post: (
                date.fromisoformat(post[sort_by])
                if sort_by == "date"
                else post[sort_by]
            ),
            reverse=direction == "desc",
        )

    return jsonify(_paginate(posts, page, limit)), 200


@app.route("/api/posts", methods=["POST"])
def add_post():
    posts = load_posts()
    new_id = max((post["id"] for post in posts), default=0) + 1

    response = request.json

    if (
        not response
        or not response.get("title", "").strip()
        or not response.get("content", "").strip()
        or not response.get("author", "").strip()
        or not response.get("date", "").strip()
    ):
        return jsonify({"error": "Title, content, author and date are required"}), 400

    new_post = {
        "id": new_id,
        "title": response.get("title").strip(),
        "content": response.get("content").strip(),
        "author": response.get("author").strip(),
        "date": response.get("date").strip(),
    }

    posts.append(new_post)

    if not save_posts(posts):
        return jsonify({"error": "Failed to save posts"}), 500

    return jsonify(new_post), 201


@app.route("/api/posts/<int:id>", methods=["DELETE"])
def remove_post(id):
    posts = load_posts()
    for post in posts:
        if post["id"] == id:
            posts.remove(post)

            if not save_posts(posts):
                return jsonify({"error": "Failed to save posts"}), 500

            return (
                jsonify(
                    {"message": f"Post with id {id} has been deleted successfully."}
                ),
                200,
            )

    return jsonify({"error": f"Post with id {id} doesn't exist."}), 404


@app.route("/api/posts/<int:id>", methods=["PUT"])
def update_post(id):
    posts = load_posts()
    post_to_update = None

    for post in posts:
        if post["id"] == id:
            post_to_update = post
            break

    if post_to_update is None:
        return jsonify({"error": f"Post with id {id} doesn't exist."}), 404

    response = request.json

    if "title" in response:
        post_to_update["title"] = response.get("title")

    if "content" in response:
        post_to_update["content"] = response.get("content")

    if "author" in response:
        post_to_update["author"] = response.get("author")

    if "date" in response:
        post_to_update["date"] = response.get("date")

    if not save_posts(posts):
        return jsonify({"error": "Failed to save posts"}), 500

    return jsonify(post_to_update), 200


@app.route("/api/posts/search", methods=["GET"])
def search_posts():
    posts = load_posts()
    search_query = request.args.get("search")
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=5, type=int)

    if page < 1 or limit < 1:
        return jsonify({"error": "Invalid page number or limit"}), 400

    if search_query is None or not search_query.strip():
        return jsonify({"error": "Search query is required"}), 400

    matches = [
        post
        for post in posts
        if search_query.lower() in post["title"].lower()
        or search_query.lower() in post["content"].lower()
        or search_query.lower() in post["author"].lower()
        or search_query.lower() in post["date"].lower()
    ]

    return jsonify(_paginate(matches, page, limit)), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
