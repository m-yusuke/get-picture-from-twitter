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
            'dir': "./pictures/"
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
        i = 0
        while True:
            if len(driver.find_elements_by_css_selector(
                    ".js-stream-item.stream-item.stream-item"
                    )) >= get_limit:
                break
            media_end_elem = driver.find_element_by_css_selector(
                    "#timeline > div > div.stream > div.stream-footer \
                    > div > div.stream-end")
            if media_end_elem is None or media_end_elem.is_displayed():
                break
            driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                    )
            i += 1

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
        if flags['parallel']:
            if flags['thread']:
                parallelize = 'threading'
            else:
                parallelize = 'loky'
            with parallel_backend(parallelize, n_jobs=-1):
                Parallel(verbose=10)(
                        [delayed(downloader.multi_download)(
                            pic_url,
                            get_limit,
                            file_dir
                            )
                            for pic_url in picture_urls[:get_limit]])
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
