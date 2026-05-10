import os
import json
import random
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def post_blog():
    # 1. 인증 정보 로드 (기존 성공 방식)
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    creds_info = json.loads(creds_json)
    creds = Credentials.from_authorized_user_info(creds_info)

    BLOG_ID = '3209144423549555087'
    service = build('blogger', 'v3', credentials=creds)

    # 2. 개인정보 보호법 조문 데이터베이스 (제1조, 제2조 등 전체 내용)
    law_articles = [
        {
            "title": "제1조(목적)",
            "content": "이 법은 개인정보의 처리 및 보호에 관한 사항을 정함으로써 개인의 자유와 권리를 보호하고, 나아가 개인의 존엄과 가치를 구현함을 목적으로 한다."
        },
        {
            "title": "제2조(정의) 주요 내용",
            "content": "1. '개인정보'란 살아 있는 개인에 관한 정보로서 성명, 주민등록번호 등을 통해 개인을 알아볼 수 있는 정보를 말한다.<br>2. '처리'란 개인정보의 수집, 저장, 보유, 가공, 제공, 파기 등 유사한 모든 행위를 말한다.<br>3. '정보주체'란 처리되는 정보에 의하여 알아볼 수 있는 사람으로서 그 정보의 주체가 되는 사람을 말한다."
        },
        {
            "title": "제3조(개인정보 보호 원칙)",
            "content": "① 개인정보처리자는 개인정보의 처리 목적을 명확하게 하여야 하고 그 목적에 필요한 범위에서 최소한의 개인정보만을 적법하고 정당하게 수집하여야 한다.<br>② 목적 외의 용도로 활용하여서는 아니 된다.<br>③ 개인정보의 정확성, 완전성 및 최신성이 보장되도록 하여야 한다."
        },
        {
            "title": "제4조(정보주체의 권리)",
            "content": "1. 개인정보의 처리에 관한 정보를 제공받을 권리<br>2. 동의 여부, 동의 범위 등을 선택하고 결정할 권리<br>3. 개인정보의 처리 여부 확인 및 열람 요구권<br>4. 처리 정지, 정정·삭제 및 파기 요구권"
        }
    ]

    # 3. ISMS-P 인증 항목 데이터
    isms_p_topics = [
        "1.1.1 최고경영자의 참여 - 경영진은 개인정보 보호 및 보안의 최고 의사결정 기구에 참여해야 함",
        "1.2.1 위험 관리 - 조직의 핵심 자산에 대한 위험 식별 및 평가 절차 수립",
        "2.1.1 개인정보 수집 제한 - 서비스 제공에 필요한 최소한의 정보만 수집하는지 확인"
    ]

    # 4. 랜덤 추출 (법령 1개 조문 전체 + 인증항목 3개)
    selected_law = random.choice(law_articles)
    selected_isms = random.sample(isms_p_topics, 3)

    # 5. HTML 콘텐츠 구성
    html_content = f"""
    <h3>⚖️ 법령 깊이 알기: {selected_law['title']}</h3>
    <blockquote style='background: #f9f9f9; padding: 15px;'>
        {selected_law['content']}
    </blockquote>
    
    <h3>🛠️ ISMS-P 인증항목 체크리스트</h3>
    <ul>
        {"".join([f"<li>{item}</li>" for item in selected_isms])}
    </ul>
    <p><br>출처: 국가법령정보센터 및 KISA 가이드라인 기반 자동 생성</p>
    """

    post_body = {
        'kind': 'blogger#post',
        'title': f"📅 [자동포스팅] {selected_law['title']} 및 ISMS-P 학습",
        'content': html_content
    }

    try:
        service.posts().insert(blogId=BLOG_ID, body=post_body).execute()
        print(f"✅ {selected_law['title']} 포스팅 성공!")
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == "__main__":
    post_blog()
