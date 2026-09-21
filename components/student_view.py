from datetime import datetime
from typing import List, Dict, Any
import streamlit as st
from firebase.db import get_today_data


@st.fragment(run_every="2s")
def render_live_sync_board() -> None:
    """
    2초 주기로 백그라운드에서 데이터를 가져와 화면 깜빡임 없이 
    학생용 보드를 최신 상태로 갱신하는 프래그먼트 함수입니다.
    """
    data = get_today_data()
    commands: List[Dict[str, Any]] = data.get("commands", [])
    codes: List[Dict[str, Any]] = data.get("codes", [])

    current_time_str = datetime.now().strftime("%H:%M:%S")

    # 상단 상태 표시 바
    st.markdown(
        f"🟢 **LIVE 동기화 가동 중** `[마지막 확인: {current_time_str}]` "
        f"*(교수님이 업로드하면 화면 새로고침 없이 즉시 반영됩니다)*"
    )
    st.divider()

    # 화면 2열 분할: 좌측 명령어 / 우측 소스코드
    col_commands, col_codes = st.columns(2)

    # --- 1. 아나콘다 / 터미널 명령어 표시 영역 ---
    with col_commands:
        st.markdown("### ⚡ Anaconda / PowerShell 명령어")

        if not commands:
            st.info("현재 배포된 Anaconda 명령어가 없습니다. 대기 중...")
        else:
            # 최신 등록 항목이 맨 위로 오도록 역순 정렬
            for idx, item in enumerate(reversed(commands)):
                desc = item.get("description", "실행 명령어")
                cmd_text = item.get("command", "")
                ts = item.get("timestamp", "")

                with st.container(border=True):
                    st.markdown(f"**📌 {desc}** `({ts})`")
                    # PowerShell 문법 강조 및 우측 상단 원클릭 복사 지원
                    st.code(cmd_text, language="powershell")

    # --- 2. 실습 소스코드 표시 영역 ---
    with col_codes:
        st.markdown("### 💻 실습 소스코드")

        if not codes:
            st.info("현재 배포된 실습 코드가 없습니다. 대기 중...")
        else:
            # 최신 등록 항목이 맨 위로 오도록 역순 정렬
            for idx, item in enumerate(reversed(codes)):
                title = item.get("title", "실습 소스코드")
                lang = item.get("lang", "python")
                code_text = item.get("code", "")
                ts = item.get("timestamp", "")

                with st.container(border=True):
                    st.markdown(f"**📝 {title}** `({ts})`")
                    st.code(code_text, language=lang)


def render_student_view() -> None:
    """학생용 뷰 진입 렌더러"""
    render_live_sync_board()