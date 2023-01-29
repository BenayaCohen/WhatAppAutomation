import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import pyperclip
import sys
from config import CHROME_PROFILE_PATH

try:
    if sys.argv[1]:
        with open(sys.argv[1], 'r', encoding="utf-8") as f:
            groups = [group.strip() for group in f.readlines()]
except IndexError:
    print("please provide the group name")

with open("msg.txt", 'r', encoding="utf-8") as f:
    msg = f.read()

options = webdriver.ChromeOptions()
options.add_argument(CHROME_PROFILE_PATH)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

url = "https://web.whatsapp.com/"
driver.get(url)
driver.maximize_window()

for group in groups:
    search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
    search_box = WebDriverWait(driver, 60).until(
        ec.presence_of_element_located((By.XPATH, search_xpath))
    )

    search_box.clear()

    time.sleep(2)

    pyperclip.copy(group)

    search_box.send_keys(Keys.CONTROL + 'v')

    time.sleep(2)

    contact_xpath = f'//span[@title="{group}"]'

    contact = driver.find_element(By.XPATH, contact_xpath)

    contact.click()

    input_xpath = '//div[@contenteditable="true"][@data-tab="10"]'

    input_box = driver.find_element(By.XPATH, input_xpath)

    pyperclip.copy(msg)

    input_box.send_keys(Keys.CONTROL + 'v')

    time.sleep(2)

    input_box.send_keys(Keys.ENTER)

    time.sleep(2)

    attach_xpath = '//span[@data-testid="clip"][@data-icon="clip"]'
    select_image_xpath = '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
    send_btn_xpath = '//span[@data-icon="send"]'
    try:
        if sys.argv[2]:
            add_attach = driver.find_element(By.XPATH, attach_xpath)
            add_attach.click()
            time.sleep(3)

            select_image = driver.find_element(By.XPATH, select_image_xpath)
            select_image.send_keys(sys.argv[2])

            time.sleep(3)

            send_btn = driver.find_element(By.XPATH, send_btn_xpath)
            send_btn.click()
            time.sleep(2)
    except IndexError:
        pass

    time.sleep(4)

driver.quit()
