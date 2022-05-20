from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

options = webdriver.FirefoxOptions()
options.add_argument("--headless")


browser = webdriver.Firefox(options=options)

#pls insert the username and password in here
userinfo = ["your hkcc student no.", "your moode password"]
save = []

def goToTakeAttendance():
    # go to today Calendar
    browser.get("https://moodle.cpce-polyu.edu.hk/calendar/view.php?view=day")
    coursesThatNeedToTakeAttendance = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='description card-block calendar_event_attendance']/a"))
    )

    # save today attendance link
    for coursesPage in coursesThatNeedToTakeAttendance:
        save.append(coursesPage.get_attribute("href"))

    # go to the cource link that need to take attendance
    for link in save:
        browser.get(link)
        try: 
            # take attendance
            toSubmit = WebDriverWait(browser, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//td[@class='statuscol cell c2 lastcol']/a"))
            )
            submitPage = toSubmit[0].get_attribute("href")
            browser.get(submitPage)
            presentButton = browser.find_element(By.CLASS_NAME, "form-check-input")
            presentButton.click()
            okButton = browser.find_element(By.ID, "id_submitbutton")
            okButton.click()
            print("take attendance ed")
        # handle situation that no need to take attendance
        except TimeoutException:
            print("no link ah")

try:
    #login
    browser.get("https://moodle.cpce-polyu.edu.hk/")
    username = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, "ctl00_ContentPlaceHolder1_UsernameTextBox"))
    )
    username[0].send_keys(userinfo[0])
    userpassword = browser.find_element_by_id('ctl00_ContentPlaceHolder1_PasswordTextBox')
    userpassword.send_keys(userinfo[1])
    login = browser.find_element_by_id("ctl00_ContentPlaceHolder1_SubmitButton")
    login.send_keys(Keys.RETURN)

    time.sleep(5)

    goToTakeAttendance()

    browser.quit()
#for logined situation
except NoSuchElementException:
    goToTakeAttendance()
    
    browser.quit()
#for can't find element
