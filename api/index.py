from flask import Flask, request, jsonify
from g4f.client import Client
import json  
import re  

app = Flask(__name__)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        user_message = request.args.get('message')
        if not user_message:
            return jsonify({'error': 'O parâmetro "message" é obrigatório.'}), 400
    else:
        data = request.get_json(force=True)
        if not data or 'message' not in data:
            return jsonify({'error': 'O parâmetro "message" é obrigatório.'}), 400
        user_message = data['message']

    try:
       
        client = Client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant for a roblox executor called Wave Assit. You are called WaveAI. Your main goal is to help create Luau scripts. You will not answer anything that isn't related to Luau scripting. You will keep your answers short and direct. You were made by the developers at hyper stv. You will always embed any code in a Lua code block. You will always use the custom request function for HTTP requests unless explicitly told otherwise. Do not explain how to create a script the user requests, write it yourself then give the user your script. Make few comments in your scripts. If this is the only message in our conversation, reply with a quick, generic greeting."},
                {"role": "user", "content": user_message}
            ]
        )

        
        chat_response = response.choices[0].message.content

        
        chat_response = re.sub(r'^```|```$', '', chat_response)

        
        return app.response_class(
            response=json.dumps({'response': chat_response}, ensure_ascii=False),
            mimetype='application/json'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Iniciando API do ChatGPT com G4F")
    app.run(debug=True)
