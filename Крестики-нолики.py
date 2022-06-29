STEP_DICT = {1: '00', 2: '01', 3: '02', 4: '10', 5: '11', 6: '12', 7: '20', 8: '21', 9: '22'}
WIN_LIST = (('00', '01', '02'), ('10', '11', '12'), ('20', '21', '22'), ('00', '10', '20'),
            ('01', '11', '22'), ('02', '12', '22'), ('00', '11', '22'), ('02', '11', '20'))
MATRIX = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]


def print_matrix():
    print('Крестики-нолики:')
    for elem in MATRIX:
        print(*elem)


def step_matrix(step, number):
    if step in STEP_DICT.keys():
        line = int(STEP_DICT[step][0])
        column = int(STEP_DICT[step][1])
        if number == 0:
            MATRIX[line][column] = 'X'
            STEP_DICT.pop(step)
        else:
            MATRIX[line][column] = '0'
            STEP_DICT.pop(step)
        return True
    else:
        return False


def check_win():
    for win in WIN_LIST:
        if MATRIX[int(win[0][0])][int(win[0][1])] == MATRIX[int(win[1][0])][int(win[1][1])] == \
                MATRIX[int(win[2][0])][int(win[2][1])]:
            return True
    else:
        return False


player1 = input('Введите имя первого игрока: ')
player2 = input('Введите имя второго игрока: ')

print(f'\n{player1}, Вы играете крестиками!\n'
      f'{player2}, Вы играете ноликами!\n')

players = [player1, player2]
print_matrix()
N = 2
game = True
while game:
    for i_step in range(N):
        if STEP_DICT.keys():
            while True:
                step = input(f'\n{players[i_step]} Ваш ход: ')
                if step.isdigit() and 0 < int(step) < 10:
                    if step_matrix(int(step), i_step):
                        break
                    else:
                        print('Клетка занята, попробуйте еще раз!')
                        print_matrix()
                else:
                    print('Вы сделали неверный шаг! '
                          'Такой клетки не существует!')
            print_matrix()
            if check_win():
                print(f'Поздравляем {players[i_step]}! Вы выиграли!')
                game = False
                break
        else:
            print('Ничья!')
            game = False
            break
