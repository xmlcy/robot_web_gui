# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

import websockets
import threading
import asyncio
import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray
from robot_msg.msg import Status

ros_msg = Status()

class WebsocketNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.pub = self.create_publisher(String, "web_string", 10) # 转发websocket消息
        self.pub_remote_ = self.create_publisher(Int16MultiArray, "web", 10) # 转发websocket消息
        self.sub = self.create_subscription(Status, 'status', self.std_callback, 10) # 订阅std
    
    def std_callback(self, status):
        # print(status)
        global ros_msg
        ros_msg = status

class WebSocketThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
 
    def run(self):
        print("start")
        asyncio.run(webs())
        print("stop")
 
 
async def consumer(message):
    # print(message)
    # print(type(message))
    msg = String()
    msg.data = message
    node.pub.publish(msg)
    if message == "视觉跟踪":
        print("视觉跟踪")
    elif message == "手动控制":
        print("手动控制")
    else:
        remote_data = json.loads(message)
        # print(remote_data)
        # print(type(remote_data))
        msg2 = Int16MultiArray()
        msg2.data = [0, 0, 0, 0]
        msg2.data[0] = int(remote_data['joyl_x'])
        msg2.data[1] = int(remote_data['joyl_y'])
        msg2.data[2] = int(remote_data['joyr_x'])
        msg2.data[3] = int(remote_data['joyr_y'])
        node.pub_remote_.publish(msg2)

async def producer():
    global ros_msg
    await asyncio.sleep(0.01)
    # print(ros_msg.x)
    data = { 'mode':ros_msg.mode, 'cmd':ros_msg.cmd, 'x':ros_msg.x, 'y':ros_msg.y, 'z':ros_msg.z, 'status':ros_msg.status,
     }
    # print('DATA:', repr(data))
    data_string = json.dumps(data)
    return str(data_string)

async def consumer_handler(websocket):
    try:
        async for message in websocket:
            await consumer(message)
    except websockets.exceptions.ConnectionClosedError:
        print('Connection unexpectly closed')
    except websockets.exceptions.ConnectionClosedOK:
        print('Connection closed')

async def producer_handler(websocket):
    try:
        while True:
            message = await producer()
            await websocket.send(message)
    except asyncio.exceptions.CancelledError:
        print('Could not complete sending')
    except websockets.exceptions.ConnectionClosedError:
        print('Connection unexpectly closed')
    except websockets.exceptions.ConnectionClosed:
        print('Connection closed during sending')

async def handler(websocket):
    try:
        await asyncio.gather(
            consumer_handler(websocket),
            producer_handler(websocket),
        )
    except asyncio.exceptions.CancelledError:
        print('Caught unfinished task')

    # try:
    #     consumer_task = asyncio.ensure_future(
    #         consumer_handler(websocket))
    #     producer_task = asyncio.ensure_future(
    #         producer_handler(websocket))
    #     done, pending = await asyncio.wait(
    #         [consumer_task, producer_task],
    #         return_when=asyncio.FIRST_COMPLETED,
    #     )
    #     for task in pending:
    #         task.cancel()
    # except asyncio.exceptions.CancelledError:
    #     print('Caught unfinished task')


async def webs(args=None):
    # start a websocket server
    async with websockets.serve(handler, "localhost", 8080):
        await asyncio.Future()  # run forever


def main():
    rclpy.init()
    global node
    node = WebsocketNode("web_node")

    thread_websocket = WebSocketThread("websocket")
    thread_websocket.start()
    # asyncio.run(webs())

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
