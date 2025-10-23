from flask import Flask, render_template, request
import random
import mysql.connector
from datetime import datetime
import os

# Initialize the Flask application
app = Flask(__name__)

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'Imbkihic11@12'), 
    'database': os.environ.get('DB_NAME', 'bape_bookings_db')
}

def get_db_connection():
    try:
        connect = mysql.connector.connect(**DB_CONFIG)
        return connect
    except mysql.connector.Error as error:
        print(f"Error connecting to database: {error}")
        return None


def Ambulance():
    return random.choice(["Small Ambulance", "Medium Ambulance", "Large Ambulance"])

def Driver_number():
    return str(random.randint(6, 9)) + ''.join(str(random.randint(0, 9)) for _ in range(9))

def Vehicle_number():
    return ''.join(str(random.randint(0, 9)) for _ in range(4))

# --- Database Saving Function ---
def save_booking_to_db(booking_type, case_description, booking_date, booking_time, patient_name, phone_number, address, ambulance_size, hospital_name, driver_number, vehicle_number):
    
    con = get_db_connection()
    if con:
        try:
            cursor = con.cursor()
            sql = """INSERT INTO bookings (booking_type, case_description, booking_date, booking_time, patient_name,
                     phone_number, address, ambulance_size, hospital_name, driver_number, vehicle_number)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (booking_type, case_description, booking_date, booking_time, patient_name, phone_number, address, ambulance_size, hospital_name, driver_number, vehicle_number)
            cursor.execute(sql, values)
            con.commit()
            print(f"Booking {booking_type} saved to database.")
            return True
        except mysql.connector.Error as err:
            print(f"Error saving booking to DB: {err}")
            con.rollback()  # Rollback changes if an error occurs
            return False
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if con is not None and con.is_connected():
                con.close()
    return False


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/emergency", methods=["GET", "POST"])
def emergency():
    if request.method == "POST":
        case = request.form.get("case")
        name = request.form.get("name")
        phone = request.form.get("phone")
        address = request.form.get("address")
        date_string = datetime.now().strftime("%d/%m/%Y")
        time_string = datetime.now().strftime("%H:%M:%S")
        ambulance_size = Ambulance()
        driver_number = Driver_number()
        vehicle_number = Vehicle_number()
        hospital_name = "Filled Later"

        if save_booking_to_db(
            "Emergency",
            case,
            date_string,
            time_string,
            name,
            phone,
            address,
            ambulance_size,
            hospital_name,
            driver_number,
            vehicle_number
        ):
            confirmation = f"""
                Ambulance Booked Successfully!<br>
                Case: {case}<br>
                Patient Name: {name}<br>
                Phone: {phone}<br>
                Address: {address}<br>
                Date: {date_string}<br>
                Time: {time_string}<br>
                Ambulance Size: {ambulance_size}<br>
                Hospital: {hospital_name}<br>
                Driver Number: {driver_number}<br>
                Vehicle Number: {vehicle_number}
            """
            return confirmation
        else:
            return "Failed to book ambulance. Please try again later.", 500
    
    return render_template("emergency.html")

@app.route("/pregnancy", methods=["GET", "POST"])
def pregnant():
    if request.method == "POST":
        date = request.form.get("date")
        time = request.form.get("time")
        name = request.form.get("name")
        phone = request.form.get("phone")
        address = request.form.get("address")
        ambulance_size = request.form.get("ambulance_size")
        hospital = request.form.get("hospital")
        driver_number = Driver_number()
        vehicle_number = Vehicle_number()

        if save_booking_to_db(
            "Pregnant",
            "Pregnant",
            date,
            time,
            name,
            phone,
            address,
            ambulance_size,
            hospital,
            driver_number,
            vehicle_number
        ):
            confirmation = f"""
                Ambulance Booked Successfully!<br>
                Patient Name: {name}<br>
                Phone: {phone}<br>
                Address: {address}<br>
                Date: {date}<br>
                Time: {time}<br>
                Ambulance Size: {ambulance_size}<br>
                Hospital: {hospital}<br>
                Driver Number: {driver_number}<br>
                Vehicle Number: {vehicle_number}
            """
            return confirmation
        else:
            return "Failed to book ambulance. Please try again later.", 500

    return render_template("pregnancy.html")

@app.route("/general", methods=["GET", "POST"])
def general():
    if request.method == "POST":
        case = request.form.get("case")
        date = request.form.get("date")
        time = request.form.get("time")
        name = request.form.get("name")
        phone = request.form.get("phone")
        address = request.form.get("address")
        ambulance_size = request.form.get("ambulance_size")
        hospital = request.form.get("hospital")
        driver_number = Driver_number()
        vehicle_number = Vehicle_number()

        if save_booking_to_db(
            "General",
            case,
            date,
            time,
            name,
            phone,
            address,
            ambulance_size,
            hospital,
            driver_number,
            vehicle_number
        ):
            confirmation = f"""
                Ambulance Booked Successfully!<br>
                Case: {case}<br>
                Patient Name: {name}<br>
                Phone: {phone}<br>
                Address: {address}<br>
                Date: {date}<br>
                Time:{time}<br>
                Ambulance Size: {ambulance_size}<br>
                Hospital: {hospital}<br>
                Driver Number: {driver_number}<br>
                Vehicle Number: {vehicle_number}
            """
            return confirmation
        else:
            return "Failed to book ambulance. Please try again later.", 500

    return render_template("general.html")

if __name__ == "__main__":
    app.run(debug=True)
