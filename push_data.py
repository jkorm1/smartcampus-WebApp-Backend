import psycopg2
import json

# Database connection details
DB_HOST = 'localhost'  # Change if your database is hosted elsewhere
DB_NAME = 'smartcampus'
DB_USER = 'jkorm'  # Replace with your PostgreSQL username
DB_PASSWORD = 'jkorm'  # Replace with your PostgreSQL password

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = conn.cursor()

# Load your JSON data from dataCard.jsx
data = {
    "hostel1": [
        {
            "id": 1,
            "image": "th (11).jpeg",
            "name": "St. Theresas",
            "price": "1,000.00",
            "handle": "j.korm",
        },
        {
            "id": 2,
            "name": "Victory Towers",
            "price": "500.00",
            "image": "OIP (14).jpeg",
            "handle": "j.korm",
        },
        # Add the rest of your hostel1 data here...
    ],
    "hostel2": [
        {
            "name": "St Theresa's Hostel",
            "rating": 9.9,
            "reviews": 1461,
            "price": "GHS 6k",
            "image": "th (17).jpeg",
            "handle": "st.theresas"
        },
        {
            "name": "Lienda Hostel",
            "rating": 7.9,
            "reviews": 1461,
            "price": "GHS 6k",
            "image": "th (11).jpeg",
            "handle": "lienda"
        },
        # Add handle values for other entries...
    ]
}

# Insert data into the hostels table
for hostel in data['hostel1']:
    cur.execute('INSERT INTO hostels (name, image, price, handle) VALUES (%s, %s, %s, %s)',
                (hostel['name'], hostel['image'], hostel['price'], hostel['handle']))

for hostel in data['hostel2']:
    cur.execute('INSERT INTO hostels (name, image, price, rating, reviews, handle) VALUES (%s, %s, %s, %s, %s, %s)',
                (hostel['name'], hostel['image'], hostel['price'], hostel['rating'], hostel['reviews'], hostel['handle']))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Data pushed to PostgreSQL successfully!")
