from battleship.ship import Ship

def test_horizontal():
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    output = ship.is_horizontal()
    print(output)
    assert output == True


if __name__ == "__main__":
    test_horizontal()