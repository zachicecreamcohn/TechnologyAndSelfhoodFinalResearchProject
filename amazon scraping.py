
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
from time import sleep
from termcolor import colored

def sqlSetup():
    con = psycopg2.connect(database="d76lmct1719stp", user="llubxiofuwfmlc", password="24cf674cbeb374d5dc9839cea64382fb29e952403b9c64f99a1411c5ba9af389", host="ec2-54-205-61-191.compute-1.amazonaws.com", port="5432")
    con.autocommit = True
    global cur
    cur = con.cursor()

binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\\geckodriver.exe')
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

star = 5.0


def go_to_page(star, page_number):
    if star == 5.0:
        star = "&filterByStar=five_star"
    if star == 4.0:
        star = "&filterByStar=four_star"
    if star == 3.0:
        star = "&filterByStar=three_star"
    if star == 2.0:
        star = "&filterByStar=two_star"
    if star == 1.0:
        star = "&filterByStar=one_star"


    URL = f'https://www.amazon.com/product-reviews/B074WC9YKL/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8{star}&reviewerType=all_reviews&sortBy=recent&pageNumber={page_number}'
    driver.get(URL)
    # driver.maximize_window()
    driver.implicitly_wait(.5)


def find_comments():
    return driver.find_elements_by_xpath("//*[@class='a-section review aok-relative']")
    # return driver.find_elements_by_class_name('a-size-base review-text review-text-content')

list_of_tuples = []
def parse_comments():
    sqlSetup()

    reviews = find_comments()
    for review in reviews:
        comment_date = review.find_element_by_xpath(".//*[@class='a-size-base a-color-secondary review-date']").text
        comment_body = review.find_element_by_xpath(".//*[@class='a-size-base review-text review-text-content']").text

        if "'" in comment_body:
            comment_body = comment_body.replace("'", r"''")

        list_of_tuples.append((comment_body, comment_date, star))
        
    if len(reviews) == 0:
        return 'no reviews'
    else:
        return 'done'

def main():
    for i in range(1, 20):
        go_to_page(star, i)
        if parse_comments() == 'no reviews':
            try:
                for i in list_of_tuples:
                    cur.execute(f"INSERT INTO CWP (review_body, review_date, rating) VALUES ('{i[0]}', '{i[1]}', {i[2]})" )
                    print(colored(f'Inserted Review {list_of_tuples.index(i)} Into Database', 'blue')) 
                print(colored('Database Update COMPLETE', 'blue'))
            except Exception as e:
                print(colored(f'ERROR:\n\n{e}'),"red")
            driver.quit()
            break
        else:
            print(colored(f'Page {i} done', "green"))
            # If on the last page, but there are still reviews, insert all reviews here.
            if i == 19: # last page of reviews
                print(colored("There are still reviews left, but you specified that this be the last page looked at", 'magenta'))
                try:
                    for i in list_of_tuples:
                        cur.execute(f"INSERT INTO CWP (review_body, review_date, rating) VALUES ('{i[0]}', '{i[1]}', {i[2]})" )
                        print(colored(f'Inserted Review {list_of_tuples.index(i)} Into Database', 'blue')) 
                    print(colored('Database Update COMPLETE', 'blue'))
                except Exception as e:
                    print(colored(f'ERROR:\n\n{e}'),"red")
                driver.quit()
                break
            
        sleep(5)

    
    


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        driver.close()
        