import datetime


# Белые фигуры имеют большие буквы и цвет 0

def create_file():
    with open('log_game.txt', 'w', encoding='utf-8') as file:
        pass


class ChessBoard:
    def __init__(self):
        self.ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.name_figure = ['P', 'R', 'N', 'B', 'Q', 'K', 'L', 'J']
        self.counter = 1
        self._name_player()
        self.create_board()
        self.print_board()
        create_file()
        self.__step_game()

    def _name_player(self):  # ввод имени игрока
        while True:
            player_first = input('Введите имя игрока, который играет белыми: ')
            player_second = input('Введите имя игрока, который играет черными: ')
            if player_first.isalpha() and player_second.isalpha():
                self.player_first = player_first
                self.player_second = player_second
                return
            else:
                print('Некорректный ввод! Попробуйте еще раз!')
        # player_first = 'Дима'
        # player_second = 'Марина'
        # self.player_first = player_first
        # self.player_second = player_second

    def create_board(self):
        self.coordinate_figure = {}

        for line in (0, 7):
            for element in (0, 7):
                self.coordinate_figure[(line, element)] = Rook((line, element))
            for element in (1, 6):
                self.coordinate_figure[(line, element)] = Knight((line, element))
            for element in (2, 5):
                self.coordinate_figure[(line, element)] = Bishop((line, element))
            self.coordinate_figure[(line, 4)] = King((line, 4))
            self.coordinate_figure[(line, 3)] = Queen((line, 3))
            self.coordinate_figure[(5, 3)] = Lady((5, 3))
            self.coordinate_figure[(5, 4)] = Jack((5, 4))

        for line in (1, 6):
            for element in range(8):
                self.coordinate_figure[(line, element)] = Pawn((line, element))

    def print_board(self):
        result = []
        for lines in range(8):
            res_line = []
            for columns in range(8):
                if (lines, columns) in self.coordinate_figure.keys():
                    res_line.append(self.coordinate_figure[(lines, columns)].name)
                else:
                    res_line.append('.')
            result.append(res_line)

        print('\n   Шахматная доска')
        print('  ', *self.ALPHABET, '  ', '\n')
        count = 1
        for elem in result:
            print(count, '', *elem, '', count)
            count += 1
        print()
        print('  ', *self.ALPHABET, '  ')

    def __step_game(self):
        while True:
            print(f'\nХод №{self.counter // 2 + self.counter % 2}:')
            if self.counter % 2 != 0:
                result_step = input(f'{self.player_first}, введите ход белых через тире: ')
            else:
                result_step = input(f'{self.player_second}, введите ход черных через тире: ')
            if self.__validation(result_step):
                self.__step(result_step, self.counter % 2)

    def __validation(self, step):  # проверка ввода хода игрока
        if len(step) == 5 and ('-' in step) and step.index('-') == 2:
            if step[1].isdigit() and step[-1].isdigit():
                return True
            else:
                return False
        elif len(step) == 6 and ('-' in step) and step.index('-') == 3:
            if step[2].isdigit() and step[-1].isdigit() and (step[0] in self.name_figure) and \
                    ((step[1].upper() and step[-2].upper()) in self.ALPHABET):
                return True
            else:
                return False
        else:
            return False

    def __step(self, step, color):
        str_step = step
        figure = 'P'
        if len(step) == 6:
            figure = str(step[0]).upper()
        step = step[-5:]
        stat_position, finish_position = map(list, step.split('-'))

        stat_position[1], stat_position[0] = self.ALPHABET.index(str(stat_position[0]).upper()), int(
            stat_position[1]) - 1
        finish_position[1], finish_position[0] = self.ALPHABET.index(str(finish_position[0]).upper()), int(
            finish_position[1]) - 1

        if tuple(stat_position) in self.coordinate_figure:
            if self.coordinate_figure[tuple(stat_position)].name.upper() == figure:
                if self.coordinate_figure[tuple(stat_position)].color == color:
                    if finish_position in self.coordinate_figure[tuple(stat_position)].list_of_possible_moves(
                            position_figure=self.coordinate_figure):
                        with open('log_game.txt', 'a', encoding='utf-8') as file:
                            name = self.player_first
                            if color == 0:
                                name = self.player_second
                            text = f'{datetime.datetime.now()}:\t{name}:\t{str_step}\n'
                            file.write(text)
                        self.counter += 1
                        self.coordinate_figure[tuple(finish_position)] = self.coordinate_figure.pop(
                            tuple(stat_position))
                        self.print_board()
                    else:
                        print('Сюда ходить нельзя.')
                else:
                    print('Вы можете ходить только своими фигурами')
            else:
                print('На указанной позиции установлена другая фигура')
        else:
            print('В указанных координатах нет фигуры')


class Figure:
    def __init__(self, position, name='P'):
        self.position = position
        self.name = name.lower()
        self.color = 0
        if position[0] in (0, 1):
            self.name = self.name.upper()
            self.color = 1

    def return_position(self):
        return self.position


