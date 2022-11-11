function log(msg) {
  document.getElementById('log').textContent = msg;
}

// setup websocket with callbacks
var ws = new WebSocket('ws://localhost:8080/');
ws.onopen = function() {
  log('CONNECT');
};
ws.onclose = function() {
  log('DISCONNECT');
};
ws.onmessage = function(event) {
  log('MESSAGE: ' + event.data);
};

// function createParagraph(button) {
//   let para = document.createElement('p');
//   para.textContent = '你点击了这个按钮！';
//   ws.send(button.data);
// }
  
// const buttons = document.querySelectorAll('button');

// for(let i = 0; i < buttons.length; i++) {
//   buttons[i].addEventListener('click', createParagraph);
// }

function getVal(value)
{
  ws.send(value);
}