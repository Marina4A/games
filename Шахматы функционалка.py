import os

ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
change_black = {1: 'r', 2: 'n', 3: 'b', 4: 'q'}
change_white = {1: 'R', 2: 'N', 3: 'B', 4: 'Q'}
COORDINATE = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
white_pawn = {}
black_pawn = {}
WHITE = 0
BLACK = 1
flag = False


def print_matrix():  # печать шахматной доски
    print('\n   Шахматная доска')
    print('  ', *ALPHABET, '  ', '\n')
    count = 8
    for elem in matrix:
        print(count, '', *elem, '', count)
        count -= 1
    print()
    print('  ', *ALPHABET, '  ')


matrix = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
          ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
          ['.', '.', '.', '.', '.', '.', '.', '.'],
          ['.', '.', '.', '.', '.', '.', '.', '.'],
          ['.', '.', '.', '.', '.', '.', '.', '.'],
          ['.', '.', '.', '.', '.', '.', '.', '.'],
          ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
          ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]


def change_figure(position, current_color):
    i, j = position
    while True:
        print('Фигуры, на которые можно заменить пешку:'
              '\n1 - Ладья'
              '\n2 - Слон'
              '\n3 - Конь'
              '\n4 - Ферзь')
        name_figure = input('\nВведите номер фигуры: ')
        if name_figure.isdigit() and 0 < int(name_figure) < 5:
            if current_color:
                matrix[i][j] = change_black[int(name_figure)]
                break
            else:
                matrix[i][j] = change_white[int(name_figure)]
                break
        else:
            print('Некорректный ввод! Попробуйте еще раз!\n')


def shah(coordinate, current_color):
    for i, j in coordinate:
        if matrix[i][j] == 'K' and current_color == 1:
            return True
        elif matrix[i][j] == 'k' and current_color == 0:
            return True
    else:
        return False


def check_step(moves, current_color):
    if current_color == 0:
        if moves in location_white(matrix):
            return False
        elif moves in location_black(matrix):
            return True
        else:
            return True
    else:
        if moves in location_black(matrix):
            return False
        elif moves in location_white(matrix):
            return True
        else:
            return True


def location_black(matrix):  # месторасположение черных фигур
    # position_black = []
    # for i_index, i_element in enumerate(matrix):
    #     for j_index, j_element in enumerate(i_element):
    #         if j_element.islower():
    #             position_black.append([i_index, j_index])
    position_black = [[i_index, j_index] for i_index, i_element in enumerate(matrix)
                      for j_index, j_element in enumerate(i_element) if j_element.islower()]
    return position_black


def location_white(matrix):  # месторасположение белых фигур
    # position_white = []
    # for i_index, i_element in enumerate(matrix):
    #     for j_index, j_element in enumerate(i_element):
    #         if j_element.isupper():
    #             position_white.append([i_index, j_index])
    position_white = [[i_index, j_index] for i_index, i_element in enumerate(matrix)
                      for j_index, j_element in enumerate(i_element) if j_element.isupper()]
    return position_white


def notation_chess(step, current_color, counter, show_write, shah_chess):  # запись шагов в файл и печать нотации
    with open('notation.txt', 'a+', encoding='utf-8') as file:
        if shah_chess:
            if current_color == 0:
                count = counter // 2 + 1
                file.write(f'{count}. {step}+')
            elif current_color == 1:
                file.write(f' {step}+\n')
        else:
            if current_color == 0:
                count = counter // 2 + 1
                file.write(f'{count}. {step}')
            elif current_color == 1:
                file.write(f' {step}\n')

        if show_write == 1:
            file.seek(0)
            print('Нотация партии:')
            for text in file:
                print(text, end='')


def pawn(figure_position, current_color):  # пешка
    possible_moves = []
    i, j = figure_position
    if current_color:  # ходят черные
        i += 1
        j_left = j - 1
        j_right = j + 1
        if -1 < j_left < 8 and (i - 1, j - 1) in white_pawn:
            possible_moves.append([i, j_left])
            del white_pawn[(i - 1, j - 1)]
        if -1 < j_right < 8 and (i - 1, j + 1) in white_pawn:
            possible_moves.append([i, j_right])
            del white_pawn[(i - 1, j + 1)]

        i, j = figure_position
        if i == 1:
            possible_moves.append([i + 1, j])
            possible_moves.append([i + 2, j])
        else:
            possible_moves.append([i + 1, j])
    else:
        i -= 1
        j_left = j - 1
        j_right = j + 1
        if -1 < j_left < 8 and (i + 1, j - 1) in black_pawn:
            possible_moves.append([i, j_left])
            del black_pawn[(i + 1, j - 1)]
        if -1 < j_right < 8 and (i + 1, j + 1) in black_pawn:
            possible_moves.append([i, j_right])
            del black_pawn[(i + 1, j + 1)]

        i, j = figure_position
        if i == 6:
            possible_moves.append([i - 1, j])
            possible_moves.append([i - 2, j])
        else:
            possible_moves.append([i - 1, j])

    return possible_moves


