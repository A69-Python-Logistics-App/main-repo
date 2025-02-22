from commands.base.base_command import BaseCommand
from models.user import User
from models.helpers.validation_helpers import parse_to_int
from models.truck_car_park import TruckCarPark

class AssignTruckCommand(BaseCommand):

    PERMISSION = User.MANAGER
    PARAMS = 2
    USAGE = "assigntruck {truck_type} {route_id}"

    def __init__(self, params, app_data):
        super().__init__(params, app_data)

    def execute(self) -> str:
        truck_name = self.params[0].upper()
        route_id = parse_to_int(self.params[1])

        route = self.app_data.find_route_by_id(route_id)
        if not route:
            raise ValueError(f"Route with id {route_id} not found!")
        
        if truck_name not in [TruckCarPark.ACTROS, TruckCarPark.SCANIA, TruckCarPark.MAN]:
            raise ValueError(f"Truck name '{truck_name}' is invalid.")

        truck = self.app_data.assign_truck_to_route(truck_name, route_id)
        return f"Truck '{truck.name}' assigned to route #{route.id}."