from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def openChrome():
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(options=options)
    return driver

def loginSpotify(driver, un, pw):
    print("Logging in to Spotify")
    loginUN = driver.find_element_by_id("login-username")
    loginUN.clear()
    loginUN.send_keys(un)
    loginPW = driver.find_element_by_id("login-password")
    loginPW.clear()
    loginPW.send_keys(pw)
    loginPW.send_keys(Keys.RETURN)
    time.sleep(3)

def createPlaylist(driver, title):
    print("Creating Spotify playlist: " + title)
    button = driver.find_element_by_class_name("CreatePlaylistButton")
    button.click()
    time.sleep(1)
    elem = driver.find_element_by_class_name("inputBox-input")
    elem.clear()
    elem.send_keys(title)
    elem.send_keys(Keys.RETURN)
    time.sleep(3)

def findAllTracks(driver):
    print("Finding All Tracks")
    tracks = []
    count = 0
    trackDivs = driver.find_elements_by_class_name("tracklist-item__wrapper")
    for t in trackDivs:
        atags = t.find_elements_by_tag_name("a")
        for i in range(len(atags) - 1):
            name = atags[i].text
            artist = atags[i+1].text
            tracks.append([name, artist])
            count+=1
    print("Found " + str(count) + " tracks")
    return tracks

def addAllTracks(driver, tracks, title):
    searchBar = driver.find_element_by_class_name("_2f8ed265fb69fb70c0c9afef329ae0b6-scss")
    count = 0
    print("Adding All Tracks to Playlist")
    for t in tracks:
        search = t[0] + " " + t[1]
        searchBar.clear()
        searchBar.send_keys(search)
        searchBar.send_keys(Keys.RETURN)
        time.sleep(1)
        if noResult(driver) == True or noSongs(driver) == True:
            print("No result for song: " + t[0])
        else:
            print("Trying to add song: " + t[0])
            count += addSongToPlaylist(driver, title)
    print("Finished! Added " + str(count) + " songs to playlist")

def addSongToPlaylist(driver, title):
    songs = DTAN(driver, "section", "aria-label", "Songs")
    if songs == None:
        print("Finding songs failed")
        return 0
    
    song = DTAN(songs, "div", "draggable", "true")
    if song == None:
        print("Finding song failed")
        return 0
    
    actions = webdriver.ActionChains(driver)
    actions.context_click(song)
    actions.perform()
    time.sleep(1)
    button = DCT(driver, "react-contextmenu-item", "Add to Playlist")
    if button == None:
        print("Add to Playlist failed")
        return 0
    
    button.click()
    time.sleep(1)
    playlistTitle = DTT(driver, "span", title)
    if playlistTitle == None:
        print("Finding Playlist failed")
        return 0

    playlist = findAncestor(playlistTitle, 4)
    playlistArt = playlist.find_element_by_class_name("cover-art")
    playlistArt.click()
    print("Success!")
    return 1
    
def findAncestor(child, generations):
    result = child
    for i in range(generations):
        result = result.find_element_by_xpath('..')
    return result

def DTT (driver, tag, text):
    elements = driver.find_elements_by_tag_name(tag)
    for element in elements:
        if element.text == text:
            return element
    return None

def DCT (driver, className, text):
    elements = driver.find_elements_by_class_name(className)
    for element in elements:
        if element.text == text:
            return element
    return None

def DTAN (driver, tag, attribute, name):
    elements = driver.find_elements_by_tag_name(tag)
    for element in elements:
        if element.get_attribute(attribute) == name:
            return element
    return None

def noSongs(driver):
    h2s = driver.find_elements_by_tag_name("h2")
    for h2 in h2s:
        if h2.text == "Songs":
            return False
    return True


def noResult(driver):
    h1s = driver.find_elements_by_tag_name("h1")
    prompt = "No results found for "
    for h1 in h1s:
        txt = h1.text
        t = txt[0:len(prompt)]
        if t == prompt:
            return True
    return False

def main():
    driver = openChrome()
    print("Opening Apple Playlist")
    driver.get("apple-playlist-link")
    title = driver.find_element_by_class_name("product-header__title").text
    tracks = findAllTracks(driver)
    driver.get("https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2F")
    loginSpotify(driver, "username", "password")
    createPlaylist(driver, title)
    driver.get("https://open.spotify.com/search")
    addAllTracks(driver, tracks, title)
    driver.quit()


if __name__ == '__main__':
    main()
