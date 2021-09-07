grid = [[]]
words = []
comp_grid = []
starts = []

def find_comps():
    global words
    grid = [["" for i in words] for j in words]
    for i in range(len(words)):
        for j in range(len(words)):
            grid[i][j] = compare_words(words[i], words[j])
    return grid

def compare_words(word1, word2):
    res = ""
    if word1 == word2:
        return word1
    for i in range(len(word1)):
        if word1[i] in word2:
            if word1[i] not in res:
                res += word1[i]
    return res

def leng(word):
    return len(word)

def create_grid():
    global comp_grid
    global words
    global grid
    global starts
    key = 0
    vert = False
    first = words[key]
    grid = [["" for i in range(len(words[key]) * 4)] for j in range(len(words[key]) * 4)]
    for i in range(int(len(grid) / 2 - len(words[key]) / 2), int(len(grid) / 2 - len(words[key]) / 2 + len(words[key]))):
        grid[int(len(grid) / 2)][i] = words[key][i - (int(len(grid) / 2 - len(words[key]) / 2))]
        if (i - (int(len(grid) / 2 - len(words[key]) / 2))) == 0:
            pos = tuple([(int(len(grid) / 2)), i])
            starts.append([list(pos), not vert, first])
    words.pop(key)
    place_words(first, vert, pos)

def place_words(first, vert, pos):
    global comp_grid
    global words
    global grid
    for i in range(len(comp_grid)):
        if comp_grid[i][i] == first:
            key = i
    count = []
    inter = 0
    if len(words) == 0:
        return
    while len(count) < 2 and inter < len(comp_grid):
        if comp_grid[key][inter] != "" and comp_grid[key][inter] != comp_grid[key][key] and comp_grid[inter][inter] in words:
            count.append(comp_grid[inter][inter])
        inter += 1
    if len(count) == 0:
        return    
    elif len(count) == 1:
        placed = False
        test = find_int(key, count[0])
        counter = 0
        while counter < len(test) and placed != True:
            (placed, pos) = test_placement(test[counter], vert, pos, count[0])
            counter += 1
        if placed:
            for i in range(len(comp_grid)):
                comp_grid[i].pop(key)
            comp_grid.pop(key)
            vert = not vert
            words.remove(count[0])
            return place_words(count[0], vert, pos)
        else:
            return
    else:
        placed = [False, False]
        pos = [pos, pos]
        test = [find_int(key, count[0]), find_int(key, count[1])]
        counter = 0
        while counter < len(test) and False in placed:
            idx = 0
            while idx < len(test[counter]) and placed[counter] == False:
                (placed[counter], pos[counter]) = test_placement(test[counter][idx], vert, pos[counter], count[counter])
                idx += 1
            counter += 1
        if placed[0] or placed[1]:
            for i in range(len(comp_grid)):
                comp_grid[i].pop(key)
            comp_grid.pop(key)
            vert = not vert
            if not placed[1]:
                words.remove(count[0])
                return place_words(count[0], vert, pos[0])
            elif not placed[0]:
                words.remove(count[1])
                return place_words(count[1], vert, pos[1])
            else:
                words.remove(count[0])
                words.remove(count[1])
                place_words(count[0], vert, pos[0])
                return place_words(count[1], vert, pos[1])
    return

def test_placement(test, vert, pos, word):
    global grid
    global starts
    if not vert:
        for i in range(pos[0] - test[1], pos[0] - test[1] + len(word)):
            if i < 0 or i >= len(grid):
                return (False, pos)
            if grid[i][pos[1] + test[0]] != '' and grid[i][pos[1] + test[0]] != word[i - (pos[0] - test[1])]:
                return (False, pos)
        testc = test_collision(pos, test, word, vert)
        if not testc:
            return (False, pos)
        for i in range(pos[0] - test[1], pos[0] - test[1] + len(word)):    
            grid[i][pos[1] + test[0]] = word[i - (pos[0] - test[1])]
            if i - (pos[0] - test[1]) == 0:
                newPos = tuple([i, pos[1] + test[0]])
                starts.append([list(newPos), vert, word])
        return (True, newPos)
    else:
        for i in range(pos[1] - test[1], pos[1] - test[1] + len(word)):
            if i < 0 or i >= len(grid):
                return (False, pos)
            if grid[pos[0] + test[0]][i] != '' and grid[pos[0] + test[0]][i] != word[i - (pos[1] - test[1])]:
                return (False, pos)
        testc = test_collision(pos, test, word, vert)
        if not testc:
            return (False, pos)
        for i in range(pos[1] - test[1], pos[1] - test[1] + len(word)):    
            grid[pos[0] + test[0]][i] = word[i - (pos[1] - test[1])]
            if i - (pos[1] - test[1]) == 0:
                newPos = tuple([pos[0] + test[0], i])
                starts.append([list(newPos), vert, word])
        return (True, newPos)

