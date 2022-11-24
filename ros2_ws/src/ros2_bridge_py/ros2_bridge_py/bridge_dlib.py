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
import dlib
from sympy import true

ros_msg = "none"

print(cv2.__version__)
capture = cv2.VideoCapture(0)
if not capture.isOpened():
    print('quit')
    quit()
ret, frame = capture.read()
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),95]

detector = dlib.get_frontal_face_detector()
import os 

# print(os.path.abspath(__file__))
# print(os.path.dirname(__file__))
# print(os.path.abspath(os.path.join(os.path.abspath(__file__),os.path.pardir,os.path.pardir,os.path.pardir,os.path.pardir)))
# print(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir,os.path.pardir,os.path.pardir)))

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir,os.path.pardir,os.path.pardir))
file_path += "/ros2_bridge_py/shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(file_path)

# 规定上嘴唇和下嘴唇连线的路径
lip_order_dlib = np.array([[48, 49, 50, 51, 52, 53, 54, 64, 63, 62, 61, 60, 48],
                           [48, 59, 58, 57, 56, 55, 54, 64, 65, 66, 67, 60, 48]]) - 48
lip_order_num = lip_order_dlib.shape[1]

m_state = 0

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
        await asyncio.sleep(0.01) # 如果需要转发web消息 必须加入延时

        ret, frame = capture.read()

        global m_state
        if 1 == m_state:
            landmarks_lip = []
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 1)
            # print('faces number:' + str(len(rects)))
            for (i, rect) in enumerate(rects):
                # 标记人脸中的68个landmark点
                landmarks = predictor(gray, rect)  
                for n in range(48, 68):
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    landmarks_lip.append((x, y))
                for m in range(lip_order_num-1):
                    cv2.line(frame, landmarks_lip[lip_order_dlib[0][m]], landmarks_lip[lip_order_dlib[0][m+1]], color=(0, 255, 0), thickness=2, lineType=8)
                for n in range(lip_order_num-1):
                    cv2.line(frame, landmarks_lip[lip_order_dlib[1][n]], landmarks_lip[lip_order_dlib[1][n+1]], color=(0, 255, 0), thickness=2, lineType=8)
            # cv2.imshow("face", frame)
            # if cv2.waitKey(1) & 0xff == ord('q'):
            #     break

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
    global m_state
    if message == "开始跟随":
        m_state = 1
    else:
        m_state = 0

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
