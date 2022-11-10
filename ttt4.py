sz = 3
mat = [['.' for j in range(sz)] for i in range(sz)]

ways = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
        [1, 4, 7], [2, 5, 8], [3, 6, 9],
        [1, 5, 9], [3, 5, 7]]

def main():
     global num_moves
     global player
     print("X goes first")
     player_c = input("Whhich do you want to be?  X or O   ")
     if player_c == "X":
          player = "N"
          player_o = "O"
          num_moves = 1
     else:
          player = "Y"
          player_o = "X"
          num_moves = 0
     print_mat()
     print('Moves are r,c or "0" to exit.')
     exit_flag = False
     while not exit_flag:
          if num_moves % 2 == 0:
               r, c = get_comp_move()
               exit_flag, player_ch = False, player_o
               mat[r][c] = player_ch
               print('\nOkay, my move...\n')
               print_mat()
          else:
               exit_flag, player_ch, r, c = get_move(player_c)
          if not exit_flag:
               if test_win(r, c):
                    print('\n', player_ch, 'WINS THE GAME!')
                    break
               num_moves += 1
               if (num_moves >= 10 and player == "Y") or (num_moves >= 9 and player == "N"):
                    print('No more space. Done.')
                    exit_flag = True

def get_move(player_ch):
     while True:
          prompt = 'Enter move for ' + player_ch + ': '
          s = input(prompt)
          a_list = s.split(',')
          if len(a_list) >= 1 and int(a_list[0]) == 0:
               print('Bye now.')
               return True, player_ch, 0, 0
          elif len(a_list) < 2:
               print('Use row, col. Re-enter.')
          else:
               r = int(a_list[0]) - 1
               c = int(a_list[1]) - 1
               if r < 0 or r >= sz or c < 0 or c >= sz:
                     print('Out of range. Re-enter.')
               elif not mat[r][c] == '.':
                     print('Occupied square. Re-enter.')
               else:
                     mat[r][c] = player_ch
                     print_mat()
                     break
     return False, player_ch, r, c

# Get Computer Move function.
# For each blank cell in the grid, test it according to the
# three rules; 1) look for win, 2) look to block, 3) look for
# double threat. If none of these work, use preference list
def get_comp_move():
     global num_moves
     global player
     
     # Get a list of all available (blank) cells
     cell_list = [(i, j) for j in range(sz)
                  for i in range(sz) if mat[i][j] =='.']
     
     # Test every avail. cell for "to win" condition
     for cell in cell_list:
          if test_to_win(cell[0], cell[1]):
               return cell[0], cell[1]
          
     # Test every avail. cell for "to block" condition
     for cell in cell_list:
          if test_to_block(cell[0], cell[1]):
               return cell[0], cell[1]
     if player == "N":
          if num_moves == 4:
               print("A")
               if (mat[2][0] == "X" and mat[0][2] == "X") or (mat[2][2] == "X" and mat[0][0] == "X"):
                    return 1,0  
     # Test every avail. cell for "double threat" cond.
     for cell in cell_list:
          if test_dbl_threat(cell[0], cell[1]):
               return cell[0], cell[1]
     if player == "Y":
          if num_moves == 2:
               for i in [2, 4, 6, 8]:
                    r = (i - 1) // 3
                    c = (i - 1) % 3
                    if mat[r][c] == 'O':
                         return 1, 1


     if player == "Y":
          pref_list = [1, 9, 3, 7, 5, 2, 4, 6, 8]
     else:
          pref_list = [5, 1, 9, 3, 7, 2, 4, 6, 8]
     for i in pref_list:
          r = (i - 1) // 3
          c = (i - 1) % 3
          if mat[r][c] == '.':
               return r, c
     return 0,0
     
     
# Test To Win: Test every win combo for the cell...
# If two Xs are present, this cell will win!
def test_to_win(r, c):
     cell_n = r * 3 + c + 1
     my_ways = [ls for ls in ways if cell_n in ls]
     for ls in my_ways:
          num_x, num_o, num_blanks = test_way(ls)
          if num_x == 2:
               print('Watch THIS...')
               return True
     return False

# Test to Block: Test every win combo for the cell...
# If two Os are present, this cell must be used to block
def test_to_block(r, c):
     cell_n = r * 3 + c + 1
     my_ways = [ls for ls in ways if cell_n in ls]
     for ls in my_ways:
          num_x, num_o, num_blanks = test_way(ls)
          if num_o == 2:
               print('Ha ha, I am going to block you!')
               return True
     return False

# Test Double Threat: Test all win combos for the cell;
# If there are two threats, play this cell.
def test_dbl_threat(r, c):
     threats = 0
     cell_n = r * 3 + c + 1
     my_ways = [ls for ls in ways if cell_n in ls]
     for ls in my_ways:
          num_x, num_o, num_blanks = test_way(ls)
          if num_x == 1 and num_blanks == 2:
               threats += 1
          if threats >= 2:
               print('I have you now!')
               return True
     return False
                                    
def print_mat():
     s = ''
     s += '  1 2 3\n'
     for i in range(sz):
          s += str(i+ 1) + ' '
          for j in range(sz):
               s += mat[i][j] + ' '
          s += '\n'
     print(s)

def test_win(r, c):
     cell_n = r * 3 + c + 1
     my_ways = [ls for ls in ways if cell_n in ls]
     for ls in my_ways:
          num_x, num_o, num_blanks = test_way(ls)
          if num_x == 3 or num_o == 3:
               return True
     return False

def test_way(ls):
     letters = [ ]
     for item in ls:
          r = (item - 1) // 3
          c = (item - 1) % 3
          letters.append(mat[r][c])
     num_x = letters.count('X')
     num_o = letters.count('O')
     num_blanks = letters.count('.')
     return num_x, num_o, num_blanks

main()


