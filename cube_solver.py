import copy
import sys

color_index_num = {
    'w': 0,
    'b': 1,
    'o': 2,
    'g': 3,
    'r': 4,
    'y': 5
}

edge_list = [[[1, 0],[1, 3]], [[3, 0],[1, 4]], [[5, 0],[1, 2]], [[7, 0],[1, 1]],
             [[3, 1],[5, 4]], [[5, 1],[3, 2]], [[5, 2],[3, 3]], [[5, 3],[3, 4]],
             [[7, 1],[1, 5]], [[7, 2],[5, 5]], [[7, 3],[7, 5]], [[7, 4],[3, 5]]]

corner_list = [[[0, 0], [0, 4], [2, 3]], [[2, 0], [2, 2], [0, 3]], [[6, 0], [0, 1], [2, 4]], [[8, 0], [2, 1], [0, 2]],
               [[0, 5], [6, 1], [8, 4]], [[2, 5], [8, 1], [6, 2]], [[6, 5], [6, 4], [8, 3]], [[8, 5], [8, 2], [6, 3]]]

FACE_PROMPTS = [
    ("UP",    "white",  "look down at it - the first row you type is the BACK row"),
    ("FRONT", "blue",   "look straight at it"),
    ("RIGHT", "orange", "look at it from the right - its left column touches FRONT"),
    ("BACK",  "green",  "look at it from behind - its left column touches RIGHT"),
    ("LEFT",  "red",    "look at it from the left - its right column touches FRONT"),
    ("DOWN",  "yellow", "roll the cube toward you so BLUE is on top, then read it straight on"),
]


def main():
    cube = read_cube()

    try:
        validate_cube(cube)
    except ValueError as e:
        sys.exit(f"Invalid cube: {e}")

    print("\nScrambled:\n")
    print(display_cube(cube))

    cube, solved = solve(cube)

    print("\nSolved:\n" if solved else "\nBest effort - could not finish:\n")
    print(display_cube(cube))


def find_piece(color1, color2, cube):
  for i in edge_list:
      if (cube[i[0][1]][i[0][0]] == color1 and cube[i[1][1]][i[1][0]] == color2):
        return [i[0][0], i[0][1]], [i[1][0], i[1][1]]
      elif (cube[i[0][1]][i[0][0]] == color2 and cube[i[1][1]][i[1][0]] == color1):
        return [i[1][0], i[1][1]], [i[0][0], i[0][1]]
  raise ValueError(f"no '{color1}{color2}' edge piece on this cube")

def find_corner(c1, c2, c3, cube):
  for i in corner_list:
    if (cube[i[0][1]][i[0][0]] == c1) and (cube[i[1][1]][i[1][0]] == c2) and (cube[i[2][1]][i[2][0]] == c3):
      return [i[0][0], i[0][1]], [i[1][0], i[1][1]], [i[2][0], i[2][1]]
    elif (cube[i[0][1]][i[0][0]] == c1) and (cube[i[1][1]][i[1][0]] == c3) and (cube[i[2][1]][i[2][0]] == c2):
      return [i[0][0], i[0][1]], [i[2][0], i[2][1]], [i[1][0], i[1][1]]
    elif (cube[i[0][1]][i[0][0]] == c2) and (cube[i[1][1]][i[1][0]] == c3) and (cube[i[2][1]][i[2][0]] == c1):
      return [i[2][0], i[2][1]], [i[0][0], i[0][1]], [i[1][0], i[1][1]]
    elif (cube[i[0][1]][i[0][0]] == c2) and (cube[i[1][1]][i[1][0]] == c1) and (cube[i[2][1]][i[2][0]] == c3):
      return [i[1][0], i[1][1]], [i[0][0], i[0][1]], [i[2][0], i[2][1]]
    elif (cube[i[0][1]][i[0][0]] == c3) and (cube[i[1][1]][i[1][0]] == c2) and (cube[i[2][1]][i[2][0]] == c1):
      return [i[2][0], i[2][1]], [i[1][0], i[1][1]], [i[0][0], i[0][1]]
    elif (cube[i[0][1]][i[0][0]] == c3) and (cube[i[1][1]][i[1][0]] == c1) and (cube[i[2][1]][i[2][0]] == c2):
      return [i[1][0], i[1][1]], [i[2][0], i[2][1]], [i[0][0], i[0][1]]
  raise ValueError(f"no '{c1}{c2}{c3}' corner piece on this cube")

def move_u(l):

  l[0][0], l[0][1], l[0][2], l[0][3], l[0][4], l[0][5], l[0][6], l[0][7], l[0][8] = l[0][6], l[0][3], l[0][0], l[0][7], l[0][4], l[0][1], l[0][8], l[0][5], l[0][2]

  l[1][0], l[1][1], l[1][2], l[2][0], l[2][1], l[2][2], l[3][0], l[3][1], l[3][2], l[4][0], l[4][1], l[4][2] = l[2][0], l[2][1], l[2][2], l[3][0], l[3][1], l[3][2], l[4][0], l[4][1], l[4][2], l[1][0], l[1][1], l[1][2]
  return l

