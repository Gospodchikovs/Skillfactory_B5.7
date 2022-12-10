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
from random import random, randint

ROWS = 6            # размер игорового поля
COLUMNS = 6
GAP = 10            # разрыв между отображаемыми полями
ITEM_SHIP = '■'     # в ячейке элемент корабля
ITEM_EMPTY = 'О'    # в ячейке пусто
ITEM_MISS = 'T'     # в ячейке промах
ITEM_SUNK = 'X'     # в ячейке потпленный корабль или его часть


class PlayField:
    __columns = COLUMNS
    __rows = ROWS
    play_field = []
    is_visible = False

    def __init__(self, ships):
        self.play_field = [[ITEM_EMPTY] * self.columns for _ in range(self.rows)]
        for ship in ships:
            for item in range(0, ship.decks):
                self.set_item(ship.get_coordinates()[item*2], ship.get_coordinates()[item*2 + 1], ITEM_SHIP)

    def print_row(self, row, end_string):
        # row == 0 - печатаем заглавнеую строку с номерами столбцов
        if row:
            items = map(lambda item: item if self.visible or item != ITEM_SHIP else ITEM_EMPTY,
                        self.play_field[row - 1])
            print(row, *items, sep=' | ', end=end_string)
        else:
            print(' ', *range(1, self.rows + 1), sep=' | ', end=end_string)

    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns

    @property
    def visible(self):
        return self.is_visible

    @visible.setter                                     # определяет нужно ли показвать корабли на поле
    def visible(self, value):
        self.is_visible = value

    def get_item(self, x, y):
        return self.play_field[y-1][x-1]

    def set_item(self, x, y, value):
        self.play_field[y-1][x-1] = value

    def check(self, x, y):
        return self.get_item(x, y) == ITEM_SHIP


class Ship:
    __coordinates = None                                   # список координат всех палуб корабля

    def __init__(self, coordinates):
        self.__coordinates = coordinates.copy()

    @property
    def decks(self):                                     # количество палуб
        return int(len(self.__coordinates) / 2)

    def get_coordinates(self):                          # получение спискам коорлинат корабля
        return self.__coordinates


def print_fileds(field1, field2):
    print('      Доска человека      ', ' '*GAP, '   Доска компьютера')
    for i in range(field1.rows + 1):
        field1.print_row(i, ' '*GAP)
        field2.print_row(i, '\n')


def human_get_coordinates(field):
    while True:
        coordinates = input(
            '\nВведите координаты хода в формате \'X Y\', где X-столбец, а Y-строка (q - выход): ').split()
        if coordinates[0] == 'q':
            exit(0)
        if len(coordinates) != 2:
            print('Формат ввода не соответствует запрашиваемому \'X Y\'!')
        elif not (coordinates[0].isnumeric() and coordinates[1].isnumeric()):
            print('Необходимо вводить только положительные целые числа!')
        elif not (int(coordinates[0]) in range(1,COLUMNS+1) and int(coordinates[1]) in range(1,ROWS+1)):
            print(f'Необходимо вводить числа в диапазоне от 1 до {COLUMNS} для Х и от 1 до {COLUMNS} для Y!')
        elif field.get_item(int(coordinates[0]), int(coordinates[1])) == ITEM_SUNK or \
                field.get_item(int(coordinates[0]), int(coordinates[1])) == ITEM_MISS:
            print('Такой ход уже был сделан ранее! Попробуйте снова.')
        else:
            return int(coordinates[0]), int(coordinates[1])


def comp_get_coordinates(field):
    while True:
        x = randint(1, COLUMNS)
        y = randint(1, ROWS)
        if field.get_item(x, y) != ITEM_SUNK and field.get_item(x, y) != ITEM_MISS:
            return x, y


def main():
    play_count = None
    human_ships_coordinates = [1, 2, 1, 3, 1, 4], [3, 3, 3, 4], [5, 3, 6, 3], [2, 6], [3, 1], [5, 6], [5, 1]
    comp_ships_coordinates = [1, 2, 2, 2, 3, 2], [1, 4, 1, 5], [6, 5, 6, 6], [3, 6], [6, 3], [4, 4], [5, 1]
    human_ships = []
    comp_ships = []
    for coordinates in human_ships_coordinates:
        human_ships.append(Ship(coordinates))
    for coordinates in comp_ships_coordinates:
        comp_ships.append(Ship(coordinates))
    human_play_field = PlayField(human_ships)
    comp_play_field = PlayField(comp_ships)
    human_play_field.visible = True
    comp_play_field.visible = True
    plays_human = True
    for play_count in reversed(range(ROWS * COLUMNS)):
        print_fileds(human_play_field, comp_play_field)
        if plays_human:
            x, y = human_get_coordinates(comp_play_field)
        else:
            x, y = comp_get_coordinates(human_play_field)
        if plays_human:
            if comp_play_field.check(x, y):
                comp_play_field.set_item(x, y, ITEM_SUNK)
                print('Попадание! Снова Ваш ход.\n')
            else:
                comp_play_field.set_item(x, y, ITEM_MISS)
                plays_human = False
                print('Промах! Мой ход. Нажмите <Enter>', end='')
                input()
        else:
            if human_play_field.check(x, y):
                human_play_field.set_item(x, y, ITEM_SUNK)
                print(f'\n Попадание по координатам {x, y}. Снова мой ход. Нажмите <Enter>', end='')
                input()
            else:
                human_play_field.set_item(x, y, ITEM_MISS)
                plays_human = True
                print(f'\nПромах по координатам {x, y}. Ваш ход!\n')
    if play_count:
        print('Выиграли')
    else:
        print('Ничья!')

if __name__ == '__main__':
    main()
