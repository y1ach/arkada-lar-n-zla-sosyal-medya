from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "EIUHEEWoıhıhewOUyıYODTUFvUYflutDKKyıfLYUuıyfe_##£$213€WEFWIYGSFHWF_WEFOQWEFWHEĞ29237RGUIŞWEUFGQWE"  # Burayı daha güçlü bir şey yap
}

posts = []

from flask_cors import CORS
CORS(app)

@app.route("/upload", methods=["POST"])
def upload_post():
    file = request.files.get("file")
    username = request.form.get("username")
    caption = request.form.get("caption", "")

    if not username or not file:
        return jsonify({"error": "Username and file are required"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    file_url = f"http://127.0.0.1:5000/uploads/{filename}"

    post_data = {
        "id": len(posts) + 1,
        "username": username,
        "url": file_url,
        "caption": caption,
        "comments": []
    }

    posts.insert(0, post_data)

    return jsonify({"message": "Post uploaded", "post": post_data})

@app.route("/delete_post", methods=["POST"])
def delete_post():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    post_id = data.get("post_id")

    if username != ADMIN_CREDENTIALS["username"] or password != ADMIN_CREDENTIALS["password"]:
        return jsonify({"error": "Unauthorized"}), 403

    global posts
    posts = [post for post in posts if post["id"] != post_id]

    return jsonify({"message": "Post deleted"})

@app.route("/posts", methods=["GET"])
def get_posts():
    return jsonify(posts)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
