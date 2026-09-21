import os
import streamlit as st

# Streamlit 페이지 기본 설정 (반드시 스크립트 최상단에 위치)
st.set_page_config(
    page_title="실시간 강의 코드 & 명령어 보드",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from firebase.db import get_db
from components.student_view import render_student_view
from components.professor_view import render_professor_view


def check_system_ready() -> bool:
    """Firebase 설정 상태(Streamlit Secrets 또는 로컬 키 파일) 및 DB 연결을 점검합니다."""
    # 1. 인증 수단 존재 여부 확인 (클라우드 Secrets 또는 로컬 파일)
    has_secrets = "firebase" in st.secrets
    has_local_file = os.path.exists("firebase_key.json")

    if not has_secrets and not has_local_file:
        st.error(
            "⚠️ Firebase 인증 설정을 찾을 수 없습니다.\n\n"
            "- **로컬 실행 시**: `firebase_key.json` 파일을 프로젝트 루트 폴더에 넣어주세요.\n"
            "- **Streamlit Cloud 배포 시**: App Settings > Secrets에 `[firebase]` 설정을 등록해주세요."
        )
        return False

    # 2. Firestore 클라이언트 초기화 상태 확인
    client = get_db()
    if client is None:
        st.error("⚠️ Firebase 데이터베이스 연결에 실패했습니다. 키 정보 및 네트워크 상태를 확인하세요.")
        return False

    return True


def main() -> None:
    # 대시보드 헤더
    st.title("🖥️ 실시간 수업 코드 & 명령어 공유 보드")
    st.caption("수업 중 교수님이 배포하는 Anaconda 명령어와 실습 코드를 실시간으로 복사할 수 있습니다.")

    # 환경 검증 통과 실패 시 실행 중단
    if not check_system_ready():
        st.stop()

    # 상단 탭 분리
    tab_student, tab_professor = st.tabs([
        "📋 학생용 실시간 라이브 뷰",
        "⚙️ 교수자 배포 모드"
    ])

    with tab_student:
        render_student_view()

    with tab_professor:
        render_professor_view()


if __name__ == "__main__":
    main()