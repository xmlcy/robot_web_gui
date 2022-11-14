# robot_web_gui

#### 一个很小的 robot web gui 框架

web界面使用纯静态页面实现，后台使用 python 基于 websockets 实现

### front end

web界面使用纯静态页面实现 HTML CSS JS

### back end

使用 python 基于 websockets 实现

``` shell
pip install websockets
python server.py
python clinet.py
```

### 使用

1. 开启服务端

``` shell
python server.py
```

2. 使用浏览器打开 front_end/index.html

3. 选择表情演示 点击表情菜单中的按钮即可在服务端看到消息


## ROS2 功能包

由于websockets中使用asyncio，还没研究明白，所以暂时只能单方向接收web数据，通过ros2发布

### 功能包使用

1. ros2_ws文件夹下编译运行节点

```shell
cd ros2_ws/
colcon build
source install/local_setup.bash
ros2 run ros2_bridge_py bridge_websocket
```

2. 另一个终端执行，可以看到该节点发布的消息

```shell
ros2 topic echo /action
```

3. 使用浏览器打开 front_end/index.html

4. 选择表情演示 点击表情菜单中的按钮即可在终端看到消息