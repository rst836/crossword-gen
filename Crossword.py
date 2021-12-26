import copy, random

word_grid = [[]]
words = []
character_comparison_grid = []
word_location_info = []

def find_comparisons():
    global words
    word_grid = [["" for i in words] for j in words]
    for i in range(len(words)):
        for j in range(len(words)):
            word_grid[i][j] = compare_words(words[i], words[j])
    return word_grid

def compare_words(word1, word2):
    common_characters = ""
    if word1 == word2:
        return word1
    for i in range(len(word1)):
        if word1[i] in word2:
            if word1[i] not in common_characters:
                common_characters += word1[i]
    return common_characters

def create_grid():
    global character_comparison_grid
    global words
    global word_grid
    global word_location_info
    is_vert = False
    first_word = words[0]
    word_grid = [["" for i in range(len(first_word) * 4)] for j in range(len(first_word) * 4)]
    for i in range(int(len(word_grid) / 2 - len(first_word) / 2), int(len(word_grid) / 2 - len(first_word) / 2 + len(first_word))):
        word_grid[int(len(word_grid) / 2)][i] = first_word[i - (int(len(word_grid) / 2 - len(first_word) / 2))]
        if (i - (int(len(word_grid) / 2 - len(first_word) / 2))) == 0:
            starting_position = tuple([(int(len(word_grid) / 2)), i])
            word_location_info.append([list(starting_position), not is_vert, first_word])
    words.pop(0)
    place_words(first_word, is_vert, starting_position)

def place_words(selected_word, is_vert, starting_position):
    global character_comparison_grid
    global words
    global word_grid
    for i in range(len(character_comparison_grid)):
        if character_comparison_grid[i][i] == selected_word:
            selected_word_key = i
    match_count = []
    word_list_traversal_key = 0
    if len(words) == 0:
        return
    while len(match_count) < 2 and word_list_traversal_key < len(character_comparison_grid):
        if character_comparison_grid[selected_word_key][word_list_traversal_key] != "" and character_comparison_grid[selected_word_key][word_list_traversal_key] != character_comparison_grid[selected_word_key][selected_word_key] and character_comparison_grid[word_list_traversal_key][word_list_traversal_key] in words:
            match_count.append(character_comparison_grid[word_list_traversal_key][word_list_traversal_key])
        word_list_traversal_key += 1
    if len(match_count) == 0:
        return    
    elif len(match_count) == 1:
        is_placed = False
        possible_intersections = find_intersections(selected_word_key, match_count[0])
        possible_intersections_traversal_key = 0
        while possible_intersections_traversal_key < len(possible_intersections) and is_placed != True:
            (is_placed, starting_position) = test_placement(possible_intersections[possible_intersections_traversal_key], is_vert, starting_position, match_count[0])
            possible_intersections_traversal_key += 1
        if is_placed:
            for i in range(len(character_comparison_grid)):
                character_comparison_grid[i].pop(selected_word_key)
            character_comparison_grid.pop(selected_word_key)
            is_vert = not is_vert
            words.remove(match_count[0])
            return place_words(match_count[0], is_vert, starting_position)
        else:
            return
    else:
        is_placed = [False, False]
        starting_position = [starting_position, starting_position]
        possible_intersections = [find_intersections(selected_word_key, match_count[0]), find_intersections(selected_word_key, match_count[1])]
        possible_intersections_traversal_key = 0
        while possible_intersections_traversal_key < len(possible_intersections) and False in is_placed:
            idx = 0
            while idx < len(possible_intersections[possible_intersections_traversal_key]) and is_placed[possible_intersections_traversal_key] == False:
                (is_placed[possible_intersections_traversal_key], starting_position[possible_intersections_traversal_key]) = test_placement(possible_intersections[possible_intersections_traversal_key][idx], is_vert, starting_position[possible_intersections_traversal_key], match_count[possible_intersections_traversal_key])
                idx += 1
            possible_intersections_traversal_key += 1
        if is_placed[0] or is_placed[1]:
            for i in range(len(character_comparison_grid)):
                character_comparison_grid[i].pop(selected_word_key)
            character_comparison_grid.pop(selected_word_key)
            is_vert = not is_vert
            if not is_placed[1]:
                words.remove(match_count[0])
                return place_words(match_count[0], is_vert, starting_position[0])
            elif not is_placed[0]:
                words.remove(match_count[1])
                return place_words(match_count[1], is_vert, starting_position[1])
            else:
                words.remove(match_count[0])
                words.remove(match_count[1])
                place_words(match_count[0], is_vert, starting_position[0])
                return place_words(match_count[1], is_vert, starting_position[1])
    return

