from battleship.player import RandomPlayer, AutomaticPlayer
from battleship.game import Game

def test_player():
    
    player1 = RandomPlayer("Alice")
    print(player1.select_target())
    print(player1.select_target())
    print(player1.select_target())
    player2 = AutomaticPlayer("Bob")
    print(player2)
    print(player2.select_target())
    
if __name__ == "__main__":
    test_player()