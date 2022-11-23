import asyncio
import websockets
import base64
import cv2
import numpy as np

# capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
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

        ret, frame = capture.read()

async def consumer(message):
    print(message)

async def producer():
    await asyncio.sleep(0.5)
    return str("hello")

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
        send_msg(websocket),
    )
        

async def main():
    async with websockets.serve(handler, "localhost", 8090):
        await asyncio.Future()  # run forever

asyncio.run(main())