import random

from battleship.board import Board
from battleship.convert import CellConverter

class Player:
    """ Class representing the player
    """
    count = 0  # for keeping track of number of players

    def __init__(self, board=None, name=None):
        """ Initialises a new player with its board.

        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """

        if board is None:
            self.board = Board()
        else:
            self.board = board

        Player.count += 1
        if name is None:
            self.name = f"Player {self.count}"
        else:
            self.name = name

    def __str__(self):
        return self.name

    def select_target(self):
        """ Select target coordinates to attack.

        Abstract method that should be implemented by any subclasses of Player.

        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the
                next attack
        """
        raise NotImplementedError

    def receive_opponent_ships_per_length(self, opponent_ships_per_length=None):
        """ Receive opponent's ship per length.

        Player receives information about the number of ships for each length.
        This method is expected to be invoked once before the start of a game.

        This method does not do anything by default, but can be overridden by a
        subclass to do something useful, for example remembering how many ships
        the opponent is expected to have per ship length on their board to make
        informed decisions.

        Args:
            opponent_ships_per_length (dict): The ships_per_length attribute of
                the opponent's board. See the Board class for details.

        Returns:
            None
        """
        return None

    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.

        Player receives notification on the outcome of the latest attack by the
        player, on whether the opponent's ship is hit, and whether it has been
        sunk.

        This method does not do anything by default, but can be overridden by a
        subclass to do something useful, for example to record a successful or
        failed attack.

        Args:
            is_ship_hit (bool): Is opponent's ship hit?
            has_ship_sunk (bool): Has the opponent's ship been sunk?

        Returns:
            None
        """
        return None

    def has_lost(self):
        """ Check whether player has lost the game.

        Returns:
            bool: True if and only if all the ships of the player have sunk.
        """
        return self.board.have_all_ships_sunk()


class ManualPlayer(Player):
    """ A player playing manually via the terminal
    """
    def __init__(self, board, name=None):
        """ Initialise the player with a board and other attributes.

        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        super().__init__(board=board, name=name)
        self.converter = CellConverter((board.width, board.height))

    def select_target(self):
        """ Read coordinates from user prompt.

        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the
                next attack
        """
        print(f"It is now {self}'s turn.")

        while True:
            try:
                coord_str = input('coordinates target = ')
                x, y = self.converter.from_str(coord_str)
                return x, y
            except ValueError as error:
                print(error)


class RandomPlayer(Player):
    """ A Player that plays at random positions.

    However, it does not play at the positions:
    - that it has previously attacked
    """
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.

        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        self.tracker = set()

    def select_target(self):
        """ Generate a random cell that has previously not been attacked.

        Also adds cell to the player's tracker.

        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the
                next attack
        """
        target_cell = self.generate_random_target()
        self.tracker.add(target_cell)
        return target_cell

    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked.

        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the
                next attack
        """
        has_been_attacked = True
        random_cell = None

        while has_been_attacked:
            random_cell = self.get_random_coordinates()
            has_been_attacked = random_cell in self.tracker

        return random_cell

    def get_random_coordinates(self):
        """ Generate random coordinates.

        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)


