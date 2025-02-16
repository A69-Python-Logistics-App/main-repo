#
# File I/O
#
import json
from datetime import datetime

from models.customer import Customer
from models.package import Package
from models.route import Route


def dump_to_app(app_data) -> str:
    # Import log
    with open(app_data.HISTORY, "r") as f:
        try:
            state = dict(json.load(f))
        except Exception as e:
            return f"Failed to parse state from history file:\n{e}"

    # Employees unpacking
    # employees[username]: data
    employees = state.get("employees")
    if isinstance(employees, dict):
        for username, data in employees.items():
            app_data.create_employee(username, data["password"], data["role"])

    # Customer unpacking
    # customers[id_number]: data
    customers = state.get("customers")
    if isinstance(customers, dict):
        max_customer_id = 0
        for id_number, data in customers.items():
            id_number = int(id_number)
            c = app_data.create_customer(data["first_name"], data["last_name"], data["email"])
            c._id = id_number
            max_customer_id = max(id_number, max_customer_id)
        Customer.set_internal_id(max_customer_id + 1)

    # Routes unpacking
    # routes[id_number]: data
    routes = state.get("routes")
    max_routes_id = 0
    if isinstance(routes, dict):
        for id_number, data in routes.items():
            id_number = int(id_number)
            r = app_data.create_route(data["takeoff"], data["locations"])
            r.route_id = id_number
            max_routes_id = max(id_number, max_routes_id)
        Route.set_internal_id(max_routes_id + 1)  # TODO: Add route set_internal_id class method

    # Packages unpacking
    # packages[id_number]: data
    max_package_id = 999
    packages = state.get("packages")
    if isinstance(packages, dict):
        for id_number, data in packages.items():
            id_number = int(id_number)
            p = app_data.create_package(data["weight"], data["pickup"], data["dropoff"], data["customer_id"])
            p._package_id = id_number
            p._status = data["status"]
            max_package_id = max(id_number, max_package_id)
        Package.set_internal_id(max_package_id + 1)

    log = state.get("log")
    if log:
        app_data._log = log

    return "Application Data loaded successfully from local storage."


def dump_to_file(app_data):
    # TODO: Finish implementation for saving app state
    last_user = app_data.current_employee.username if app_data.current_employee else "None"
    state: dict[str:dict] = {
        "employees": {},
        "customers": {},
        "packages": {},
        "routes": {},
        "locations": {},
        "log": app_data.log + [f" >>> Last User: [{last_user}] <<< "]
    }

    for employee in app_data._employees:
        state["employees"][employee.username] = {
            "password": employee.password,
            "role": employee.role
        }

    for customer in app_data._customers:
        state["customers"][customer.id] = {  # TODO: Customer ID is string
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "packages": customer.package_ids
        }

    for package in app_data._packages:
        state["packages"][package.id] = {
            "weight": package.weight,
            "pickup": package.pickup_location,
            "dropoff": package.dropoff_location,
            "customer_id": package.customer_id,
            "status": package.status,
            "current_loc": package.current_location,
            "date_creation": package.date_creation
        }

    for route in app_data._routes:  # TODO: Add route getters and an ID setter for initialization from history
        state["routes"][route.route_id] = {
            "stops": route.stops,
            "takeoff": datetime.now().isoformat()  # route.date.isoformat() # TODO: Route doesn't have takeoff date getter
        }

    for location in app_data._locations:
        state["locations"][location.hub_name] = {
            "name": location.hub_name,
            "packages": location.packages
        }

    with open(app_data.HISTORY, "w") as f:
        json.dump(state, f)