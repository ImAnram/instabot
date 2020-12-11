# My selenium project

from selenium import webdriver
from selenium.webdriver.chrome import options
from time import sleep
from datetime import datetime
import random
random.seed()


class InstagramBot:
    def __init__(self, mod='pc'):
        self.time = {
            'start': datetime.now(),
            'comment': datetime.now(),
            'like': datetime.now(),
            'follow': datetime.now()
        }
        option = options.Options()
        option.add_argument("--log-level=3")
        option.add_argument("--silent")
        # option.add_argument("--headless")
        if mod == 'mobile':
            mobile_tem = {"deviceName": "Nexus 5"}
            option.add_experimental_option("mobileEmulation", mobile_tem)
        self.driver = webdriver.Chrome(options=option)
        # self.driver = webdriver.Firefox()

    def login(self, username, password):
        self.driver.get(r'https://www.instagram.com/accounts/login/')
        sleep(1)
        use = self.driver.find_element_by_xpath(r'//input[@name="username"]')
        use.clear()
        use.send_keys(username)
        pas = self.driver.find_element_by_xpath(r'//input[@name="password"]')
        pas.send_keys(password)
        self.driver.find_element_by_xpath(r'//button[@type="submit"]').click()
        sleep(10)
        self.driver.get(f"https://www.instagram.com/{username}/")

    def __urls(self, tag, mod):
        if mod == 'search':
            self.driver.get('https://www.instagram.com/explore/')
        elif mod == 'hashtag':
            self.driver.get(f'https://www.instagram.com/explore/tags/{tag}/')
        elif mod == 'user':
            self.driver.get(f'https://www.instagram.com/{tag}/')
        else:
            self.quit()

    def __link(self, tags, num, mod):
        tags = tags if type(tags) != str else tags.split()
        links = []
        num1, len_link = 0, 0
        for tag in tags:
            if mod != 'message':
                self.__urls(tag, mod)
            scroll, full = 0, 0
            num1 += num / len(tags)
            while num1 > len(links):
                scroll += 5000
                sleep(0.8)
                link = self.driver.find_elements_by_tag_name('a')
                links += (li.get_attribute('href') for li in link)
                self.driver.execute_script(f'scroll({scroll-5000},{scroll})')
                text_filter = '/' if mod == 'message' else '.com/p/'
                links = filter(lambda l: text_filter in l, links)
                sleep(0.3)
                links = list(set(links))
                if len(links) == len_link:
                    full += 1
                    if full == 3:
                        break
                len_link = len(links)

        return links

    def __like(self):
        like_button = self.driver.find_element_by_css_selector('#react-root \
                       > section > main > div > div.ltEKP > article > \
                       div.eo2As > section.ltpMr.Slqrh > span.fr66n > button')
        like_svg = like_button.find_element_by_tag_name('svg')
        if like_svg.get_attribute('fill') == '#262626':
            like_button.click()

    def __follow(self):
        selector = '#react-root > section > main > div > div.ltEKP > article > \
                        header > div.o-MQd > div.PQo_0 > div.bY2yH > button'
        foll = self.driver.find_element_by_css_selector(selector)
        if foll.text == 'Follow':
            foll.click()

    def __comment(self, comment):
        button_comment = '#react-root > section > main > div > div.ltEKP > \
                        article > div.eo2As > section.ltpMr.Slqrh > \
                        span._15y0l > button'
        self.driver.find_element_by_css_selector(button_comment).click()
        text_in = '#react-root > section > main > div > div.ltEKP > \
                        article > div.eo2As > section.sH9wk._JgwE > div > \
                        form > textarea'
        com = self.driver.find_element_by_css_selector(text_in)
        if len(comment) > 1:
            comment1 = random.choice(comment)
        else:
            comment1 = comment[0]
        com.send_keys(comment1)
        self.driver.find_element_by_xpath(r'//button[@type="submit"]').click()

    def __job(self, links, like=True, follow=False, comment=None, time=40):
        for lin in links:
            self.driver.get(lin)
            if like:
                self.__like()
            if comment:
                if self.time['comment'].minute + 1 <= datetime.now().minute:
                    self.__comment(comment)
                    self.time['comment'] = datetime.now()
            if follow:
                if self.time['follow'].minute + 6 <= datetime.now().minute:
                    self.__follow()
                    self.time['follow'] = datetime.now()
            sleep(random.randint(time-10, time))

    def tag(self, tags, num, like=True, follow=False, comments=None):
        links = self.__link(tags, num, 'hashtag')
        self.__job(links, like, follow, comments)

    def user(self, users, num, like=True, comments=None):
        links = self.__link(users, num, 'user')
        self.__job(links, like, comments)

    def search(self, num, like=True, follow=False, comments=None):
        links = self.__link([0], num, 'search')
        self.__job(links, like, follow, comments)

    def __follow_ers_or_ing(self, user, fol):
        self.driver.get(f"https://www.instagram.com/{user}/")
        sleep(2)
        all_options = self.driver.find_elements_by_tag_name('a')
        for option in all_options:
            if fol in option.get_attribute('href'):
                option.click()
                break

    def follow(self, user, fol='followers', unfollow=False):
        text = 'Following' if unfollow else 'Follow'
        self.__follow_ers_or_ing(user, fol)
        sleep(3)
        buttons = self.driver.find_elements_by_tag_name('button')
        for button in buttons:
            if button.text == text:
                button.click()
                sleep(200)
                if text == 'Following':
                    un = '/html/body/div[5]/div/div/div/div[3]/button[1]'
                    self.driver.find_element_by_xpath(un).click()

    def message(self, user, num, fol='followers'):
        self.__follow_ers_or_ing(user, fol)
        links = self.__link([0], num, 'message')

    def quit(self):
        self.driver.quit()
