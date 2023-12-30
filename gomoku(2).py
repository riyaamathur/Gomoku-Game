import time

def is_empty(board):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != " ":
                return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    d_y_2 = - d_x
    d_x_2 = - d_y
    x = y_end + 1
    y = x_end + 1
    color = str(board[y_end][x_end])
    opposite_color = ""
    if color == "w":
        opposite_color = "b"
    elif color == "b":
        opposite_color = "w"
    sequence_type = ""
    failures = 0
    for i in range(length + 2):
        try:
            if str(board[x][y]) == opposite_color:
                failures = failures + 1
        except:
            failures = failures + 1
        x = x + d_x_2
        y = y + d_y_2
    if failures == 1:
         sequence_type = "SEMIOPEN"
    elif failures == 2:
        sequence_type = "CLOSED"
    elif failures == 0:
        sequence_type = "OPEN"
    return sequence_type

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq = 0
    semiopen_seq = 0
    x  = y_start
    y = x_start
    d_y_2 = d_x
    d_x_2 = d_y
    seq_type_list1 = []
    seq_type_list2 = []
    seq_length = []
    num_of_seqs = []
    # check for length
    length2 = 0
    for i in range(8):
        try:
            if (board[x][y] == col):
                length2 = length2
                try:
                    if (x - d_x_2) < 0 or (y - d_y_2) < 0:
                        length2 = 0
                        seq_type_list1.append(False)
                    elif str(board[x - d_x_2][y - d_y_2]) == " ":
                        length2 = 0
                        seq_type_list1.append(True)
                    elif str(board[x - d_x_2][y - d_y_2]) != col:
                        length2 = 0
                        seq_type_list1.append(False)
                except:
                    length2 = 0
                    seq_type_list1.append(False)
                    pass
                length2 = length2 + 1
                try:
                    if (x + d_x_2) < 0 or (y + d_y_2) < 0:
                        length2 = 0
                        seq_type_list1.append(False)
                    elif str(board[x + d_x_2][y + d_y_2]) == " ":
                    #   " ", "b", "w"
                        seq_type_list2.append(True)
                        num_of_seqs.append(" ")
                        seq_length.append(length2)
                        length2 = 0
                    elif str(board[x + d_x_2][y + d_y_2]) != col:
                        seq_type_list2.append(False)
                        num_of_seqs.append(" ")
                        seq_length.append(length2)
                        length2 = 0
                except:
                    seq_type_list2.append(False)
                    num_of_seqs.append(" ")
                    seq_length.append(length2)
                    length2 = 0
            x = x + d_x_2
            y = y + d_y_2
        except:
            pass
    for i in range(len(num_of_seqs)):
        if (seq_type_list1[i] == True and seq_type_list2[i] == True and seq_length[i] == length):
            open_seq = open_seq + 1
        elif (seq_type_list1[i] == False and seq_type_list2[i] == True and seq_length[i] == length):
            semiopen_seq = semiopen_seq + 1
        elif (seq_type_list1[i] == True and seq_type_list2[i] == False and seq_length[i] == length):
            semiopen_seq = semiopen_seq + 1
    return (open_seq, semiopen_seq)

def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    values = [0,0]
    for i in range(8): #rows correct
        return_values = list(detect_row(board, col, i, 0, length, 0, 1))
        values = [values[0] + return_values[0], values[1] + return_values[1]]
    # print("1: " + str(values))
    for i in range(8): #col correct
        return_values = list(detect_row(board, col, 0, i, length, 1, 0))
        values = [values[0] + return_values[0], values[1] + return_values[1]]
    # print("2: " + str(values))
    for i in range(8): #lower diagonals left correct
        try:
            return_values = list(detect_row(board, col, i, 0, length, 1, 1))
            values = [values[0] + return_values[0], values[1] + return_values[1]]
        except:
            pass
    # print("3: " + str(values))
    for i in range(7): #upper diagonals left correct
        try:
            return_values = list(detect_row(board, col, i, 7, length, -1, -1)) # y, x
            values = [values[0] + return_values[0], values[1] + return_values[1]]
        except:
            pass
    # print("4: " + str(values))
    for i in range(7): #upper diagonals right correct
        try:
            return_values = list(detect_row(board, col, 0, i, length, 1, -1)) # was - 1,1 was 1,1
            values = [values[0] + return_values[0], values[1] + return_values[1]]
        except:
            pass
    # print("5: " + str(values))
    for i in range(8): #lower diagonals right correct
        try:
            return_values = list(detect_row(board, col, 7, i, length, -1, 1)) # was -1,-1 y, x
            values = [values[0] + return_values[0], values[1] + return_values[1]]
        except:
            pass
    # print("6: " + str(values))
    open_seq_count = values[0]
    semi_open_seq_count = values[1]
    return (open_seq_count, semi_open_seq_count)

def search_max(board):
    top_score = -100000
    top_move_y = 0
    top_move_x = 0
    for row in range(len(board)):
        top_score = top_score
        top_move_y = top_move_y
        top_move_x = top_move_x
        for col in range(len(board[row])):
            top_score = top_score
            top_move_y = top_move_y
            top_move_x = top_move_x
            if (board[row][col] == " "):
                board[row][col] = "b"
                score4 = score(board)
                print_board(board)
                if score4 >= top_score:
                    top_score = score4
                    top_move_y = row
                    top_move_x = col
                board[row][col] = " "
    move_y = top_move_y
    move_x = top_move_x
    return move_y, move_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    for x in range(5,9):
        if (detect_rows(board, "w", x) != (0, 0)):
            return "White won"
        elif (detect_rows(board, "b", x) != (0, 0)):
            return "Black won"
    full = True
    for row in range(len(board)):
        for col in range(len(board[0])):
            if (str(board[row][col]) == " ") :
                full = False
    if (full):
        return "Draw"
    else:
        return "Continue playing"
    # ["White won", "Black won", "Draw", "Continue playing"]


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            # (0,0)
            # Computer chooses its move

        print("Computer move: (%d, %d)" % (move_y, move_x))
        # Computer places its move
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res


        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        # Player places move
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def test_detect_row():
    board = make_empty_board(8)
    x = 2; y = 2; d_x = 0; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    x = 2; y = 5; d_x = 0; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,2,length,d_y,d_x) == (2,0):
        print(detect_row(board, "w", 0,2,length,d_y,d_x))
        print("TEST CASE for detect_row PASSED")
    else:
        print(detect_row(board, "w", 0,0,length,d_y,d_x))
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    """
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    x = 0; y = 0; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    """
    x = 3; y = 2; d_x = 1; d_y = 1; length = 2; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    print(detect_rows(board, col,length))
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0


    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == '__main__':
    play_gomoku(8)
