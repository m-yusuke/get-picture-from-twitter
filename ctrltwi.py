from selenium import webdriver
import chromedriver_binary
import re


def setDriver(options=None):
    driver = webdriver.Chrome(options=options)
    return driver


def twitterLogin(user_info, driver, flags):
    driver.get("https://twitter.com")
    userID_box = driver.find_element_by_name("session[username_or_email]")
    driver.execute_script(
            'document.getElementsByName\
                    ("session[username_or_email]")[0]\
                    .setAttribute("value","'
            + user_info['userID'] + '");'
            )
    password_box = driver.find_element_by_name("session[password]")
    driver.execute_script(
            'document.getElementsByName\
                    ("session[password]")[0].setAttribute("value","'
            + user_info['password'] + '");'
            )
    driver.execute_script("window.scrollTo(0, \
            document.body.scrollHeight);")
    userID_box.submit()

    pattern = re.compile(".*login.*")
    find_login_err = pattern.match(driver.current_url)
    if find_login_err:
        print("wrong userID or password")
        print("Please try again")

        flags['login_retry'] = True

        return -1
    else:
        print("Login succeeded!")

        return 0


def get_urls(tweet, picture_urls, flags):
    date = tweet.find('a', class_='tweet-timestamp')['title']
    img = tweet.find_all('div', class_='js-adaptive-photo')
    tweet_data = tweet.find(class_='tweet')
    follower = tweet_data['data-follows-you']
    if 'data-retweeter' in tweet_data:
        print(tweet_data['data-retweeter'])
    if follower == "true" and not flags['followers']:
        return
    userName = tweet_data['data-name']
    for pic_url in img:
        picture_urls.append(pic_url['data-image-url'])
