from flask import Flask, jsonify, request
from characterai import PyCAI

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        data = "hello world"
        return jsonify({'data': data})

@app.route('/chat/send/<string:msg>', methods=['GET'])
def send_message(msg):
    token = "34f5788ba1f0cfcb8b8f03437c732bad6e0abd2a"
    client = PyCAI(token)

    char = "AbuIXFqY7EsLrOjUDLR0bDNYwqU6MDQyAKtzGIMeLI4"

    chat = client.chat.get_chat(char)
    participants = chat['participants']

    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    data = client.chat.send_message(chat['external_id'], tgt, msg)

    name = data['src_char']['participant']['name']
    text = data['replies'][0]['text']

    return jsonify({'data': text})

@app.route('/chat/receive', methods=['GET'])
def receive_message():
    # Add logic here to fetch and return received messages
    return jsonify({'data': 'Placeholder for receiving messages'})

@app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST' and 'msg' in request.json:
        msg = request.json['msg']
        token = "34f5788ba1f0cfcb8b8f03437c732bad6e0abd2a"
        client = PyCAI(token)

        char = "AbuIXFqY7EsLrOjUDLR0bDNYwqU6MDQyAKtzGIMeLI4"

        chat = client.chat.get_chat(char)
        participants = chat['participants']

        if not participants[0]['is_human']:
            tgt = participants[0]['user']['username']
        else:
            tgt = participants[1]['user']['username']

        data = client.chat.send_message(chat['external_id'], tgt, msg)

        name = data['src_char']['participant']['name']
        text = data['replies'][0]['text']

        return jsonify({'reply': text})
    else:
        return jsonify({'error': 'Invalid request or missing "msg" in JSON payload'})

if __name__ == '__main__':
    app.run(debug=True)
