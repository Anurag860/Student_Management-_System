from flask import Flask, render_template, request, redirect, url_for, session
from database.sqlite_db import SQLiteDB
from utils.crypto import encrypt_password, verify_password
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

db_path = os.path.join("database", "students.db")
db = SQLiteDB(db_path)
       
@app.route("/")
def index():
   return render_template("index.html")  
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = encrypt_password(request.form["password"])
        try:
            with db._connect() as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
            return redirect(url_for("login"))
        except:
            return "Username already exists!"
    return render_template("register.html")
   
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with db._connect() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and verify_password(user[2], password):
            session["username"] = username
            return redirect(url_for("view_students"))
        return "Invalid credentials"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/students")
def view_students():
    if "username" not in session:
        return redirect(url_for("login"))
    students = db.get_all_students()
    return render_template("view_students.html", students=students)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        student = {
            'id': int(request.form['id']),
            'name': request.form['name'],
            'age': int(request.form['age']),
            'course': request.form['course']
        }
        db.add_student(student)
        return redirect(url_for("view_students"))
    return render_template("add_student.html")

@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    if "username" not in session:
        return redirect(url_for("login"))
    db.delete_student(student_id)
    return redirect(url_for("view_students"))

@app.route("/update/<int:student_id>", methods=["GET", "POST"])
def update_student(student_id):
    if "username" not in session:
        return redirect(url_for("login"))
    student = db.get_student_by_id(student_id)
    if not student:
        return "Student not found", 404

    if request.method == "POST":
        updated_student = {
            'id': student_id,
            'name': request.form['name'],
            'age': int(request.form['age']),
            'course': request.form['course']
        }
        db.update_student(updated_student)
        return redirect(url_for("view_students"))

    return render_template("update_student.html", student=student)

if __name__ == "__main__":
    app.run(debug=True)
