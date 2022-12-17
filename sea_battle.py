# Используя знания, полученные в данном модуле напишите следующее приложение: игру «Морской бой».
#
# Интерфейс приложения должен представлять из себя консольное окно с двумя полями 6х6.
# Игрок играет с компьютером. Компьютер делает ходы наугад, но не ходит по тем клеткам, в которые он уже сходил.
# Для представления корабля опишите класс Ship с конструктором принимающим в себя набор точек (координат) на
# игровой доске.
# Опишите класс доски. Доска должна принимать в конструкторе набор кораблей.
# Корабли должны находится на расстоянии минимум одна клетка друг от друга.
# Корабли на доске должны отображаться следующим образом (пример):
#
#   | 1 | 2 | 3 | 4 | 5 | 6 |
# 1 | X | X | X | О | О | О |
# 2 | О | О | О | X | X | О |
# 3 | О | T | О | О | О | О |
# 4 | ■ | О | ■ | О | ■ | О |
# 5 | О | О | О | О | ■ | О |
# 6 | ■ | О | ■ | О | О | О |
#
# На каждой доске (у ИИ и у игрока) должно находится следующее количество кораблей:
# 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку.
# Запретите игроку стрелять в одну и ту же клетку несколько раз. При ошибках хода игрока должно возникать исключение.
#
# В случае, если возникают непредвиденные ситуации, выбрасывать и обрабатывать исключения.
# Буквой X помечаются подбитые корабли, буквой T — промахи.
# Побеждает тот, кто быстрее всех разгромит корабли противника.
from random import randint

ROWS = 6            # размер игорового поля
COLUMNS = 6
GAP = 10            # разрыв между отображаемыми полями
ITEM_SHIP = '■'     # в ячейке элемент корабля
ITEM_EMPTY = 'О'    # в ячейке пусто
ITEM_MISS = 'T'     # в ячейке промах
ITEM_SUNK = 'X'     # в ячейке потпленный корабль или его часть


class GameExeptions:
    def board_out_exception(self):
        pass

class Dot:
    def __init__(self,  x=0, y=0):
        self.__x = x
        self.__y = y

    def __eq__(self, coordinates):
        a = self.__x == coordinates.x
        b = self.__y == coordinates.y
        return a and b

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y


class Ship:
    def __init__(self, coordinates_bow = None, length = 0, orientation_is_horizontal = True):
        self.__coordinates_bow = coordinates_bow                                # координаты носа корабля
        self.__orientation_is_horizontal = orientation_is_horizontal            # ориентация горизонтальная/вертикальная
        self.__length = length                                                  # длина корабля
        self.__number_life = length                                             # число оставшихя жизней
        self.__coordinates = []                                                 # список координат корабля
        for i in range(length):
            x = coordinates_bow.x + i*int(self.__orientation_is_horizontal)
            y = coordinates_bow.y + i*int(not self.__orientation_is_horizontal)
            self.__coordinates.append(Dot(x, y))

    @property
    def dots(self):                                                             # получение спискам коорлинат корабля
        return self.__coordinates

    @property
    def number_life(self):
        return self.__number_life

    @number_life.setter
    def number_life(self, value):
        self.__number_life = value

class Board:
    def __init__(self, is_visible = False):
        self.__play_field = [[ITEM_EMPTY] * COLUMNS for _ in range(ROWS)]
        self.__ships = []
        self.__hid = not is_visible
        self.__not_sunked_ships = 0

    def add_ship(self, ship):
        for ship_coordinates in self.contour(ship):                 # проверяем контур, точки за границей сюда не входят
            if self.get_item(ship_coordinates) == ITEM_SHIP:
                return False
        for ship_coordinates in ship.dots:                          # проверяем сам корабль на выход за границы
            if self.out(ship_coordinates):
                return False
        for ship_coordinates in ship.dots:
            self.set_item(ship_coordinates, ITEM_SHIP)              # добавляем точки на доску
        self.__ships.append(ship)
        self.__not_sunked_ships += 1
        return True

    def contour(self, ship):                        # список точек корабля вместе с контуром
        contour = []
        for ship_coordinates in ship.dots:
            for delta_x in range(-1,2):
                for delta_y in range (-1,2):
                    x = ship_coordinates.x + delta_x
                    y = ship_coordinates.y + delta_y
                    if not self.out(Dot(x,y)):
                        contour.append(Dot(x,y))
        return contour

    def clear(self):
        for i in range(ROWS):
            for j in range(COLUMNS):
                self.set_item(Dot(i+1, j+1), ITEM_EMPTY)
        self.__not_sunked_ships = 0
        self.__ships = []

    def out(self, coordinates):
        return not (coordinates.x in range(1, COLUMNS+1) and coordinates.y in range(1, ROWS))

    def shot(self, shot_coordinates):
        item = self.get_item(shot_coordinates)
        if item == ITEM_SHIP:
            self.set_item(shot_coordinates, ITEM_SUNK)
            for ship in self.__ships:
                for coordinates in ship.dots:
                    if coordinates == shot_coordinates:
                        ship.number_life -= 1
                        if not ship.number_life:
                            self.__not_sunked_ships -= 1
            return True                                         # попадание по кораблю
        else:
            self.set_item(shot_coordinates, ITEM_MISS)
            return False                                        # нет попадания по кораблю

    def check(self, coordinates):                               # проверка точки лоски на повторное попалание
        item = self.get_item(coordinates)
        return item != ITEM_SUNK and item != ITEM_MISS

    @property
    def not_sunked_ships(self):
        return self.__not_sunked_ships

    def print_row(self, row, end_string):
        # выводим строку доски в консоль
        # row == 0 - печатаем заглавнеую строку с номерами столбцов
        if row:
            items = map(lambda item: item if not self.__hid or item != ITEM_SHIP else ITEM_EMPTY,
                        self.__play_field[row - 1])
            print(row, *items, sep=' | ', end=end_string)
        else:
            print(' ', *range(1, ROWS + 1), sep=' | ', end=end_string)

    def show(self):
        for i in range(ROWS + 1):
            self.print_row(i, '\n')

    def get_item(self, coordinates):
        return self.__play_field[coordinates.y-1][coordinates.x-1]

    def set_item(self, coordinates, value):
        self.__play_field[coordinates.y-1][coordinates.x-1] = value

