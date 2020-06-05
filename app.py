import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from getpass import getpass
import os
from sys import platform
import time


class InstaBot:
    # Constructor
    def __init__(self, username, password):
        self.bot = webdriver.Firefox()
        self.bot.set_window_size(1536, 864)  # Maximize window
        self.username = username
        self.password = password

    def login(self):
        bot = self.bot
        bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)

        # Finds the required input fields
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
            raise Exception(alert.text)

        except NoSuchElementException:
            print('User logged in!')

    def like_post(self, hashtag: str, count: int = 5):
        bot = self.bot
        bot.get(f'https://www.instagram.com/explore/tags/{hashtag}')
        time.sleep(2)

        # Scroll
        scroll_count = 2
        for _ in range(scroll_count):
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(1)

        posts = bot.find_elements_by_class_name('v1Nh3')  # All posts
        links = [post.find_element_by_tag_name(
            'a').get_attribute('href') for post in posts]  # Links of all posts

        # --------- Debug ----------------
        print({'Scrolls': scroll_count,
               'Posts': len(posts),
               'Links': len(links)})
        print()

        # Check if the hashtag page exists
        if len(links) == 0:
            raise Exception(f"Page with hashtag '{hashtag}' does not exist")

        # iterate over the posts
        for i in range(count):
            if i > 50:
                print("Could not like more than 51 posts")
                break

            bot.get(links[i])  # Opens a post
            time.sleep(2)

            # Likes a post
            try:
                like_btn = bot.find_element_by_class_name('wpO6b')

                # Check if post is already liked
                label = like_btn.find_element_by_tag_name(
                    'svg').get_attribute('aria-label')
                if label == 'Unlike':
                    print(f"Post {i+1} already liked.")
                    continue

                like_btn.click()
                print("Liked post", i+1)
                time.sleep(2)

            except Exception as e:
                print(f"Could not like post {i+1}")
                raise Exception(e)  # For Debugging purposes

    # Closes the bot
    def close_bot(self):
        self.bot.close()


# Driver Code
if __name__ == '__main__':
    # Input login credentials
    username = input('\nEnter Username/Email/Mobile: ')
    password = getpass('Enter Password: ')

    if username == 'me' and password == 'me' and os.path.exists('config.py'):
        import config
        username = config.username
        password = config.password

    try:
        tag = input('\nHashtag: ')
        count = int(input('Count: '))

        tag = ''.join(e for e in tag if e.isalnum())

    except ValueError:
        print('\nError: Count must be an integer')
        try:
            count = int(input('Count: '))
        except ValueError:
            print('\nSorry, you entered a wrong count....Quitting!')
            time.sleep(5)
            quit()

    print('\nStarting the bot...\n')

    try:
        bot = InstaBot(username, password)  # Instantiate a bot object
        bot.login()  # User login
        bot.like_post(tag, count)  # Like posts

    except Exception as E:
        print("Error - ", E)

    # If no error occurs
    else:
        print('Done !')

    # Finally closes the bot
    finally:
        time.sleep(1)
        bot.close_bot()
