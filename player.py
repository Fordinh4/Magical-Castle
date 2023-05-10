from diamond import Diamond
from castle import Castle


class Player:
    """
    The Player class represent a player who have ID, the amount of diamonds, nested list of path history as a data
    structure, and their current location.
    """

    def __init__(self, player_id) -> None:
        """
        Initialize a player with its property
        """
        self.player_id = player_id  # Can be 0 or 1
        self.diamond = Diamond(0)
        self.path_history = []  # [[room_id, door_id],...]
        self.location = None  # Initial location of the player is at the entrance

    def __str__(self) -> str:
        """
        Return the diamond count of a player
        """
        return f"Player {self.get_player_id()}. Diamond count: {self.get_diamonds()}"

    def get_position(self) -> int:
        """
        Returning a player's location
        """
        return self.location

    def set_position(self, id) -> None:
        """
        Set a player's location
        """
        # id = room_id
        if id > 25:
            raise Exception("ID is out of range 25!")
        self.location = id

    def get_player_id(self) -> int:
        """
        Return a player's ID
        """
        return self.player_id

    def get_diamonds(self) -> int:
        """
        Return a player's amount of diamonds
        """
        return self.diamond.get_diamonds()

    def set_diamonds(self, count) -> None:
        """
        Set a player's amount of diamond
        """
        self.diamond.set_diamonds(count)

    def print_path(self) -> None:
        """
        Print a history of player's path
        """
        temp_str = ""
        for location in self.path_history:
            temp_str += f"{location[0]} -> {location[1]}, "
        print(temp_str[:-2])

    def add_to_path(self, room_id, door_id) -> None:
        """
        Updating the history of a player's path
        """
        self.path_history.append([room_id, door_id])
