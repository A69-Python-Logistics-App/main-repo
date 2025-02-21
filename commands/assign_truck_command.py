from commands.base.base_command import BaseCommand
from models.user import User
from models.helpers.validation_helpers import parse_to_int

class AssignTruckCommand(BaseCommand):

    PERMISSION = User.MANAGER
    PARAMS = 3
    USAGE = "assigntruck {truck_id} {truck_capacity} {route_id}"

    def __init__(self, params, app_data):
        super().__init__(params, app_data)

    def execute(self) -> str:
        truck_id = parse_to_int(self.params[0])
        truck_capacity = parse_to_int(self.params[1])
        route_id = parse_to_int(self.params[2])

        route = self.app_data.find_route_by_id(route_id)
        if not route:
            raise ValueError(f"Route with id {route_id} not found!")

        route.assign_truck(truck_id, truck_capacity)
        return f"Truck with ID {truck_id} and capacity {truck_capacity}kg assigned to route #{route_id}."