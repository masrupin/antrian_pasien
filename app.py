from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)



# Koneksi ke database MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'queue_system'
}

# Fungsi untuk menghubungkan ke database
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Fungsi untuk mendapatkan waktu akhir layanan terakhir
def get_last_service_end_time():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT service_end_time FROM service ORDER BY service_end_time DESC LIMIT 1")
    last_service = cursor.fetchone()
    conn.close()
    if last_service:
        return last_service['service_end_time']
    return None

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    cursor.execute("SELECT * FROM queue")
    queue = cursor.fetchall()
    cursor.execute("SELECT * FROM service")
    services = cursor.fetchall()
    conn.close()
    return render_template('index.html', customers=customers, queue=queue, services=services)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    name = request.form['name']
    arrival_time = request.form['arrival_time']
    
    arrival_time_dt = datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M")
    last_service_end_time = get_last_service_end_time()
    
    if last_service_end_time and arrival_time_dt < last_service_end_time:
        service_start_time = last_service_end_time
    else:
        service_start_time = arrival_time_dt
    
    service_end_time = service_start_time + timedelta(minutes=4)

    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO customers (name, arrival_time) VALUES (%s, %s)', (name, arrival_time_dt))
    cursor.execute('INSERT INTO queue (customer_name, queue_number, status) VALUES (%s, %s, %s)', 
                   (name, cursor.lastrowid, "Antri"))
    cursor.execute('INSERT INTO service (customer_name, service_start_time, service_end_time) VALUES (%s, %s, %s)', 
                   (name, service_start_time.strftime("%Y-%m-%d %H:%M:%S"), 
                   service_end_time.strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/clear_all', methods=['POST'])
def clear_all():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM customers')
    cursor.execute('DELETE FROM queue')
    cursor.execute('DELETE FROM service')
    
    # Reset auto increment
    cursor.execute('ALTER TABLE customers AUTO_INCREMENT = 1')
    cursor.execute('ALTER TABLE queue AUTO_INCREMENT = 1')
    cursor.execute('ALTER TABLE service AUTO_INCREMENT = 1')
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/update_status', methods=['GET'])
def update_status():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    current_time = datetime.now()
    cursor.execute('''
        SELECT q.id, s.service_start_time, s.service_end_time
        FROM queue q
        JOIN service s ON q.customer_name = s.customer_name
        WHERE q.status != 'selesai'
    ''')
    queue_data = cursor.fetchall()
    
    for row in queue_data:
        queue_id = row['id']
        service_start_time = row['service_start_time']
        service_end_time = row['service_end_time']
        
        if current_time >= service_end_time:
            new_status = 'Selesai'
        elif current_time >= service_start_time:
            new_status = 'Periksa'
        else:
            new_status = 'Antri'
        
        cursor.execute('UPDATE queue SET status = %s WHERE id = %s', (new_status, queue_id))
    
    conn.commit()
    conn.close()
    return jsonify(success=True)

@app.route('/delete_customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Delete customer from all tables
        cursor.execute('DELETE FROM customers WHERE id = %s', (customer_id,))
        cursor.execute('DELETE FROM queue WHERE id = %s', (customer_id,))
        cursor.execute('DELETE FROM service WHERE id = %s', (customer_id,))

        # Get all remaining customer IDs
        cursor.execute('SELECT id FROM customers ORDER BY id ASC')
        customer_ids = cursor.fetchall()

        # Update IDs to be sequential
        new_id = 1
        for (old_id,) in customer_ids:
            cursor.execute('UPDATE customers SET id = %s WHERE id = %s', (new_id, old_id))
            cursor.execute('UPDATE queue SET id = %s WHERE id = %s', (new_id, old_id))
            cursor.execute('UPDATE service SET id = %s WHERE id = %s', (new_id, old_id))
            new_id += 1

        # Reset auto increment to the next available ID
        cursor.execute('ALTER TABLE customers AUTO_INCREMENT = %s', (new_id,))
        cursor.execute('ALTER TABLE queue AUTO_INCREMENT = %s', (new_id,))
        cursor.execute('ALTER TABLE service AUTO_INCREMENT = %s', (new_id,))

        conn.commit()
        success = True
    except Exception as e:
        conn.rollback()
        success = False
        print(f"Error: {e}")

    conn.close()
    return jsonify(success=success)


if __name__ == '__main__':
    app.run(debug=True)
