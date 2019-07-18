import config
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from getpass import getpass
import time


class InstaBot:
    # Constructor
    def __init__(self, username, password):
        self.bot = webdriver.Firefox()
        # Provide your display resolution here
        self.bot.set_window_size(1536, 864)
        self.username = username
        self.password = password

    def login(self):
        bot = self.bot
        bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)

        # Finds the required input boxes
        username = bot.find_element_by_name('username')
        password = bot.find_element_by_name('password')

        # Clears any previous input
        username.clear()
        password.clear()

        # Sends login credentials to the input boxes
        username.send_keys(self.username)
        password.send_keys(self.password)
        time.sleep(2)

        password.send_keys(Keys.RETURN)
        time.sleep(3)

        # Check for invalid login credentials
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

        # Scroll 3 times
        for _ in range(3):
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)

        posts = bot.find_elements_by_class_name('v1Nh3')  # All posts
        links = [post.find_element_by_tag_name(
            'a').get_attribute('href') for post in posts]  # Links of all posts
        # print(len(links))

        # Check if the hashtag page exists
        if len(links) == 0:
            print(f"Page with hashtag '{hashtag}' does not exist")
            quit()

        # iterate over the posts
        for i in range(count):
            if i > 50:
                print("Could not like more than 51 posts")
                break

            bot.get(links[i])  # Opens a post
            time.sleep(2)

            # Likes a post
            try:
                like = bot.find_element_by_class_name('dCJp8')

                # Check if post is already liked
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

    # Closes the bot
    def close_bot(self):
        self.bot.close()


if __name__ == '__main__':
    # Input login credentials
    username = input('\nEnter Username/Email/Mobile: ')
    password = getpass('Enter Password: ')

    try:
        tag = input('\nHashtag: ')   # Hashtag to search
        tag = ''.join(e for e in tag if e.isalnum())
        count = int(input('Count [max=50]: '))  # No. of posts to like

    except ValueError:
        print('\nError: Count must be an integer')
        quit()

    print('\nStarting...\n')

    try:
        user = InstaBot(username, password)  # Instantiate a bot
        user.login()  # Login user
        user.like_post(tag, count)  # Like posts

    except Exception as E:
        print("Error occured: ", E)

    # If no error occurs
    else:
        print('Done !')

    # Finally closes the bot
    finally:
        user.close_bot()
