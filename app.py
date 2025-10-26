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
        name = request.form['name']
        program = request.form['program']
        year = request.form['year']
        course = request.form['course']
        new_record = Record(name=name, program=program, year=year, course=course)
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
        record.name = request.form['name']
        record.program = request.form['program']
        record.year = request.form['year'],
        record.course =  request.form['course']
        db.session.commit()
        flash('Record updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit.html', record=record)

# --- Delete Route ---
@app.route('/delete/<int:id>')
def delete_record(id):
    student = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('Record deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
