from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Video ve resim postları burada saklanacak
posts = []

# CORS için izin veriyoruz
from flask_cors import CORS
CORS(app)

# Yazı ekleme fonksiyonu (sadece resimler için)
def add_text_to_image(image_path, text):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 40)  # Windows için
    except:
        font = ImageFont.load_default()  # Eğer font yoksa default kullan
    
    text_position = (50, 50)  # Yazının konumu
    text_color = (255, 255, 255)  # Beyaz renk
    draw.text(text_position, text, font=font, fill=text_color)
    
    new_path = image_path.replace(".", "_text.")
    img.save(new_path)
    return new_path

# Post Yükleme API'si
@app.route("/upload", methods=["POST"])
def upload_post():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    username = request.form.get("username")
    caption = request.form.get("caption", "")
    overlay_text = request.form.get("overlay_text", "")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Görsellerin üstüne metin ekle
    if file.filename.lower().endswith(("png", "jpg", "jpeg")) and overlay_text:
        file_path = add_text_to_image(file_path, overlay_text)

    file_url = f"http://127.0.0.1:5000/uploads/{os.path.basename(file_path)}"

    # Post'u kaydediyoruz
    post_data = {
        "username": username,
        "url": file_url,
        "caption": caption,
        "overlay_text": overlay_text,
        "comments": []
    }
    posts.append(post_data)

    return jsonify({"message": "Post uploaded", "post": post_data})

# Yorum Ekleme API'si
@app.route("/add_comment", methods=["POST"])
def add_comment():
    data = request.json
    username = data.get("username")
    post_url = data.get("post_url")
    comment_text = data.get("comment")

    if not username or not post_url or not comment_text:
        return jsonify({"error": "Missing fields"}), 400

    # Doğru post'u bul ve yorum ekle
    for post in posts:
        if post["url"] == post_url:
            post["comments"].append({"username": username, "comment": comment_text})
            return jsonify({"message": "Comment added", "post": post})

    return jsonify({"error": "Post not found"}), 404

# Kaydedilen Postları Listeleme API'si
@app.route("/posts", methods=["GET"])
def get_posts():
    return jsonify(posts)

# Dosyaları Sunma API'si
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