def move_d(l):

    l[5][0], l[5][1], l[5][2], l[5][3], l[5][4], l[5][5], l[5][6], l[5][7], l[5][8] = l[5][6], l[5][3], l[5][0], l[5][7], l[5][4], l[5][1], l[5][8], l[5][5], l[5][2]

    l[2][6], l[2][7], l[2][8], l[1][6], l[1][7], l[1][8], l[4][6], l[4][7], l[4][8], l[3][6], l[3][7], l[3][8] = l[1][6], l[1][7], l[1][8], l[4][6], l[4][7], l[4][8], l[3][6], l[3][7], l[3][8], l[2][6], l[2][7], l[2][8]
    return l

def move_r(l):

    l[2][0], l[2][1], l[2][2], l[2][3], l[2][4], l[2][5], l[2][6], l[2][7], l[2][8] = l[2][6], l[2][3], l[2][0], l[2][7], l[2][4], l[2][1], l[2][8], l[2][5], l[2][2]

    l[0][2], l[0][5], l[0][8], l[1][2], l[1][5], l[1][8], l[5][2], l[5][5], l[5][8], l[3][0], l[3][3], l[3][6] = l[1][2], l[1][5], l[1][8], l[5][2], l[5][5], l[5][8], l[3][6], l[3][3], l[3][0], l[0][8], l[0][5], l[0][2]
    return l

def move_l(l):
    l[4][0], l[4][1], l[4][2], l[4][3], l[4][4], l[4][5], l[4][6], l[4][7], l[4][8] = l[4][6], l[4][3], l[4][0], l[4][7], l[4][4], l[4][1], l[4][8], l[4][5], l[4][2]
    l[0][0], l[0][3], l[0][6], l[1][0], l[1][3], l[1][6], l[5][0], l[5][3], l[5][6], l[3][2], l[3][5], l[3][8] = l[3][8], l[3][5], l[3][2], l[0][0], l[0][3], l[0][6], l[1][0], l[1][3], l[1][6], l[5][6], l[5][3], l[5][0]
    return l
def move_f(l):
    l[1][0], l[1][1], l[1][2], l[1][3], l[1][4], l[1][5], l[1][6], l[1][7], l[1][8] = l[1][6], l[1][3], l[1][0], l[1][7], l[1][4], l[1][1], l[1][8], l[1][5], l[1][2]
    l[0][6], l[0][7], l[0][8], l[2][0], l[2][3], l[2][6], l[5][2], l[5][1], l[5][0], l[4][8], l[4][5], l[4][2] = l[4][8], l[4][5], l[4][2], l[0][6], l[0][7], l[0][8], l[2][0], l[2][3], l[2][6], l[5][2], l[5][1], l[5][0]
    return l

def move_b(l):

    l[3][0], l[3][1], l[3][2], l[3][3], l[3][4], l[3][5], l[3][6], l[3][7], l[3][8] = l[3][6], l[3][3], l[3][0], l[3][7], l[3][4], l[3][1], l[3][8], l[3][5], l[3][2]

    l[0][0], l[0][1], l[0][2], l[4][0], l[4][3], l[4][6], l[5][6], l[5][7], l[5][8], l[2][2], l[2][5], l[2][8] = l[2][2], l[2][5], l[2][8], l[0][2], l[0][1], l[0][0], l[4][0], l[4][3], l[4][6], l[5][8], l[5][7], l[5][6]
    return l

def return_layer(face_1, face_2):
  face_lis = [face_1, face_2]
  if 0 in face_lis:
    return 1
  elif 5 in face_lis:
    return 3
  else:
    return 2

def return_corner_layer(f1, f2, f3):
  face_lis = [f1, f2, f3]
  if 0 in face_lis:
    return 1
  else:
    return 3

