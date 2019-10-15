import os


def count_func():
    en_lst = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    en_dict = {i: ord(i) - ord(i) for i in en_lst}
    rus_lst = [chr(i) for i in range(ord('а'), ord('ё') + 1) if i != ord('ѐ')]
    rus_dict = {i: ord(i) - ord(i) for i in rus_lst}
    os.chdir(input())
    file_lst = os.listdir()
    for i in file_lst:
        f = open(i, 'r', encoding='utf-8')
        for line in f.readlines():
            for c in line.lower():
                if c in en_lst:
                    en_dict[c] += 1
                elif c in rus_lst:
                    rus_dict[c] += 1
    print(en_dict)
    print(rus_dict)
    return 0


count_func()

