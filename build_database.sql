CREATE DATABASE laundry;

USE laundry;

CREATE TABLE orders (
    order_id real, 
    email_client varchar(30),
    phone_client varchar(30),
    order_cost real,
    amount_items real,
    order_entered DATETIME DEFAULT CURRENT_TIMESTAMP, 
    order_notes varchar(100),
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
    password_client VARCHAR(64),
    message_type ENUM('email','sms')
);

CREATE TABLE managers (
    name VARCHAR(30), 
    family_name VARCHAR(30), 
    city VARCHAR(30),
    street VARCHAR(30),
    house_number real,
    phone_manager VARCHAR(30), 
    email_manager VARCHAR(30),
    password_manager VARCHAR(64),
    message_type ENUM('email','sms')
);

CREATE TABLE stock (
    material_name VARCHAR(30) PRIMARY KEY,
    material_value NUMERIC(10,0)
);

CREATE TABLE variables (
    variable_name VARCHAR(30) PRIMARY KEY,
    variable_value NUMERIC(10,2)
);