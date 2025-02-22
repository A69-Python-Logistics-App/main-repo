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

    # System time unpacking
    if isinstance(state.get("time"), str):
        app_data._sys_time = datetime.fromisoformat(state["time"])

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
            r = app_data.create_route(datetime.fromisoformat(data["takeoff"]), data["stops"])
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

    return "Application Data (if any) loaded successfully from local storage."


def dump_to_file(app_data):
    last_user = app_data.current_employee.username if app_data.current_employee else "None"
    state: dict[str:dict] = {
        "time": app_data.system_time.isoformat(),
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
        state["customers"][customer.id] = {
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
            "date_creation": package.date_creation.isoformat() if isinstance(package.date_creation, datetime) else package.date_creation
        }

    for route in app_data._routes:
        state["routes"][route.route_id] = {
            "stops": route.stops,
            "takeoff": route.route_stop_estimated_arrival[0].isoformat() if isinstance(route.route_stop_estimated_arrival[0], datetime) else route.route_stop_estimated_arrival[0]
        }

    for location in app_data._locations:
        state["locations"][location.hub_name] = {
            "name": location.hub_name,
            "packages": location.packages
        }

    with open(app_data.HISTORY, "w") as f:
        json.dump(state, f)