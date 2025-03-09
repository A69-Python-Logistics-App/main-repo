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
    id TEXT PRIMARY KEY,
    weight REAL NOT NULL,
    pickup_location TEXT,
    dropoff_location TEXT,
    customer_id TEXT,
    status TEXT,
    current_location TEXT,
    date_creation TEXT
);

-- Create Routes table
CREATE TABLE routes (
    id TEXT PRIMARY KEY,
    takeoff TEXT
);

-- Create Customer_Packages junction table
CREATE TABLE customer_packages (
    customer_id TEXT,
    package_id TEXT,
    PRIMARY KEY (customer_id, package_id)
);

-- Create Route_Stops junction table
CREATE TABLE route_stops (
    route_id TEXT,
    stop_location TEXT,
    stop_order INTEGER,
    PRIMARY KEY (route_id, stop_location)
);

-- Create Location_Packages junction table
CREATE TABLE location_packages (
    location_hub_name TEXT,
    package_id TEXT,
    PRIMARY KEY (location_hub_name, package_id)
);

-- Create Log table
CREATE TABLE system_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_entry TEXT NOT NULL,
    timestamp TEXT DEFAULT (DATETIME('now'))
);

-- Create indexes for better performance
CREATE INDEX idx_packages_customer_id           ON packages(customer_id);
CREATE INDEX idx_packages_pickup                ON packages(pickup_location);
CREATE INDEX idx_packages_dropoff               ON packages(dropoff_location);
CREATE INDEX idx_packages_current               ON packages(current_location);
CREATE INDEX idx_customer_packages_customer     ON customer_packages(customer_id);
CREATE INDEX idx_customer_packages_package      ON customer_packages(package_id);
CREATE INDEX idx_route_stops_route              ON route_stops(route_id);
CREATE INDEX idx_location_packages_location     ON location_packages(location_hub_name);