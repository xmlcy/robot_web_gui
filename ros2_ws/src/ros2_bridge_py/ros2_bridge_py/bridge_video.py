# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

import websockets
import threading
import asyncio
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import base64
import cv2
import numpy as np

ros_msg = "none"


capture = cv2.VideoCapture(0)
if not capture.isOpened():
    print('quit')
    quit()
ret, frame = capture.read()
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),95]

# 向服务器端实时发送视频截图
async def send_msg(websocket):
    global ret,frame
    while ret:
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = np.array(imgencode)
        img = data.tobytes()

        # base64编码传输
        img = base64.b64encode(img).decode()
        await websocket.send(img)
        await asyncio.sleep(0.05) # 如果需要转发web消息 必须加入延时

        ret, frame = capture.read()

class WebsocketNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.pub = self.create_publisher(String, "action", 10) # 转发websocket消息
        self.sub = self.create_subscription(String, 'nihao', self.std_callback, 10) # 订阅std
    
    def std_callback(self, action):
        print(action)
        global ros_msg
        ros_msg = action.data
 
class CListen(threading.Thread):
    def __init__(self, loop):
        threading.Thread.__init__(self)
        self.mLoop = loop
 
    def run(self):
        asyncio.set_event_loop(self.mLoop)  # 在新线程中开启一个事件循环
        print("prepare run_for")
        self.mLoop.run_forever()
        print("end run_for")  # 跑不到这里
 
 
async def consumer(message):
    print(message)
    msg = String()
    msg.data = message
    node.pub.publish(msg)

async def producer():
    global ros_msg
    await asyncio.sleep(0.5)
    return str(ros_msg)

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
        # producer_handler(websocket),
        send_msg(websocket),
    )


async def webs(args=None):
    # start a websocket server
    async with websockets.serve(handler, "localhost", 8090):
        await asyncio.Future()  # run forever


def main():
    rclpy.init()
    global node
    node = WebsocketNode("web_video_node")

    newLoop = asyncio.new_event_loop()
    listen = CListen(newLoop)
    listen.setDaemon(True)
    listen.start()
 
    asyncio.run_coroutine_threadsafe(webs(), newLoop)

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