def rook(figure_position, current_color):  # ладья
    possible_moves = []
    i, j = figure_position
    while i > 0:
        i -= 1
        if ([i, j] in location_white(matrix) and current_color == 0) or \
                ([i, j] in location_black(matrix) and current_color == 1):
            break
        elif ([i, j] in location_white(matrix) and current_color == 1) or \
                ([i, j] in location_black(matrix) and current_color == 0):
            possible_moves.append([i, j])
            break
        else:
            if check_step([i, j], current_color):
                possible_moves.append([i, j])
            else:
                break

    i, j = figure_position
    while j < 7:
        j += 1
        if ([i, j] in location_white(matrix) and current_color == 0) or \
                ([i, j] in location_black(matrix) and current_color == 1):
            break
        elif ([i, j] in location_white(matrix) and current_color == 1) or \
                ([i, j] in location_black(matrix) and current_color == 0):
            possible_moves.append([i, j])
            break
        else:
            if check_step([i, j], current_color):
                possible_moves.append([i, j])
            else:
                break

    i, j = figure_position
    while i < 7:
        i += 1
        if ([i, j] in location_white(matrix) and current_color == 0) or \
                ([i, j] in location_black(matrix) and current_color == 1):
            break
        elif ([i, j] in location_white(matrix) and current_color == 1) or \
                ([i, j] in location_black(matrix) and current_color == 0):
            possible_moves.append([i, j])
            break
        else:
            if check_step([i, j], current_color):
                possible_moves.append([i, j])
            else:
                break

    i, j = figure_position
    while j > 0:
        j -= 1
        if ([i, j] in location_white(matrix) and current_color == 0) or \
                ([i, j] in location_black(matrix) and current_color == 1):
            break
        elif ([i, j] in location_white(matrix) and current_color == 1) or \
                ([i, j] in location_black(matrix) and current_color == 0):
            possible_moves.append([i, j])
            break
        else:
            if check_step([i, j], current_color):
                possible_moves.append([i, j])
            else:
                break
    return possible_moves


def knight(figure_position, current_color):  # конь
    DISPLACEMENTS = [[-2, -1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-2, 1], [-1, -2]]
    possible_moves = []
    i, j = figure_position
    for disp in DISPLACEMENTS:
        i += disp[0]
        j += disp[1]
        if -1 < i < 8 and -1 < j < 8:
            if ([i, j] in location_white(matrix) and current_color == 1) or \
                    ([i, j] in location_black(matrix) and current_color == 0):
                possible_moves.append([i, j])
            elif matrix[i][j] == '.':
                if check_step([i, j], current_color):
                    possible_moves.append([i, j])
                else:
                    break
        i, j = figure_position
    return possible_moves


def bishop(figure_position, current_color):  # слон
    possible_moves = []
    i, j = figure_position
    while i > 0 and j > 0:
        i -= 1
        j -= 1
        if ([i, j] in location_white(matrix) and current_color == 0) or \
                ([i, j] in location_black(matrix) and current_color == 1):
            break
        elif ([i, j] in location_white(matrix) and current_color == 1) or \
                ([i, j] in location_black(matrix) and current_color == 0):
            possible_moves.append([i, j])
            break
        else:
            if check_step([i, j], current_color):
                possible_moves.append([i, j])
            else:
                break

    i, j = figure_position
    while i > 0 and j < 7:
        i -= 1
        j += 1
        if ([i, j] in location_white(matrix) and current_color == 0) or \
                ([i, j] in location_black(matrix) and current_color == 1):
            break
        elif ([i, j] in location_white(matrix) and current_color == 1) or \
                ([i, j] in location_black(matrix) and current_color == 0):
            possible_moves.append([i, j])
            break
        else:
            if check_step([i, j], current_color):
                possible_moves.append([i, j])
            else:
                break

    i, j = figure_position
    while i < 7 and j < 7:
        i += 1
        j += 1
        if ([i, j] in location_white(matrix) and current_color == 0) or \
                ([i, j] in location_black(matrix) and current_color == 1):
            break
        elif ([i, j] in location_white(matrix) and current_color == 1) or \
                ([i, j] in location_black(matrix) and current_color == 0):
            possible_moves.append([i, j])
            break
        else:
            if check_step([i, j], current_color):
                possible_moves.append([i, j])
            else:
                break

    i, j = figure_position
    while i < 7 and j > 0:
        i += 1
        j -= 1
        if ([i, j] in location_white(matrix) and current_color == 0) or \
                ([i, j] in location_black(matrix) and current_color == 1):
            break
        elif ([i, j] in location_white(matrix) and current_color == 1) or \
                ([i, j] in location_black(matrix) and current_color == 0):
            possible_moves.append([i, j])
            break
        else:
            if check_step([i, j], current_color):
                possible_moves.append([i, j])
            else:
                break
    return possible_moves