def test_placement(intersection, is_vert, possible_intersections, word):
    global word_grid
    global word_location_info
    if not is_vert:
        for i in range(possible_intersections[0] - intersection[1], possible_intersections[0] - intersection[1] + len(word)):
            if i < 0 or i >= len(word_grid):
                return (False, possible_intersections)
            if word_grid[i][possible_intersections[1] + intersection[0]] != '' and word_grid[i][possible_intersections[1] + intersection[0]] != word[i - (possible_intersections[0] - intersection[1])]:
                return (False, possible_intersections)
        is_no_collision = test_collision(possible_intersections, intersection, word, is_vert)
        if not is_no_collision:
            return (False, possible_intersections)
        for i in range(possible_intersections[0] - intersection[1], possible_intersections[0] - intersection[1] + len(word)):    
            word_grid[i][possible_intersections[1] + intersection[0]] = word[i - (possible_intersections[0] - intersection[1])]
            if i - (possible_intersections[0] - intersection[1]) == 0:
                new_position = tuple([i, possible_intersections[1] + intersection[0]])
                word_location_info.append([list(new_position), is_vert, word])
        return (True, new_position)
    else:
        for i in range(possible_intersections[1] - intersection[1], possible_intersections[1] - intersection[1] + len(word)):
            if i < 0 or i >= len(word_grid):
                return (False, possible_intersections)
            if word_grid[possible_intersections[0] + intersection[0]][i] != '' and word_grid[possible_intersections[0] + intersection[0]][i] != word[i - (possible_intersections[1] - intersection[1])]:
                return (False, possible_intersections)
        is_no_collision = test_collision(possible_intersections, intersection, word, is_vert)
        if not is_no_collision:
            return (False, possible_intersections)
        for i in range(possible_intersections[1] - intersection[1], possible_intersections[1] - intersection[1] + len(word)):    
            word_grid[possible_intersections[0] + intersection[0]][i] = word[i - (possible_intersections[1] - intersection[1])]
            if i - (possible_intersections[1] - intersection[1]) == 0:
                new_position = tuple([possible_intersections[0] + intersection[0], i])
                word_location_info.append([list(new_position), is_vert, word])
        return (True, new_position)

def test_collision(possible_intersections, intersection, word, is_vert):
    global word_grid
    if not is_vert:
        if possible_intersections[0] - intersection[1] > 0:
            if word_grid[possible_intersections[0] - intersection[1] - 1][possible_intersections[1] + intersection[0]] != '':
                return False
        if possible_intersections[0] + (len(word) - 1 - intersection[1]) < len(word_grid) - 1:
            if word_grid[possible_intersections[0] + len(word) - intersection[1]][possible_intersections[1] + intersection[0]] != '':
                return False
        for i in range(possible_intersections[0] - intersection[1], possible_intersections[0] - intersection[1] + len(word)):
            if word_grid[i][possible_intersections[1] + intersection[0]] == '':
                if (possible_intersections[1] + intersection[0] > 0) and (possible_intersections[1] + intersection[0] < len(word_grid) - 1):
                    if (word_grid[i][possible_intersections[1] + intersection[0] - 1] != '') or (word_grid[i][possible_intersections[1] + intersection[0] + 1] != ''):
                        return False
                elif possible_intersections[1] + intersection[0] > 0:
                    if word_grid[i][possible_intersections[1] + intersection[0] - 1] != '':
                        return False
                elif possible_intersections[1] + intersection[0] < len(word_grid) - 1:
                    if word_grid[i][possible_intersections[1] + intersection[0] + 1] != '':
                        return False
    else:
        if possible_intersections[1] - intersection[1] > 0:
            if word_grid[possible_intersections[0] + intersection[0]][possible_intersections[1] - intersection[1] - 1] != '':
                return False
        if possible_intersections[1] + (len(word) - 1 - intersection[1]) < len(word_grid) - 1:
            if word_grid[possible_intersections[0] + intersection[0]][possible_intersections[1] + len(word) - intersection[1]] != '':
                return False
        for i in range(possible_intersections[1] - intersection[1], possible_intersections[1] - intersection[1] + len(word)):
            if word_grid[possible_intersections[0] + intersection[0]][i] == '':
                if (possible_intersections[0] + intersection[0] > 0) and (possible_intersections[0] + intersection[0] < len(word_grid) - 1):
                    if (word_grid[possible_intersections[0] + intersection[0] - 1][i] != '') or (word_grid[possible_intersections[0] + intersection[0] + 1][i] != ''):
                        return False
                elif possible_intersections[0] + intersection[0] > 0:
                    if word_grid[possible_intersections[0] + intersection[0] - 1][i] != '':
                        return False
                elif possible_intersections[0] + intersection[0] < len(word_grid) - 1:
                    if word_grid[possible_intersections[0] + intersection[0] + 1][i] != '':
                        return False
    return True

