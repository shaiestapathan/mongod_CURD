🚗 Car Management System (Python + MongoDB + CustomTkinter)

This is a desktop GUI application built with Python, CustomTkinter, and MongoDB to manage car records.
You can add, read, update, and delete car details easily using an intuitive interface.

📌 Features

Add new car records (Brand, Model, Year)

View all car records in a table

Update existing records by selecting from the table

Delete records with confirmation

Clear input fields quickly

MongoDB database integration for storage

🛠️ Requirements

Make sure you have the following installed:

Python 3.8+

MongoDB (Running locally on default port: 27017)

Python libraries:

pip install customtkinter pymongo

📂 Project Structure
car_management/
│
├── main.py       # Main application code
├── README.md     # Project documentation

▶️ How to Run

Start MongoDB on your system:

mongod


Ensure it’s running on mongodb://localhost:27017/

Clone or download this project.

Install dependencies:

pip install customtkinter pymongo


Run the app:

python main.py

🖥️ Usage Instructions

Add Record – Enter Brand, Model, and Year, then click Add.

View Records – Click Read to load data from the database.

Update Record – Select a row, edit details, and click Update.

Delete Record – Select a row and click Delete.

Clear Fields – Click Clear to reset input boxes.

🖼️ Screenshot

(Add your app screenshot here)

📌 Notes

This app connects to a local MongoDB instance.

To change database or collection name, modify:

db = client["car_db"]
collection = db["cars"]


You can extend the project with search functionality or data export.