class AutomaticPlayer(Player):
    """ Player playing automatically using a strategy."""
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.

        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)

        # TODO: Add any other attributes necessary for your strategic player
        self.opponent_ships_per_length = None
        self.result = None
        self.available_cells = {(x,y) : None for x in range(1, self.board.width + 1)
                                             for y in range(1, self.board.height + 1)}
        self.hitted_ship_cells = []  # stack: first in, last out


    def receive_opponent_ships_per_length(self, opponent_ships_per_length=None):
        """ Receive opponent's ship per length.

        Player receives information about the number of ships for each length.
        This method is expected to be invoked once before the start of a game.

        Args:
            opponent_ships_per_length (dict): The ships_per_length attribute of
                the opponent's board. See the Board class for details.

        Returns:
            dict: The ships_per_length attribute of the opponent's board.
        """
        self.opponent_ships_per_length = opponent_ships_per_length
        return self.opponent_ships_per_length

    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.

        Player receives notification on the outcome of the latest attack by the
        player, on whether the opponent's ship is hit, and whether it has been
        sunk.

        Args:
            is_ship_hit (bool): Is opponent's ship hit?
            has_ship_sunk (bool): Has the opponent's ship been sunk?

        Returns:
            tuple[bool, bool]: (is_ship_hit, has_ship_sunk)
        """
        self.result = (is_ship_hit, has_ship_sunk)
        return self.result

    def get_random_coordinates(self):
        """ Generate random coordinates.

        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)

    def hit_along_ship(self, orientation):
        """ Hit along the ship based on the orientation of the ship.

        Args:
            orientation (str): The orientation of the ship ('vertical' or 'horizontal').

        Returns:
            tuple[int, int]: (x, y) cell coordinates at which to launch the
                next attack
        """
        orientation_to_index = {'vertical': 1, 'horizontal': 0}
        index = orientation_to_index[orientation]
        tail = list(min(self.hitted_ship_cells, key=lambda cell:cell[index]))
        head = list(max(self.hitted_ship_cells, key=lambda cell:cell[index]))
        tail[index] -= 1
        head[index] += 1
        target_cell = random.choice([tail, head])  # Explore from one end randomly
        return tuple(target_cell)


    def run_hit_strategy(self, cell):
        """ Run a strategy to attack the opponent's ships after a successful hit.

        Args:
            cell (tuple[int, int]): (x, y) cell coordinates that were hit.

        Returns:
            tuple[int, int]: (x, y) cell coordinates at which to launch the
                next attack
        """
        x, y = cell
        target_cell = None
        orientation = None

        if len(self.hitted_ship_cells) <= 1:  # Explore adjacent cells
            while target_cell is None:
                adjacent_cell = random.choice([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
                # Judge if adjacent_cell is on board and if it is already occpied
                if self.available_cells.get(adjacent_cell, 'off board') is None:
                    target_cell = adjacent_cell
                    return target_cell
                
        # If you get here, now len(self.hitted_ship_cells)>=2
        # Judge orientation
        if self.hitted_ship_cells[0][0] == self.hitted_ship_cells[1][0]:
            orientation = 'vertical'
        else:
            orientation = 'horizontal'
        
        while (target_cell is None) or \
              (self.available_cells.get(target_cell, 'off board') is not None):
            target_cell = self.hit_along_ship(orientation)

        return target_cell

    def update_cells_around_sunk_ship(self, sunk_ship_cells):
        """ Update the available cells around a sunk ship to avoid attacking them.

        Args:
            sunk_ship_cells (list[tuple[int, int]]): List of (x, y) cell 
            coordinates of the sunk ship.

        Returns:
            None
        """
        for cell in sunk_ship_cells:
            x, y = cell
            # Mark the cells around the sunk ship as unavailable
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    adjacent_cell = (x + dx, y + dy)
                    if adjacent_cell in self.available_cells:
                        self.available_cells[adjacent_cell] = (False, False)
        return None


    def select_target(self):
        """ Select target coordinates to attack.

        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the
                next attack
        """
        # TODO: Complete this method
        target_cell = None

        if self.result is not None:
            self.available_cells[self.hitted_ship_cells[-1]] = self.result
            is_ship_hit, has_ship_sunk = self.result
            if is_ship_hit and not has_ship_sunk:
                target_cell = self.run_hit_strategy(self.hitted_ship_cells[-1])
            elif is_ship_hit and has_ship_sunk:
                self.update_cells_around_sunk_ship(self.hitted_ship_cells)
                self.hitted_ship_cells.clear()
            else:  # Missed
                self.hitted_ship_cells.pop()
                if self.hitted_ship_cells:  # We hitted last round, but missed now
                    target_cell = self.run_hit_strategy(self.hitted_ship_cells[-1])
                    
        # If there is no information, choose random strategy
        while (target_cell is None) or \
              (self.available_cells.get(target_cell, 'off board') is not None):
            target_cell = self.get_random_coordinates()

        self.hitted_ship_cells.append(target_cell)  # Chambering
        return target_cell  # Fire!
