![App Title Image](images/readme_title_image.jpg)

*A package and route management system designed for streamlined logistics operations, featuring SQLite3 integration and robust role-based command execution.*

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Commands](#commands)
- [License](#license)

## Features
- **Package Management**: Create, update status, and track packages.
- **Route Management**: Plan, edit, and calculate distances and ETAs.
- **SQLite3 Integration**: Maintain the application's state for seamless operation.
- **Employee Management**: Roles include **User**, **Manager**, **Supervisor**, and **Admin**.
- **Role-Based Commands**: Commands are executed based on logged-in employee roles.

## Prerequisites
- Python 3.8 or higher
- SQLite3
- Install required libraries:
```sh
pip install -r requirements.txt
```

## Commands
| Command                  | Description                                                          | Example Usage                                      |
| ------------------------ | -------------------------------------------------------------------- | -------------------------------------------------- |
| `createemployee`         | Create a new employee with username, password, and role.             | `createemployee ElliotAlderson hackerman123 Admin` |
| `removeemployee`         | Remove a employee with username.                                     | `removeemployee ElliotAlderson`                    |
| `createcustomer`         | Add a new customer with name and email.                              | `createcustomer Peter Griffin peter@griffin.com`   |
| `removecustomer`         | Remove a customer with email.                                        | `removecustomer peter@griffin.com`                 |
| `createpackage`          | Create a package with weight, pickup, and drop-off info.             | `createpackage 50 SYD MEL peter@griffin.com`       |
| `customerpackages`       | List all packages assigned to a given customer.                      | `customerpackages peter@griffin.com`               |
| `removepackage`          | Remove a package with ID.                                            | `removepackage 1000`                               |
| `createroute`            | Schedule a route with a date and locations.                          | `createroute Mar 2 11:30 SYD MEL BRI`              |
| `removeroute`            | Remove a route with ID.                                              | `removeroute 1`                                    |
| `assigntruck`            | Assign a truck (SCANIA, MAN, ACTROS) to a given route (id).          | `assigntruck MAN 1`                                |
| `addpackagetoroute`      | Add a package to a given route, using their IDs.                     | `addpackagetoroute 1000 1`                         |
| `fastforward`            | Advances the system time by the given amount (minutes, hours, days). | `fastforward 2 days`                               |
| `systemtime`             | Show the current system time.                                        | `systemtime`                                       |
| `updatecustomer`         | Update a given customer's first and last name.                       | `updatecustomer peter@griffin.com Glenn Quagmire`  |
| `changeemployeename`     | Update a given employee's name to a new one.                         | `changeemployeename ElliotAlderson MrRobot`        |
| `changeemployeepassword` | Update a given employee's password to a new one.                     | `changeemployeepassword MrRobot fSociety!#34`      |
| `changeemployeerole`     | Update a given employee's role to a new one.                         | `changeemployeerole MrRobot SUPERVISOR`            |
| `employees`              | List all registered employees.                                       | `employees`                                        |
| `trucks`                 | List all registered trucks.                                          | `trucks`                                           |
| `routes`                 | List all registered routes.                                          | `routes`                                           |
| `logout`                 | Logout from the current employee.                                    | `logout`                                           |
| `system_reset`           | Reset the program's state and exit.                                  | `system_reset`                                     |
| `exit`                   | Save the program's state and exit.                                   | `exit`                                             |

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.