def queen(figure_position, current_color):  # ферзь
    possible_moves = []
    possible_moves.extend(bishop(figure_position, current_color))
    possible_moves.extend((rook(figure_position, current_color)))
    return possible_moves


def king(figure_position, current_color):  # король
    DISPLACEMENTS = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
    possible_moves = []
    i, j = figure_position
    for disp in DISPLACEMENTS:
        i += disp[0]
        j += disp[1]
        if -1 < i < 8 and -1 < j < 8:
            if ([i, j] in location_white(matrix) and current_color == 1) or \
                    ([i, j] in location_black(matrix) and current_color == 0):
                possible_moves.append([i, j])
            elif matrix[i][j] == '.':
                if check_step([i, j], current_color):
                    possible_moves.append([i, j])
                else:
                    break
        i, j = figure_position
    return possible_moves


CHESSMEN = {'P': pawn, 'R': rook, 'N': knight, 'B': bishop, 'Q': queen, 'K': king}


def figure(step, current_color):
    global flag
    start_step, finish_step = step.split('-')
    if len(step) == 5:
        change_pawn = 0
        start_position_pawn = [8 - int(start_step[1]), COORDINATE[start_step[0]]]
        finish_position_pawn = [8 - int(finish_step[1]), COORDINATE[finish_step[0]]]
        length_step = abs(start_position_pawn[0] - finish_position_pawn[0])
        if length_step == 2:
            i, j = finish_position_pawn
            if current_color:
                black_pawn[(i, j)] = True
            else:
                white_pawn[(i, j)] = True
            flag = True
        start_position = pawn(start_position_pawn, current_color)
        finish_position = pawn(finish_position_pawn, current_color)
        if (finish_position_pawn[0] == 0 and current_color == 0) or \
                (finish_position_pawn[0] == 7 and current_color == 1):
            change_pawn = 1
        return start_position_pawn, finish_position_pawn, start_position, finish_position, change_pawn
    else:
        start_position = [8 - int(start_step[2]), COORDINATE[start_step[1]]]
        finish_position = [8 - int(finish_step[1]), COORDINATE[finish_step[0]]]
        if step[0] in CHESSMEN.keys():
            possible_position = CHESSMEN[step[0]](start_position, current_color)
            finish_step = CHESSMEN[step[0]](finish_position, current_color)
            return start_position, finish_position, possible_position, finish_step, 0


def validation(step):  # проверка ввода хода игрока
    if len(step) == 5 and step.index('-') == 2:
        if step[1].isdigit() and step[-1].isdigit():
            return True
        else:
            return False
    elif len(step) == 6 and step.index('-') == 3:
        if step[2].isdigit() and step[-1].isdigit() and (step[0] in CHESSMEN.keys()) and \
                ((step[1].upper() and step[-2].upper()) in ALPHABET):
            return True
        else:
            return False
    else:
        return False


def step_player(players, current_color, counter):  # функция для ввода шага
    print(f'\nХод №{counter // 2 + counter % 2}:')
    if current_color == 0:
        return input(f'{players[current_color]}, введите ход белых через тире: ')
    else:
        return input(f'{players[current_color]}, введите ход черных через тире: ')


def name_player():  # ввод имени игрока
    while True:
        player_first = input('Введите имя игрока, который играет белыми: ')
        player_second = input('Введите имя игрока, который играет черными: ')
        if player_first.isalpha() and player_second.isalpha():
            return player_first, player_second
        else:
            print('Некорректный ввод! Попробуйте еще раз!')
    # play_first = 'Юрий'
    # player_second = 'Марина'
    # return play_first, player_second


def main():
    global flag
    players = name_player()
    counter = 1
    go_out = 1
    current_color = WHITE
    while go_out:
        print_matrix()
        while True:
            step = step_player(players, current_color, counter)  # ввод шага
            if validation(step):
                start, finish, start_position, finish_position, change_pawn = figure(step, current_color)
                if change_pawn:
                    change_figure(finish, current_color)
                    matrix[start[0]][start[1]] = '.'
                    break
                elif flag:
                    matrix[finish[0]][finish[1]] = matrix[start[0]][start[1]]
                    matrix[start[0]][start[1]] = '.'
                    if current_color:
                        matrix[finish[0] - 1][finish[1]] = '.'
                        break
                    else:
                        matrix[finish[0] + 1][finish[1]] = '.'
                        break
                elif finish in start_position:
                    matrix[finish[0]][finish[1]] = matrix[start[0]][start[1]]
                    matrix[start[0]][start[1]] = '.'
                    break
                flag = False
        while True:
            answer = input('Вывести нотацию партии?(да/нет) ').lower()  # запрос печати записанной нотации
            if answer == 'да':
                notation_chess(step, current_color, counter, 1, shah(finish_position, current_color))
                break
            elif answer == 'нет':
                notation_chess(step, current_color, counter, 0, shah(finish_position, current_color))
                break
        current_color = not current_color
        counter += 1


if os.path.exists('notation.txt'):  # очищение файла при запуске новой партии
    os.remove('notation.txt')
main()
print_matrix()
