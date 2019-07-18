# PyPI Library
import html5lib
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from joblib import parallel_backend, Parallel, delayed
# standard Library
import sys
import os
import traceback
# my module
import ctrltwi
import downloader
import storeinfo
import argparser
import send


def main():
    SYS_STATUS = 0
    flags = {
            'followers': False,
            'media': False,
            'likes': True,
            'headless': True,
            'target': "i",
            'userID': False,
            'password': False,
            'number': 20,
            'parallel': False,
            'thread': False,
            'login_retry': False,
            'dir': "./pictures/",
            'dop': -1,
            'remote': False,
            'address': []
            }
    argparser.arg_parser(flags)
    options = Options()
    if flags['headless']:
        options.add_argument('--headless')
    driver = ctrltwi.setDriver(options)

    file_dir = flags['dir']

    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    elif not os.path.isdir(file_dir):
        print("{0} is not directory.".format(file_dir))
        sys.exit(1)

    login_status = -1

    while login_status == -1:
        user_info = storeinfo.store_Id_Password(flags)
        login_status = ctrltwi.twitterLogin(user_info, driver, flags)

    if flags['number'] == -1:
        get_limit = input('Please, input number of download:')
        get_limit = storeinfo.get_limit_number(get_limit)
    else:
        get_limit = flags['number']

    try:
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
        
        ctrltwi.scan_timeline(get_limit,driver)

        print("Scan Complete")

        soup = BeautifulSoup(driver.page_source, "html5lib")

        timeline = soup.select(".js-stream-item.stream-item.stream-item")

        j = 0
        picture_urls = []
        for tweet in timeline:
            try:
                if j >= get_limit:
                    break
                ctrltwi.get_urls(tweet, picture_urls, flags)
                j += 1
            except TypeError:
                continue
        i = 0
        print("Picture downloading...")
        if flags['remote']:
            urlfile = "tmp.txt"
            with open(urlfile, 'w') as f:
                for pic_url in picture_urls:
                    f.write(pic_url + '\n')

            #send.send_file_master(flags, urlfile)

        elif flags['parallel']:
            if flags['thread']:
                parallelize = 'threading'
            else:
                parallelize = 'loky'
            downloader.parallel_proc(
                    parallelize,
                    picture_urls,
                    get_limit,
                    file_dir,
                    flags['dop']
                    )
        else:
            for pic_url in picture_urls:
                if i >= get_limit:
                    break
                downloader.download_img(pic_url, file_dir)
                print("\r{0:d}(done)/{1:d}".format(i+1, get_limit), end="")
                i += 1
            print("")
        print("Download Complete")

    except Exception:
        print(traceback.format_exc())
        SYS_STATUS = 1

    finally:
        driver.quit()
        sys.exit(SYS_STATUS)


if __name__ == '__main__':
    main()
