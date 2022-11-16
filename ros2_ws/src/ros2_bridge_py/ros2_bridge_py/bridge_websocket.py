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

import asyncio 
import websockets
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
 
x = "02"


class WebsocketNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.pub = self.create_publisher(String, "action", 10) # 转发websocket消息
        self.sub = self.create_subscription(String, 'nihao', self.std_callback, 10) # 订阅std
    
    def std_callback(self, action):
            print(action)


rclpy.init()
node = WebsocketNode("web_node")

async def run_node():
    # rclpy.init()
    # node = WebsocketNode("web_node")
    while rclpy.ok():
        rclpy.spin_once(node)
        print("ni")
        # await asyncio.sleep(1)
        a = 1
    # rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()




async def consumer(message):
    print(message)
    msg = String()
    msg.data = message
    node.pub.publish(msg)
    # await run_node()

async def producer():
    await asyncio.sleep(1)
    global x
    x = time.asctime(time.localtime()) 
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


async def main(args=None):
    async with websockets.serve(handler, "", 8080):
        await asyncio.Future()  # run forever

asyncio.run(main())
