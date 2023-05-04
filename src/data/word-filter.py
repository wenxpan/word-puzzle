with open('data/profanity-words.txt') as f:
    profanity_list = []
    for line in f:
        if len(line) == 6:
            profanity_list.append(line.strip())

with open('data/sgb-words.txt') as f_input:
    with open('data/sgb-words-filtered.txt', 'w') as f_output:
        for line in f_input:
            if line.strip() not in profanity_list:
                f_output.write(line)