class Player:
    def __init__(self, board_self, board_opponent):
        self.__board_self = board_self
        self.__board_opponent = board_opponent

    def ask(self):
        pass

    def check(self, coordinates):
        return self.__board_opponent.check(coordinates)

    def move(self):
        coordinates = self.ask()
        return self.__board_opponent.shot(coordinates)

class User(Player):
    def ask(self):
        while True:
            coordinates = input(
                '\nВведите координаты хода в формате \'X Y\', где X-столбец, а Y-строка (q - выход): ').split()
            if len(coordinates) and coordinates[0] == 'q':
                exit(0)
            if len(coordinates) != 2:
                print('Формат ввода не соответствует запрашиваемому \'X Y\'!')
            elif not (coordinates[0].isnumeric() and coordinates[1].isnumeric()):
                print('Необходимо вводить только положительные целые числа!')
            elif not (int(coordinates[0]) in range(1, COLUMNS + 1) and int(coordinates[1]) in range(1, ROWS + 1)):
                print(f'Необходимо вводить числа в диапазоне от 1 до {COLUMNS} для Х и от 1 до {COLUMNS} для Y!')
            elif not self.check(Dot(int(coordinates[0]), int(coordinates[1]))):
                print('Такой ход уже был сделан ранее! Попробуйте снова.')
            else:
                return Dot(int(coordinates[0]), int(coordinates[1]))


class Ai(Player):
    def ask(self):
        while True:
            x = randint(1, COLUMNS)
            y = randint(1, ROWS)
            if self.check(Dot(x,y)):
                return Dot(x, y)

class Game:
    def __init__(self):
        self.__board_human = Board(True)
        self.__board_ai = Board(True)
        self.__human = User(self.__board_human, self.__board_ai)
        self.__ai = Ai(self.__board_ai, self.__board_human)

    def random_board_human(self):
        return self.random_board(self.__board_human)

    def random_board_ai(self):
        return  self.random_board(self.__board_ai)

    def random_board(self, board):
        board.clear()
        ships_total = [(3,1),(2,2),(1,4)]               # сколько и каких кораблей генерируем
        for ships in ships_total:
            for _ in range(ships[1]):
                for attempt_counter in reversed(range(10000)):
                    coordinates_bow = Dot(randint(1, COLUMNS), randint(1, ROWS))
                    number_life = ships[0]
                    orientation = bool(randint(0,1))
                    if board.add_ship(Ship(coordinates_bow, number_life, orientation)):
                        break
                if not attempt_counter:
                    return False                        # неудачная попытка
        return True                                     # все корабли расставлены

    def show_boards(self):
        count_human = self.__board_human.not_sunked_ships
        count_ai = self.__board_ai.not_sunked_ships
        print('Осталось потопить - ', count_human, ' ' * GAP, ' Осталось потопить - ', count_ai)
        for i in range(ROWS + 1):
                self.__board_human.print_row(i, ' ' * GAP)
                self.__board_ai.print_row(i, '\n')

    def greet(self):
        print('Игра "Морской бой". Для хода необходимо вводить координаты в виде \'X Y\', где X-столбец, а Y-строка\n')

    def loop(self):
        plays_human = True
        while True:
            if plays_human:
                if self.__human.move():
                    print('Попадание! Снова Ваш ход.\n')
                else:
                    plays_human = False
                    print('Промах! Мой ход. Нажмите <Enter>', end='')
                    input()
                    print('')
            else:
                if self.__ai.move():
                    print(f'\n Попадание! Снова мой ход. Нажмите <Enter>', end='')
                    input()
                    print('')
                else:
                    plays_human = True
                    print(f'\nПромах! Ваш ход!\n')
            self.show_boards()
            if not (self.__board_human.not_sunked_ships and self.__board_ai.not_sunked_ships):
                break
        if plays_human:
            print('Вы выиграли!')
        else:
            print('Я выиграл!')

    def start(self):
        while not self.random_board_human():
            pass
        while not self.random_board_ai():
            pass
        self.greet()
        self.show_boards()
        self.loop()

def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
