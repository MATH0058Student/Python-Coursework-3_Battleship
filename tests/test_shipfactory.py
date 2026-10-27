from battleship.ship import ShipFactory
from battleship.board import Board

def test_generate_ships():
    ships_per_length = {1:1, 2:1, 3:1, 4:1, 5:1}
    ship_factory = ShipFactory(ships_per_length=ships_per_length)
    ships = ship_factory.generate_ships()
    print(ships)
    board = Board(ships=ships)
    board.validate_ships() # No ValueError is good news!

if __name__ == "__main__":
    test_generate_ships()