
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
from time import sleep


def sqlSetup():
    con = psycopg2.connect(database="d76lmct1719stp", user="llubxiofuwfmlc", password="24cf674cbeb374d5dc9839cea64382fb29e952403b9c64f99a1411c5ba9af389", host="ec2-54-205-61-191.compute-1.amazonaws.com", port="5432")
    con.autocommit = True
    global cur
    cur = con.cursor()

binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\\geckodriver.exe')
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

star = 1.0

URL = "https://www.google.com/search?q=food+near+me&hl=en&sxsrf=AOaemvKpZYzUhdm_t-0JE_ppFdAKcxVtJA%3A1635873582810&source=hp&ei=LnOBYc2xLZqO9PwPoIOdsA4&iflsig=ALs-wAMAAAAAYYGBPp_vXfkG6xbDR6H9VmSQTqDpcvAZ&oq=food+near+me&gs_lcp=Cgdnd3Mtd2l6EAMyBwgjEMkDECcyBQgAEJIDMgUIABCSAzIFCAAQgAQyCAgAEIAEELEDMgUIABCABDIFCAAQgAQyCggAEIAEEIcCEBQyBQgAEIAEMgUIABCABDoECCMQJzoECAAQQzoHCAAQsQMQQzoKCC4QxwEQowIQQzoRCC4QgAQQsQMQgwEQxwEQ0QM6DQgAEIAEEIcCELEDEBQ6CwguELEDEMcBEKMCOgcIABCABBAKUJAGWJsQYOwQaABwAHgCgAH8AYgBpQmSAQU5LjIuMZgBAKABAQ&sclient=gws-wiz&ved=0ahUKEwjNgLD-l_rzAhUaB50JHaBBB-YQ4dUDCAo&uact=5"
def go_to_page():

    driver.get(URL)
    # driver.maximize_window()
    driver.implicitly_wait(5)


def click_first_option():
    driver.find_element_by_xpath("//*[@class='VkpGBb']").click()
def open_reviews():
    try:
        reviews_button = driver.find_element_by_partial_link_text('Google reviews')
        if reviews_button:
            reviews_button.click()
            return 'Reviews Button Clicked'	
    except Exception as e:
        print(e)

    # driver.find_element_by_xpath("//*[@data-async-trigger='reviewDialog']").click()

def get_reviews():
    return driver.find_elements_by_xpath("//*[@jscontroller='MZnM8e']")

def parse_reviews():
    reviews = get_reviews()
    for review in reviews:
        print(review.text)

def scroll_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)
# def parse_comments():
#     sqlSetup()

#     reviews = find_comments()
#     for review in reviews:
#         comment_date = review.find_element_by_xpath(".//*[@class='a-size-base a-color-secondary review-date']").text
#         comment_body = review.find_element_by_xpath(".//*[@class='a-size-base review-text review-text-content']").text

#         if "'" in comment_body:
#             comment_body = comment_body.replace("'", r"''")
#         cur.execute(f"INSERT INTO CWP (review_body, review_date, rating) VALUES ('{comment_body}', '{comment_date}', {star})" )
#     if len(reviews) == 0:
#         return 'no reviews'
#     else:
#         return 'done'

def main():
    go_to_page()
    click_first_option()
    while open_reviews() != 'Reviews Button Clicked':
        try:
            open_reviews()
        except:
            print('error')
        sleep(1)
    try:
        while True:
            parse_reviews()
            scroll_down()
            sleep(1)
    except:
        print('done')

    
    


if __name__ == "__main__":
    try:

        main()
    except Exception as e:
        print(e)
        # driver.close()
        