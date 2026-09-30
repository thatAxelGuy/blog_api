from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "This is Axel's actual first post", "content": "You don't see me?"},
    {"id": 4, "title": "Learning Flask", "content": "Flask is a lightweight Python web framework."},
    {"id": 5, "title": "Python Tips", "content": "Here are some useful tips for writing clean Python code."},
    {"id": 6, "title": "Building REST APIs", "content": "You can build REST APIs with Flask and Python."},
    {"id": 7, "title": "Web Development Basics", "content": "HTTP, JSON, and APIs are important concepts in web development."},
    {"id": 8, "title": "My First Flask API", "content": "Today I built my first API using Flask."},
    {"id": 9, "title": "Understanding JSON", "content": "JSON is commonly used to exchange data between clients and servers."}
]

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

    if sort_by not in ['title', 'content']:
        return jsonify({"error" : "Sort can be either 'title' or 'content'"}), 400

    if direction not in ['asc', 'desc']:
        return jsonify({"error" : "Direction can only be 'asc' or 'desc'"}), 400

    if sort_by and direction:
        posts = sorted(
            POSTS,
            key=lambda post: post[sort_by],
            reverse= direction == "desc"
        )
    
    return jsonify(_paginate(posts, page, limit)), 200

@app.route('/api/posts', methods=['POST'])
def add_post():
    new_id = max((post["id"] for post in POSTS), default=0) + 1

    response = request.json

    if not response or not response.get("title", "").strip() or not response.get("content", "").strip():
        return jsonify({"error" : "Title and content are required"}), 400
    
    new_post = {
        "id": new_id,
        "title": response.get('title').strip(),
        "content": response.get('content').strip()
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<id>', methods=['DELETE'])
def remove_post(id):
    if not id.isdigit():
        return jsonify({"error" : "Post id should be an integer"}), 400

    id  = int(id)

    for post in POSTS:
        if post["id"] == id:
            POSTS.remove(post)
            return jsonify(
                {
                    "message": f"Post with id {id} has been deleted successfully."
                }
            ), 200

    return jsonify({
        "error": f"Post with id {id} doesn't exist."
    }), 404


@app.route('/api/posts/<id>', methods=['PUT'])
def update_post(id):

    if not id.isdigit():
            return jsonify({"error" : "Post id should be an integer"}), 400
    
    id  = int(id)

    post_to_update = None
    for post in POSTS:
        if post['id'] == id:
            post_to_update = post
            break

    if post_to_update is None:
        return jsonify({
                "error": f"Post with id {id} doesn't exist."
            }), 404

    response = request.json

    if "title" in response:
        post_to_update['title'] = response.get('title')

    if "content" in response:
        post_to_update['content'] = response.get('content')

    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get("title")
    content_query = request.args.get("content")
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=5, type=int)

    if page < 1 or limit < 1:
        return jsonify({"error": "Invalid page number or limit"}), 400

    matches = [
        post 
        for post in POSTS 
        if title_query is not None and title_query.lower() in post['title'].lower() 
        or content_query is not None and content_query.lower() in post['content'].lower()
    ]

    return jsonify(_paginate(matches, page, limit)), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
