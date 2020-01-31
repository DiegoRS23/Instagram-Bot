from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import mysql.connector


def find():  # fucntion to search IG, using the search bar, particulary for an account
    search = wait.until((EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))))
    search.send_keys(SEARCH + Keys.ENTER)
    search = wait.until((EC.element_to_be_clickable((By.XPATH, "//a[@href='/{}/']".format(SEARCH)))))
    search.click()
    return;


def findtag():  # fucntion to search IG, using the search bar, particulary for a tag
    search = wait.until((EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))))
    search.send_keys(SEARCH + Keys.ENTER)
    search = wait.until((EC.element_to_be_clickable((By.XPATH, "//a[@href='/explore/tags/{}/']".format(SEARCH)))))
    search.click()
    return;


numberofposts = 0


def getnumberofpost():  # function to get the number of post from an account
    global numberofposts
    numberofposts = wait.until(EC.presence_of_element_located((By.XPATH, "//li/span[text()=' posts']/span"))).text
    numberofposts = int(numberofposts)
    return;


def clicklastpost():  # function to click on the most recent post of an account
    clickpost = wait.until((EC.element_to_be_clickable((By.XPATH, "//div[@class='eLAPa']"))))
    clickpost.click()
    return;


# login credentials
USERNAME = "enter account username here"
PASSWORD = "enter account password here"

# database so we can keep a log of what has been done
db = mysql.connector.connect(
    host="localhost",  # if you are not using localhost change appropriately
    user="enter you database user here",
    passwd="enter your database password here",
    database="enter your database name here"
)
cursor = db.cursor(buffered=True)

# create table for specific user
cursor.execute("CREATE TABLE IF NOT EXISTS {} (actionid int unsigned not null auto_increment primary key, receiver varchar(255), postliked int unsigned not null default '0', numberofpostwhenliked int unsigned not null default '0')".format(USERNAME))
db.commit()

CHOICE = input("Enter the number of the option which you desire: \n"
               "1. Like all post from a user \n"
               "2. Like post from a user \n"
               "3. Like post from a #tag \n"
               "4. Unlike post from a user \n"
               "5. Unlike all post from a user \n"
               "6. get followers \n"
               "7. check following to followers \n"
               "8. for testing purposes \n")
CHOICE = int(CHOICE)
if CHOICE == 1:
    SEARCH = input("who's post do you want to like: \n")  # what you're trying to search
    cursor.execute("insert into {} (receiver) values (%s)".format(USERNAME), ("{}".format(SEARCH)))
    db.commit()
elif CHOICE == 2:
    SEARCH = input("who's post do you want to like: \n")  # what you're trying to search
    LIKES = input("How many post do you want to like: \n")
    LIKES = int(LIKES)
elif CHOICE == 3:
    SEARCH = input("what #tag do you want to like post from: \n")

elif CHOICE == 4:
    SEARCH = input("who's post do you want to unlike: \n")

elif CHOICE == 5:
    SEARCH = input("whos post do you want to unlike: \n")

elif CHOICE == 6:
    SEARCH = 'followforfollow'

elif CHOICE == 8:
    SEARCH = input("Search for a profile: \n")

# open browser
browser = webdriver.Chrome()
browser.get('https://www.instagram.com/accounts/login/')

# delay to allow the page to load completely before we try to find any elements
wait = WebDriverWait(browser, 30)

# login to Instagram account
username = wait.until(EC.element_to_be_clickable((By.NAME, 'username')))
username.send_keys(USERNAME)
password = wait.until(EC.element_to_be_clickable((By.NAME, 'password')))
password.send_keys(PASSWORD + Keys.ENTER)

