from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def openChrome():
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(options=options)
    return driver

def loginReddit(driver, un, pw):
    print("Logging in to Reddit account: " + un)
    loginUN = driver.find_element_by_id("loginUsername")
    loginUN.clear()
    loginUN.send_keys(un)
    loginPW = driver.find_element_by_id("loginPassword")
    loginPW.clear()
    loginPW.send_keys(pw)
    loginPW.send_keys(Keys.RETURN)
    time.sleep(3)
    
    

def searchReddit(driver, string):
    print("Searching Reddit for the phrase: " + string)
    elem = driver.find_element_by_id("header-search-bar")
    elem.clear()
    elem.send_keys(string)
    elem.send_keys(Keys.RETURN)
    time.sleep(3)
    assert string in driver.title

def downvoteAll(driver):
    count = 0
    skip = False;
    buttons = driver.find_elements_by_class_name("voteButton")
    for button in buttons:
        if button.get_attribute("aria-label").lower() == "downvote":
            if skip == False:
                count+=1             
                button.click()
                father = button.find_element_by_xpath('..')
                grandfather = father.find_element_by_xpath('..')
                greatgrandfather = grandfather.find_element_by_xpath('..')
                title =  greatgrandfather.find_element_by_tag_name("h3")
                print("Downvoted post: " + title.text)
            skip = not skip;
    print("Downvoted " + str(count) + " post")
            
        

def main():
    driver = openChrome()
    driver.get("https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F")
    loginReddit(driver, "username", "password")
    searchReddit(driver, "phrase")
    downvoteAll(driver)
    driver.quit()


if __name__ == '__main__':
    main()
