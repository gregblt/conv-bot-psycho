from app import app
from flask import request
import uuid

from flask_socketio import SocketIO
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
print(int(os.environ.get('PORT')))
clients = {};

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('connect_master')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    socketio.emit('my response', json, callback=messageReceived)

@socketio.on('connect_user')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    uuid_user = str(uuid.uuid4());
    clients[request.sid]=(request.namespace);
    socketio.emit('user_connected', {'uuid':uuid_user}, callback=messageReceived)

@socketio.on('new_user_msg')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    print(request.sid)
    json['sid'] = request.sid
    socketio.emit('to_master', json, callback=messageReceived)

@socketio.on('new_master_msg')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    socketio.emit('to_client', json, callback=messageReceived, room=json['user'])


if __name__ == '__main__':
    
  #app.run()

  #socketio.run(app, debug=True)
