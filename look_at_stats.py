import pickledb

db = pickledb.load('db.db', False)


def get_stats(word_count_dict):
    return (db.get(word_count_dict))

def main():
    word_list = []
    dict = get_stats('word_count_5')
    for i in dict:
        word_list.append(i)
    for i in word_list:
        print(i, end=' ')	
        print(dict[i])

if __name__ == '__main__':
    main()