def find_intersections(key, count):
    global character_comparison_grid
    intersections = []
    for j in range(len(count)):
        for k in range(len(character_comparison_grid[key][key])):
            if count[j] == character_comparison_grid[key][key][k]:
                intersections.append(tuple([k,j]))
    return intersections

def left_column_is_clear():
    global word_grid
    for i in range(len(word_grid)):
        if word_grid[i][0] != '':
            return False
    return True

def right_column_is_clear():
    global word_grid
    for i in range(len(word_grid)):
        if word_grid[i][-1] != '':
            return False
    return True

def clear_left_grid_column():
    global word_grid
    for i in range(len(word_grid)):
        word_grid[i].pop(0)
    
def clear_right_grid_column():
    global word_grid
    for i in range(len(word_grid)):
        word_grid[i].pop(-1)

def do_calculation(input):
    global words
    global character_comparison_grid
    global word_grid
    global word_location_info
    words = input
    for i in range(len(words)):
        words[i] = words[i].lower()
    original_words = copy.deepcopy(words)
    original_character_comparison_grid = copy.deepcopy(character_comparison_grid)
    original_grid = copy.deepcopy(word_grid)
    original_word_location_info = copy.deepcopy(word_location_info)
    best_words = copy.deepcopy(original_words)
    best_character_comparison_grid = copy.deepcopy(original_character_comparison_grid)
    best_grid = copy.deepcopy(original_grid)
    best_word_location_info = copy.deepcopy(original_word_location_info)
    num_words_remaining = len(original_words)
    words.sort()
    words.sort(key = len)
    words.reverse()
    for i in range(20):
        character_comparison_grid = find_comparisons()
        create_grid()
        if len(words) < num_words_remaining:
            best_words = copy.deepcopy(words)
            best_character_comparison_grid = copy.deepcopy(character_comparison_grid)
            best_grid = copy.deepcopy(word_grid)
            best_word_location_info = copy.deepcopy(word_location_info)
            num_words_remaining = len(best_words)
        if num_words_remaining == 0:
            break
        character_comparison_grid = copy.deepcopy(original_character_comparison_grid)
        word_grid = copy.deepcopy(original_grid)
        word_location_info = copy.deepcopy(original_word_location_info)
        words = copy.deepcopy(original_words)
        random.shuffle(words)
    character_comparison_grid = copy.deepcopy(best_character_comparison_grid)
    word_grid = copy.deepcopy(best_grid)
    word_location_info = copy.deepcopy(best_word_location_info)
    words = copy.deepcopy(best_words)
    clear = ["" for i in range(len(word_grid))]
    count = 0
    while word_grid[0] == clear:
        count += 1
        word_grid.pop(0)
    while word_grid[-1] == clear:
        word_grid.pop(-1)
    for i in range(len(word_location_info)):
        word_location_info[i][0][0] -= count
    count = 0
    column_is_clear = left_column_is_clear()
    while column_is_clear:
        count += 1
        clear_left_grid_column()
        column_is_clear = left_column_is_clear()
    column_is_clear = right_column_is_clear()
    while column_is_clear:
        clear_right_grid_column()
        column_is_clear = right_column_is_clear()
    for i in range(len(word_location_info)):
        word_location_info[i][0][1] -= count
    res = ''
    height = len(word_grid)
    width = len(word_grid[0])
    for i in range(len(word_grid)):
        for j in word_grid[i]:
            if j == '':
                res += ' '
            else:
                res += j
    res = res.upper()
    return res, width, height