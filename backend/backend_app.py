from datetime import date

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from posts import POSTS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/blog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Axel-Blog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


def _paginate(posts: list[dict], page: int, limit: int) -> list[dict]:
    start = (page - 1) * limit
    end = start + limit
    return posts[start:end]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_by = request.args.get("sort")
    direction = request.args.get("direction")
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=5, type=int)

    if page < 1 or limit < 1:
            return jsonify({"error": "Invalid page number or limit"}), 400

    posts = POSTS


    if sort_by is None and direction is None:
        return jsonify(_paginate(posts, page, limit)), 200

    if sort_by is None or direction is None:
        return jsonify({"error" : "Both sort and direction values required"}), 400

    if sort_by not in ['title', 'content', 'author', 'date']:
        return jsonify({"error" : "Sort can be 'title', 'content', 'author', or 'date'"}), 400

    if direction not in ['asc', 'desc']:
        return jsonify({"error" : "Direction can only be 'asc' or 'desc'"}), 400

    if sort_by and direction:
        posts = sorted(
            POSTS,
            
            key=lambda post: (
                date.fromisoformat(post[sort_by])
                if sort_by == "date" 
                else post[sort_by]
            ),
            
            reverse=direction == "desc"
        )
        
    
    return jsonify(_paginate(posts, page, limit)), 200

@app.route('/api/posts', methods=['POST'])
def add_post():
    new_id = max((post["id"] for post in POSTS), default=0) + 1

    response = request.json

    if (
        not response
        or not response.get("title", "").strip()
        or not response.get("content", "").strip()
        or not response.get("author", "").strip()
        or not response.get("date", "").strip()
    ):
        return jsonify({
        "error": "Title, content, author and date are required"
        }), 400
    
    new_post = {
        "id": new_id,
        "title": response.get('title').strip(),
        "content": response.get('content').strip(),
        "author": response.get("author").strip(),
        "date": response.get("date").strip()
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def remove_post(id):
    for post in POSTS:
        if post["id"] == id:
            POSTS.remove(post)
            return jsonify({
                "message": f"Post with id {id} has been deleted successfully."
            }), 200

    return jsonify({
        "error": f"Post with id {id} doesn't exist."
    }), 404


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post_to_update = None

    for post in POSTS:
        if post["id"] == id:
            post_to_update = post
            break

    if post_to_update is None:
        return jsonify({
            "error": f"Post with id {id} doesn't exist."
        }), 404

    response = request.json

    if "title" in response:
        post_to_update["title"] = response.get("title")

    if "content" in response:
        post_to_update["content"] = response.get("content")

    if "author" in response:
        post_to_update["author"] = response.get("author")

    if "date" in response:
        post_to_update["date"] = response.get("date")

    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    search_query = request.args.get("search")
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=5, type=int)

    if page < 1 or limit < 1:
        return jsonify({"error": "Invalid page number or limit"}), 400

    matches = [
        post 
        for post in POSTS 
        if search_query is not None and(
            search_query.lower() in post["title"].lower()
            or search_query.lower() in post["content"].lower()
            or search_query.lower() in post["author"].lower()
            or search_query.lower() in post["date"].lower()
        )
    ]

    return jsonify(_paginate(matches, page, limit)), 200

if __name__ == '__main__':
    print(app.url_map)
    app.run(host="0.0.0.0", port=5002, debug=True)