# gets rid of notification pop-up
button = wait.until((EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Not Now')]"))))
button.click()

if CHOICE == 1:  # to like all post from a user
    # search instagram and click on first result
    find()
    # get number of post the user has
    getnumberofpost()
    # click on the most recent post
    clicklastpost()
    # like post/s
    like = int(0)
    likelimit = int(200)
    while like < numberofposts and like < likelimit:  # like the post and go to the next post while the number of post and post limit is greater than how many post have been liked
        clicknext = wait.until((EC.element_to_be_clickable((By.XPATH, "//a[@class='HBoOv coreSpriteRightPaginationArrow']"))))
        button = wait.until((EC.element_to_be_clickable((By.CLASS_NAME, "fr66n"))))
        # button.click() # *commented out for testing, otherwise we would like and unlike post evertime this portion of code is ran*
        clicknext.click()
        like = like + 1
    browser.quit()

elif CHOICE == 2:  # to like post from a user
    # search instagram and click on first result
    find()
    # get number of post the user has
    getnumberofpost()
    # click on the most recent post
    clicklastpost()
    # like post/s
    like = int(0)
    likelimit = int(200)
    while like < numberofposts and like < likelimit and LIKES != 0:  # like the post and go to the next post while the number of post and post limit is greater than how many post have been liked
        clicknext = wait.until((EC.element_to_be_clickable((By.XPATH, "//a[@class='HBoOv coreSpriteRightPaginationArrow']"))))
        button = wait.until((EC.element_to_be_clickable((By.CLASS_NAME, "fr66n"))))
        # button.click()  # *commented out for testing, otherwise we would like and unlike post evertime this portion of code is ran*
        clicknext.click()
        like = like + 1
        LIKES = LIKES - 1
    cursor.execute("insert into {} (receiver,postliked,numberofpostwhenliked) values (%s, %s, %s)".format(USERNAME), ("{}".format(SEARCH), "{}".format(like), "{}".format(numberofposts)))
    db.commit()
    browser.quit()

elif CHOICE == 3:  # to like post from a hashtag
    # search instagram and click on first result
    findtag()

elif CHOICE == 4:  # to unlike post from a user
    # search instagram and click on first result
    find()
    # get number of post the user has
    getnumberofpost()
    # click on most recent post
    clicklastpost()
    # get the number of post the user had when the post were liked
    cursor.execute("select numberofpostwhenliked from {} where receiver = '{}'".format(USERNAME, SEARCH))
    numberofpostwhenliked = cursor.fetchone()
    numberofpostwhenliked = int(numberofpostwhenliked[0])
    loop = numberofposts - numberofpostwhenliked
    while loop != 0:  # go to the first post that was liked last time
        clicknext = wait.until((EC.element_to_be_clickable((By.XPATH, "//a[@class='HBoOv coreSpriteRightPaginationArrow']"))))
        clicknext.click()
        loop = loop - 1
    cursor.execute("select postliked from {} where receiver = '{}'".format(USERNAME, SEARCH))
    postliked = cursor.fetchone()
    postliked = int(postliked[0])
    while postliked != 0:  # unlike the number of post that were liked last time
        clicknext = wait.until((EC.element_to_be_clickable((By.XPATH, "//a[@class='HBoOv coreSpriteRightPaginationArrow']"))))
        button = wait.until((EC.element_to_be_clickable((By.CLASS_NAME, "fr66n"))))
        # button.click()  # *commented out for testing, otherwise we would like and unlike post evertime this portion of code is ran*
        clicknext.click()
        postliked = postliked - 1
    browser.quit()

elif CHOICE == 5:  # to unlike all post from a user
    # search instagram and click on first result
    find()
    # get number of post the user has
    getnumberofpost()
    # click on most recent post
    clicklastpost()
    # get how many times like or like all post was ran
    cursor.execute("select count(*) from {} where receiver = '{}'".format(USERNAME, SEARCH))
    lc = cursor.fetchone()
    lc = int(lc[0])
    # get the number of post when liked from most recent to least recent
    cursor.execute("select numberofpostwhenliked from {} where receiver = '{}' order by numberofpostwhenliked desc".format(USERNAME, SEARCH))
    x = cursor.fetchall()
    list(x)
    # get the number of post liked based on the order of numberofpostwhenliked, which is from most recent to least recent
    cursor.execute("select postliked from {} where receiver = '{}' order by numberofpostwhenliked desc".format(USERNAME, SEARCH))
    y = cursor.fetchall()
    list(y)
    j = [i[0] for i in x]  # number of post when liked
    k = [h[0] for h in y]  # postliked
    a = 0
    b = 0
    while lc != 0:
        loop = numberofposts - j[a]
        while loop != 0:  # go to the first post that was liked last time
            clicknext = wait.until((EC.element_to_be_clickable((By.XPATH, "//a[@class='HBoOv coreSpriteRightPaginationArrow']"))))
            clicknext.click()
            loop = loop - 1
        postliked = k[b]
        while postliked != 0:  # unlike the number of post that were liked last time
            clicknext = wait.until((EC.element_to_be_clickable((By.XPATH, "//a[@class='HBoOv coreSpriteRightPaginationArrow']"))))
            button = wait.until((EC.element_to_be_clickable((By.CLASS_NAME, "fr66n"))))
            # button.click() # *commented out for testing, otherwise we would like and unlike post evertime this portion of code is ran*
            clicknext.click()
            postliked = postliked - 1
        a = a + 1
        b = b + 1
        lc = lc - 1
    browser.quit()

elif CHOICE == 6:  # to get followers
    # search instagram and click on first result
    search = wait.until((EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))))
    search.send_keys(SEARCH + Keys.ENTER)
    search = wait.until((EC.element_to_be_clickable((By.XPATH, "//a[@href='/explore/tags/{}/']".format(SEARCH)))))
    search.click()
    # click on most recent post
    clicklastpost()
    # create database table to keep track of followers
    fff = "{}".format(USERNAME)+"fff"
    cursor.execute("CREATE TABLE IF NOT EXISTS {} (actionid int unsigned not null auto_increment primary key, dayofaction datetime not null default now(), receiver varchar(255) not null, isfollowingback boolean not null default false)".format(fff))
    db.commit()
    # set follow limit so we dont get banned
    followlimit = 30
    while followlimit != 0:
        # to follow
        follow = wait.until((EC.element_to_be_clickable((By.XPATH, "//button[@class='oW_lN sqdOP yWX7d    y3zKF     ']"))))
        follow.click()
        # to like
        button = wait.until((EC.element_to_be_clickable((By.CLASS_NAME, "fr66n"))))
        button.click()
        followlimit = followlimit - 1
        browser.implicitly_wait(5)
        # to click on next post
        clicknext = wait.until((EC.element_to_be_clickable((By.XPATH, "//a[@class='HBoOv coreSpriteRightPaginationArrow']"))))
        clicknext.click()

