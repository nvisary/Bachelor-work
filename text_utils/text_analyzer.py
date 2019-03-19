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


def text_compare(text_array1, text_array2):
    first_text_len = len(text_array1)
    second_text_len = len(text_array2)
    if first_text_len >= second_text_len:
        count_words = first_text_len
    else:
        count_words = second_text_len

    compare_words = []
    for i in range(count_words):
        first_word_len = 0
        second_word_len = 0

        if i < first_text_len:
            first_word_len = len(text_array1[i])

        if i < second_text_len:
            second_word_len = len(text_array2[i])

        if first_word_len >= second_word_len:
            count_letters = first_word_len
        else:
            count_letters = second_word_len

        compare_letters = []
        for j in range(count_letters):
            letter1 = 0
            letter2 = 0

            if j < first_word_len and i < first_text_len:
                letter1 = text_array1[i][j]
            if j < second_word_len and i < second_text_len:
                letter2 = text_array2[i][j]

            if letter1 == letter2:
                compare_letters.append(1)
            else:
                compare_letters.append(0)
        compare_words.append(sum(compare_letters) * 100 / count_letters)

    return sum(compare_words) / len(compare_words)



