import requests
import os
from joblib import parallel_backend, Parallel, delayed


def download_img(url, file_dir):
    r = requests.get(url, stream=True)
    if file_dir[-1] != "/":
        file_dir += "/"
    file_name = file_dir + url.split('/')[-1]
    if r.status_code == 200 and (not os.path.exists(file_name)):
        with open(file_name, 'wb') as f:
            f.write(r.content)
    elif os.path.exists(file_name):
        print("")
        print("'{0}'is already exist".format(file_name))


def multi_download(url, get_limit, file_dir):
    download_img(url, file_dir)

def parallel_proc(parallelize, picture_urls, get_limit, file_dir):
    with parallel_backend(parallelize, n_jobs=-1):
                Parallel(verbose=10)(
                        [delayed(multi_download)(
                            pic_url,
                            get_limit,
                            file_dir
                            )
                            for pic_url in picture_urls[:get_limit]])
