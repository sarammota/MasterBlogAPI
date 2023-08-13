from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_by = request.args.get('sort', default=None, type=str)
    direction = request.args.get('direction', default=None, type=str)

    if sort_by is None or direction is None:
        return jsonify(POSTS)

    if sort_by not in ['title', 'content'] or direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid sort field or direction"}), 400

    sorted_posts = sorted(POSTS, key=lambda post: post[sort_by], reverse=(direction == 'desc'))
    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.json
    if "title" in data and "content" in data:
        new_post = {
            "id": len(POSTS) + 1,
            "title": data["title"],
            "content": data["content"]
        }
        POSTS.append(new_post)
        return jsonify({"message": "Post added successfully", "post": new_post}), 201
    else:
        return jsonify({"error": "Title and content are required fields"}), 400


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post_index = None
    for index, post in enumerate(POSTS):
        if post['id'] == post_id:
            post_index = index
            break

    if post_index is not None:
        deleted_post = POSTS.pop(post_index)
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200
    else:
        return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.json
    post_to_update = None
    for post in POSTS:
        if post['id'] == post_id:
            post_to_update = post
            break

    if post_to_update is not None:
        if "title" in data:
            post_to_update["title"] = data["title"]
        if "content" in data:
            post_to_update["content"] = data["content"]

        updated_post = {
            "id": post_to_update["id"],
            "title": post_to_update["title"],
            "content": post_to_update["content"]
        }
        return jsonify(updated_post), 200
    else:
        return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', default='', type=str)
    content_query = request.args.get('content', default='', type=str)

    matching_posts = []
    for post in POSTS:
        if title_query.lower() in post['title'].lower() or content_query.lower() in post['content'].lower():
            matching_posts.append(post)

    return jsonify(matching_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
