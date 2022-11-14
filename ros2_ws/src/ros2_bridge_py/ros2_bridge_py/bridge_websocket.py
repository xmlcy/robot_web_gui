#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import asyncio
import websockets


class WebsocketNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.pub = self.create_publisher(String, "action", 10) # 转发websocket消息


# async def run_node():
#     rclpy.init()
#     node = WebsocketNode("web_node")
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()

rclpy.init()
node = WebsocketNode("web_node")


async def echo(websocket):
    #fetch msg
    async for message in websocket:
        print("got a message:{}".format(message))
        await websocket.send(message)
        msg = String()
        # print(type(msg.data))
        # print(type(message))
        msg.data = message
        node.pub.publish(msg)


async def main(args=None):
    # start a websocket server
    async with websockets.serve(echo, "localhost", 8080):
        await asyncio.Future()  # run forever

asyncio.run(main())
