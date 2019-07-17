import config
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


class InstaBot:
    def __init__(self, username, password):
        self.bot = webdriver.Firefox()
        self.bot.set_window_size(1536, 864)
        self.username = username
        self.password = password

    def login(self):
        bot = self.bot
        bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)

        username = bot.find_element_by_name('username')
        password = bot.find_element_by_name('password')
        username.clear()
        password.clear()

        username.send_keys(self.username)
        password.send_keys(self.password)
        time.sleep(2)

        password.send_keys(Keys.RETURN)
        time.sleep(3)

        try:
            alert = bot.find_element_by_id('slfErrorAlert')
            print(alert.text)
            quit()

        except NoSuchElementException:
            print('Login Successful !')

    def like_post(self, hashtag: str, count: int = 5):
        bot = self.bot
        bot.get(f'https://www.instagram.com/explore/tags/{hashtag}')
        time.sleep(2)

        for _ in range(3):
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)

        posts = bot.find_elements_by_class_name('v1Nh3')
        links = [post.find_element_by_tag_name(
            'a').get_attribute('href') for post in posts]
        # print(len(links))

        if len(links) == 0:
            print(f"Page with hashtag '{hashtag}' does not exist")
            quit()

        for i in range(count):
            if i > 50:
                print("Could not like more than 51 posts")
                break

            bot.get(links[i])
            time.sleep(2)

            try:
                like = bot.find_element_by_class_name('dCJp8')
                label = like.find_element_by_tag_name(
                    'span').get_attribute('aria-label')

                if label == 'Unlike':
                    print(f"Post {i+1} already liked.")
                    continue

                like.click()
                print("Liked post", i+1)
                time.sleep(2)

            except:
                print(f"Could not like post {i+1}")

    def close_bot(self):
        self.bot.close()


if __name__ == '__main__':
    username = config.username
    password = config.password

    try:
        tag = input('Hashtag: ')
        tag = ''.join(e for e in tag if e.isalnum())
        count = int(input('Count [max=50]: '))

    except ValueError:
        print('Error: Count must be an integer')
        quit()

    print('Starting...')

    try:
        shubbi = InstaBot(username, password)
        shubbi.login()
        shubbi.like_post(tag, count)

    except Exception as E:
        print("Error occured: ", E)

    else:
        print('Done !')

    finally:
        shubbi.close_bot()
