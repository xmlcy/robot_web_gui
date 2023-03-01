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
    log('CONNECT');
    // log(event.data);
    const data = JSON.parse(event.data);
    document.getElementById('mode').textContent = 'mode:' + data.mode;
    document.getElementById('cmd').textContent = 'cmd:' + data.cmd;
    document.getElementById('pos_x').textContent = 'x:' + data.x;
    document.getElementById('pos_y').textContent = 'y:' + data.y;
    document.getElementById('pos_z').textContent = 'z:' + data.z;
    document.getElementById('status').textContent = 'status:' + data.status;
  };
  
  function createParagraph(button) {
    let para = document.createElement('p');
    para.textContent = '你点击了这个按钮！';
    ws.send(button.data);
  }
    
  const buttons = document.querySelectorAll('button');
  
  for(let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', createParagraph);
  }
  
  function getVal(value)
  {
    ws.send(value);
  }