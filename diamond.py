class Diamond:
    """
    This is a simple class to show the number of diamonds for each players.
    """

    def __init__(self, Diamonds: int = 1) -> None:
        """
        Initializes the number of diamonds and it take one arguments: Diamonds
        """
        self.diamonds = Diamonds

    def __str__(self) -> str:
        """
        Return the string representation that shows the number of diamonds
        """
        return f"Number of Diamonds: {self.diamonds}"

    def get_diamonds(self) -> int:
        """
        Return the number of diamonds. Take no argument
        """
        return self.diamonds

    def set_diamonds(self, Diamonds: int) -> None:
        """
        Set the amount of diamonds. Take one argument: Diamonds. Raise if negative
        """
        if Diamonds < 0:
            raise Exception("The number of diamonds cannot be negative!")

        else:
            self.diamonds = Diamonds
