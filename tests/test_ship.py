from battleship.ship import Ship, ShipFactory

def test_horizontal():
    start = (4, 5)
    end = (2, 5)
    ship = Ship(start=start, end=end)
    output = ship.is_horizontal()
    print(output)
    assert output == True
    cells = ship.get_cells()
    print(cells)
    print(len(cells))
    shipfactory = ShipFactory()
    print(shipfactory.generate_ships())


if __name__ == "__main__":
    test_horizontal()