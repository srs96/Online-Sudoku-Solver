import random

def parse(input_string):
    units = {}
    peers = {}
    grid = {}
    rows = 'ABCDEFGHI'
    columns = '123456789'
    for row_index, row in enumerate(rows):
        for column_index, column in enumerate(columns):
            rs = (row_index // 3)*3
            rs3 = rs+3
            cs = (column_index // 3)*3
            cs3 = cs + 3
            units[row+column] = [[row+new_col for new_col in columns], [new_row+column for new_row in rows], [new_row+new_col for new_row in rows[rs:rs3] for new_col in columns[cs:cs3]]]
            if input_string[row_index*9 + column_index] == '.' or input_string[row_index*9 + column_index] == '0' :
                grid[row+column] = '123456789'
            else:
                grid[row+column] = input_string[row_index*9 + column_index]
            peers[row+column] = sorted(list(set([idx for unit in units[row+column] for idx in unit if idx != row+column])))
    display(grid)
    for sq in grid:
        if len(grid[sq]) == 1:
            grid = eliminate(grid, sq, grid[sq], peers)
    display(grid)
    return grid, units, peers

def eliminate(grid, sq, option, peers):
    grid[sq] = option
    for peer in peers[sq]:
        if grid and option in grid[peer]:
            grid[peer] = grid[peer].replace(option, '')
            if len(grid[peer]) == 0:
                return False
            if len(grid[peer]) == 1:
                grid = eliminate(grid, sq, grid[sq], peers)


    return grid

def search(grid, completed, peers):
    if grid is False:
        return False
    vals_list = sorted([(sq, len(grid[sq])) for sq in grid], key = lambda x:x[1])
    if all(x[1] == 1 for x in vals_list):
        return grid
    for pair in vals_list:
        if pair[0] not in completed:
            completed[pair[0]] = 1
            sq = pair[0]
            break
    ls = list(grid[sq])
    random.shuffle(ls)
    for option in ls:
        new_grid = search(eliminate(grid.copy(), sq, option, peers), completed.copy(), peers)
        if new_grid:
            return new_grid
    return False

def display(values):
    if values:
        values_list = list(values.items())
        sorted_values = [y[1] for y in sorted([x for x in values_list], key = lambda x:(x[0][0], x[0][1]))]
        new_values = []
        for i in range(len(sorted_values)):
                new_values.append(sorted_values[i])
        return new_values


def solve(input_string):
    grid, unit, peers = parse(input_string)
    completed = {}
    grid = search(grid, completed, peers)
    return display(grid)

