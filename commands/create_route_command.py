from datetime import datetime

from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.location import Location
from models.user import User


class CreateRouteCommand(BaseCommand):

    PERMISSION = User.MANAGER
    USAGE = "createroute {Month} {Day} {Hour} {LOCATIONS}: (sep by space)}"
    SPECIAL_CASE = True # Skip params validation

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)

        # Validate at least 5 or more params
        if len(params) < 5:
            raise ValueError(f"Expected at least 5 parameters, {len(params)} provided.")

    def execute(self):
        # Unpacking values from params
        month, day, time, *stops = self.params

        # Make sure locations are valid
        Location.validate_locations(stops)

        # Make sure the route isn't from one city to the same location
        for i in range(len(stops) - 1):
            if stops[i] == stops[i + 1]:
                raise ValueError(f"Route cannot include the same location in succession (from {stops[i]} to {stops[i]})")

        # Datetime
        date = " ".join((month, day, time))
        try:
            date = datetime.strptime(date, "%b %d %H:%M")
            date = date.replace(year=datetime.now().year)
            if date < datetime.now():
                raise ValueError("Date of creation can not be in the past")

        except:
            raise ValueError(f"Invalid date ({date}) provided!")

        # returning the result of create_route execution
        r = self.app_data.create_route(date, *stops)
        return f"Route #{r.route_id} from {stops[0]} to {stops[-1]} with {len(stops) - 2} stop(s) in-between created."