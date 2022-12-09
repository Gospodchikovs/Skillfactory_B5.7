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

ROWS = 6            # размер игорового поля
COLUMNS = 6
GAP = 10            # разрыв между отображаемыми полями
SHIP_DECK = '■'     # обозгачние елемента корабля


class PlayField:
    __columns = COLUMNS
    __rows = ROWS
    play_field = []
    is_visible = False

    def __init__(self):
        self.play_field = [['О'] * self.__columns for _ in range(self.__rows)]

    def print_row(self, row, end_string):
        # row == 0 - печатаем заглавнеую строку с номерами столбцов
        if row:
            items = map(lambda item: item if self.visible or item != SHIP_DECK else 'О', self.play_field[row-1])
            print(row, *items, sep=' | ', end=end_string)
        else:
            print(' ', *range(1, self.__rows + 1), sep=' | ', end=end_string)

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


class Ship:
    coordinates = []                                   # список координат всех палуб корабля

    def __init__(self, coordinates):
        self.coordinates = coordinates

    @property
    def deks(self):                                     # количество палуб
        return len(self.coordinates)


def print_fileds(field1, field2):
    print('      Доска человека      ',' '*GAP,'   Доска компьютера')
    for i in range(field1.rows + 1):
        field1.print_row(i, ' '*GAP)
        field2.print_row(i, '\n')


def main():
    human_play_field = PlayField()
    comp_play_field = PlayField()
    human_play_field.play_field[2][2] = SHIP_DECK
    human_play_field.visible = True
    print_fileds(human_play_field, comp_play_field)


if __name__ == '__main__':
    main()
