import sqlite3
import os
import csv
import shutil
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.utils import secure_filename
from yolo_detection import process_invoice  # Import your YOLO function
from datetime import datetime,timedelta

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Define a secret key for session
app.config['SECRET_KEY'] = os.urandom(24)

app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder where images will be uploaded
DATA_FOLDER = 'data'  # Folder where user data and CSV will be stored
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
UPLOAD_FOLDER = 'static/uploads'

# Helper function to check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Home route
@app.route("/")
def home():
    return redirect(url_for("login"))

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    
    
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

# Signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            os.makedirs(os.path.join(DATA_FOLDER, username), exist_ok=True)  # Create a folder for the user
        except sqlite3.IntegrityError:
            return render_template("signup.html", error="Username already exists")
        finally:
            conn.close()
        return redirect(url_for("login"))
    return render_template("signup.html")

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('You must be logged in to view the dashboard.')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

# Process invoice route
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        username = session.get('user')
        if not username:
            flash("You must be logged in to upload files.")
            return redirect(url_for('login'))

        # Ensure the user's data folder exists
        user_data_folder = os.path.join(DATA_FOLDER, username)
        os.makedirs(user_data_folder, exist_ok=True)

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            # Extract data from the invoice using YOLO detection
            try:
                extracted_data = process_invoice(image_path)
                if extracted_data and len(extracted_data) == 4:
                    company_name, date, total, item_name = extracted_data
                else:
                    raise ValueError("Invalid data extracted")
            except Exception as e:
                flash(f"Data extraction failed: {str(e)}")
                return redirect(url_for('upload'))

            # User-specific folder for image data
            image_name = os.path.splitext(filename)[0]
            image_data_folder = os.path.join(user_data_folder, image_name)
            os.makedirs(image_data_folder, exist_ok=True)

            # Move image to user's data folder
            new_image_path = os.path.join(image_data_folder, filename)
            shutil.move(image_path, new_image_path)

            # Save the extracted data in CSV format
            csv_path = os.path.join(image_data_folder, f'{image_name}.csv')
            csv_data = [
                ['Company', 'Date', 'Total', 'Item Name'],  # Updated header to include "Item Name"
                [company_name, date, total, item_name],
            ]
            with open(csv_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(csv_data)

            if os.path.exists(csv_path):
                flash(f"File '{filename}' uploaded and data saved successfully!")
                
            else:
                flash("An error occurred while saving the data.")
                return redirect(url_for('upload'))

        else:
            flash("No file selected or invalid file type.")
            return redirect(url_for('upload'))
    
    return render_template('upload.html')



# Settings route
@app.route("/settings", methods=["GET", "POST"])
def settings():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        file = request.files.get("profile_picture")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            session["profile_picture"] = url_for("static", filename=f"uploads/{filename}")
            return redirect(url_for("dashboard"))

    return render_template("settings.html")

# Logout route
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("profile_picture", None)
    return redirect(url_for("login"))



@app.route('/history')
def history():
    user_name = session.get('user_name')  # Retrieve the current user name from session
    user_data_path = os.path.join('data', user_name)

    # Fetch image and CSV details for the user
    history_items = []
    if os.path.exists(user_data_path):
        for image_folder in os.listdir(user_data_path):
            image_path = os.path.join(user_data_path, image_folder, f"{image_folder}.jpg")
            csv_path = os.path.join(user_data_path, image_folder, f"{image_folder}.csv")
            if os.path.exists(image_path) and os.path.exists(csv_path):
                upload_time = os.path.getmtime(image_path)  # Get the upload time
                history_items.append({
                    'image': f'static/uploads/{user_name}/{image_folder}/{image_folder}.jpg',
                    'csv': f'data/{user_name}/{image_folder}/{image_folder}.csv',
                    'upload_time': upload_time
                })
    return render_template('history.html', history_items=history_items)

@app.route('/download_csv/<path:filename>')
def download_csv(filename):
    return send_file(filename, as_attachment=True)


@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')




if __name__ == "__main__":
    app.run(debug=True)
