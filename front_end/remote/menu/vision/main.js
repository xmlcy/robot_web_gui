function log(msg) {
  document.getElementById('log').textContent = "视觉:" + msg + '\n';
}

function log2(msg) {
  document.getElementById('log2').textContent = "控制:" + msg + '\n';
}

// setup websocket with callbacks
var ws = new WebSocket('ws://localhost:8090/');
ws.onopen = function() {
  log('CONNECT');
};
ws.onclose = function() {
  log('DISCONNECT');
};
ws.onmessage = function(event) {
  // log('MESSAGE: ' + event.data);
  document.getElementById("image").src = "data:image/jpeg;base64," + event.data;
};

var ws_2 = new WebSocket('ws://localhost:8080/');
ws_2.onopen = function() {
  log2('CONNECT');
};
ws_2.onclose = function() {
  log2('DISCONNECT');
};
ws_2.onmessage = function(event) {
  // log('CONNECT');
  // log(event.data);
  const data = JSON.parse(event.data);
  document.getElementById('mode').textContent = 'mode:' + data.mode;
  document.getElementById('cmd').textContent = 'cmd:' + data.cmd;
  document.getElementById('pos_x').textContent = 'x:' + data.x;
  document.getElementById('pos_y').textContent = 'y:' + data.y;
  document.getElementById('pos_z').textContent = 'z:' + data.z;
  document.getElementById('status').textContent = 'status:' + data.status;
};

function createParagraph() {
  let para = document.createElement('p');
  para.textContent = '你点击了这个按钮！';
  ws.send("你点击了这个按钮！")
}
  
const buttons = document.querySelectorAll('button');

for(let i = 0; i < buttons.length ; i++) {
  buttons[i].addEventListener('click', createParagraph);
}

function getVal(value)
{
  ws_2.send(value);
}