def white_cross(cube):
  ok = True
  count = 0
  while ([cube[0][1], cube[0][3], cube[0][5], cube[0][7]] != ['w', 'w', 'w', 'w']) or ([cube[1][1], cube[2][1], cube[3][1], cube[4][1]] != ['b', 'o', 'g', 'r']):
    count += 1
    if count > 50:
      print("white_cross stuck!")
      ok = False
      break
    for colour in ['b', 'o', 'g', 'r']:
      l1, l2 = find_piece('w', colour, cube)
      target = color_index_num[colour]

      if (l1[1] == 0) and (target != l2[1]):
        if l1[0] == 1:
          move_b(cube)
          move_b(cube)
        elif l1[0] == 3:
          move_l(cube)
          move_l(cube)
        elif l1[0] == 5:
          move_r(cube)
          move_r(cube)
        elif l1[0] == 7:
          move_f(cube)
          move_f(cube)

      l1, l2 = find_piece('w', colour, cube)
      if (return_layer(l1[1], l2[1]) == 1) and (l1[1] != 0):
        if l1[1] == 1:
          move_f(cube)
          move_r(cube)
          move_r(cube)
          move_r(cube)
          move_d(cube)
          move_r(cube)
          move_f(cube)
          move_f(cube)
          move_f(cube)
        elif l1[1] == 2:
          move_r(cube)
          move_b(cube)
          move_b(cube)
          move_b(cube)
          move_d(cube)
          move_b(cube)
          move_r(cube)
          move_r(cube)
          move_r(cube)
        elif l1[1] == 3:
          move_b(cube)
          move_l(cube)
          move_l(cube)
          move_l(cube)
          move_d(cube)
          move_l(cube)
          move_b(cube)
          move_b(cube)
          move_b(cube)
        elif l1[1] == 4:
          move_l(cube)
          move_f(cube)
          move_f(cube)
          move_f(cube)
          move_d(cube)
          move_f(cube)
          move_l(cube)
          move_l(cube)
          move_l(cube)

      l1, l2 = find_piece('w', colour, cube)
      if return_layer(l1[1], l2[1]) == 2:
        if l1[1] == 1:
          if l1[0] == 3:
            move_l(cube)
          else:
            move_r(cube)
            move_r(cube)
            move_r(cube)

        elif l1[1] == 2:
          if l1[0] == 3:
            move_f(cube)
          else:
            move_b(cube)
            move_b(cube)
            move_b(cube)

        elif l1[1] == 3:
          if l1[0] == 3:
            move_r(cube)
          else:
            move_l(cube)
            move_l(cube)
            move_l(cube)

        elif l1[1] == 4:
          if l1[0] == 3:
            move_b(cube)
          else:
            move_f(cube)
            move_f(cube)
            move_f(cube)

      l1, l2 = find_piece('w', colour, cube)
      if l1[1] == 5:
        spins = 0
        while l2[1] != target and spins < 4:
          spins += 1
          move_d(cube)
          l1, l2 = find_piece('w', colour, cube)

        if l2[1] == 1:
          move_f(cube)
          move_f(cube)

        elif l2[1] == 2:
          move_r(cube)
          move_r(cube)

        elif l2[1] == 3:
          move_b(cube)
          move_b(cube)

        else:
          move_l(cube)
          move_l(cube)

      l1, l2 = find_piece('w', colour, cube)
      if (return_layer(l1[1], l2[1]) == 3) and (l1[1] not in [0, 5]):
        spins = 0
        if target != 4:
          while l1[1] != (target+1) and spins < 4:
            spins += 1
            move_d(cube)
            l1, l2 = find_piece('w', colour, cube)
        else:
          while l1[1] != 1 and spins < 4:
            spins += 1
            move_d(cube)
            l1, l2 = find_piece('w', colour, cube)
        if colour == 'r':
          move_f(cube)
          move_l(cube)
          move_l(cube)
          move_l(cube)
          move_f(cube)
          move_f(cube)
          move_f(cube)

        elif colour == 'b':
          move_r(cube)
          move_f(cube)
          move_f(cube)
          move_f(cube)
          move_r(cube)
          move_r(cube)
          move_r(cube)

        elif colour == 'o':
          move_b(cube)
          move_r(cube)
          move_r(cube)
          move_r(cube)
          move_b(cube)
          move_b(cube)
          move_b(cube)

        elif colour == 'g':
          move_l(cube)
          move_b(cube)
          move_b(cube)
          move_b(cube)
          move_l(cube)
          move_l(cube)
          move_l(cube)
  return ok

