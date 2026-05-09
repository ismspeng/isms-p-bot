import os
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def post_blog():
    # 1. 금고에서 열쇠 꺼내기
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    creds_info = json.loads(creds_json)

    # 2. 사용자 인증 정보 설정
    # 이 방식은 '초대'가 필요 없습니다. 
    creds = Credentials.from_authorized_user_info(creds_info)

    # 3. 블로그 ID
    BLOG_ID = '3209144423549555087' 
    service = build('blogger', 'v3', credentials=creds)

    post_body = {
        'kind': 'blogger#post',
        'title': '오늘의 ISMS-P 학습 (완성본)',
        'content': '<h3>인증 성공!</h3><p>이제 자동 포스팅이 정상 작동합니다.</p>'
    }

    try:
        service.posts().insert(blogId=BLOG_ID, body=post_body).execute()
        print("🎉 드디어 포스팅에 성공했습니다!")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    post_blog()
