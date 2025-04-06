from . import main
from flask import request
from response_utils import make_response
from bs4 import BeautifulSoup
from openai import OpenAI
import os

# 设置OpenAI配置
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL')
)

def get_ai_paraphrase(text, prompt, model=None):
    try:
        # Use provided model or fallback to environment variable
        model = model or os.getenv('OPENAI_MODEL', 'deepseek-chat')
        # Log request parameters
        print(f"[DEBUG] API Request params: model={model}, text={text[:100]}...")
        print(f"[DEBUG] API Base URL: {os.getenv('OPENAI_BASE_URL')}")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt or "You are a text paraphrasing assistant. Your task is to rewrite the text while maintaining the same meaning but using different expressions. Maintain professionalism and fluency while ensuring accuracy."},
                {"role": "user", "content": text}
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = f"AI Processing Failed:\nError Type: {type(e).__name__}\nError Message: {str(e)}\nEnvironment Config:\n- API Key: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not Set'}\n- Base URL: {os.getenv('OPENAI_BASE_URL')}\n- Model: {os.getenv('OPENAI_MODEL', 'deepseek-chat')}"
        print(f"[ERROR] {error_msg}")
        raise Exception(error_msg)

@main.route('/ai_paraphrase', methods=['POST'])
def ai_paraphrase():
    data = request.get_json()
    if not data:
        return make_response(code=400, message="No request data provided")
    
    text = data.get('text')
    prompt = data.get('prompt')
    model = data.get('model')
    
    if not text:
        return make_response(code=400, message="No original text provided")
    
    try:
        result = get_ai_paraphrase(text, prompt, model)
        return make_response(data={"original_text": text, "paraphrased_text": result})
    except Exception as e:
        return make_response(code=500, message=str(e))

@main.route('/analyze', methods=['POST'])
def analyze_file():
    if 'file' not in request.files:
        return make_response(code=400, message="没有上传文件")

    file = request.files['file']
    if file.filename == '':
        return make_response(code=400, message="未选择文件")

    try:
        # 读取文件内容
        html_content = file.read().decode('utf-8')

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 找到所有包含原文、相似源和修改建议的 <tr> 元素
        results = []
        for tr in soup.find_all('tr'):
            # 提取原文
            origin_text_div = tr.find('td', class_='Origin_text')
            origin_text = origin_text_div.find('p').get_text(strip=True) if origin_text_div and origin_text_div.find(
                'p') else ""

            # 提取相似源
            similar_source_div = tr.find('div', class_='siminfo')
            similar_source_text = ""
            if similar_source_div:
                similar_source_text = '\n'.join(
                    [p.get_text(strip=True) for p in similar_source_div.find_all('p') if p.get_text(strip=True)])

            # 提取修改建议
            correction_advice_div = tr.find('div', class_='correct_advice')
            correction_advice_text = ""
            if correction_advice_div:
                correction_advice_text = '\n'.join(
                    [span.get_text(strip=True) for span in correction_advice_div.find_all('span')])

            # 将提取到的数据添加到结果列表中
            results.append({
                "original_text": origin_text,
                "similar_source": similar_source_text,
                "correction_advice": correction_advice_text
            })

        return make_response(data=results)
    except Exception as e:
        return make_response(code=500, message=str(e))