from sea_battle import Dot, Ship, Board, GameAddShipException, GameShotIsRepeated, GameOutCoordinatesException


def test_dot():
    coordinates = Dot(10,20)
    assert coordinates == Dot(10,20)
    assert coordinates.x == 10
    assert coordinates.y == 20


def test_ship():
    ship = Ship(Dot(1, 2), 3, True)
    ship.number_life -= 1
    assert ship.number_life == 2
    xy = ship.dots
    xy_test = [Dot(1, 2), Dot(2, 2), Dot(3, 2)]
    for i in range(len(xy)):
        assert xy[i] == xy_test[i]
    ship.not_sunked_ships = 10
    assert ship.not_sunked_ships == 10


def test_board():
    board = Board()
    board.visible = True
    assert board.visible
    assert not board.out(Dot(6, 6))
    assert board.out(Dot(0, 0))
    assert board.out(Dot(7, 1))
    assert board.out(Dot(1, 7))
    assert board.out(Dot(7, 7))
    s1 = Ship(Dot(1, 2), 2, False)
    s2 = Ship(Dot(1, 3), 2, False)
    assert board.add_ship(s1)
    try:
        assert not board.add_ship(s2)
    except GameAddShipException:
        pass
    assert board.shot(Dot(1, 2))
    try:
        assert not board.shot(Dot(1, 2))
        assert not board.shot(Dot(1, 1))
    except GameShotIsRepeated:
        pass
    except GameOutCoordinatesException:
        pass
    assert board.not_sunked_ships == 1
    assert board.check(Dot(1, 3))
    assert board.shot(Dot(1, 3))
    assert not board.check(Dot(1, 3))
    assert not board.check(Dot(1, 3))
    assert board.not_sunked_ships == 0
    s3 = Ship(Dot(4, 4), 1, True)
    assert board.add_ship(s3)
    xy = board.contour(s3)
    xy_test = [Dot(3, 3), Dot(3, 4), Dot(3, 5), Dot(4, 3), Dot(4, 4), Dot(4, 5), Dot(5, 3), Dot(5, 4), Dot(5, 5)]
    for i in range(len(xy)):
        assert xy[i] == xy_test[i]
    board.clear()
    assert board.not_sunked_ships == 0
    board.set_item(Dot(6, 6), '!')
    assert board.get_item(Dot(6, 6)) == '!'

