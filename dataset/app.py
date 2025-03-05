from flask import Flask, render_template, request
import pandas as pd
import mysql.connector
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "yourdatabase"
}

ALLOWED_EXTENSIONS = {"csv"}

def allowed_file(filename):
    # Check if the filename contains a dot (.) to separate the extension
    has_extension = "." in filename
    
    # Extract the file extension by splitting at the last dot and converting to lowercase
    extension = filename.rsplit(".", 1)[1].lower() if has_extension else ""
    
    # Check if the extracted extension is in the allowed set of extensions
    is_allowed = extension in ALLOWED_EXTENSIONS
    
    return is_allowed


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file1" not in request.files:
            return "Missing files"

        file1 = request.files["file1"]

        if file1.filename == "":
            return "No selected file"
        
        if not allowed_file(file1.filename):
            return "Invalid file format. Only CSV files are allowed."

        file1_path = os.path.join(app.config["UPLOAD_FOLDER"], file1.filename)
        file1.save(file1_path)

        try:
            upload_to_db(file1_path, "your_table")
            return "File uploaded and data saved in database! <br><a href='/view_data'>View Uploaded Data</a>"
        except Exception as e:
            return f"Error: {e}"

    return render_template("upload.html")

def upload_to_db(csv_file, table_name):
    """Uploads CSV data to MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        df = pd.read_csv(csv_file)

        # Create table dynamically with appropriate column types
        columns = ", ".join([f"`{col}` TEXT" for col in df.columns])  # Using TEXT for flexibility
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        cursor.execute(create_table_query)

        # Insert data using batch execution
        placeholders = ", ".join(["%s"] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.executemany(insert_query, df.values.tolist())

        conn.commit()
        cursor.close()
        conn.close()
        print("Data uploaded successfully!")

    except Exception as e:
        print(f"Error uploading to database: {e}")
        raise



if __name__ == "__main__":
    app.run(debug=True)
