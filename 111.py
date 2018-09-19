##liuhuihui 1-5 plan
###see https://blog.csdn.net/typing_yes_no/article/details/51758938
'''
WebSocketApp是websocket的一个类
封装了websocket里面的connect、send消息等函数,更方便于调用
'''
import websocket
import json
import redis
import threading
import threadpool

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)  ##decode_response=True，写入的键值对中的value为str类型,无则为字节类型

r = redis.Redis(connection_pool=pool)



##全局变量 币对
SYMBOL_LIST= ['ETHBTC','LTCBTC','NEOBTC','BNBBTC']

##全局变量 交易所列表
EX_NAME_LIST = []

##建立连接
def on_open(ws):
    pass


##接收到服务器返回的消息时调用
def on_message(ws, message):
     
    print('data update: %s' % message)
    ##撰写自定义函数

##线程函数
def run(ws):
    ws.run_forever()

if __name__ == "__main__":
    
    WS_LIST = []
    for symbol in SYMBOL_LIST:
        print(symbol)
        apiUrl = "wss://stream.binance.com:9443/ws/"+symbol.lower()+"@depth"
        ##实例化websocket对象 
        ws = websocket.WebSocketApp(apiUrl, on_message = on_message, on_open = on_open)
        WS_LIST.append(ws)


    '''
    ##threading模块手动创建线程跑symbol对
    threadpool = []
    t1 = threading.Thread(target=run, args=(WS_LIST[0],))
    threadpool.append(t1)

    t2 = threading.Thread(target=run, args=(WS_LIST[1],))
    threadpool.append(t2)

    t3 = threading.Thread(target=run, args=(WS_LIST[2],))
    threadpool.append(t3)

    t4 = threading.Thread(target=run, args=(WS_LIST[3],))
    threadpool.append(t4)

    for th in threadpool:
        th.start()
    '''
    ##使用线程池执行每个无线循环
    pool = threadpool.ThreadPool(len(WS_LIST))

    requests = threadpool.makeRequests(run,WS_LIST)

    [pool.putRequest(req) for req in requests]

    pool.wait()  ##阻塞直至完成

    print('finish')

