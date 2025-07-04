from flask import Flask , render_template , redirect, flash , get_flashed_messages , url_for, request
from markupsafe import escape
import sqlite3
import logging
import create_db
import re



# Configure logging with timestamps, level, and message, output to file app.log
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)


# Suppress Flask and Werkzeug internal logs (only show warnings and above)
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('flask.app').setLevel(logging.WARNING)
logging.getLogger('flask').setLevel(logging.WARNING)


app = Flask(__name__)
app.secret_key = '34A67CVB78O8'


# Email validation function
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None



@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')


@app.route('/classes', methods=['GET'])
def classes():
    """
    Display all available fitness classes from the database.
    """
    try:
        conn = sqlite3.connect("fitness.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, datetime, instructor, available_slots, total_slots FROM classes")
        rows = cursor.fetchall()
        conn.close()

        class_list = []
        for row in rows:
            class_list.append({
                "id": row[0],
                "name": row[1],
                "datetime": row[2],
                "instructor": row[3],
                "available_slots": row[4],
                "total_slots": row[5]
            })

        logging.info("Classes retrieved successfully.")
        return render_template('classes.html', classes = class_list)

    except Exception as e:
        logging.error(f"Error retrieving classes: {e}")
        flash("Internal server error", "error")
        return redirect(url_for('home'))



@app.route('/book', methods = ['GET' , 'POST'])
def book():
    """
    Handle booking of a fitness class.
    GET: Show booking form.
    POST: Submit booking details.
    """
    try:
        if request.method == 'GET':
            class_id = request.args.get('class_id')
            if not class_id:
                logging.warning("Booking GET request missing class_id")
                flash("No class selected to book", "error")
                return redirect(url_for('classes'))

            conn = sqlite3.connect('fitness.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM classes WHERE id = ?", (class_id,))
            fitness_class = cursor.fetchone()
            conn.close()

            if not fitness_class:
                logging.warning(f"Booking GET request class not found: class_id={class_id}")
                flash("Class not found", "error")
                return redirect(url_for('classes'))

            return render_template('book.html', fitness_class = fitness_class)

        elif request.method == 'POST':
            class_id = request.form.get('class_id')
            client_name = request.form.get('client_name')
            client_email = request.form.get('client_email')

            if not all([class_id, client_name, client_email]):
                logging.warning(f"Booking POST missing fields: class_id={class_id}, client_email={client_email}")
                flash("All fields are required", "error")
                return redirect(url_for('classes'))
            
            # Check email format
            if not is_valid_email(client_email):
                flash('Invalid email format. Please enter a valid email.','error')
                return redirect(url_for('book', class_id=class_id))


            conn = sqlite3.connect('fitness.db')
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM bookings WHERE class_id = ? AND client_email = ?",
                (class_id, client_email)
            )
            if cursor.fetchone():
                conn.close()
                logging.warning(f"Duplicate booking attempt: client_email={client_email}, class_id={class_id}")
                flash("You have already booked this class.", "error")
                return redirect(url_for('classes'))

            cursor.execute("SELECT available_slots FROM classes WHERE id = ?", (class_id,))
            class_data = cursor.fetchone()

            if not class_data:
                conn.close()
                logging.error(f"Class not found during booking: class_id={class_id}")
                flash("Class not found", "error")
                return redirect(url_for('classes'))

            available_slots = class_data[0]
            if available_slots <= 0:
                conn.close()
                logging.warning(f"No slots available for class_id={class_id}, booking attempt by {client_email}")
                flash("No slots available", "error")
                return redirect(url_for('classes'))

            logging.info(f"Attempting booking: client_email={client_email}, class_id={class_id}, client_name={client_name}")

            cursor.execute(
                "INSERT INTO bookings (class_id, client_name, client_email) VALUES (?, ?, ?)",
                (class_id, client_name, client_email)
            )

            cursor.execute(
                "UPDATE classes SET available_slots = available_slots - 1 WHERE id = ?",
                (class_id,)
            )
            conn.commit()
            conn.close()

            logging.info(f"Booking successful for {client_email} in class {class_id}")
            flash("Successfully booked the class!", "success")
            return redirect(url_for('classes'))

    except AssertionError as ae:
        logging.warning(f"Validation failed: {ae}")
        flash(str(ae), "error")
        return redirect(url_for('classes'))
    except Exception as e:
        logging.error(f"Booking error: {e}")
        flash("Internal server error", "error")
        return redirect(url_for('classes'))



@app.route('/bookings/<email_id>', methods = ['GET' , 'POST'])
def bookings(email_id):
    """
    Display all bookings for a specific user by email ID.
    """
    try:
        safe_email = escape(email_id)
        conn = sqlite3.connect('fitness.db')
        cursor = conn.cursor()

        cursor.execute("select class_id from bookings where client_email = ? ", (safe_email,))
        class_ids = cursor.fetchall()

        if not class_ids:
            conn.close()
            logging.info(f"No bookings found for email: {safe_email}")
            flash("No bookings found for this email address.", "error")
            return redirect(url_for('home'))

        class_ids = [cid[0] for cid in class_ids]
        placeholders = ",".join("?" * len(class_ids))

        cursor.execute(f"SELECT name , datetime , instructor FROM classes join bookings on classes.id = bookings.class_id where class_id IN ({placeholders}) AND client_email = ? " , class_ids + [safe_email])
        class_details = cursor.fetchall()
        conn.close()
        logging.info(f"Retrieved bookings for {safe_email}")
        return render_template('bookings.html' , class_details = class_details , safe_email = safe_email)

    except Exception as e:
        logging.error(f"Error retrieving bookings for {email_id}: {e}")
        flash("Internal server error", "error")
        return redirect(url_for('home'))


if __name__ == '__main__':
    create_db.init_db()
    app.run(debug=False)
