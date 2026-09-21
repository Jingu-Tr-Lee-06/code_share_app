import streamlit as st
from firebase.db import add_command_item, add_code_item

# 관리자 인증 기본 비밀번호 (필요에 따라 변경 가능)
PROFESSOR_ACCESS_KEY = "prof1234"

# 지원 프로그래밍 언어 목록
SUPPORTED_LANGUAGES = [
    "python",
    "c",
    "cpp",
    "java",
    "sql",
    "html",
    "javascript",
    "bash",
    "markdown"
]


def render_professor_view() -> None:
    """교수자 전용 배포 화면을 렌더링합니다."""
    st.markdown("### 👨‍🏫 교수자 배포 센터")
    st.caption("학생들에게 실시간으로 공유할 명령어 또는 소스코드를 작성하여 배포하세요.")

    # 1. 관리자 인증 입력창
    col_auth, _ = st.columns([1, 2])
    with col_auth:
        entered_key = st.text_input(
            "관리자 인증 키",
            type="password",
            placeholder="인증 키를 입력하세요",
            key="prof_auth_input",
            help="배포 권한을 확인하기 위한 비밀번호입니다."
        )

    if entered_key != PROFESSOR_ACCESS_KEY:
        st.info("올바른 관리자 인증 키를 입력하면 배포 폼이 활성화됩니다.")
        return

    st.success("관리자 권한이 확인되었습니다.")
    st.divider()

    # 2. 업로드 폼 분할 레이아웃
    col_cmd, col_code = st.columns(2)

    # --- [왼쪽] 아나콘다/터미널 명령어 배포 영역 ---
    with col_cmd:
        st.markdown("#### ⚡ Anaconda / PowerShell 명령어 배포")
        with st.form("form_anaconda_command", clear_on_submit=True):
            cmd_desc = st.text_input(
                "명령어 설명 / 작업 단계",
                placeholder="예: [1단계] 실습 가상환경 생성 및 패키지 설치"
            )
            cmd_body = st.text_area(
                "PowerShell 명령어 내용",
                height=220,
                placeholder="conda create -n test_env python=3.10 -y\nconda activate test_env\npip install numpy pandas"
            )
            btn_submit_cmd = st.form_submit_button(
                "⚡ 명령어 실시간 배포",
                type="primary",
                use_container_width=True
            )

            if btn_submit_cmd:
                if not cmd_body.strip():
                    st.warning("배포할 명령어 내용을 입력해주세요.")
                else:
                    success = add_command_item(
                        description=cmd_desc,
                        command=cmd_body
                    )
                    if success:
                        st.toast("명령어가 성공적으로 배포되었습니다!", icon="🚀")

    # --- [오른쪽] 실습 소스코드 배포 영역 ---
    with col_code:
        st.markdown("#### 💻 실습 소스코드 배포")
        with st.form("form_source_code", clear_on_submit=True):
            code_title = st.text_input(
                "코드 제목 / 실습 문제 번호",
                placeholder="예: [실습 1] 버블 정렬 알고리즘 구현"
            )
            selected_lang = st.selectbox(
                "문법 강조 언어",
                SUPPORTED_LANGUAGES,
                index=0
            )
            code_body = st.text_area(
                "소스코드 내용",
                height=220,
                placeholder="# 학생들에게 전달할 소스코드를 여기에 작성하거나 붙여넣으세요."
            )
            btn_submit_code = st.form_submit_button(
                "💻 소스코드 실시간 배포",
                type="primary",
                use_container_width=True
            )

            if btn_submit_code:
                if not code_body.strip():
                    st.warning("배포할 소스코드 내용을 입력해주세요.")
                else:
                    success = add_code_item(
                        title=code_title,
                        lang=selected_lang,
                        code=code_body
                    )
                    if success:
                        st.toast("소스코드가 성공적으로 배포되었습니다!", icon="🚀")