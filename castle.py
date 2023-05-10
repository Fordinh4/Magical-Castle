from room import Room


class Castle:
    """
    The Castle class have a data structure containing the room objects (the graph of rooms)
    """

    def __init__(self) -> None:
        """
        Initialize the data structure with room objects
        """
        self.rooms = {}  # {room_id : Room_Object}
        self.entrance_id = None
        self.exit_id = None

    def add_room(self, room) -> None:
        """ 
        Adding a given room to the current data structure. If room already exist -> raise        
        """
        if room.get_id() in self.rooms:
            raise Exception("The given room is already exist in the castle!")

        self.rooms[room.get_id()] = room

    def get_room(self, id) -> object:
        """
        Returning a specific room with a given ID. If the room not in Castle -> raise
        """
        try:
            room = self.rooms[id]
        except:
            raise Exception("The given room is not inside the castle!")
        return room

    def get_entrance_id(self) -> int:
        """
        Return the ID of the room with the entrance door
        """
        return self.entrance_id

    def get_ext_id(self) -> int:
        """
        Return the ID of the room with the exit door
        """
        return self.exit_id

    def get_next_room(self, room_id, door) -> object:
        """
        Return the ID of the next room based on the given direction of the door
        """
        # It receives room id and a door (news) and return another room id which is going to be the room behind that
        # door.
        next_room = self.rooms[room_id].get_door(door)

        if type(next_room) != str:
            if next_room is None:
                # If the next room is None - blocked door, return None
                return None

            elif next_room.isthere_entrance_exit_door():
                # If the next room contain entrance/exit -> return the "entrance"/"exit"
                return next_room

            elif next_room.get_portal():
                # If the next room contain the portal, return the entrance_id
                return self.rooms[self.get_entrance_id()]

            elif next_room.get_wormhole():
                # If the next room have a wormhole -> generate the random id, and check that new room with the
                # random id have the wormhole or not. If yes, while loop until it's not
                while True:
                    random_id = next_room.generate_random_room_id()
                    if not self.rooms[random_id].get_wormhole():
                        return self.rooms[random_id]
            else:
                # Return the room behind given door
                return next_room
        else:
            # For entrance case
            return next_room
