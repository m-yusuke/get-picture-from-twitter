from joblib import parallel_backend, Parallel, delayed
import subprocess

def send_file_slave(address, file_name):
    subprocess.run(["rsync", "-auvzP",file_name, address + ":/home/e175703/practice/get-picture-from-twitter/"])

def send_file_master(flags, file_name):
    with parallel_backend('loky', n_jobs=-1):
        Parallel(verbose=10)(
                [delayed(send_file_slave)(
                    address, file_name
                    )
                    for address in flags['address']])