class Pawn(Figure):  # пешка
    def __init__(self, position, name='P'):
        super().__init__(position, name)

    def list_of_possible_moves(self, position_figure: dict):
        possible_moves = []
        i, j = self.position
        if self.color == 1:  # ходят черные
            i += 1
            j_left = j - 1
            j_right = j + 1
            if -1 < j_left < 8 and (i - 1, j - 1) in position_figure.keys() and position_figure[
                (i - 1, j - 1)].color == 0:
                possible_moves.append([i, j_left])
            if -1 < j_right < 8 and (i - 1, j + 1) in position_figure.keys() and position_figure[
                (i - 1, j + 1)].color == 0:
                possible_moves.append([i, j_right])

            i, j = self.position
            if i == 1:
                possible_moves.append([i + 1, j])
                possible_moves.append([i + 2, j])
            else:
                possible_moves.append([i + 1, j])
        else:
            i -= 1
            j_left = j - 1
            j_right = j + 1
            if -1 < j_left < 8 and (i + 1, j - 1) in position_figure.keys() and position_figure[
                (i + 1, j - 1)].color == 1:
                possible_moves.append([i, j_left])
            if -1 < j_right < 8 and (i + 1, j + 1) in position_figure.keys() and position_figure[
                (i + 1, j + 1)].color == 1:
                possible_moves.append([i, j_right])

            i, j = self.position
            if i == 6:
                possible_moves.append([i - 1, j])
                possible_moves.append([i - 2, j])
            else:
                possible_moves.append([i - 1, j])

        return possible_moves


class Rook(Figure):  # ладья
    def __init__(self, position, name='R'):
        super().__init__(position, name)

    def list_of_possible_moves(self, position_figure: dict):
        possible_moves = []
        i, j = self.position
        while i > 0:
            i -= 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while j < 7:
            j += 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i < 7:
            i += 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while j > 0:
            j -= 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        return possible_moves


class Knight(Figure):  # конь
    def __init__(self, position, name='N'):
        super().__init__(position, name)

    def list_of_possible_moves(self, position_figure: dict):
        DISPLACEMENTS = [[-2, -1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-2, 1], [-1, -2]]
        possible_moves = []
        for disp in DISPLACEMENTS:
            i, j = self.position
            i += disp[0]
            j += disp[1]
            if -1 < i < 8 and -1 < j < 8:
                if (i, j) not in position_figure.keys():
                    possible_moves.append([i, j])
                else:
                    if self.color != position_figure[(i, j)].color:
                        possible_moves.append([i, j])

        return possible_moves


class Bishop(Figure):  # Слон
    def __init__(self, position, name='B'):
        super().__init__(position, name)

    def list_of_possible_moves(self, position_figure: dict):
        possible_moves = []
        i, j = self.position
        while i > 0 and j > 0:
            i -= 1
            j -= 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i > 0 and j < 7:
            i -= 1
            j += 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i < 7 and j < 7:
            i += 1
            j += 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i < 7 and j > 0:
            i += 1
            j -= 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        return possible_moves


class Queen(Bishop, Rook):  # ферзь
    def __init__(self, position, name='Q'):
        super().__init__(position, name)

    def list_of_possible_moves(self, position_figure: dict):
        possible_moves = []
        i, j = self.position
        while i > 0:
            i -= 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while j < 7:
            j += 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i < 7:
            i += 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while j > 0:
            j -= 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i > 0 and j > 0:
            i -= 1
            j -= 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i > 0 and j < 7:
            i -= 1
            j += 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i < 7 and j < 7:
            i += 1
            j += 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i < 7 and j > 0:
            i += 1
            j -= 1
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        return possible_moves


class King(Figure):  # король
    def __init__(self, position, name='K'):
        super().__init__(position, name)

    def list_of_possible_moves(self, position_figure: dict):
        DISPLACEMENTS = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
        possible_moves = []
        i, j = self.position
        for disp in DISPLACEMENTS:
            i += disp[0]
            j += disp[1]
            if -1 < i < 8 and -1 < j < 8:
                if (i, j) not in position_figure.keys():
                    possible_moves.append([i, j])
                else:
                    if self.color != position_figure[(i, j)].color:
                        possible_moves.append([i, j])
                    else:
                        break
        return possible_moves


class Lady(Figure):  # Новая фигура 1
    def __init__(self, position, name='L'):
        super().__init__(position, name)

    def list_of_possible_moves(self, position_figure: dict):
        possible_moves = []
        i, j = self.position
        while i > 0 and j > 0:
            i -= 2
            j -= 2
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i > 0 and j < 7:
            i -= 2
            j += 2
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i < 7 and j < 7:
            i += 2
            j += 2
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i < 7 and j > 0:
            i += 2
            j -= 2
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        return possible_moves


class Jack(Figure):  # Новая фигура 2
    def __init__(self, position, name='J'):
        super().__init__(position, name)

    def list_of_possible_moves(self, position_figure: dict):
        possible_moves = []
        i, j = self.position
        while i > 0:
            i -= 2
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while j < 7:
            j += 2
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while i < 7:
            i += 2
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        i, j = self.position
        while j > 0:
            j -= 2
            if (i, j) not in position_figure.keys():
                possible_moves.append([i, j])
            else:
                if self.color == position_figure[(i, j)].color:
                    break
                else:
                    possible_moves.append([i, j])

        return possible_moves


chess_board = ChessBoard()
