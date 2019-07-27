# クライアントを作成

import socket
import pickle
import sys

args = sys.argv
st = pickle.dumps(args)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # サーバを指定
    s.connect(('10.0.0.227', 20))
    # サーバにメッセージを送る
    s.sendall(st)
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    data = s.recv(1024)
    res = pickle.loads(data)
    #
    print(res)