elif CHOICE == 7:  # to check following to followers
    # go to users profile
    profile = wait.until((EC.element_to_be_clickable((By.XPATH, "//a[@href='/{}/']".format(USERNAME)))))
    profile.click()

    # get number of people user follows
    following = wait.until(EC.presence_of_element_located((By.XPATH, "//li/a[text()=' following']/span"))).text
    following = int(following)

    # get number of people that follow user
    followers = wait.until(EC.presence_of_element_located((By.XPATH, "//li/a[text()=' followers']/span"))).text
    followers = int(followers)

    # click on following to view following list
    click = wait.until(EC.presence_of_element_located((By.XPATH, "//li/a[text()=' following']/span")))
    click.click()

    # get and store following list * in the proccess of figuring this out*
    followinglist = []
    followingcount = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "FPmhX")))
    for c in followingcount:
        # following_list = c.find_element_by_class_name("_0imsa").get_attribute("textContent")
        following_list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_0imsa"))).get_attribute("textContent")
        # following_list = c.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_0imsa"))).get_attribute("textContent")
        followinglist.append(following_list)

    for x in range(0, len(followinglist)):  # * for testing purposes to see what is scraped for the following list *
        print(followinglist[x])

elif CHOICE == 8:
    # for testing purposes
    find()
    clicklastpost()
    profilename = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nJAzx"))).get_attribute("textContent")
    print(profilename)