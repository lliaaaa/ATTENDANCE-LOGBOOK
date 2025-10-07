from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# --- Create tables ---
with app.app_context():
    db.create_all()

# --- Home Route (Read) ---
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# --- Create Route ---
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        new_student = Student(name=name, email=email, course=course)
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully!')
        return redirect(url_for('index'))
    return render_template('add.html')

# --- Update Route ---
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.course = request.form['course']
        db.session.commit()
        flash('Student updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit.html', student=student)

# --- Delete Route ---
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
