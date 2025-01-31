from flask import Flask, request, jsonify, render_template
import json
import re

app = Flask(__name__)

# JSON 파일에서 제품 데이터 로드
with open('products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# 메시지 기반 기본 응답
default_responses = {
    r"\\bhello\\b": "안녕하세요! 중고 핸드폰 가게에 오신 것을 환영합니다. 무엇을 도와드릴까요?",
    r"\\bbye\\b": "안녕히 가세요! 또 방문해주세요!",
    r"\\bthanks\\b": "감사합니다. 더 도와드릴 일이 있으면 알려주세요."
}

# 제품 검색 함수
def search_products(query):
    results = []
    for product in products:
        if query.lower() in product['model'].lower():
            results.append(product)
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "메시지를 입력해주세요."}), 400

        # 기본 응답 처리
        response_message = None
        for pattern, response in default_responses.items():
            if re.search(pattern, user_message, re.IGNORECASE):
                response_message = response
                break

        # 제품 검색 처리
        if not response_message:
            matched_products = search_products(user_message)
            if matched_products:
                response_message = "다음은 검색 결과입니다:\n"
                for product in matched_products:
                    response_message += f"- {product['model']} {product['storage']} ({product['condition']}): {product['price']} {product['currency']}\n"
            else:
                response_message = "죄송합니다. 해당 제품을 찾을 수 없습니다. 다른 검색어를 입력해 주세요."

        return jsonify({"message": response_message})

    except Exception as e:
        return jsonify({"error": f"오류가 발생했습니다: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
