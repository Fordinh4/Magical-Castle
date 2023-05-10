from diamond import Diamond
import random


class Room:
    """
    This class is to represent the nodes of the castle graph
    """

    def __init__(self, ID=None, north=None, south=None, east=None, west=None, portal: bool = False,
                 wormhole: bool = False, diamond: Diamond = None):
        """
        initialize each room that contain its ID, four links (N.E.W.S), and is that room in one of four states:
        empty, containing diamonds, containing a portal or containing a wormhole.
        """
        self.ID = ID
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.portal = portal
        self.wormhole = wormhole
        self.diamond = diamond

    def get_id(self) -> int:
        """
        Return the ID of the room
        """
        return self.ID

    def set_id(self, ID: int) -> None:
        """
        Set the room ID. If the ID is not int -> raise
        """
        if type(ID) != int:
            raise Exception("The ID should be int type!")
        else:
            self.ID = ID

    def generate_random_room_id(self) -> int:
        """
        Return the random room ID if there is a wormhole inside the room. If the room doesn't have a wormhole -> raise
        """
        if not self.wormhole:
            raise Exception("The room doesn't have a wormhole!")
        while True:
            random_id = random.randint(1, 25)
            if self.ID != random_id:
                return random_id

    def get_portal(self) -> bool:
        """
        Return a bool value on whether there is a portal in a room
        """
        return self.portal

    def set_portal(self, portal: bool) -> None:
        """
        Set the portal for the room as bool. If more than one state is attempted to be set, and the current room is
        an Exit or Entrance -> raise
        """
        directions = [self.north, self.east, self.west, self.south]
        if "entrance" in directions or "exit" in directions:
            raise Exception("Cannot set portal in the room contain entrance/exit door!")

        elif self.wormhole:
            raise Exception("Cannot set portal in the room contain wormhole!")

        elif self.diamond.get_diamonds() > 0:
            raise Exception("Cannot set portal in the room contain diamonds!")

        self.portal = portal

    def get_wormhole(self) -> bool:
        """
        Return a bool value on whether there is a wormhole in a room
        """
        return self.wormhole

    def set_wormhole(self, wormhole: bool) -> None:
        """
        Set the wormhole for the room as bool. If more than one state is attempted to be set, and the current room is
        an Exit or Entrance -> raise
        """
        directions = [self.north, self.east, self.west, self.south]
        if "entrance" in directions or "exit" in directions:
            raise Exception("Cannot set wormhole in the room contain entrance/exit door!")

        elif self.portal:
            raise Exception("Cannot set wormhole in the room contain portal!")

        elif self.diamond.get_diamonds() > 0:
            raise Exception("Cannot set wormhole in the room contain diamonds!")

        self.wormhole = wormhole

    def get_diamond(self) -> object:
        """
        Return the diamond object
        """
        return self.diamond

    def set_diamond(self, diamond: Diamond) -> None:
        """
        Set the diamond object
        """
        self.diamond = diamond

    def get_door(self, direction: str) -> object:
        """
        Return the door link based on the given direction. If the direction is not in the list -> raise
        """
        if direction.lower() not in ["north", "east", "west", "south"]:
            raise Exception("Invalid direction!")

        else:
            if direction.lower() == "north":
                return self.north
            elif direction.lower() == "east":
                return self.east
            elif direction.lower() == "west":
                return self.west
            elif direction.lower() == "south":
                return self.south

    def set_link(self, direction: str, val) -> None:
        """
        Set the door link to the next room with val based on the given direction. If the val is not the object type
        and not in list, and the direction is also not in the list -> raise
        """

        if not isinstance(val, object) and val not in ["entrance", "exit", None]:
                raise Exception(
                    "Cannot set link because the next room is not an object, 'entrance', 'exit', or None type!")

        elif direction.lower() not in ["north", "east", "west", "south"]:
            raise Exception("Cannot set link because the given direction is not north, east, west, south!")

        else:
            if direction.lower() == "north":
                self.north = val
            elif direction.lower() == "east":
                self.east = val
            elif direction.lower() == "west":
                self.west = val
            elif direction.lower() == "south":
                self.south = val

    def isthere_entrance_exit_door(self) -> bool:
        """
        Return a bool value on whether there is an entrance or exit door inside the room
        """
        return "entrance" in [self.north, self.east, self.west, self.south] or "exit" in [self.north, self.east, self.west, self.south]
