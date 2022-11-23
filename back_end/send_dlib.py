import asyncio
import websockets
import base64
import cv2
import numpy as np
import dlib
from sympy import true

print(cv2.__version__)
# capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture = cv2.VideoCapture(0)
if not capture.isOpened():
    print('quit')
    quit()
ret, frame = capture.read()
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),95]

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

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

        ret, frame = capture.read()

        await asyncio.sleep(0.01)
        global m_state
        if 1 == m_state:
            landmarks_lip = []
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 1)
            print('faces number:' + str(len(rects)))
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

async def consumer(message):
    print(message)
    global m_state
    if message == "开始跟随":
        m_state = 1
    else:
        m_state = 0

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