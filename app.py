import sqlite3
import os
import csv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from yolo_detection import process_invoice  # Import your YOLO function

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder where images will be uploaded
DATA_FOLDER = 'data'  # Folder where user data and CSV will be stored
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS












ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config['UPLOAD_FOLDER'] = UPLOAD



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

# Helper function to check file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

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
    if 'username' not in session:
        flash('You must be logged in to view the dashboard.')
        return redirect('/login')
    
    # Your dashboard content here
    return render_template('dashboard.html')
# Process invoice route
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        username = session.get('username')
        if not username:
            flash("You must be logged in to upload files.")
            return redirect('/login')

        # Ensure the user's data folder exists
        user_data_folder = os.path.join(DATA_FOLDER, username)
        os.makedirs(user_data_folder, exist_ok=True)

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            # Extract data from the invoice using YOLO detection
            extracted_data = process_invoice(image_path)
            if extracted_data:
                company_name, date, total = extracted_data
            else:
                flash("Data extraction from invoice failed.")
                return redirect(url_for('upload'))

            # User-specific folder for image data
            image_name = os.path.splitext(filename)[0]
            image_data_folder = os.path.join(user_data_folder, image_name)
            os.makedirs(image_data_folder, exist_ok=True)

            # Move image to user's data folder
            new_image_path = os.path.join(image_data_folder, filename)
            os.rename(image_path, new_image_path)

            # Save the extracted data in CSV format
            csv_path = os.path.join(image_data_folder, f'{image_name}.csv')
            csv_data = [
                ['Company', 'Date', 'Total'],
                [company_name, date, total],
            ]
            with open(csv_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(csv_data)

            # Check if CSV is created successfully
            if os.path.exists(csv_path):
                flash(f"File '{filename}' uploaded and data saved successfully!")
                return redirect(url_for('upload_success'))  # Redirect to success page
            else:
                flash("An error occurred while saving the data.")
                return redirect(url_for('upload'))

        else:
            flash("No file selected or invalid file type.")
            return redirect(url_for('upload'))
    
    return render_template('upload.html')

@app.route('/upload_success')
def upload_success():
    return render_template('upload_success.html')


# Write extracted invoice data to CSV
def write_to_csv(username, extracted_data):
    user_folder = os.path.join("data", username)  # Path to user folder
    csv_path = os.path.join(user_folder, "expenses.csv")

    # Open the CSV file in append mode to add new rows
    with open(csv_path, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Check if the CSV file is empty (if so, write the header)
        if csvfile.tell() == 0:
            writer.writerow(["Company", "Date", "Total"])  # CSV header

        # Write the extracted data
        writer.writerow([extracted_data["company"], extracted_data["date"], extracted_data["total"]])

# Settings route
@app.route("/settings", methods=["GET", "POST"])
def settings():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        file = request.files.get("profile_picture")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Save the file path in the session or database
            session["profile_picture"] = url_for("static", filename=f"uploads/{filename}")
            return redirect(url_for("dashboard"))

    return render_template("settings.html")

# Logout route
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("profile_picture", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
