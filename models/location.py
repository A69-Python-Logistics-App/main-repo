
from models.package import Package
class Location:
    SYDNEY_CODE = "SYD"
    MELBOURNE_CODE = "MEL"
    ADELAIDE_CODE = "ADL"
    ALICE_SPRINGS_CODE = "ASP"
    BRISBANE_CODE = "BRI"
    DARWIN_CODE = "DAR"
    PERTH_CODE = "PER"
    
    cities = [SYDNEY_CODE, MELBOURNE_CODE, ADELAIDE_CODE, ALICE_SPRINGS_CODE, BRISBANE_CODE, DARWIN_CODE, PERTH_CODE]

    def __init__(self,hub_name):
        if hub_name not in Location.Cities:
            raise ValueError("Invalid Location")
        self.hub_name = hub_name
        # self.list_of_trucks_on_location:list[Truck] = []
        self.list_of_packages_on_location: list[Package] = []

    @classmethod
    def validate_locations(cls, *locations: list[str]):
        """
        Checks if locations are valid
        :param locations: accepts at least one location or more as argument(s)
        :raise ValueError: if any location is invalid
        """
        for location in locations:
            if not location in cls.Cities:
                raise ValueError("\n".join([f"Invalid location [{location}] provided.",
                                            f"Available locations: {', '.join(cls.Cities)}"]))