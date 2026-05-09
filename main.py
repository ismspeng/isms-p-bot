import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

def post_blog():
    # 1. 금고에서 열쇠(JSON) 꺼내기
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    creds_info = json.loads(creds_json)
    
    if not creds_json:
        print("에러: GOOGLE_CREDENTIALS 를 찾을 수 없습니다.")
        return
    
    # 2. 인증 정보 설정 (OAuth 2.0 방식)
    # credentials.json 내용 중 필요한 정보만 추출하여 인증합니다.
    try:
        creds = Credentials.from_authorized_user_info(creds_info)
    except Exception as e:
        # 만약 위 방법이 안 될 경우를 대비한 예외 처리
        from google.oauth2 import service_account
        try:
            creds = service_account.Credentials.from_service_account_info(creds_info)
        except:
            print(f"인증 생성 실패: {e}")
            return

    # 3. 블로그 ID 설정 (이미 확인하신 ID입니다)
    BLOG_ID = '3209144423549555087' 

    service = build('blogger', 'v3', credentials=creds)

    # 4. 포스팅 내용 (학습용 5개 항목 예시)
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
        service.posts().insert(blogId=BLOG_ID, body=post_body).execute()
        print("🎉 블로그 포스팅에 성공했습니다!")
    except Exception as e:
        print(f"포스팅 실패: {e}")

if __name__ == "__main__":
    post_blog()
