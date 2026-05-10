import os
import json
import random
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
# 데이터 파일 임포트
from law_data import law_db

def post_blog():
    # 1. Google API 인증
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    if not creds_json:
        print("❌ GOOGLE_CREDENTIALS 설정 확인 필요")
        return
        
    creds_info = json.loads(creds_json)
    creds = Credentials.from_authorized_user_info(creds_info)
    BLOG_ID = '3209144423549555087'
    service = build('blogger', 'v3', credentials=creds)

    # 2. 랜덤하게 정확히 3개 조항 선택
    selected_articles = random.sample(law_db, 3)

    # 3. 포스팅 제목 생성
    title_parts = [a['title'] for a in selected_articles]
    post_title = f"🛡️ [법령 정복] 오늘의 조문 학습: {', '.join(title_parts)}"

    # 4. 포스팅 본문 생성 (예시 포맷 유지)
    html_content = "<div style='font-family: sans-serif; line-height: 1.8;'>"
    html_content += "<h2 style='color: #2c3e50;'>📅 오늘의 개인정보 보호법 학습</h2><hr>"
    
    for art in selected_articles:
        html_content += f"""
        <div style="margin-bottom: 40px;">
            <h3 style="color: #e74c3c;">{art['title']}</h3>
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 8px; border-left: 5px solid #ccc;">
                {art['full_text']}
            </div>
        </div>
        """
    
    html_content += "<br><p style='color: gray;'>출처: 국가법령정보센터</p></div>"

    # 5. 블로그 게시
    post_body = {
        'kind': 'blogger#post',
        'title': post_title,
        'content': html_content
    }

    try:
        service.posts().insert(blogId=BLOG_ID, body=post_body).execute()
        print(f"✅ 성공: {', '.join(title_parts)} 포스팅 완료")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    post_blog()
