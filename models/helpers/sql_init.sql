-- Create Employees table
CREATE TABLE employees (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

-- Create Customers table
CREATE TABLE customers (
    id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Create Locations table
CREATE TABLE locations (
    hub_name TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

-- Create Packages table
CREATE TABLE packages (
    id INTEGER PRIMARY KEY,
    weight REAL NOT NULL,
    pickup_location TEXT,
    dropoff_location TEXT,
    customer TEXT NOT NULL,
    status TEXT,
    current_location TEXT,
    date_creation TEXT
);

-- Create Routes table
CREATE TABLE routes (
    id INTEGER PRIMARY KEY,
    takeoff TEXT,
    start TEXT NOT NULL,
    stops TEXT,
    destination TEXT NOT NULL
);

-- Create Customer_Packages junction table
CREATE TABLE customer_packages (
    customer TEXT NOT NULL,
    package_id INTEGER NOT NULL,
    PRIMARY KEY (customer, package_id)
);

-- Create Location_Packages junction table
CREATE TABLE location_packages (
    hub_name TEXT,
    package_id INTEGER,
    PRIMARY KEY (hub_name, package_id)
);

-- Create Log table
CREATE TABLE system_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_entry TEXT NOT NULL,
    timestamp TEXT DEFAULT (DATETIME('now'))
);

-- Create indexes for better performance
CREATE INDEX idx_packages_customer           ON packages(customer);
CREATE INDEX idx_packages_pickup                ON packages(pickup_location);
CREATE INDEX idx_packages_dropoff               ON packages(dropoff_location);
CREATE INDEX idx_packages_current               ON packages(current_location);
CREATE INDEX idx_customer_packages_customer     ON customer_packages(customer);
CREATE INDEX idx_customer_packages_package      ON customer_packages(package_id);
CREATE INDEX idx_location_packages_location     ON location_packages(hub_name);