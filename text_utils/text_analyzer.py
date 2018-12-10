def jacquard_coefficient(text1, text2):
    count_compare = 0
    for word in text1:
        for word2 in text2:
            word.lower()
            word2.lower()
            if word == word2:
                count_compare += 1
    a = len(text1) - 1
    b = len(text2) - 1
    return count_compare / (a + b - count_compare)

