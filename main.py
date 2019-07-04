import time
from selenium import webdriver
import sys
import os
import re
from getpass import getpass
import html5lib
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import traceback
import requests
import getopt
import argparse
from joblib import Parallel, delayed

def setDriver(options=None):
    driver = webdriver.Chrome(executable_path='./chromedriver',options=options)
    return driver

def twitterLogin(userID, password,driver):
    driver.get("https://twitter.com")
    userID_box = driver.find_element_by_name("session[username_or_email]")
    driver.execute_script('document.getElementsByName("session[username_or_email]")[0].setAttribute("value","' + userID + '");')
    password_box = driver.find_element_by_name("session[password]")
    driver.execute_script('document.getElementsByName("session[password]")[0].setAttribute("value","' + password + '");')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        userID_box.submit()
        
        pattern = re.compile("https://twitter.com/login/")
        find_login_err = pattern.match(driver.current_url)
        if find_login_err != None:
            sys.stderr.write("wrong userID or password")
            driver.quit()
            #sys.exit(1)
    except:
        print("hoge")
        sys.exit()

def download_img(url,file_dir):
    r = requests.get(url, stream=True)
    file_name = file_dir + url.split('/')[-1]
    if r.status_code == 200 and (not os.path.exists(file_name)):
        with open(file_name, 'wb') as f:
            f.write(r.content)
    elif os.path.exists(file_name):
        print("")
        print("'{0}'is already exist".format(file_name))

def multi_download(url, get_limit, file_dir):
        download_img(url,file_dir)

def get_urls(tweet, picture_urls,flags):
    date = tweet.find('a',class_='tweet-timestamp')['title']
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

def get_limit_number(limit_number):
    if limit_number == "":
        limit_number = 20
    elif limit_number.isdecimal():
        limit_number = int(limit_number)
    else:
        print("wrong format")
        sys.exit(1)
    return limit_number

def arg_parser(flags):
    parser = argparse.ArgumentParser(description="This is the program for download from tweet with picture")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-H', "--head",
            help='display browser.(default:False)',
            action = "store_false",default = True)
    parser.add_argument("--parallel",
            help='Parallelize download.(default:False)',
            action = "store_true",default = False)
    parser.add_argument('-f', "--followers",
            help='adapt to followers tweet.(default:False)',
            action = "store_true")
    group.add_argument('-m', "--media",
            help='download target\'s media tweet. Don\'t use with -l option. (default:False)',
            action = "store_true",default = False)
    group.add_argument('-l', "--likes",
            help='download target\'s likes tweet. Don\'t use with -m option.(default:True)',
            action = "store_true",default = True)
    parser.add_argument('-t', "--target",
            help='set download target.(default:i)',default = "i")
    parser.add_argument('-u',"--user",dest='UserID',
            help='set your twitter userID.',default = False)
    parser.add_argument('-p',"--password",dest='Password',
            help='set your twitter password.',default = False)
    parser.add_argument('-n','--number',dest='N',
            help='set number of download.',type=int,default = -1)
    args = parser.parse_args()
    flags['followers'] = args.followers
    flags['media'] = args.media
    flags['likes'] = args.likes
    flags['target'] = args.target
    flags['userID'] = args.UserID
    flags['password'] = args.Password
    flags['number'] = args.N
    flags['headless'] = args.head
    flags['parallel'] = args.parallel

def main():
    SYS_STATUS = 0
    flags = {'followers':False,'media':False,'likes':True,'headless':True,'target':"i",'userID':False,'password':False,'number':20, 'parallel':False}
    arg_parser(flags)
    if flags['userID'] == False or flags['password'] == False:
        userID = input('Please, input your userID:')
        password = getpass('Please, input your password:')
    else:
        userID = flags['userID']
        password = flags['password']
    if flags['number'] == -1:
        get_limit = input('Please, input number of download:')
        get_limit = get_limit_number(get_limit)
    else:
        get_limit = flags['number']
    file_dir = './pictures/'
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)

    try:
        options = Options()
        if flags['headless']:
            options.add_argument('--headless')
        driver = setDriver(options)
        
        twitterLogin(userID,password,driver)

        twitter_url = "https://twitter.com/"

        media = "/media"
        likes = "/likes"
        tweet = "/"

        if flags['likes']:
            target = likes
        elif flags['media']:
            target = media

        url = twitter_url + flags['target'] + target
        
        driver.get(url)
        
        print("Scanning Timeline...")
        i = 0
        while True:
            if len(driver.find_elements_by_css_selector(".js-stream-item.stream-item.stream-item")) >= get_limit:
                break
            media_end_elem = driver.find_element_by_css_selector("#timeline > div > div.stream > div.stream-footer > div > div.stream-end")
            if media_end_elem is None or media_end_elem.is_displayed():
                break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            i+=1

        print("Scan Complete")

        soup = BeautifulSoup(driver.page_source, "html5lib")

        timeline = soup.select(".js-stream-item.stream-item.stream-item")
        
        j = 0
        picture_urls = []
        for tweet in timeline:
            try:
                if j >= get_limit:
                    break
                get_urls(tweet, picture_urls,flags)
                j+=1
            except TypeError:
                continue
        i=0
        print("Picture downloading...")
        if flags['parallel']:
            Parallel(n_jobs=-1, verbose=10)( [delayed(multi_download)(pic_url, get_limit, file_dir) for pic_url in picture_urls[:get_limit]] )
        else:
            for pic_url in picture_urls:
                if i >= get_limit:
                    break
                download_img(pic_url,file_dir)
                print("\r{0:d}(done)/{1:d}".format(i+1,get_limit),end="")
                i+=1
            print("")
        print("Download Complete")

    except:
        print(traceback.format_exc())
        SYS_STATUS = 1

    finally:
        driver.quit()
        sys.exit(SYS_STATUS)

if __name__ == '__main__':
    main()
