import os
import json
import google.auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# 깃허브 시크릿에서 열쇠(JSON) 가져오기
creds_json = os.environ.get('GOOGLE_CREDENTIALS')
creds_data = json.loads(creds_json)

# 블로그 설정 (여기에 본인 블로그 ID를 넣어야 합니다)
BLOG_ID = '여기에_본인의_블로그_ID를_넣으세요' 

def post_blog():
    creds = Credentials.from_authorized_user_info(creds_data)
    service = build('blogger', 'v3', credentials=creds)

    post_body = {
        'kind': 'blogger#post',
        'title': '오늘의 ISMS-P 및 개인정보보호법 학습',
        'content': '''
        <h3>1. 개인정보보호법 주요 내용</h3>
        <ul>
            <li>제1조(목적): 개인의 자유와 권리를 보호함...</li>
            <li>제2조(정의): "개인정보"란 살아 있는 개인에 관한 정보로서...</li>
        </ul>
        <br>
        <h3>2. ISMS-P 인증 항목</h3>
        <ul>
            <li>1.1.1 경영진의 참여: 최고경영자는 보안 의무를 다해야 함...</li>
        </ul>
        '''
    }

    service.posts().insert(blogId=BLOG_ID, body=post_body).execute()
    print("포스팅 성공!")

if __name__ == "__main__":
    post_blog()
