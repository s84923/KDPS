import os
from dotenv import load_dotenv
import google.generativeai as genai

# .envファイルの読み込み
load_dotenv()
 
# API-KEYの設定
GOOGLE_API_KEY='AIzaSyC308665bjO5vUHYQw246Q7Ri84swfw9CI'
genai.configure(api_key=GOOGLE_API_KEY)
 
gemini_pro = genai.GenerativeModel("gemini-pro")
prompt = "おすすめのアニメおしえて"
response = gemini_pro.generate_content(prompt)
print(response.text)