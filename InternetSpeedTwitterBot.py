from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

MAIL = "YOURMAIL"
USER = "@YOURUSER"
PASS = "YOURPASSWORD"
PROMISED_DOWN = 600
PROMISED_UP = 100

class InternetSpeedTwitterBot:
    def __init__(self):
        chrome_driver_path = Service("/Users/israelos/Development/chromedriver")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=chrome_driver_path, options=chrome_options)
        self.down = "--"
        self.up = "--"

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        self.driver.find_element(By.CLASS_NAME, "start-text").click()
        sleep(5)
        while self.up == "--" or self.down == "--":
            try:
                self.down = self.driver.find_element(By.CSS_SELECTOR,
                                                     ".download-speed").text
                self.up = self.driver.find_element(By.CSS_SELECTOR,
                                                   ".upload-speed").text
            except NoSuchElementException:
                print("waiting for internet speed...")
            finally:
                sleep(1)

    def tweet_at_provider(self):
        if int(self.down != PROMISED_DOWN) or int(self.up != PROMISED_UP):
            complaint = f"Hi internet-provider, why is my down-s:{self.down}, up-s:{self.up}\n while you " \
                        f"promised down-s:{PROMISED_DOWN}, up-s:{PROMISED_UP}?"
            self.driver.get("https://twitter.com/login")
            sleep(2)
            acc = self.driver.find_element(By.NAME, value="text")
            acc.send_keys(MAIL, Keys.ENTER)
            sleep(1)
            try:
                password = self.driver.find_element(By.NAME, value="password")
                password.send_keys(PASS)
                password.send_keys(Keys.ENTER)
            except NoSuchElementException:
                user = self.driver.find_element(By.NAME, value="text")
                user.send_keys(USER)
                sleep(1)
                password = self.driver.find_element(By.NAME, value="password")
                password.send_keys(PASS, Keys.ENTER)
            finally:
                sleep(4)
                tweet = self.driver.find_element(By.CSS_SELECTOR, ".public-DraftStyleDefault-block")
                tweet.send_keys(complaint)
                tweet.send_keys(Keys.COMMAND, Keys.ENTER)
