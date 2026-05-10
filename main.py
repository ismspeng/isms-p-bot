import os
import json
import random
import re  # 조항 번호 추출을 위한 정규표현식 모듈
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

try:
    from law_data import law_db
except ImportError:
    law_db = []

def post_blog():
    # 1. 인증 및 서비스 빌드
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    if not creds_json:
        print("❌ 오류: GOOGLE_CREDENTIALS 환경 변수가 없습니다.")
        return
    
    creds_info = json.loads(creds_json)
    creds = Credentials.from_authorized_user_info(creds_info)
    BLOG_ID = '3209144423549555087'
    service = build('blogger', 'v3', credentials=creds)

    # 2. 데이터 확인 및 3개 추출
    if not law_db:
        print("❌ 오류: law_data.py에 데이터가 없거나 형식이 잘못되었습니다.")
        return

    selected_articles = random.sample(law_db, min(len(law_db), 3))

    # 3. 제목 및 본문 생성
    post_title = f"🛡️ [법령 학습] 오늘의 조문: " + ", ".join([a['title'] for a in selected_articles])
    
    html_content = "<div style='font-family: sans-serif; line-height: 1.8;'>"
    html_content += "<h2 style='color: #2c3e50;'>📅 오늘의 개인정보 보호법 학습</h2><p style='color: #666; font-size: 14px;'>조항을 클릭하면 국가법령정보센터로 연결됩니다.</p><hr>"
    
    for art in selected_articles:
        # [핵심 로직] "제12조(제목)"에서 숫자 "12"만 추출
        jo_match = re.search(r'제(\d+)조', art['title'])
        if jo_match:
            jo_num = jo_match.group(1)
            # 국가법령정보센터 직링크 생성
            direct_link = f"https://www.law.go.kr/법령/개인정보보호법/제{jo_num}조"
        else:
            direct_link = "https://www.law.go.kr/법령/개인정보보호법"

        html_content += f"""
        <div style="margin-bottom: 40px; padding: 20px; background: #fdfdfd; border: 1px solid #eee; border-radius: 8px;">
            <h3 style="margin-top: 0;">
                <a href="{direct_link}" target="_blank" style="color: #e74c3c; text-decoration: none; border-bottom: 2px solid #e74c3c;">
                    {art['title']} 🔗
                </a>
            </h3>
            <div style="padding: 10px 0; color: #333;">{art['full_text']}</div>
            <div style="margin-top: 15px; text-align: right;">
                <a href="{direct_link}" target="_blank" style="font-size: 12px; color: #3498db; text-decoration: none;">
                    국가법령정보센터에서 자세히 보기 →
                </a>
            </div>
        </div>
        """
        
    html_content += "<br><p style='color: gray; font-size: 0.8em; text-align: center;'>출처: 국가법령정보센터</p></div>"

    # 4. 게시
    post_body = {'kind': 'blogger#post', 'title': post_title, 'content': html_content}
    try:
        service.posts().insert(blogId=BLOG_ID, body=post_body).execute()
        print(f"✅ 성공: {len(selected_articles)}개 조항 링크 포함 포스팅 완료!")
    except Exception as e:
        print(f"❌ Blogger API 오류: {e}")

if __name__ == "__main__":
    post_blog()
