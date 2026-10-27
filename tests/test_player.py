from battleship.player import RandomPlayer

def test_player():
    player = RandomPlayer("Alice")
    print(player.select_target())
    print(player.select_target())
    print(player.select_target())
    
if __name__ == "__main__":
    test_player()