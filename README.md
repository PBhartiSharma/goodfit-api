# 🏋️‍♀️ Fitness Studio Booking API

A simple RESTful API for a fictional fitness studio to manage class bookings using **Flask** and **SQLite**.  
Built as part of a Python Developer assignment (1+ years experience level).

---

## 📌 Features

- View all upcoming fitness classes (`/classes`)
- Book a slot in a class (`/book`)
- View all bookings by client email (`/bookings`)
- Timezone-aware: All classes are stored in **UTC**, displayed in **user's local system timezone**
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

```text
fitness_booking_api/
├── app.py               # Main Flask application
├── create_db.py         # Seed data script
├── templates/           # HTML templates (optional frontend)
│   └── base.html        # Example template
├── static/              # Optional static files (CSS/JS)
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Install Dependencies:

```pip install -r requirements.txt```



## Run The Application:

```python app.py```
The server will start on : http://127.0.0.1:5000

## 🧪 API EndPoints:

- 1. **Get All Classes**
GET /classes

```text
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
```


- 2. **Book A Class**
GET /book

```text
Response (JSON)
{
  "class_id": 1,
  "client_name": "Riya Sharma",
  "client_email": "riya@example.com"
}
```

```text
Response (Success)
{
  "message": "Booking successful for Yoga at 2025-06-09T18:00:00+05:30"
}
```

```text
Response (Error)
{
  "error": "No slots available for this class"
}
```


- 3. **Get Bookings By Email**
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

👉 [https://www.loom.com/share/4c5755f139bb425fb6e81ab7a0169e86]


## 📧 Author
- Name: Pragya Bharti Sharama
- Email: pbssharma.1998@gmail.com
- GitHub: [PBhartiSharma](https://github.com/PBhartiSharma)