def test_collision(pos, test, word, vert):
    global grid
    if not vert:
        if pos[0] - test[1] > 0:
            if grid[pos[0] - test[1] - 1][pos[1] + test[0]] != '':
                return False
        if pos[0] + (len(word) - 1 - test[1]) < len(grid) - 1:
            if grid[pos[0] + len(word) - test[1]][pos[1] + test[0]] != '':
                return False
        for i in range(pos[0] - test[1], pos[0] - test[1] + len(word)):
            if grid[i][pos[1] + test[0]] == '':
                if (pos[1] + test[0] > 0) and (pos[1] + test[0] < len(grid) - 1):
                    if (grid[i][pos[1] + test[0] - 1] != '') or (grid[i][pos[1] + test[0] + 1] != ''):
                        return False
                elif pos[1] + test[0] > 0:
                    if grid[i][pos[1] + test[0] - 1] != '':
                        return False
                elif pos[1] + test[0] < len(grid) - 1:
                    if grid[i][pos[1] + test[0] + 1] != '':
                        return False
    else:
        if pos[1] - test[1] > 0:
            if grid[pos[0] + test[0]][pos[1] - test[1] - 1] != '':
                return False
        if pos[1] + (len(word) - 1 - test[1]) < len(grid) - 1:
            if grid[pos[0] + test[0]][pos[1] + len(word) - test[1]] != '':
                return False
        for i in range(pos[1] - test[1], pos[1] - test[1] + len(word)):
            if grid[pos[0] + test[0]][i] == '':
                if (pos[0] + test[0] > 0) and (pos[0] + test[0] < len(grid) - 1):
                    if (grid[pos[0] + test[0] - 1][i] != '') or (grid[pos[0] + test[0] + 1][i] != ''):
                        return False
                elif pos[0] + test[0] > 0:
                    if grid[pos[0] + test[0] - 1][i] != '':
                        return False
                elif pos[0] + test[0] < len(grid) - 1:
                    if grid[pos[0] + test[0] + 1][i] != '':
                        return False
    return True

def find_int(key, count):
    global comp_grid
    res = []
    for j in range(len(count)):
        for k in range(len(comp_grid[key][key])):
            if count[j] == comp_grid[key][key][k]:
                res.append(tuple([k,j]))
    return res

def colClear():
    global grid
    for i in range(len(grid)):
        if grid[i][0] != '':
            return False
    return True

def colClearEnd():
    global grid
    for i in range(len(grid)):
        if grid[i][-1] != '':
            return False
    return True

def clearCol():
    global grid
    for i in range(len(grid)):
        grid[i].pop(0)
    
def clearColEnd():
    global grid
    for i in range(len(grid)):
        grid[i].pop(-1)

def main():
    global words
    global comp_grid
    global grid
    global starts
    words = ['Heller', 'Fitzgerald', 'Williams', 'London', 'Miller', 'Hemingway', 'Orwell', 'Kesey', 'Steinbeck']
    for i in range(len(words)):
        words[i] = words[i].lower()
    words.sort()
    words.sort(key = leng)
    words.reverse()
    comp_grid = find_comps()
    create_grid()
    clear = ["" for i in range(len(grid))]
    count = 0
    while grid[0] == clear:
        count += 1
        grid.pop(0)
    while grid[-1] == clear:
        grid.pop(-1)
    for i in range(len(starts)):
        starts[i][0][0] -= count
    count = 0
    cClear = colClear()
    while cClear:
        count += 1
        clearCol()
        cClear = colClear()
    cClear = colClearEnd()
    while cClear:
        clearColEnd()
        cClear = colClearEnd()
    for i in range(len(starts)):
        starts[i][0][1] -= count
    for i in grid:
        print(i)
    for i in starts:
        print(i)


if __name__ == "__main__":
  main()