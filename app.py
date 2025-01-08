from flask import Flask, request, render_template, flash
import psycopg2
import hash #custom library to hash using hash.hash_text(data)
import os
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("host"),
        database=os.getenv("database"),
        user=os.getenv("user"),
        password=os.getenv("password")
    )
    return conn

def init_db():
    try:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(255) NOT NULL,
                        password VARCHAR(255) NOT NULL
                    );
                """)
                conn.commit()  # Commit only if the query runs successfully
    except Exception as e:
        flash(f"Error initializing the database: {e}", "danger")
    finally:
        if conn:
            conn.close()
init_db()

app = Flask(__name__)
app.secret_key = os.getenv("secret")
port = int(os.getenv("PORT", 5000))
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
    app.run(host='0.0.0.0', port=port, debug=True)
