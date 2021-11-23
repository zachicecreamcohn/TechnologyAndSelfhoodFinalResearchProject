import psycopg2
from time import sleep
import pickledb

db = pickledb.load('db.db', False)

def sqlSetup():
    con = psycopg2.connect(database="d76lmct1719stp", user="llubxiofuwfmlc", password="24cf674cbeb374d5dc9839cea64382fb29e952403b9c64f99a1411c5ba9af389", host="ec2-54-205-61-191.compute-1.amazonaws.com", port="5432")
    con.autocommit = True
    global cur
    cur = con.cursor()


def get_all_reviews(rating):
    sqlSetup()
    cur.execute(f"SELECT review_body FROM CWP WHERE rating = {rating}")
    rows = cur.fetchall()
    return rows

def main():
    word_count_1 = {}
    word_count_2 = {}
    word_count_3 = {}
    word_count_4 = {}
    word_count_5 = {}

    for review in get_all_reviews(rating=1):
        for word in review[0].split():
            word_count_1[word] = word_count_1.get(word, 0) + 1
    for review in get_all_reviews(rating=2):
        for word in review[0].split():
            word_count_2[word] = word_count_2.get(word, 0) + 1
    for review in get_all_reviews(rating=3):
        for word in review[0].split():
            word_count_3[word] = word_count_3.get(word, 0) + 1

    for review in get_all_reviews(rating=4):
        for word in review[0].split():
            word_count_4[word] = word_count_4.get(word, 0) + 1
    
    for review in get_all_reviews(rating=5):
        for word in review[0].split():
            word_count_5[word] = word_count_5.get(word, 0) + 1


    db.set('word_count_1', word_count_1)
    db.set('word_count_2', word_count_2)
    db.set('word_count_3', word_count_3)
    db.set('word_count_4', word_count_4)
    db.set('word_count_5', word_count_5)
    db.dump()



if __name__ == "__main__":
    # main()
    for i in get_all_reviews(rating=5):
        if input('next?\n') == 'y':
            print(i)
