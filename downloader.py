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

def parallel_proc(parallelize, picture_urls, get_limit, file_dir, degree_of_parallelism):
    with parallel_backend(parallelize, n_jobs=degree_of_parallelism):
                Parallel(verbose=10)(
                        [delayed(multi_download)(
                            pic_url,
                            get_limit,
                            file_dir
                            )
                            for pic_url in picture_urls[:get_limit]])

if __name__ == '__main__':
    import sys
    args = sys.argv
    file_dir = "../tmp"
    if len(args) < 2:
        print("file not inputted")
    else:
        if os.path.exists(args[1]):
            with open(args[1], 'r') as f:
                picture_urls = [s.strip() for s in f.readlines()]
                for pic_url in picture_urls:
                    download_img(pic_url, file_dir)
        else:
            print("No such file or directory")
