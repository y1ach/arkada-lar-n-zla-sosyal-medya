from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# Cloudinary Config (API Key ve Cloud Name bilgilerinizi burada kullanın)
cloudinary.config(
    cloud_name="ddzz9gofb",
    api_key="448296236667549",
    api_secret="JvoUD8z8SA0Zs2zIAAChfg3PSt4"
)

posts = []  # Yüklenen postları burada tutacağız.

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    caption = request.form.get('caption', '')
    username = request.form.get('username', 'Unknown User')

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Cloudinary'ye dosya yükleme
    upload_result = cloudinary.uploader.upload(file)

    # Yüklenen dosyanın URL'si
    file_url = upload_result['secure_url']

    # Yeni postu listeye ekle
    post = {
        "username": username,
        "caption": caption,
        "file_url": file_url
    }
    posts.insert(0, post)  # Yeni postu başa ekleyelim (en son eklenen üstte olsun)

    return jsonify({
        "message": "File uploaded successfully",
        "url": file_url,
        "caption": caption,
        "username": username
    })

@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)

if __name__ == '__main__':
    app.run(debug=True)
