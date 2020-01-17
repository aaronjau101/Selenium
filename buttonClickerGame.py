from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def openChrome():
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(options=options)
    return driver

def clickButton(driver):
    button = driver.find_element_by_class_name("button")
    print("Starting 1000 left clicks")
    for i in range(1000):
        button.click()
    print("Finished 1000 left clicks")
    actions = webdriver.ActionChains(driver)
    actions.move_to_element(button)
    print("Starting 3 right clicks")
    for i in range(3):
        actions.context_click(button)
    actions.perform()
    print("Finished 3 right clicks")

def scroll(driver):
    print("Scrolling to all sides of the document")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, 0);")
    driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);")
    driver.execute_script("window.scrollTo(0, 0);")

def moveAround(driver):
    button = driver.find_element_by_class_name("button")
    body = driver.find_element_by_tag_name("body")
    sw = list(body.get_property("width"))
    sh = list(body.get_property("height"))
    w = int(''.join(sw[0:-2]))
    h = int(''.join(sh[0:-2]))
    print("w: " + str(w))
    print("h: " + str(h))
    print("Moving to button")
    actions = webdriver.ActionChains(driver)
    actions.move_to_element(button)
    actions.move_by_offset(w/2, h/2)
    actions.move_by_offset(0, -h)
    actions.move_by_offset(-w, 0)
    actions.move_by_offset(0, h)
    actions.move_by_offset(w, 0)
    actions.move_by_offset(-w, -w)
    actions.perform()

def screenshotAchievements(driver):
    button = driver.find_element_by_class_name("progress")
    button.click()
    driver.save_screenshot('screenshot.png')

def main():
    start_time = time.time()
    driver = openChrome()
    #driver.maximize_window()
    driver.get("https://clickclickclick.click/")
    scroll(driver)
    moveAround(driver)
    clickButton(driver)
    screenshotAchievements(driver)
    driver.quit()
    print("Program took " + str(time.time() - start_time) + " seconds")


if __name__ == '__main__':
    main()
