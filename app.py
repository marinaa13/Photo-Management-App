from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from PIL import Image, ImageOps, ImageFilter
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['THUMBNAIL_FOLDER'] = 'static/thumbnails'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

# Ensure the upload and thumbnail directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['THUMBNAIL_FOLDER'], exist_ok=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

photos = []

def create_thumbnail(image_path, thumbnail_path):
    with Image.open(image_path) as img:
        img = ImageOps.fit(img, (200, 200), Image.ANTIALIAS)
        img = img.filter(ImageFilter.GaussianBlur(2))
        img.save(thumbnail_path)

@app.route('/')
def index():
    sorted_photos = sorted(photos, key=lambda x: x['category'])
    return render_template('index.html', photos=sorted_photos)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123456':
            user = User(id=username)
            login_user(user)
            return redirect(url_for('upload'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['image']
        name = request.form['name']
        category = request.form['category']

        if file:
            # Sanitize filename
            filename = secure_filename(name)
            original_extension = os.path.splitext(file.filename)[1]
            sanitized_name = os.path.splitext(filename)[0]
            filename = sanitized_name + original_extension

            category_path = os.path.join(app.config['UPLOAD_FOLDER'], category)
            thumbnail_category_path = os.path.join(app.config['THUMBNAIL_FOLDER'], category)
            os.makedirs(category_path, exist_ok=True)
            os.makedirs(thumbnail_category_path, exist_ok=True)

            filepath = os.path.join(category_path, filename)
            thumbnail_path = os.path.join(thumbnail_category_path, f"{sanitized_name}.thumb{original_extension}")
            
            file.save(filepath)
            create_thumbnail(filepath, thumbnail_path)

            photo = {
                'name': sanitized_name,
                'category': category,
                'thumbnail_url': '/' + thumbnail_path.replace('\\', '/'),
                'full_res_url': '/' + filepath.replace('\\', '/')
            }
            photos.append(photo)
            
            return redirect(url_for('index'))

    return render_template('upload.html')

@app.route('/remove_photo', methods=['POST'])
@login_required
def remove_photo():
    photo_name = request.args.get('photo_name')
    category = request.args.get('category')
    global photos
    photos = [photo for photo in photos if not (photo['name'] == photo_name and photo['category'] == category)]

    # Remove the photo and its thumbnail from the filesystem
    possible_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    for ext in possible_extensions:
        full_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], category, f"{photo_name}{ext}")
        full_thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], category, f"{photo_name}.thumb{ext}")
        if os.path.exists(full_photo_path):
            os.remove(full_photo_path)
        if os.path.exists(full_thumbnail_path):
            os.remove(full_thumbnail_path)
    
    # Attempt to remove the category folders if they are empty
    category_path = os.path.join(app.config['UPLOAD_FOLDER'], category)
    thumbnail_category_path = os.path.join(app.config['THUMBNAIL_FOLDER'], category)
    try:
        if not os.listdir(category_path):  # Check if the directory is empty
            os.rmdir(category_path)
        if not os.listdir(thumbnail_category_path):  # Check if the directory is empty
            os.rmdir(thumbnail_category_path)
    except OSError as e:
        print(f"Error: {category} directory not removed. {e.strerror}")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
