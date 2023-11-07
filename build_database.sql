CREATE DATABASE laundry;

USE laundry;

CREATE TABLE orders (
    order_id real, 
    email_client varchar(30),
    phone_client varchar(30),
    order_amount real,
    amount_items real,
    order_entered DATETIME DEFAULT CURRENT_TIMESTAMP, 
    order_notes varchar(40),
    order_collected BOOLEAN
);

CREATE TABLE clients (
    name VARCHAR(30), 
    family_name VARCHAR(30), 
    city VARCHAR(30),
    street VARCHAR(30),
    house_number real,
    phone_client VARCHAR(30), 
    email_client VARCHAR(30),
    password_client VARCHAR(30),
    message_type ENUM('email','sms')
);

CREATE TABLE equipment (
    equipment_name VARCHAR(30) PRIMARY KEY,
    equipment_value NUMERIC(10,0)
);

CREATE TABLE variables (
    variable_name VARCHAR(30) PRIMARY KEY,
    variable_value NUMERIC(10,2)
);