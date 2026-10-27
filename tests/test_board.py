from battleship.board import Board
from battleship.ship import Ship

def test_board():
    ships = [
        Ship(start=(3, 1), end=(3, 5)),  # length = 5
        Ship(start=(9, 7), end=(9, 10)), # length = 4
        Ship(start=(1, 9), end=(3, 9)),  # length = 3
        Ship(start=(5, 2), end=(6, 2)),  # length = 2
        Ship(start=(8, 3), end=(8, 3)),  # length = 1
    ]
    
    board = Board(ships=ships)
    print(board.ships)
    is_ship_hit, has_ship_sunk = board.is_attacked_at((3, 4))
    print(is_ship_hit, has_ship_sunk)
    assert is_ship_hit == True
    assert has_ship_sunk == False


if __name__ == "__main__":
    test_board()