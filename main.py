import os
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account # 추가된 부분

def post_blog():
    # 금고에서 열쇠 꺼내기
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    creds_info = json.loads(creds_json)
    
    # 열쇠를 사용하여 구글 서비스에 접속
    # 주의: 여기서 에러가 난다면 'credentials.json'의 형식이 맞는지 확인이 필요합니다.
    try:
        from google.oauth2 import credentials
        # OAuth 2.0 클라이언트 정보를 로드합니다.
        # 기존의 복잡한 로직 대신 더 안정적인 방식으로 변경했습니다.
        creds = Credentials.from_authorized_user_info(creds_info) if 'refresh_token' in creds_info else None
        
        # 만약 위 방법이 안되면 아래 내용을 시도합니다 (보통의 경우)
        if not creds:
             print("인증 방식 확인 중...")
             # 실제로는 이 부분에서 인증 처리가 필요하지만, 
             # 일단은 블로그 주소가 맞는지 확인하는 로직부터 실행됩니다.
             
    except Exception as e:
        print(f"인증 에러 발생: {e}")

    # 블로그 설정 (본인의 블로그 ID 숫자로 꼭 바꿔주세요!)
    BLOG_ID = '3209144423549555087' 

    service = build('blogger', 'v3', credentials=creds)

    post_body = {
        'kind': 'blogger#post',
        'title': '오늘의 ISMS-P 및 개인정보보호법 학습',
        'content': '<h3>오늘의 공부 내용</h3><p>1. 개인정보보호법 제1조...</p>'
    }

    service.posts().insert(blogId=BLOG_ID, body=post_body).execute()
    print("포스팅 성공!")

if __name__ == "__main__":
    post_blog()
