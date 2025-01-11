from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',  # Change if your database is hosted elsewhere
        database='smartcampus',
        user='jkorm',  # Replace with your PostgreSQL username
        password='jkorm'  # Replace with your PostgreSQL password
    )
    return conn

# Route to handle both GET and POST requests for hostels
@app.route('/api/hostels', methods=['GET', 'POST'])
def handle_hostels():
    if request.method == 'POST':
        # Handle adding a new hostel
        data = request.get_json()
        name = data['name']
        image = data['image']
        price = data['price']
        handle = data['handle']
        category = data.get('category', 'normal')
        type = data.get('type', 'hostel')  # New field for type

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO hostels (name, image, price, handle, category, type) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
            (name, image, price, handle, category, type)
        )
        hostel_id = cur.fetchone()[0]  # Get the newly created hostel ID
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Hostel added successfully', 'hostelId': hostel_id}), 201

    elif request.method == 'GET':
        # Handle fetching all hostels or by category and type
        category = request.args.get('category', None)
        type = request.args.get('type', 'hostel')
        conn = get_db_connection()
        cur = conn.cursor()
        if category:
            cur.execute('SELECT * FROM hostels WHERE category = %s AND type = %s;', (category, type))
        else:
            cur.execute('SELECT * FROM hostels WHERE type = %s;', (type,))
        hostels = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{
            'id': hostel[0],
            'name': hostel[1],
            'image': hostel[2],
            'price': hostel[3],
            'handle': hostel[4],
            'rating': hostel[5],
            'reviews': hostel[6],
            'category': hostel[7],
            'type': hostel[8]  # Include the type field
        } for hostel in hostels])

# Route to handle both GET and POST requests for pricing
@app.route('/api/pricing', methods=['GET', 'POST'])
def handle_pricing():
    if request.method == 'POST':
        # Handle adding a new pricing entry
        data = request.get_json()
        title = data['title']
        price = data['price']
        amenities = data['amenities']
        hostel_id = data['hostel_id']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO Pricing (title, price, amenities, hostel_id) VALUES (%s, %s, %s, %s)',
            (title, price, amenities, hostel_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Pricing added successfully'}), 201

    elif request.method == 'GET':
        # Handle fetching all pricing entries
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM Pricing;')
        pricing = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{
            'id': p[0],
            'title': p[1],
            'price': p[2],
            'amenities': p[3],
            'hostel_id': p[4]
        } for p in pricing])

# Route to fetch pricing entries for a specific hostel
@app.route('/api/pricing/<int:hostel_id>', methods=['GET'])
def get_pricing_for_hostel(hostel_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Pricing WHERE hostel_id = %s;', (hostel_id,))
    pricing = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        'id': p[0],
        'title': p[1],
        'price': p[2],
        'amenities': p[3],
        'hostel_id': p[4]
    } for p in pricing])

if __name__ == '__main__':
    app.run(debug=True)
