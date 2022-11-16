# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# import rclpy
# from rclpy.node import Node
# from std_msgs.msg import String
# import asyncio
# import websockets


# class WebsocketNode(Node):
#     def __init__(self, name):
#         super().__init__(name)
#         self.pub = self.create_publisher(String, "action", 10) # 转发websocket消息


# # async def run_node():
# #     rclpy.init()
# #     node = WebsocketNode("web_node")
# #     rclpy.spin(node)
# #     node.destroy_node()
# #     rclpy.shutdown()

# rclpy.init()
# node = WebsocketNode("web_node")


# async def echo(websocket):
#     #fetch msg
#     async for message in websocket:
#         print("got a message:{}".format(message))
#         await websocket.send(message)
#         msg = String()
#         # print(type(msg.data))
#         # print(type(message))
#         msg.data = message
#         node.pub.publish(msg)


# async def main(args=None):
#     # start a websocket server
#     async with websockets.serve(echo, "localhost", 8080):
#         await asyncio.Future()  # run forever

# asyncio.run(main())




#-----------------------------------------------------------------------------------

# import asyncio 
# import websockets
# import time
# import rclpy
# from rclpy.node import Node
# from std_msgs.msg import String
 
# x = "02"


# class WebsocketNode(Node):
#     def __init__(self, name):
#         super().__init__(name)
#         self.pub = self.create_publisher(String, "action", 10) # 转发websocket消息
#         self.sub = self.create_subscription(String, 'nihao', self.std_callback, 10) # 订阅std
    
#     def std_callback(self, action):
#             print(action)


# rclpy.init()
# node = WebsocketNode("web_node")

# async def run_node():
#     # rclpy.init()
#     # node = WebsocketNode("web_node")
#     while rclpy.ok():
#         rclpy.spin_once(node)
#         print("ni")
#         # await asyncio.sleep(1)
#         a = 1
#     # rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()




# async def consumer(message):
#     print(message)
#     msg = String()
#     msg.data = message
#     node.pub.publish(msg)
#     # await run_node()

# async def producer():
#     await asyncio.sleep(1)
#     global x
#     x = time.asctime(time.localtime()) 
#     return str(x)

# async def consumer_handler(websocket):
#     async for message in websocket:
#         await consumer(message)

# async def producer_handler(websocket):
#     while True:
#         message = await producer()
#         await websocket.send(message)

# async def handler(websocket):
#     await asyncio.gather(
#         consumer_handler(websocket),
#         producer_handler(websocket),
#     )


# async def main(args=None):
#     async with websockets.serve(handler, "", 8080):
#         await asyncio.Future()  # run forever

# asyncio.run(main())




#-----------------------------------------------------------------------------------

import websockets
import threading
import asyncio
import datetime
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class WebsocketNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.pub = self.create_publisher(String, "action", 10) # 转发websocket消息
        self.sub = self.create_subscription(String, 'nihao', self.std_callback, 10) # 订阅std
    
    def std_callback(self, action):
            print(action)


# async def run_node():
#     rclpy.init()
#     node = WebsocketNode("web_node")
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()
 
gLock = threading.Lock()
 
 
def getTime():
    global gLock
    gLock.acquire()
    now = datetime.datetime.now()
    tm = ":".join([
        str(now.day).zfill(2),
        str(now.hour).zfill(2),
        str(now.minute).zfill(2),
        str(now.second).zfill(2),
        str(now.microsecond)
    ])
    gLock.release()
    return tm
 
 
def log(*msg):
 
    tm = getTime()
    global gLock
    gLock.acquire()
    # 数组前面加参数，代表把数组拆分成多个逗号分割的变量，类似js中的展开符号...
    text = ",".join([tm, "  ", *msg])
    print(text)
    gLock.release()
 
 
class CListen(threading.Thread):
    def __init__(self, loop):
        threading.Thread.__init__(self)
        self.mLoop = loop
 
    def run(self):
        asyncio.set_event_loop(self.mLoop)  # 在新线程中开启一个事件循环
        log("prepare run_for")
        self.mLoop.run_forever()
        log("end run_for")  # 跑不到这里
 
 
async def consumer(message):
    print(message)

async def producer():
    await asyncio.sleep(1)
    x = 500
    return str(x)

async def consumer_handler(websocket):
    async for message in websocket:
        await consumer(message)

async def producer_handler(websocket):
    while True:
        message = await producer()
        await websocket.send(message)

async def handler(websocket):
    await asyncio.gather(
        consumer_handler(websocket),
        producer_handler(websocket),
    )


async def webs(args=None):
    # start a websocket server
    async with websockets.serve(handler, "localhost", 8080):
        await asyncio.Future()  # run forever


def main():
    newLoop = asyncio.new_event_loop()
    listen = CListen(newLoop)
    listen.setDaemon(True)
    listen.start()
 
    asyncio.run_coroutine_threadsafe(webs(), newLoop)

    rclpy.init()
    node = WebsocketNode("web_node")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
