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

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file1" not in request.files:
            return "Missing files"

        file1 = request.files["file1"]
        

        if file1.filename == "":
            return "No selected files"

        file1_path = os.path.join(app.config["UPLOAD_FOLDER"], file1.filename)
        
        file1.save(file1_path)
       

        

        # Upload to database
        if file1_path is not None:
            upload_to_db(file1_path, "your_table")
            return "File uploaded and data saved in database! <br><a href='/view_data'>View Uploaded Data</a>"

    return render_template("upload.html")




def upload_to_db(csv_file, table_name):
    """Uploads merged CSV data to MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        df = pd.read_csv(csv_file)

        # Create table dynamically
        columns = ", ".join([f"`{col}` VARCHAR(255)" for col in df.columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        cursor.execute(create_table_query)
        print(f"Table {table_name} created or already exists.")

        # Insert data using parameterized queries
        placeholders = ", ".join(["%s"] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"

        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))
            print(f"Inserted row: {tuple(row)}")

        conn.commit()
        cursor.close()
        conn.close()
        print("Data uploaded successfully!")

    except Exception as e:
        print(f"Error uploading to database: {e}")


@app.route("/view_data")
def view_data():
    """Fetches and displays data from the database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM your_table")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        cursor.close()
        conn.close()

        return render_template("view_data.html", column_names=column_names, rows=rows)
    except Exception as e:
        return f"Error fetching data: {e}"


if __name__ == "__main__":
    app.run(debug=True)
