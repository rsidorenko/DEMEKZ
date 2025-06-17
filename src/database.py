from pymysql.cursors import DictCursor
import pymysql
import os


DB_CONFIG = {
    'host': os.getenv('DB_HOST') or 'localhost',
    'user': os.getenv('DB_USER') or 'root',
    'password': os.getenv('DB_PASSWORD') or 'toor',
    'database': os.getenv('DB_NAME') or 'furniture',
    'port': int(os.getenv('DB_PORT') or 3306),
    'charset': 'utf8mb4',
    'autocommit': True,
    'cursorclass': DictCursor
}

CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS partners (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type ENUM('Розничный магазин', 'Оптовый магазин', 'Интернет-магазин') NOT NULL,
        name VARCHAR(255) NOT NULL,
        inn VARCHAR(12) NOT NULL,
        director VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        email VARCHAR(255) NOT NULL,
        rating DECIMAL(2,1) NOT NULL CHECK (rating >= 0 AND rating <= 5),
        sales_volume BIGINT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS suppliers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        inn VARCHAR(12) NOT NULL,
        supplier_type ENUM('Розничный магазин', 'Оптовый магазин', 'Интернет-магазин') NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS material_types (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        loss_percent DECIMAL(5, 2) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS product_types (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type_name VARCHAR(100) NOT NULL UNIQUE,
        type_coefficient DECIMAL(5, 2) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        article VARCHAR(50) NOT NULL UNIQUE,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL,
        size_length DECIMAL(10, 2) NOT NULL,
        size_width DECIMAL(10, 2) NOT NULL,
        size_height DECIMAL(10, 2) NOT NULL,
        weight DECIMAL(10, 2) NOT NULL,
        manufacture_time VARCHAR(50),
        FOREIGN KEY (type) REFERENCES product_types(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS materials (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type INT NOT NULL,
        name VARCHAR(255) NOT NULL UNIQUE,
        supplier_id INT,
        description TEXT,
        unit_price DECIMAL(10, 2) NOT NULL,
        stock_quantity DECIMAL(10, 2) NOT NULL,
        min_quantity DECIMAL(10, 2) NOT NULL,
        package_quantity DECIMAL(10, 2) NOT NULL,
        unit VARCHAR(20) NOT NULL,
        FOREIGN KEY (type) REFERENCES material_types(id),
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS product_materials (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT NOT NULL,
        material_id INT NOT NULL,
        quantity_needed DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (material_id) REFERENCES materials(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        birth_date DATE NOT NULL,
        passport VARCHAR(50) NOT NULL,
        bank_details VARCHAR(100) NOT NULL,
        family VARCHAR(50) NOT NULL,
        health VARCHAR(100) NOT NULL
    );
    """
]


def create_database():
    connection = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        connection.commit()
        print(
            f"База данных `{DB_CONFIG['database']}` проверена/создана.")
    finally:
        connection.close()


def initialize_tables():
    connection = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
    try:
        with connection.cursor() as cursor:
            for sql in CREATE_TABLES_SQL:
                cursor.execute(sql)
        connection.commit()
        print("Таблицы инициализированы.")
    finally:
        connection.close()
