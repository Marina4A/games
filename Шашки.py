class Figure():

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color


class Shashka(Figure):
    def __init__(self, color):
        super().__init__(color)

    def get_color(self):
        return self.color

    def name(self):
        if self.color == 1:
            return 'S'
        else:
            return 's'

    def check_figure(self, A, x0, y0, x, y, color):
        if abs(x - x0) == 1 and abs(y - y0) == 1 and A.square[x][y] == '.':
            return True
        elif x0 - x == 2 and y0 - y == 2 and A.square[x + 1][y + 1] != '.' and A.square[x + 1][y + 1].color != color:
            return True
        elif x0 - x == 2 and y0 - y == -2 and A.square[x + 1][y - 1] != '.' and A.square[x + 1][y - 1].color != color:
            return True
        elif x0 - x == -2 and y0 - y == 2 and A.square[x - 1][y + 1] != '.' and A.square[x - 1][y + 1].color != color:
            return True
        elif x0 - x == -2 and y0 - y == -2 and A.square[x - 1][y - 1] != '.' and A.square[x - 1][y - 1].color != color:
            return True
        return False


class Board():
    def __init__(self):
        # white =  1, black = 0
        self.square = []
        for row in range(8):
            self.square.append(['.'] * 8)
        self.square[0] = ['.', Shashka(1), '.', Shashka(1), '.', Shashka(1), '.', Shashka(1)]
        self.square[1] = [Shashka(1), '.', Shashka(1), '.', Shashka(1), '.', Shashka(1), '.']
        self.square[6] = ['.', Shashka(0), '.', Shashka(0), '.', Shashka(0), '.', Shashka(0)]
        self.square[7] = [Shashka(0), '.', Shashka(0), '.', Shashka(0), '.', Shashka(0), '.']

    def print_figure_name(self, i, j):
        if self.square[i][j] == '.':
            return '.'
        elif self.square[i][j] == '*':
            return '*'
        else:
            return self.square[i][j].name()

    def print_board(self, square):
        print('\n   A B C D E F G H   \n')
        for i in range(8):
            print(str(8 - i), end='  ')
            for j in range(8):
                print(self.print_figure_name(i, j), end=' ')
            print(' ' + str(8 - i))
        print('\n   A B C D E F G H   \n')

    def check_move(self, x0, y0, x, y, color):
        if self.square[x0][y0].check_figure(A, x0, y0, x, y, color):
            return True
        else:
            return False

    def move(self, x0, y0, x, y, color):
        if self.check_move(x0, y0, x, y, color):
            if abs(x-x0) == 2:
                self.square[x][y] = self.square[x0][y0]
                self.square[(x + x0) // 2][(y + y0) // 2] = '.'
                self.square[x0][y0] = '.'
            else:
                self.square[x][y] = self.square[x0][y0]
                self.square[x0][y0] = '.'
            return True
        else:
            raise Exception


def convert_coordinates(s):
    s = s.lower()
    if len(s) == 6 and s[0] in 's' and s[1] in 'abcdefgh' and s[2] in '12345678' \
            and s[4] in 'abcdefgh' and s[5] in '12345678':
        x0 = 8 - int(s[2])
        y0 = s[1]
        x = 8 - int(s[5])
        y = s[4]
    for i in range(8):
        if y0 == 'abcdefgh'[i]:
            y0 = i
            break
    for i in range(8):
        if y == 'abcdefgh'[i]:
            y = i
            break
    return x0, y0, x, y


A = Board()
move = 0
d = {1: 'больших фигур', 0: 'маленьких фигур: '}
while True:
    move_bl_or_wh = move % 2
    A.print_board(A)
    print(f'Ход номер {move + 1}')
    s = input("Введите ход " + d[move_bl_or_wh])
    if s == 'exit':
        print("Конец игры!")
        break
    if len(s) != 6:
        print("Ошибка ввода, попробуйте еще раз!")
        continue
    if convert_coordinates(s) is False:
        print("Ошибка ввода, попробуйте еще раз!")
        continue
    x0, y0, x, y = convert_coordinates(s)

    if A.square[x0][y0].color != move_bl_or_wh:
        print("Выбран не тот цвет фигуры!")
        continue
    try:
        A.move(x0, y0, x, y, move_bl_or_wh)
    except:
        print("Неверный ход для фигуры, введите ход заново!")
        continue
    if abs(x-x0) == 2:
        print("Выберите, бить дальше или передать ход:")
        print("1 - бить дальше, 2 - передать ход")
        n = int(input())
        if n == 1:
            continue
    move += 1
