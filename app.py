from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# 미리 정의된 키워드와 답변
responses = {
    "hello": "Hi there! How can I help you today?",
    "bye": "Goodbye! Have a nice day!",
    "thanks": "You're welcome!",
    "product": "We have a variety of products including electronics, clothing, and more.",
    # 추가 키워드와 답변을 여기에 추가할 수 있습니다.
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # 메시지에서 키워드 찾기
    response_message = "I'm sorry, I don't understand."
    for keyword, response in responses.items():
        if keyword in user_message.lower():
            response_message = response
            break
    
    return jsonify({"message": response_message})

if __name__ == '__main__':
    app.run(debug=True)
