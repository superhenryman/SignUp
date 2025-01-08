from flask import Flask, request, render_template, flash
import psycopg2
import hash #custom library to hash using hash.hash_text(data)

def get_db_connection():
    conn = psycopg2.connect(
        host="your_host",
        database="your_database",
        user="your_user",
        password="your_password"
    )
    return conn

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])

def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = hash.hash_text(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        user = cursor.fetchone()
        conn.close()
        if user:
            flash("Login successful!", "success")
            return render_template("success.html", username=username)
        else:
            flash("Invalid Username or password!", "danger")
        #include captcha
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)