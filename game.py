from diamond import Diamond
from player import Player
from castle import Castle
from room import Room


class Game:
    """
    The Game class represent the game
    """

    def __init__(self) -> None:
        """
        Initialize the game with attributes like castle as a data structure, player, finished as a list to indicate
        whether each player has finished the game or not, and turn as the turn of the game.
        """
        self.castle = Castle()
        self.players = [Player(0), Player(1)]
        self.finished = [False, False]
        self.turn = 0

    def initialize_from_file(self, filename):
        """
        This method is to build all the rooms using appropriate function and passing it contents of the room. Next,
        set the links of all the rooms according to the given text file; after each room's links have been set,
        add them to the castle.
        """
        temp_rooms = {}  # {room_id : room object,...}
        room_doors = []  # [[north, south, east, west],...]

        with open(filename, "r") as file:
            # To create every room objects then add to the dictionary named temp_rooms
            for line in file:
                diamond = Diamond(0)
                portal = False
                wormhole = False
                room_prop = line.split()
                # ['1:', '0,', '21,', '2,', '0,'] = [room_id, North, South, East, West]

                try:
                    # To get the room_id in each lines
                    room_id = int(room_prop[0].split(":")[0])

                except:
                    # For the exit and entrance id cases
                    if room_prop[0][0] == "E":
                        self.castle.entrance_id = int(room_prop[1][:-1])
                        for player in self.players:
                            # Set the initial location of the player
                            player.location = int(room_prop[1][:-1])
                    else:
                        self.castle.exit_id = int(room_prop[1][:-1])

                else:
                    # For other cases (with room_id):
                    if len(room_prop) > 5:

                        # To set the type of the room
                        room_type = room_prop[-1]
                        if room_type == "P":
                            portal = True
                        elif room_type == "W":
                            wormhole = True
                        else:
                            diamond.set_diamonds(len(room_type))

                    north_door = room_prop[1][:-1]
                    south_door = room_prop[2][:-1]
                    east_door = room_prop[3][:-1]
                    west_door = room_prop[4][:-1]

                    temp_rooms[room_id] = self.build_room(room_id, diamond, portal, wormhole)
                    room_doors.append([north_door, south_door, east_door, west_door])

        # To link every room objects together
        for room_id, directions in enumerate(room_doors):
            str_directions_list = ["north", "south", "east", "west"]
            directions_list = [directions[0], directions[1], directions[2], directions[3]]

            for i, direction in enumerate(directions_list):
                # The for loop is to go through every direction and set their link. I use room_id + 1 because I want
                # my room_id keys in temp_rooms dictionary to start with 1
                if direction == "E":
                    temp_rooms[room_id + 1].set_link(str_directions_list[i], "entrance")

                elif direction == "X":
                    temp_rooms[room_id + 1].set_link(str_directions_list[i], "exit")

                elif int(direction) == 0:
                    temp_rooms[room_id + 1].set_link(str_directions_list[i], None)

                else:
                    temp_rooms[room_id + 1].set_link(str_directions_list[i], temp_rooms[int(direction)])

        for room_context in temp_rooms.values():
            # To add every room objects in the castle class
            self.castle.add_room(room_context)

    def get_turn(self):
        """
        Return the game turn.
        """
        return self.turn

    def set_turn(self, turn):
        """
        Set the game turn.
        """
        self.turn = turn

    def get_player(self, player_id):
        """
        Return the player object based on player id
        """
        return self.players[player_id]

    def build_room(self, room_id, diamond, portal, wormhole):
        """
        Return a room object and decide if this room has diamond or wormhole or portal.
        """
        room = Room(diamond=diamond)
        room.set_id(room_id)

        if diamond.get_diamonds() > 0:
            room.set_diamond(diamond)
            return room

        elif portal:
            room.set_portal(portal)
            return room

        elif wormhole:
            room.set_wormhole(wormhole)
            return room

        else:
            return room

    def move(self):
        """
        Asks the user to enter a decision (East, West, North, South) and move the player whose turn it is
        """
        direction = input("Please input a direction (North, South, East, West): ").lower()

        while direction not in ['north', 'south', 'east', 'west']:
            direction = input("Invalid input! Please enter a correct direction again: ").lower()

        try:
            current_player = self.players[self.get_turn()]
            current_room_id = current_player.get_position()
            next_room = self.castle.get_next_room(current_room_id, direction)

            print(f"Player {self.get_turn() + 1}, previous room {current_room_id}")

            current_player.set_position(next_room.get_id())

        except:
            if next_room == 'entrance':
                print("It's the entrance")

            elif next_room == "exit":
                print(f"Player {self.get_turn() + 1} exited the castle! {direction}")
                self.finished[self.get_turn()] = True
                current_player.add_to_path(current_room_id, direction)

            elif next_room == None:
                print("The door is blocked")

        else:

            if next_room.diamond.get_diamonds() > 0:
                print(f"{next_room.get_diamond()} ", end="")
                self.update_diamonds()
                print(f"TOTAL: {current_player.get_diamonds()}")

            elif self.castle.rooms[current_room_id].get_door(direction).get_portal():
                print("You entered a portal")

            elif self.castle.rooms[current_room_id].get_door(direction).get_wormhole():
                print("Wormhole devoured you")

                # If wormhole to the room that contain the portal -> the player will go back the entrance!
                if next_room.get_portal():
                    print("You entered a portal")
                    next_room = self.castle.rooms[self.castle.get_entrance_id()]

            print(f"Player {self.get_turn() + 1}, {direction}, New room {next_room.get_id()}")

            current_player.add_to_path(current_room_id, direction)


    def is_finished(self):
        """
        Return whether the game is finished or not. The game will be finished when both of the players exit from the
        castle. If it's finished, print the path both players traveled so far.
        """
        if self.finished == [True, True]:
            print("The game is finished!")
            for i in range(len(self.players)):
                self.players[i].print_path()
            return True
        return False

    def update_diamonds(self):
        """
        Updates the number of diamonds the player has based on the current position of the player and set the number
        of diamonds to zero after visiting the room containing diamonds
        """
        current_player = self.players[self.get_turn()]
        player_diamond = current_player.diamond.get_diamonds()
        current_room_id = current_player.get_position()
        diamonds_count = self.castle.rooms[current_room_id].diamond.get_diamonds()

        if diamonds_count > 0:
            # Set the diamond for the current player first and then set the room that contain diamond to 0.
            current_player.set_diamonds(player_diamond + diamonds_count)
            self.castle.rooms[current_room_id].diamond.set_diamonds(0)
