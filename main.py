import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

def post_blog():
    # 1. 금고에서 열쇠(JSON) 꺼내기
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    
    if not creds_json:
        print("에러: GOOGLE_CREDENTIALS를 찾을 수 없습니다.")
        return

    creds_info = json.loads(creds_json)
    
    # 2. 서비스 계정 인증 설정 (가장 확실한 로봇 전용 방식)
    # 님께서 방금 생성하신 서비스 계정 전용 인증 로직입니다.
    try:
        creds = service_account.Credentials.from_service_account_info(
            creds_info, 
            scopes=['https://www.googleapis.com/auth/blogger']
        )
    except Exception as e:
        print(f"인증 생성 실패: {e}")
        return

    # 3. 블로그 ID 설정
    BLOG_ID = '3209144423549555087' 

    service = build('blogger', 'v3', credentials=creds)

    # 4. 포스팅 내용
    post_body = {
        'kind': 'blogger#post',
        'title': '오늘의 ISMS-P 및 개인정보보호법 학습',
        'content': '''
        <h2>[개인정보보호법]</h2>
        <ul>
            <li>1. 개인정보의 정의: 살아있는 개인에 관한 정보</li>
            <li>2. 민감정보의 보호: 유전자정보, 범죄경력자료 등</li>
            <li>3. 고유식별정보: 주민등록번호, 여권번호 등</li>
            <li>4. 개인정보 처리 원칙: 목적 내 최소 수집</li>
            <li>5. 정보주체의 권리: 열람, 정정, 삭제 권리</li>
        </ul>
        <br>
        <h2>[ISMS-P 인증항목]</h2>
        <ul>
            <li>1.1.1 경영진의 참여: 최고경영자의 보안 의사결정</li>
            <li>1.1.2 조직 구성: 정보보호 위원회 운영</li>
            <li>1.1.3 책임 할당: 각 부서별 보안 역할 정의</li>
            <li>1.2.1 정책 수립: 정보보호 및 개인정보보호 정책 수립</li>
            <li>1.2.2 정책 검토: 연 1회 이상 정책의 타당성 검토</li>
        </ul>
        '''
    }

    try:
        # 글쓰기 명령 실행
        service.posts().insert(blogId=BLOG_ID, body=post_body).execute()
        print("🎉 블로그 포스팅에 성공했습니다!")
    except Exception as e:
        print(f"포스팅 실패 (권한 문제일 수 있음): {e}")

if __name__ == "__main__":
    post_blog()
