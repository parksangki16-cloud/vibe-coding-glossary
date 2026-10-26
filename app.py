import streamlit as st
import time
import random

# 페이지 기본 설정
st.set_page_config(
    page_title="바이브 코딩 용어 사전 & 프롬프트 변환기",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------------------------------------------
# CSS를 활용한 글로벌 글자 크기 확대 (기존보다 큼직하게 폰트 지정)
# -------------------------------------------------------------------
st.markdown("""
    <style>
    /* 전체 기본 본문 글자 크기 확대 (18px) */
    html, body, [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li {
        font-size: 18px !important;
    }
    /* 입력창 및 버튼 글자 크기 확대 */
    .stTextInput input, .stTextArea textarea, .stButton button p {
        font-size: 18px !important;
    }
    /* 토글(Expander) 제목 글자 크기 확대 */
    [data-testid="stExpander"] summary p {
        font-size: 20px !important;
        font-weight: bold !important;
    }
    /* 탭 메뉴 글자 크기 확대 */
    button[data-baseweb="tab"] p {
        font-size: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# 1. 30선 용어 데이터베이스 (JSON 구조)
# -------------------------------------------------------------------
TERMS_DATA = [
    # [카테고리 1: 기획 & 구조 설계]
    {"category": "기획/설계", "term": "프롬프트 (Prompt)", "analogy": "요리사에게 내리는 '주문서'", "vibe_use": "AI에게 원하는 기능, 디자인, 규칙을 지시하는 모든 자연어 명령문입니다.", "prompt_ex": "회원가입 기능이 있는 웹사이트를 만들 수 있는 프롬프트를 작성해줘."},
    {"category": "기획/설계", "term": "컨텍스트 (Context)", "analogy": "의사가 환자의 상태를 파악할 때 보는 '진료 기록부'", "vibe_use": "AI가 이전 대화 내용, 현재 프로젝트의 코드 구조, 파일 상황을 기억하고 이해하는 '맥락 정보'입니다.", "prompt_ex": "지금까지 작성한 main.py 코드를 컨텍스트로 참고해서, 로그인 함수를 추가해줘."},
    {"category": "기획/설계", "term": "기술 스택 (Tech Stack)", "analogy": "집을 지을 때 사용하는 '자재 목록'", "vibe_use": "웹/앱을 만드는 데 사용되는 언어, 프레임워크, 데이터베이스의 조합입니다.", "prompt_ex": "초보자가 관리하기 가장 쉬운 파이썬 기반 기술 스택으로 프로젝트 구조를 잡아줘."},
    {"category": "기획/설계", "term": "와이어프레임 (Wireframe)", "analogy": "건축물의 '평면 설계도'", "vibe_use": "디자인 요소나 색상 없이, 화면 요소들의 위치와 배치만 간략히 그린 뼈대입니다.", "prompt_ex": "쇼핑몰 메인 페이지에 들어갈 화면 요소들의 와이어프레임 구조를 텍스트로 정리해줘."},
    {"category": "기획/설계", "term": "사용자 여정 (User Flow)", "analogy": "놀이공원의 '관람 동선'", "vibe_use": "사용자가 앱에 접속해서 목적을 달성할 때까지 거치는 화면 이동 순서입니다.", "prompt_ex": "사용자가 상품 검색부터 결제 완료까지 거치는 유저 플로우를 단계별로 설명해줘."},
    {"category": "기획/설계", "term": "MVP (최소 기능 제품)", "analogy": "정식 출시에 앞서 만든 '시식용 핑거푸드'", "vibe_use": "핵심 기능 1~2개만 빠르게 작동하도록 만들어 테스트하는 초기 시제품입니다.", "prompt_ex": "일단 회원가입 빼고, 검색 기능만 작동하는 MVP 버전으로 코드를 짜줘."},

    # [카테고리 2: 프론트엔드 & UI]
    {"category": "프론트엔드/UI", "term": "프론트엔드 (Frontend)", "analogy": "카페의 '카운터와 매장 인테리어'", "vibe_use": "사용자가 눈으로 보고 직접 클릭하는 웹사이트/앱의 모든 화면 영역입니다.", "prompt_ex": "모바일 화면에서도 예쁘게 보이는 반응형 프론트엔드 코드를 만들어줘."},
    {"category": "프론트엔드/UI", "term": "HTML", "analogy": "건물의 '콘크리트 뼈대'", "vibe_use": "웹페이지의 글자, 이미지, 버튼 등 구조적 틀을 형성하는 언어입니다.", "prompt_ex": "제목, 입력창, 제출 버튼이 포함된 기본 HTML 구조를 만들어줘."},
    {"category": "프론트엔드/UI", "term": "CSS", "analogy": "건물의 '페인트칠과 인테리어'", "vibe_use": "HTML로 만든 뼈대에 색상, 글꼴, 크기, 여백 등 스타일을 입히는 디자인 언어입니다.", "prompt_ex": "버튼에 마우스를 올리면 파란색으로 부드럽게 커지는 CSS 효과를 적용해줘."},
    {"category": "프론트엔드/UI", "term": "JavaScript (JS)", "analogy": "건물 안의 '엘리베이터와 자동문 동작장치'", "vibe_use": "버튼 클릭 시 팝업 창이 뜨거나 데이터가 바뀌는 등 화면에 생동감을 주는 언어입니다.", "prompt_ex": "버튼을 누르면 '제출되었습니다' 팝업이 뜨는 자바스크립트 함수를 작성해줘."},
    {"category": "프론트엔드/UI", "term": "UI / UX", "analogy": "자동차의 '핸들 디자인(UI)'과 '승차감(UX)'", "vibe_use": "UI는 눈에 보이는 화면 디자인, UX는 사용자가 느낄 때의 편리함과 경험입니다.", "prompt_ex": "어르신들도 쉽게 읽을 수 있도록 UI/UX를 고려해 폰트 크기와 버튼을 크게 만들어줘."},
    {"category": "프론트엔드/UI", "term": "컴포넌트 (Component)", "analogy": "마음대로 뗐다 붙이는 '레고 블록'", "vibe_use": "상단 메뉴바, 버튼, 카드 등 재사용이 가능하도록 독립적으로 만든 화면 부품 단위입니다.", "prompt_ex": "여러 페이지에서 돌려쓸 수 있는 카드 형태의 컴포넌트를 분리해서 만들어줘."},
    {"category": "프론트엔드/UI", "term": "반응형 웹 (Responsive Web)", "analogy": "몸집에 따라 자동으로 늘어나는 '요술 옷'", "vibe_use": "PC, 태블릿, 스마트폰 화면 크기에 맞춰 레이아웃이 자동으로 변하는 웹페이지입니다.", "prompt_ex": "스마트폰으로 볼 때는 메뉴바가 삼선 버튼으로 바뀌는 반응형 웹으로 작성해줘."},
    {"category": "프론트엔드/UI", "term": "토글 (Toggle)", "analogy": "방 안의 '전등 스위치'", "vibe_use": "하나의 버튼으로 2가지 상태를 번갈아 바꾸는 기능입니다.", "prompt_ex": "Q&A 항목을 클릭하면 답변이 쫙 펼쳐지고 다시 누르면 접히는 토글 리스트를 만들어줘."},

    # [카테고리 3: 백엔드 & 데이터]
    {"category": "백엔드/데이터", "term": "백엔드 (Backend)", "analogy": "카페의 '주방과 재고 창고'", "vibe_use": "데이터 저장, 계산, 회원 인증 등 핵심 로직을 처리하는 서버 영역입니다.", "prompt_ex": "비밀번호를 암호화해서 데이터베이스에 저장하는 백엔드 로직을 작성해줘."},
    {"category": "백엔드/데이터", "term": "서버 (Server)", "analogy": "24시간 쉬지 않는 '중앙 주문센터'", "vibe_use": "사용자의 요청을 받아 원하는 데이터나 화면을 전달해 주는 컴퓨터 프로그램입니다.", "prompt_ex": "파이썬 Flask를 사용해서 간단하게 동작하는 로컬 서버 코드를 짜줘."},
    {"category": "백엔드/데이터", "term": "API", "analogy": "손님과 주방 사이를 오가는 '점원(웨이터)'", "vibe_use": "서로 다른 프로그램이 데이터를 주고받기 위한 통로/규약입니다.", "prompt_ex": "구글 지도 API를 연결해서 위치 정보를 화면에 표시해줘."},
    {"category": "백엔드/데이터", "term": "데이터베이스 (DB)", "analogy": "정보를 정리해 두는 '전자 서류함'", "vibe_use": "회원정보, 게시글 내역 등을 안전하게 보관하고 필요할 때 찾아 쓰는 창고입니다.", "prompt_ex": "사용자 아이디, 이메일, 가입일자를 저장할 수 있는 DB 테이블 구조를 짜줘."},
    {"category": "백엔드/데이터", "term": "JSON", "analogy": "전 세계 공통으로 쓰는 '표준 서식 양식지'", "vibe_use": "서버와 웹 브라우저가 데이터를 주고받을 때 쓰는 텍스트 형식입니다.", "prompt_ex": "이름, 나이, 직업 데이터를 표준 JSON 형식으로 출력해줘."},
    {"category": "백엔드/데이터", "term": "환경 변수 (.env)", "analogy": "비밀번호를 보관하는 '금고'", "vibe_use": "API 키나 비밀번호 등 민감한 정보를 저장하는 별도 설정 파일입니다.", "prompt_ex": "OpenAI API 키가 코드에 노출되지 않도록 .env 파일로 분리해줘."},
    {"category": "백엔드/데이터", "term": "CRUD (크루드)", "analogy": "서류를 '만들고, 읽고, 수정하고, 파쇄하는' 업무", "vibe_use": "데이터 관리 프로그램이 갖춰야 할 기본 4대 기능(생성, 조회, 수정, 삭제)입니다.", "prompt_ex": "게시판 메모장을 위해 기본적인 CRUD 기능이 포함된 파이썬 코드를 작성해줘."},
    {"category": "백엔드/데이터", "term": "라우팅 (Routing)", "analogy": "건물의 '이정표'", "vibe_use": "입력한 웹 주소(URL)에 따라 알맞은 화면이나 데이터를 연결해 주는 안내 역할입니다.", "prompt_ex": "`/login` 주소로 들어오면 로그인 페이지를 보여주는 라우팅 코드를 추가해줘."},

    # [카테고리 4: 배포 & 오류 해결]
    {"category": "배포/오류해결", "term": "디버깅 (Debugging)", "analogy": "음식에서 '이물질을 찾아 제거하는 작업'", "vibe_use": "코드의 잘못된 부분(버그)을 찾아 정상 작동하도록 수정하는 과정입니다.", "prompt_ex": "이 코드에서 에러가 발생하는데 원인을 디버깅하고 수정된 코드를 보여줘."},
    {"category": "배포/오류해결", "term": "터미널 / CLI", "analogy": "글자로만 명령을 내리는 '조종석 모니터'", "vibe_use": "텍스트 명령어를 직접 입력하여 프로그램을 실행하고 제어하는 창입니다.", "prompt_ex": "이 프로젝트를 실행하기 위해 터미널에 입력해야 하는 명령어를 순서대로 알려줘."},
    {"category": "배포/오류해결", "term": "패키지 / 의존성", "analogy": "직접 요리하지 않고 사서 쓰는 '밀키트'", "vibe_use": "남들이 미리 만들어 둔 유용한 코드 모음(라이브러리)입니다.", "prompt_ex": "엑셀 파일 읽기에 필요한 파이썬 패키지를 install하는 명령어를 알려줘."},
    {"category": "배포/오류해결", "term": "배포 (Deploy)", "analogy": "신제품을 매장 '진열대에 올리고 오픈'하는 것", "vibe_use": "내 컴퓨터에서 만든 프로그램을 실제 인터넷상에 올려 남들도 접속하게 만드는 과정입니다.", "prompt_ex": "이 웹 앱을 Netlify나 Vercel을 이용해 무료로 배포하는 순서를 가르쳐줘."},
    {"category": "배포/오류해결", "term": "Git / GitHub", "analogy": "게임의 '타임머신 저장 기능과 온라인 저장소'", "vibe_use": "코드 변경 이력을 관리하고 백업하며 협업할 수 있는 도구입니다.", "prompt_ex": "지금까지 만든 코드를 GitHub 저장소에 올리는 Git 명령어를 순서대로 써줘."},
    {"category": "배포/오류해결", "term": "CORS 에러", "analogy": "다른 아파트 출입문에서 '외부인 출입 통제'", "vibe_use": "보안상 이유로 서로 다른 서버 간 데이터 요청이 막혔을 때 발생하는 오류입니다.", "prompt_ex": "프론트엔드와 백엔드를 통신할 때 CORS 에러가 발생하는데 해결 코드를 작성해줘."},
    {"category": "배포/오류해결", "term": "터미널 권한 에러", "analogy": "열쇠가 없어서 문을 열지 못함", "vibe_use": "컴퓨터가 관리자 권한이 없는 사용자의 실행을 차단했을 때 발생하는 오류입니다.", "prompt_ex": "터미널에서 Permission denied 에러가 떠. 해결 조치 방법을 알려줘."},
    {"category": "배포/오류해결", "term": "환각 현상 (Hallucination)", "analogy": "AI가 너무 진지하게 말하는 '거짓말'", "vibe_use": "AI가 존재하지 않는 패키지 이름을 말하거나 틀린 코드를 맞다고 우기는 현상입니다.", "prompt_ex": "환각 없이 실제 PyPI에 등록된 공식 패키지로 다시 추천해 줘."}
]

# -------------------------------------------------------------------
# 2. 메인 화면 레이아웃 및 탭 구성
# -------------------------------------------------------------------
st.title("🚀 바이브 코딩 용어 사전 & 프롬프트 변환기")
st.caption("초보자를 위한 비유 기반 용어 학습 및 AI 프롬프트 변환 도구 (글자 크기 확대 버젼)")

tab1, tab2, tab3 = st.tabs(["📚 30선 용어 사전", "🪄 프롬프트 변환기", "🧩 용어 복습 퀴즈"])

# -------------------------------------------------------------------
# [TAB 1] 30선 용어 사전 (검색 + 토글 UI)
# -------------------------------------------------------------------
with tab1:
    st.subheader("🔍 핵심 용어 검색 및 학습")

    # 검색어 및 카테고리 필터
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("검색어를 입력하세요 (예: API, 프론트엔드, 토글)", "")
    with col2:
        # dict.fromkeys로 중복 제거하면서 데이터 순서(기획 → 프론트 → 백엔드 → 배포) 유지
        categories = ["전체"] + list(dict.fromkeys(item["category"] for item in TERMS_DATA))
        selected_cat = st.selectbox("카테고리 선택", categories)

    st.divider()

    # 데이터 필터링 로직 (용어명·비유·설명 모두에서 대소문자 무시 검색)
    filtered_terms = TERMS_DATA
    if selected_cat != "전체":
        filtered_terms = [t for t in filtered_terms if t["category"] == selected_cat]
    query = search_query.strip().lower()
    if query:
        filtered_terms = [
            t for t in filtered_terms
            if query in t["term"].lower() or query in t["analogy"].lower() or query in t["vibe_use"].lower()
        ]

    st.write(f"총 **{len(filtered_terms)}개**의 용어가 검색되었습니다.")

    # 토글(Expander) UI로 목록 출력
    for item in filtered_terms:
        with st.expander(f"📌 [{item['category']}] {item['term']}"):
            st.markdown(f"**💡 실생활 비유:** {item['analogy']}")
            st.markdown(f"**📖 바이브 코딩 쓰임새:** {item['vibe_use']}")
            st.info(f"**💬 AI 지시 프롬프트 예시:**\n\"{item['prompt_ex']}\"")

# -------------------------------------------------------------------
# [TAB 2] 프롬프트 변환기 (무료 테스트 모드)
# -------------------------------------------------------------------
with tab2:
    st.subheader("🪄 초보자의 쉬운 말을 전문 프롬프트로 변환")
    st.success("🟢 **무료 테스트 모드 동작 중:** 별도의 API Key나 요금 지불 없이 바로 사용 가능합니다.")
    
    user_input = st.text_area("만들고 싶은 기능이나 요청 사항을 쉬운 말로 적어주세요:", 
                              placeholder="예: 상품 목록 화면 만들어주고 클릭하면 상세 페이지로 넘어가게 해줘.")
    
    if st.button("전문 프롬프트로 변환하기 🚀"):
        if not user_input.strip():
            st.warning("변환할 요청 내용을 입력해 주세요.")
        else:
            with st.spinner("AI가 고품질 프롬프트를 생성 중입니다..."):
                time.sleep(1) # 시각적 효과를 위한 1초 대기
                
                st.success("변환 완료!")
                
                # 여러 줄 입력 시 인용(>) 블록이 깨지지 않도록 한 줄로 합침
                request_text = " ".join(user_input.split())
                
                # 입력받은 모호한 표현을 기술 프롬프트로 재구성
                st.markdown(f"""
### ■ AI 지시용 업그레이드 프롬프트 (Cursor / Claude에 그대로 복사하세요)

> 너는 10년 차 수석 프론트엔드 및 백엔드 개발자다.
> 사용자의 요구사항 **"{request_text}"**을 바탕으로 완전한 코드를 작성해 줘.
> 
> **[기술 스택]** React, Tailwind CSS, Node.js/Express
> **[구현 요구사항]**
> 1. 모던하고 깔끔한 UI 컴포넌트를 설계하고, 반응형 레이아웃을 적용해 줘.
> 2. 상태 관리(State Management)를 통해 사용자의 입력값 및 데이터 흐름을 안전하게 처리해 줘.
> 3. 주소 이동(Routing) 처리 시 페이지 전환이 부드럽게 이루어지도록 라우팅 로직을 구축해 줘.
> 4. 발생할 수 있는 에러(예: 데이터 부재, 통신 오류)에 대한 예외 처리 로직을 포함해 줘.

---

### ■ 이 프롬프트에 사용된 핵심 용어 한 줄 학습
* **컴포넌트 (Component):** 재사용 가능한 화면 부품 (상품 카드, 상세 화면 등)
* **라우팅 (Routing):** 클릭 시 원하는 다른 페이지 주소로 안내해 주는 이정표 역할
* **상태 관리 (State Management):** 사용자가 입력하거나 변경한 데이터를 기억해 두는 서류함
""")

# -------------------------------------------------------------------
# [TAB 3] 용어 복습 퀴즈 (4지선다)
# -------------------------------------------------------------------
def save_current_to_history():
    """현재 문제(선택한 보기 포함)를 기록에 저장"""
    quiz = st.session_state.quiz
    if quiz:
        quiz["picked"] = st.session_state.get(f"quiz_pick_{st.session_state.quiz_round}")
        st.session_state.quiz_history.append(quiz)

def new_quiz_question():
    """정답 1개 + 오답 3개로 새 문제를 만들어 session_state에 저장"""
    save_current_to_history()
    answer_idx = random.randrange(len(TERMS_DATA))
    wrong_idxs = random.sample([i for i in range(len(TERMS_DATA)) if i != answer_idx], 3)
    choices = [TERMS_DATA[i]["term"] for i in [answer_idx] + wrong_idxs]
    random.shuffle(choices)
    st.session_state.quiz = {"answer_idx": answer_idx, "choices": choices, "checked": False, "correct": False, "picked": None}
    st.session_state.quiz_round += 1  # 라디오 버튼 선택값 초기화용

def prev_quiz_question():
    """기록에서 바로 전 문제를 꺼내 다시 표시 (채점 결과·선택값 그대로)"""
    if not st.session_state.quiz_history:
        return
    st.session_state.quiz = st.session_state.quiz_history.pop()
    st.session_state.quiz_round += 1
    st.session_state[f"quiz_pick_{st.session_state.quiz_round}"] = st.session_state.quiz["picked"]

def check_quiz_answer():
    """선택한 보기를 채점하고 점수 반영"""
    quiz = st.session_state.quiz
    picked = st.session_state.get(f"quiz_pick_{st.session_state.quiz_round}")
    quiz["checked"] = True
    quiz["picked"] = picked
    quiz["correct"] = picked == TERMS_DATA[quiz["answer_idx"]]["term"]
    st.session_state.quiz_total += 1
    if quiz["correct"]:
        st.session_state.quiz_score += 1

def restart_quiz():
    """[처음으로] 점수·기록·현재 문제를 모두 리셋하고 새 문제로 시작"""
    st.session_state.quiz_score = 0
    st.session_state.quiz_total = 0
    st.session_state.quiz_history = []
    st.session_state.quiz = None
    st.session_state.quiz_active = True
    new_quiz_question()

def stop_quiz():
    """[퀴즈 중단] 진행을 멈추고 초기 화면으로 전환"""
    st.session_state.quiz_active = False

with tab3:
    st.subheader("🧩 용어 복습 퀴즈")

    if "quiz_active" not in st.session_state:
        st.session_state.quiz_active = False
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = 0
        st.session_state.quiz_round = 0
        st.session_state.quiz_history = []
        st.session_state.quiz = None

    total = st.session_state.quiz_total

    # 퀴즈 초기 화면 (안내 + 시작 버튼)
    if not st.session_state.quiz_active:
        st.info("💡 비유와 설명을 읽고, 알맞은 용어를 4개 보기 중에서 골라 보세요.\n\n"
                "문제는 30선 용어 중에서 무작위로 출제됩니다.")
        if total:
            st.write(f"📊 지난 퀴즈 결과: **{st.session_state.quiz_score} / {total}**")
        st.button("퀴즈 시작하기 ▶️", on_click=restart_quiz, type="primary")

    # 퀴즈 진행 화면
    else:
        quiz = st.session_state.quiz
        answer = TERMS_DATA[quiz["answer_idx"]]

        st.write(f"**문제 {len(st.session_state.quiz_history) + 1}**")
        st.info(f"**💡 실생활 비유:** {answer['analogy']}\n\n**📖 설명:** {answer['vibe_use']}")

        picked = st.radio("정답을 고르세요:", quiz["choices"], index=None,
                          key=f"quiz_pick_{st.session_state.quiz_round}", disabled=quiz["checked"])

        btn1, btn2 = st.columns(2)
        btn1.button("채점하기 ✅", on_click=check_quiz_answer, disabled=quiz["checked"] or picked is None)
        btn2.button("다음 문제 ➡️", on_click=new_quiz_question)

        if quiz["checked"]:
            if quiz["correct"]:
                st.success(f"🎉 정답입니다! **{answer['term']}**")
            else:
                st.error(f"아쉬워요. 정답은 **{answer['term']}** 입니다.")
            st.markdown(f"**💬 AI 지시 프롬프트 예시:** \"{answer['prompt_ex']}\"")

        st.divider()
        rate = round(st.session_state.quiz_score / total * 100) if total else 0
        st.write(f"📊 현재 점수: **{st.session_state.quiz_score} / {total}** (정답률 {rate}%)")

        ctrl1, ctrl2, ctrl3 = st.columns(3)
        ctrl1.button("이전 문제 ⬅️", on_click=prev_quiz_question, disabled=not st.session_state.quiz_history)
        ctrl2.button("처음으로 🔄", on_click=restart_quiz)
        ctrl3.button("퀴즈 중단 🛑", on_click=stop_quiz)
