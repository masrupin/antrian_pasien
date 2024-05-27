import mysql.connector

# Konfigurasi koneksi database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'queue_system'
}

# Membuat koneksi ke database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Membuat tabel customers
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    arrival_time DATETIME NOT NULL
)
''')

# Membuat tabel queue
cursor.execute('''
CREATE TABLE IF NOT EXISTS queue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    queue_number INT NOT NULL,
    status VARCHAR(255) NOT NULL
)
''')

# Membuat tabel service
cursor.execute('''
CREATE TABLE IF NOT EXISTS service (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    service_start_time DATETIME NOT NULL,
    service_end_time DATETIME NOT NULL
)
''')

# Commit perubahan dan menutup koneksi
conn.commit()
conn.close()
