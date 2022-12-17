from sea_battle import Dot, Ship, Board

def test_dot():
    coordinates = Dot(10,20)
    assert coordinates == [10,20]
    assert coordinates.x == 10
    assert coordinates.y == 20
    assert coordinates.xy == Dot(10,20)

def test_ship():
    ship = Ship(Dot(1,2), 3, True)
    assert ship.length == 3
    assert ship.number_life == 3
    ship.number_life -= 1
    assert ship.number_life == 2
    ship.not_sunked_ships = 10
    assert ship.not_sunked_ships == 10

def test_board():
    board = Board()
    board.visible = True
    assert board.visible
    assert not board.out(Dot(1,2))
    assert board.out(Dot(0, 0))
    assert board.out(Dot(7, 1))
    assert board.out(Dot(1, 7))
    assert board.out(Dot(7, 7))
    s1 = Ship(Dot(1, 2), 2, False)
    s2 = Ship(Dot(1, 3), 2, False)
    assert board.add_ship(s1)
    assert not board.add_ship(s2)
    assert board.shot(Dot(1, 2))
    assert not board.shot(Dot(1, 2))
    assert  not board.shot(Dot(1, 1))
    assert board.not_sunked_ships == 1
    assert board.shot(Dot(1, 3))
    assert board.not_sunked_ships == 0


if __name__ == '__main__':
    unittest.main()
