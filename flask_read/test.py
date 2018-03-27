'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/21/下午1:30
file:test.py
IDE:PyCharm 
'''

from flask import Flask

app = Flask(__name__)  # 生成app实例


@app.route('/')
def index():
    return 'Hello World'