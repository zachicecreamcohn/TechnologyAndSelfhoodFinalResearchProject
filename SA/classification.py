import openai
import psycopg2
openai.api_key = #SECRET KEY
from termcolor import colored

# Train the data:
### trainData = openai.File.create(file=open(r"C:\Users\zwc12\Documents\Documents\Programming\CWP Review Research Project\SA\train.jsonl"), purpose="classifications")



def sqlSetup():
    con = psycopg2.connect(database="d76lmct1719stp", user="llubxiofuwfmlc", password="24cf674cbeb374d5dc9839cea64382fb29e952403b9c64f99a1411c5ba9af389", host="ec2-54-205-61-191.compute-1.amazonaws.com", port="5432")
    con.autocommit = True
    global cur
    cur = con.cursor()


def classify(text):
    classification = openai.Classification.create(
    file="file-o6d1yl28QdiollXhU06eII56",
    query=text,
    search_model="ada",
    model="curie",
    )
    return classification["label"]

def get_all_data():
    sqlSetup()
    cur.execute("SELECT * FROM cwp")
    data = cur.fetchall()
    return data

def main():
    data = get_all_data()
    for i in data:
        id = i[0]
        rating = str(i[1])
        review = i[2]

        try:
            classification = classify(review)
        except Exception as e:
            print(colored(f'ERROR:\n\n{e}'),"red")
            print(f'PROBELMATIC review: {review}')
            continue
        cur.execute(f"UPDATE cwp SET sa_label = '{classification}' WHERE id = {id}")
        
        # alert the user!
        print("\n CLASSIFICATION COMPLETE")
        if classification == 'Positive':
            if rating == '5' or rating == '4':
                print(f'Review ' + colored({id}, 'white', 'on_green') + ' is ' + colored(f'{classification}', 'green'))
            else:
                print(f'Review ' + colored({id}, 'white', 'on_red') + ' is ' + colored(f'{classification}', 'green'))
        elif classification == 'Neutral':
            if rating == '3':
                print(f'Review ' + colored({id}, 'white', 'on_green') + ' is ' + colored(f'{classification}', 'cyan'))
            else:
                print(f'Review ' + colored({id}, 'white', 'on_red') + ' is ' + colored(f'{classification}', 'cyan'))
        else:
            if rating == '1' or rating == '2':
                print(f'Review ' + colored({id}, 'white', 'on_green') + ' is ' + colored(f'{classification}', 'red'))
            else:
                print(f'Review ' + colored({id}, 'white', 'on_red') + ' is ' + colored(f'{classification}', 'red'))





if __name__ == '__main__':
    main()