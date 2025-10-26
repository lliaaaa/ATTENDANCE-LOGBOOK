from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Record
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
    records = Record.query.all()
    return render_template('index.html', records=records)

# --- Create Route ---
@app.route('/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        name = request.form['name'].strip()
        program = request.form['program'].strip()
        year = request.form['year'].strip()
        course = request.form['course'].strip()

        # --- Validation ---
        if not name or not program or not year or not course:
            flash('All fields are required!')
            return redirect(url_for('add_record'))

        if any(char.isdigit() for char in name) or any(char.isdigit() for char in program) or any(char.isdigit() for char in course):
            flash('Name, Program, and Course should not contain numbers!')
            return redirect(url_for('add_record'))

        if not year.isdigit():
            flash('Year must be a number!')
            return redirect(url_for('add_record'))

        new_record = Record(name=name, program=program, year=int(year), course=course)
        db.session.add(new_record)
        db.session.commit()
        flash('Record added successfully!')
        return redirect(url_for('index'))

    return render_template('add.html')

# --- Update Route ---
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_record(id):
    record = Record.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name'].strip()
        program = request.form['program'].strip()
        year = request.form['year'].strip()
        course = request.form['course'].strip()

        # --- Validation ---
        if not name or not program or not year or not course:
            flash('All fields are required!')
            return redirect(url_for('edit_record', id=id))

        if any(char.isdigit() for char in name) or any(char.isdigit() for char in program) or any(char.isdigit() for char in course):
            flash('Name, Program, and Course should not contain numbers!')
            return redirect(url_for('edit_record', id=id))

        if not year.isdigit():
            flash('Year must be a number!')
            return redirect(url_for('edit_record', id=id))

        record.name = name
        record.program = program
        record.year = int(year)
        record.course = course
        db.session.commit()
        flash('Record updated successfully!')
        return redirect(url_for('index'))

    return render_template('edit.html', record=record)

# --- Delete Route ---
@app.route('/delete/<int:id>')
def delete_record(id):
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('Record deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)