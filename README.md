# 🏋️‍♀️ Fitness Studio Booking API

A simple RESTful API for a fictional fitness studio to manage class bookings using **Flask** and **SQLite**.  
Built as part of a Python Developer assignment (1+ years experience level).

---

## 📌 Features

- View all upcoming fitness classes (`/classes`)
- Book a slot in a class (`/book`)
- View all bookings by client email (`/bookings`)
- Timezone-aware: All classes are stored in **UTC**, displayed in **IST**
- Input validation, error handling, and logging included

---

## 🚀 Technologies Used

- Python 3
- Flask
- SQLite
- ZoneInfo (for timezone management)
- HTML templates (for demo view)

---

## 📂 Project Structure

fitness_booking_api/
├── app.py # Main Flask application
├── create_db.py # Seed data with class timings
├── templates/ # HTML templates (not used in API mode)
├── static/ # Optional CSS/JS (if any)
├── README.md # Project instructions
└── requirements.txt # Python dependencies

## Install Dependencies:

pip install -r requirements.txt



## Run The Application:

- python app.py
The server will start on: http://127.0.0.1:5000

## 🧪 API EndPoints:

📘 1. Get All Classes
GET /classes

Response : 
[
  {
    "id": 1,
    "name": "Yoga",
    "datetime": "2025-06-09T18:00:00+05:30",
    "instructor": "Aditi Sharma",
    "available_slots": 10
  }
]


📘 2. Book A Class
GET /book

Response (JSON)
{
  "class_id": 1,
  "client_name": "Riya Sharma",
  "client_email": "riya@example.com"
}


Response (Success)
{
  "message": "Booking successful for Yoga at 2025-06-09T18:00:00+05:30"
}


Response (Error)
{
  "error": "No slots available for this class"
}

3. Get Bookings By Email
GET /bookings?email=riya@example.com

Response
[
  {
    "class_name": "Yoga",
    "datetime": "2025-06-09T18:00:00+05:30",
    "instructor": "Aditi Sharma"
  }
]


## 🕒 Timezone Handling

- All class times are stored in **UTC** in the database.
- Times are returned in UTC from the API.
- On the frontend (HTML), JavaScript converts UTC time to the **user's local system timezone** for display.



## 📹 Loom Video Walkthrough

👉 []


## 📧 Author
Pragya Bharti Sharama
Email: pbssharma.1998@gmail.com
GitHub: [your-username](https://github.com/PBhartiSharma)