def first_layer(cube):
  ok = True
  color_list = [['b', 'o'], ['o', 'g'], ['g', 'r'], ['r', 'b']]
  count = 0
  while not (cube[0] == ['w','w','w','w','w','w','w','w','w'] and
             cube[1][0:3] == ['b','b','b'] and cube[2][0:3] == ['o','o','o'] and
             cube[3][0:3] == ['g','g','g'] and cube[4][0:3] == ['r','r','r']):
    count += 1
    if count > 50:
      print("first_layer stuck!")
      ok = False
      break
    for i in color_list:
      l1, l2, l3 = find_corner('w', i[0], i[1], cube)

      if return_corner_layer(l1[1], l2[1], l3[1]) == 1 and (l1[1] == 0):
        if (i[0] != cube[l2[1]][4]) or (i[1] != cube[l3[1]][4]):
          inner = 0
          while l1 != [6, 0] and inner < 4:
            inner += 1
            move_u(cube)
            l1, l2, l3 = find_corner('w', i[0], i[1], cube)
          move_l(cube)
          move_d(cube)
          move_d(cube)
          move_l(cube)
          move_l(cube)
          move_l(cube)
          spins = 0
          while cube[1][1] != cube[1][4] and spins < 4:
            spins += 1
            move_u(cube)
      l1, l2, l3 = find_corner('w', i[0], i[1], cube)

      if return_corner_layer(l1[1], l2[1], l3[1]) == 1 and (l1[1] != 0):
        if l1[0] == 0:
          if l1[1] == 1:
            move_l(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_l(cube)
            move_l(cube)
            move_l(cube)
          elif l1[1] == 2:
            move_f(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_f(cube)
            move_f(cube)
            move_f(cube)
          elif l1[1] == 3:
            move_r(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_r(cube)
            move_r(cube)
            move_r(cube)
          elif l1[1] == 4:
            move_b(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_b(cube)
            move_b(cube)
            move_b(cube)
        elif l1[0] == 2:
          if l1[1] == 1:
            move_r(cube)
            move_r(cube)
            move_r(cube)
            move_d(cube)
            move_r(cube)
          elif l1[1] == 2:
            move_b(cube)
            move_b(cube)
            move_b(cube)
            move_d(cube)
            move_b(cube)
          elif l1[1] == 3:
            move_l(cube)
            move_l(cube)
            move_l(cube)
            move_d(cube)
            move_l(cube)
          elif l1[1] == 4:
            move_f(cube)
            move_f(cube)
            move_f(cube)
            move_d(cube)
            move_f(cube)
      l1, l2, l3 = find_corner('w', i[0], i[1], cube)

      if return_corner_layer(l1[1], l2[1], l3[1]) == 3 and (l1[1] == 5):
        spins = 0
        while l1[0] != 0 and spins < 4:
          spins += 1
          move_d(cube)
          l1, l2, l3 = find_corner('w', i[0], i[1], cube)
        move_l(cube)
        move_d(cube)
        move_d(cube)
        move_l(cube)
        move_l(cube)
        move_l(cube)
      l1, l2, l3 = find_corner('w', i[0], i[1], cube)

      if return_corner_layer(l1[1], l2[1], l3[1]) == 3 and (l1[1] != 5):
        if l3[1] == 5:
          if l1[0] == 6:
            spins = 0
            while cube[l3[1]][l3[0]] != cube[l1[1]][4] and spins < 4:
              spins += 1
              move_d(cube)
              l1, l2, l3 = find_corner('w', i[0], i[1], cube)
            if cube[l1[1]][4] == 'b':
              move_f(cube)
              move_f(cube)
              move_f(cube)
              move_d(cube)
              move_d(cube)
              move_d(cube)
              move_f(cube)
            elif cube[l1[1]][4] == 'o':
              move_r(cube)
              move_r(cube)
              move_r(cube)
              move_d(cube)
              move_d(cube)
              move_d(cube)
              move_r(cube)
            elif cube[l1[1]][4] == 'g':
              move_b(cube)
              move_b(cube)
              move_b(cube)
              move_d(cube)
              move_d(cube)
              move_d(cube)
              move_b(cube)
            elif cube[l1[1]][4] == 'r':
              move_l(cube)
              move_l(cube)
              move_l(cube)
              move_d(cube)
              move_d(cube)
              move_d(cube)
              move_l(cube)
        elif l2[1] == 5:
          if l1[0] == 8:
            spins = 0
            while cube[l2[1]][l2[0]] != cube[l3[1]][4] and spins < 4:
              spins += 1
              move_d(cube)
              l1, l2, l3 = find_corner('w', i[0], i[1], cube)

            if cube[l1[1]][4] == 'b':
              move_b(cube)
              move_b(cube)
              move_b(cube)
              move_d(cube)
              move_b(cube)
            elif cube[l1[1]][4] == 'o':
              move_l(cube)
              move_l(cube)
              move_l(cube)
              move_d(cube)
              move_l(cube)
            elif cube[l1[1]][4] == 'g':
              move_f(cube)
              move_f(cube)
              move_f(cube)
              move_d(cube)
              move_f(cube)
            elif cube[l1[1]][4] == 'r':
              move_r(cube)
              move_r(cube)
              move_r(cube)
              move_d(cube)
              move_r(cube)
  return ok

def second_layer(cube):

  ok = True
  edge_list2 = [['r', 'b'], ['b', 'o'], ['o', 'g'], ['g', 'r']]
  count = 0
  while not (cube[1][3] == 'b' and cube[1][5] == 'b' and
             cube[2][3] == 'o' and cube[2][5] == 'o' and
             cube[3][3] == 'g' and cube[3][5] == 'g' and
             cube[4][3] == 'r' and cube[4][5] == 'r'):
    count += 1
    if count > 50:
      print("second_layer stuck!")
      ok = False
      break
    for i in edge_list2:
        l1, l2 = find_piece(i[0], i[1], cube)
        if (return_layer(l1[1], l2[1]) == 2 and cube[l1[1]][l1[0]] == cube[l1[1]][4] and cube[l2[1]][l2[0]] == cube[l2[1]][4]):
          in_slot = True
        else:
          in_slot = False
        if not in_slot:
          if return_layer(l1[1], l2[1]) == 2:
            l1, l2 = find_piece(i[0], i[1], cube)
            if (l1[1] == 1):
              if l1[0] == 3:
                move_d(cube)
                move_l(cube)
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_l(cube)
                move_l(cube)
                move_l(cube)
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_f(cube)
                move_f(cube)
                move_f(cube)
                move_d(cube)
                move_f(cube)
              elif l1[0] == 5:
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_r(cube)
                move_r(cube)
                move_r(cube)
                move_d(cube)
                move_r(cube)
                move_d(cube)
                move_f(cube)
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_f(cube)
                move_f(cube)
                move_f(cube)
            elif (l2[1] == 1):
              if l2[0] == 3:
                move_d(cube)
                move_l(cube)
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_l(cube)
                move_l(cube)
                move_l(cube)
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_f(cube)
                move_f(cube)
                move_f(cube)
                move_d(cube)
                move_f(cube)
              elif l2[0] == 5:
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_r(cube)
                move_r(cube)
                move_r(cube)
                move_d(cube)
                move_r(cube)
                move_d(cube)
                move_f(cube)
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_f(cube)
                move_f(cube)
                move_f(cube)
            elif l1[1] == 3:
              if l1[0] == 3:
                move_d(cube)
                move_r(cube)
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_r(cube)
                move_r(cube)
                move_r(cube)
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_b(cube)
                move_b(cube)
                move_b(cube)
                move_d(cube)
                move_b(cube)
              elif l1[0] == 5:
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_l(cube)
                move_l(cube)
                move_l(cube)
                move_d(cube)
                move_l(cube)
                move_d(cube)
                move_b(cube)
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_b(cube)
                move_b(cube)
                move_b(cube)
            elif l2[1] == 3:
              if l2[0] == 3:
                move_d(cube)
                move_r(cube)
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_r(cube)
                move_r(cube)
                move_r(cube)
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_b(cube)
                move_b(cube)
                move_b(cube)
                move_d(cube)
                move_b(cube)
              elif l2[0] == 5:
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_l(cube)
                move_l(cube)
                move_l(cube)
                move_d(cube)
                move_l(cube)
                move_d(cube)
                move_b(cube)
                move_d(cube)
                move_d(cube)
                move_d(cube)
                move_b(cube)
                move_b(cube)
                move_b(cube)

          l1, l2 = find_piece(i[0], i[1], cube)

          if return_layer(l1[1], l2[1]) == 3:
            if l1[1] == 5 and l1[0] in [1,3,5,7]:
              spins = 0
              while cube[l2[1]][l2[0]] != cube[l2[1]][4] and spins < 4:
                spins += 1
                move_d(cube)
                l1, l2 = find_piece(i[0], i[1], cube)
              if cube[l2[1]][l2[0]] == 'b':
                if cube[l1[1]][l1[0]] == 'r':
                  move_d(cube)
                  move_l(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_l(cube)
                  move_l(cube)
                  move_l(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_f(cube)
                  move_f(cube)
                  move_f(cube)
                  move_d(cube)
                  move_f(cube)
                if cube[l1[1]][l1[0]] == 'o':
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_r(cube)
                  move_r(cube)
                  move_r(cube)
                  move_d(cube)
                  move_r(cube)
                  move_d(cube)
                  move_f(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_f(cube)
                  move_f(cube)
                  move_f(cube)
              if cube[l2[1]][l2[0]] == 'o':
                if cube[l1[1]][l1[0]] == 'b':
                  move_d(cube)
                  move_f(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_f(cube)
                  move_f(cube)
                  move_f(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_r(cube)
                  move_r(cube)
                  move_r(cube)
                  move_d(cube)
                  move_r(cube)
                if cube[l1[1]][l1[0]] == 'g':
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_b(cube)
                  move_b(cube)
                  move_b(cube)
                  move_d(cube)
                  move_b(cube)
                  move_d(cube)
                  move_r(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_r(cube)
                  move_r(cube)
                  move_r(cube)
              if cube[l2[1]][l2[0]] == 'g':
                if cube[l1[1]][l1[0]] == 'o':
                  move_d(cube)
                  move_r(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_r(cube)
                  move_r(cube)
                  move_r(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_b(cube)
                  move_b(cube)
                  move_b(cube)
                  move_d(cube)
                  move_b(cube)
                if cube[l1[1]][l1[0]] == 'r':
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_l(cube)
                  move_l(cube)
                  move_l(cube)
                  move_d(cube)
                  move_l(cube)
                  move_d(cube)
                  move_b(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_b(cube)
                  move_b(cube)
                  move_b(cube)
              if cube[l2[1]][l2[0]] == 'r':
                if cube[l1[1]][l1[0]] == 'g':
                  move_d(cube)
                  move_b(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_b(cube)
                  move_b(cube)
                  move_b(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_l(cube)
                  move_l(cube)
                  move_l(cube)
                  move_d(cube)
                  move_l(cube)
                if cube[l1[1]][l1[0]] == 'b':
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_f(cube)
                  move_f(cube)
                  move_f(cube)
                  move_d(cube)
                  move_f(cube)
                  move_d(cube)
                  move_l(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_l(cube)
                  move_l(cube)
                  move_l(cube)
            if l2[1] == 5 and l2[0] in [1,3,5,7]:
              spins = 0
              while cube[l1[1]][l1[0]] != cube[l1[1]][4] and spins < 4:
                spins += 1
                move_d(cube)
                l1, l2 = find_piece(i[0], i[1], cube)
              if cube[l1[1]][l1[0]] == 'b':
                if cube[l2[1]][l2[0]] == 'r':
                  move_d(cube)
                  move_l(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_l(cube)
                  move_l(cube)
                  move_l(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_f(cube)
                  move_f(cube)
                  move_f(cube)
                  move_d(cube)
                  move_f(cube)
                if cube[l2[1]][l2[0]] == 'o':
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_r(cube)
                  move_r(cube)
                  move_r(cube)
                  move_d(cube)
                  move_r(cube)
                  move_d(cube)
                  move_f(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_f(cube)
                  move_f(cube)
                  move_f(cube)
              if cube[l1[1]][l1[0]] == 'o':
                if cube[l2[1]][l2[0]] == 'b':
                  move_d(cube)
                  move_f(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_f(cube)
                  move_f(cube)
                  move_f(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_r(cube)
                  move_r(cube)
                  move_r(cube)
                  move_d(cube)
                  move_r(cube)
                if cube[l2[1]][l2[0]] == 'g':
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_b(cube)
                  move_b(cube)
                  move_b(cube)
                  move_d(cube)
                  move_b(cube)
                  move_d(cube)
                  move_r(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_r(cube)
                  move_r(cube)
                  move_r(cube)
              if cube[l1[1]][l1[0]] == 'g':
                if cube[l2[1]][l2[0]] == 'o':
                  move_d(cube)
                  move_r(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_r(cube)
                  move_r(cube)
                  move_r(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_b(cube)
                  move_b(cube)
                  move_b(cube)
                  move_d(cube)
                  move_b(cube)
                if cube[l2[1]][l2[0]] == 'r':
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_l(cube)
                  move_l(cube)
                  move_l(cube)
                  move_d(cube)
                  move_l(cube)
                  move_d(cube)
                  move_b(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_b(cube)
                  move_b(cube)
                  move_b(cube)
              if cube[l1[1]][l1[0]] == 'r':
                if cube[l2[1]][l2[0]] == 'g':
                  move_d(cube)
                  move_b(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_b(cube)
                  move_b(cube)
                  move_b(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_l(cube)
                  move_l(cube)
                  move_l(cube)
                  move_d(cube)
                  move_l(cube)
                if cube[l2[1]][l2[0]] == 'b':
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_f(cube)
                  move_f(cube)
                  move_f(cube)
                  move_d(cube)
                  move_f(cube)
                  move_d(cube)
                  move_l(cube)
                  move_d(cube)
                  move_d(cube)
                  move_d(cube)
                  move_l(cube)
                  move_l(cube)
                  move_l(cube)
  return ok

def sune(c):
    move_l(c)
    move_d(c)
    move_l(c)
    move_l(c)
    move_l(c)
    move_d(c)
    move_l(c)
    move_d(c)
    move_d(c)
    move_l(c)
    move_l(c)
    move_l(c)

def antisune(c):
    move_l(c)
    move_d(c)
    move_d(c)
    move_l(c)
    move_l(c)
    move_l(c)
    move_d(c)
    move_d(c)
    move_d(c)
    move_l(c)
    move_d(c)
    move_d(c)
    move_d(c)
    move_l(c)
    move_l(c)
    move_l(c)

def corner_3cycle(c):
    move_r(c)
    move_r(c)
    move_r(c)
    move_b(c)
    move_r(c)
    move_r(c)
    move_r(c)
    move_f(c)
    move_f(c)
    move_r(c)
    move_b(c)
    move_b(c)
    move_b(c)
    move_r(c)
    move_r(c)
    move_r(c)
    move_f(c)
    move_f(c)
    move_r(c)
    move_r(c)

def edge_3cycle(c):
    move_l(c)
    move_d(c)
    move_d(c)
    move_d(c)
    move_l(c)
    move_d(c)
    move_l(c)
    move_d(c)
    move_l(c)
    move_d(c)
    move_d(c)
    move_d(c)
    move_l(c)
    move_l(c)
    move_l(c)
    move_d(c)
    move_d(c)
    move_d(c)
    move_l(c)
    move_l(c)

def OLL(cube):
    ok = True
    count = 0
    while [cube[5][1], cube[5][3], cube[5][5], cube[5][7]] != ['y','y','y','y']:
        count += 1
        if count > 50:
            print("OLL cross stuck!")
            ok = False
            break
        if (cube[5][1]!='y') and (cube[5][3]!='y') and (cube[5][5]!='y') and (cube[5][7]!='y'):
            move_f(cube)
            move_l(cube)
            move_d(cube)
            move_l(cube)
            move_l(cube)
            move_l(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_f(cube)
            move_f(cube)
            move_f(cube)
        if (cube[5][1]=='y') and (cube[5][3]=='y') and (cube[5][5]!='y') and (cube[5][7]!='y'):
            move_b(cube)
            move_r(cube)
            move_d(cube)
            move_r(cube)
            move_r(cube)
            move_r(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_b(cube)
            move_b(cube)
            move_b(cube)
            move_f(cube)
            move_l(cube)
            move_d(cube)
            move_l(cube)
            move_l(cube)
            move_l(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_f(cube)
            move_f(cube)
            move_f(cube)
        elif (cube[5][1]=='y') and (cube[5][3]!='y') and (cube[5][5]=='y') and (cube[5][7]!='y'):
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_b(cube)
            move_r(cube)
            move_d(cube)
            move_r(cube)
            move_r(cube)
            move_r(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_b(cube)
            move_b(cube)
            move_b(cube)
            move_f(cube)
            move_l(cube)
            move_d(cube)
            move_l(cube)
            move_l(cube)
            move_l(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_f(cube)
            move_f(cube)
            move_f(cube)
        elif (cube[5][1]!='y') and (cube[5][3]!='y') and (cube[5][5]=='y') and (cube[5][7]=='y'):
            move_d(cube)
            move_d(cube)
            move_b(cube)
            move_r(cube)
            move_d(cube)
            move_r(cube)
            move_r(cube)
            move_r(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_b(cube)
            move_b(cube)
            move_b(cube)
            move_f(cube)
            move_l(cube)
            move_d(cube)
            move_l(cube)
            move_l(cube)
            move_l(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_f(cube)
            move_f(cube)
            move_f(cube)
        elif (cube[5][1]!='y') and (cube[5][3]=='y') and (cube[5][5]!='y') and (cube[5][7]=='y'):
            move_d(cube)
            move_b(cube)
            move_r(cube)
            move_d(cube)
            move_r(cube)
            move_r(cube)
            move_r(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_b(cube)
            move_b(cube)
            move_b(cube)
            move_f(cube)
            move_l(cube)
            move_d(cube)
            move_l(cube)
            move_l(cube)
            move_l(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_f(cube)
            move_f(cube)
            move_f(cube)
        if (cube[5][1]!='y') and (cube[5][3]=='y') and (cube[5][5]=='y') and (cube[5][7]!='y'):
            move_f(cube)
            move_l(cube)
            move_d(cube)
            move_l(cube)
            move_l(cube)
            move_l(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_f(cube)
            move_f(cube)
            move_f(cube)
        elif (cube[5][1]=='y') and (cube[5][3]!='y') and (cube[5][5]!='y') and (cube[5][7]=='y'):
            move_d(cube)
            move_f(cube)
            move_l(cube)
            move_d(cube)
            move_l(cube)
            move_l(cube)
            move_l(cube)
            move_d(cube)
            move_d(cube)
            move_d(cube)
            move_f(cube)
            move_f(cube)
            move_f(cube)
    count = 0
    while [cube[5][0], cube[5][2], cube[5][6], cube[5][8]] != ['y','y','y','y']:
        count += 1
        if count > 10:
            print("OLL corners stuck!")
            ok = False
            break
        oriented = sum(1 for p in [0,2,6,8] if cube[5][p]=='y')
        target = 4 if oriented == 1 else 1
        committed = False
        for alg in (sune, antisune):
            for d_pre in range(4):
                test = copy.deepcopy(cube)
                for i in range(d_pre):
                  move_d(test)
                alg(test)
                if sum(1 for p in [0,2,6,8] if test[5][p]=='y') == target:
                    for i in range(d_pre):
                      move_d(cube)
                    alg(cube)
                    committed = True
                    break
            if committed:
              break
        if not committed:
            sune(cube)
    return ok

def t_perm(c):

    move_r(c)
    move_r(c)
    move_r(c)
    move_d(c)
    move_d(c)
    move_d(c)
    move_r(c)
    move_d(c)
    move_r(c)
    move_f(c)
    move_f(c)
    move_f(c)
    move_r(c)
    move_r(c)
    move_d(c)
    move_r(c)
    move_d(c)
    move_r(c)
    move_r(c)
    move_r(c)
    move_d(c)
    move_d(c)
    move_d(c)
    move_r(c)
    move_f(c)

def PLL(cube):
    ok = True

    def corners_permuted(c):
        return (c[1][6]==c[1][8] and c[2][6]==c[2][8]
                and c[3][6]==c[3][8] and c[4][6]==c[4][8])
    def edges_permuted(c):
        return ([c[1][7], c[2][7], c[3][7], c[4][7]] ==
                [c[1][4], c[2][4], c[3][4], c[4][4]])

    count = 0
    while not corners_permuted(cube):
        count += 1
        if count > 12:
            print("PLL corners stuck!")
            ok = False
            break
        committed = False
        for alg in (corner_3cycle, t_perm):
            for d_pre in range(4):
                test = copy.deepcopy(cube)
                for i in range(d_pre):
                  move_d(test)
                alg(test)
                if corners_permuted(test):
                    for i in range(d_pre):
                      move_d(cube)
                    alg(cube)
                    committed = True
                    break
            if committed: break
        if not committed:
            t_perm(cube)

    count = 0
    while cube[1][6] != cube[1][4]:
        count += 1
        if count > 4:
            print("PLL corner align stuck!")
            ok = False
            break
        move_d(cube)

    count = 0
    while not edges_permuted(cube):
        count += 1
        if count > 12:
            print("PLL edges stuck!")
            ok = False
            break
        committed = False
        for d_pre in range(4):
            for n_apply in (1, 2):
                test = copy.deepcopy(cube)
                for i in range(d_pre):
                  move_d(test)
                for i in range(n_apply):
                  edge_3cycle(test)
                for i in range((4 - d_pre) % 4):
                  move_d(test)
                if edges_permuted(test):
                    for i in range(d_pre):
                      move_d(cube)
                    for i in range(n_apply):
                      edge_3cycle(cube)
                    for i in range((4 - d_pre) % 4):
                      move_d(cube)
                    committed = True
                    break
            if committed:
              break
        if not committed:
            edge_3cycle(cube)

    count = 0
    while cube[1][6] != cube[1][4]:
        count += 1
        if count > 4:
            print("PLL final align stuck!")
            ok = False
            break
        move_d(cube)
    return ok

def get_row(f, r, cube):
  stri = ""
  for i in range(3):
    stri += cube[f][r*3+i]
  return stri


def display_cube(cube):
    pad = " " * 6
    lines = []

    for r in range(3):
        lines.append(pad + " ".join(get_row(0, r, cube)))

    lines.append("")

    for r in range(3):
        lines.append(" ".join(" ".join(get_row(f, r, cube)) for f in (4, 1, 2, 3)))

    lines.append("")

    for r in range(3):
        lines.append(pad + " ".join(get_row(5, r, cube)))

    return "\n".join(lines)


def read_cube():
    print("Hold the cube WHITE up and BLUE toward you, and keep it there.")
    print("Type nine letters per face, left to right, top to bottom (w b o g r y).\n")

    cube = []
    for face, centre, how in FACE_PROMPTS:
        while True:
            raw = input(f"{face} ({centre}) - {how}\n> ").strip().lower().replace(" ", "")
            if len(raw) != 9:
                print(f"  Need exactly 9 stickers, got {len(raw)}.\n")
                continue
            if any(ch not in color_index_num for ch in raw):
                print("  Use only the letters w b o g r y.\n")
                continue
            cube.append(list(raw))
            break
    return cube


def validate_cube(cube):
    colors = list(color_index_num)

    if len(cube) != 6:
        raise ValueError(f"expected 6 faces, got {len(cube)}")

    flat = [sticker for face in cube for sticker in face]
    if len(flat) != 54:
        raise ValueError(f"expected 54 stickers, got {len(flat)}")
    if any(len(face) != 9 for face in cube):
        raise ValueError("every face must have exactly 9 stickers")

    unknown = sorted({s for s in flat if s not in color_index_num})
    if unknown:
        raise ValueError(f"unknown sticker colour(s): {', '.join(unknown)}")

    for colour in colors:
        n = flat.count(colour)
        if n != 9:
            raise ValueError(f"expected 9 '{colour}' stickers, got {n}")

    centres = [face[4] for face in cube]
    if len(set(centres)) != 6:
        raise ValueError(f"the 6 centres must all differ, got {''.join(centres)}")
    if centres != colors:
        raise ValueError(
            f"centres must read {''.join(colors)} for UP FRONT RIGHT BACK LEFT DOWN, "
            f"got {''.join(centres)}"
        )

    solved = [[colour] * 9 for colour in colors]

    def cubies(state, cells):
        return sorted(tuple(sorted(state[c[1]][c[0]] for c in piece)) for piece in cells)

    if cubies(cube, edge_list) != cubies(solved, edge_list):
        raise ValueError("the 12 edges are not a valid set of real cubies")
    if cubies(cube, corner_list) != cubies(solved, corner_list):
        raise ValueError("the 8 corners are not a valid set of real cubies")

    return True


def solve(cube):
    solved = True
    for stage in (white_cross, first_layer, second_layer, OLL, PLL):
        if not stage(cube):
            solved = False
    return cube, solved


if __name__ == "__main__":
    main()
