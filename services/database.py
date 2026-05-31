import sqlite3

DB_NAME = "terrafresh.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sellers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        business_name TEXT NOT NULL,
        whatsapp TEXT UNIQUE NOT NULL,
        city TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seller_id INTEGER,
        product_name TEXT NOT NULL,
        category TEXT,
        price REAL,
        quantity INTEGER,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (seller_id) REFERENCES sellers(id)
    )
    """)

    conn.commit()
    conn.close()


def create_seller(
    full_name,
    business_name,
    whatsapp,
    city,
    password_hash
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sellers (
            full_name,
            business_name,
            whatsapp,
            city,
            password_hash
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        full_name,
        business_name,
        whatsapp,
        city,
        password_hash
    ))

def get_seller_by_whatsapp(whatsapp):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM sellers WHERE whatsapp = ?",
        (whatsapp,)
    )

    seller = cursor.fetchone()

    conn.close()

    return seller

    conn.commit()
    conn.close()