import os
from datetime import datetime
from typing import Dict, Any, Optional
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore


KEY_FILE_PATH = "firebase_key.json"


@st.cache_resource
def get_db() -> Optional[firestore.Client]:
    """
    Firebase Admin SDK를 초기화하고 Firestore 클라이언트를 반환합니다.
    Streamlit Cloud(st.secrets)와 로컬(firebase_key.json) 환경을 모두 지원합니다.
    """
    try:
        if not firebase_admin._apps:
            # 1. Streamlit Community Cloud 배포 환경 (Secrets 사용)
            if "firebase" in st.secrets:
                key_dict = dict(st.secrets["firebase"])
                cred = credentials.Certificate(key_dict)
                firebase_admin.initialize_app(cred)
            # 2. 로컬 실행 환경 (루트 경로의 JSON 파일 사용)
            elif os.path.exists(KEY_FILE_PATH):
                cred = credentials.Certificate(KEY_FILE_PATH)
                firebase_admin.initialize_app(cred)
            else:
                return None
        return firestore.client()
    except Exception as exc:
        st.error(f"Firebase 초기화 중 오류가 발생했습니다: {exc}")
        return None


def get_today_doc_ref() -> Optional[firestore.DocumentReference]:
    """당일 날짜(YYYY-MM-DD)를 문서 ID로 사용하는 Firestore DocumentReference를 반환합니다."""
    client = get_db()
    if client is None:
        return None
    today_str = datetime.now().strftime("%Y-%m-%d")
    return client.collection("daily_live_boards").document(today_str)


def add_command_item(description: str, command: str) -> bool:
    """아나콘다/터미널 명령어를 당일 문서의 commands 배열에 추가합니다."""
    doc_ref = get_today_doc_ref()
    if doc_ref is None:
        st.error("데이터베이스에 연결할 수 없습니다. Firebase 설정을 확인하세요.")
        return False

    item: Dict[str, Any] = {
        "description": description.strip() if description.strip() else "실행 명령어",
        "command": command.strip(),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

    try:
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update({"commands": firestore.ArrayUnion([item])})
        else:
            doc_ref.set({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "commands": [item],
                "codes": []
            })
        return True
    except Exception as exc:
        st.error(f"명령어 등록 중 오류가 발생했습니다: {exc}")
        return False


def add_code_item(title: str, lang: str, code: str) -> bool:
    """실습 소스코드를 당일 문서의 codes 배열에 추가합니다."""
    doc_ref = get_today_doc_ref()
    if doc_ref is None:
        st.error("데이터베이스에 연결할 수 없습니다. Firebase 설정을 확인하세요.")
        return False

    item: Dict[str, Any] = {
        "title": title.strip() if title.strip() else "실습 소스코드",
        "lang": lang.lower(),
        "code": code.strip(),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

    try:
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update({"codes": firestore.ArrayUnion([item])})
        else:
            doc_ref.set({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "commands": [],
                "codes": [item]
            })
        return True
    except Exception as exc:
        st.error(f"코드 등록 중 오류가 발생했습니다: {exc}")
        return False


def get_today_data() -> Dict[str, Any]:
    """
    당일 날짜에 등록된 명령어와 코드 전체 데이터를 반환합니다.
    문서가 없거나 에러 발생 시 기본 빈 리스트 딕셔너리를 반환합니다.
    """
    doc_ref = get_today_doc_ref()
    if doc_ref is None:
        return {"commands": [], "codes": []}

    try:
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict() or {}
            return {
                "commands": data.get("commands", []),
                "codes": data.get("codes", [])
            }
    except Exception as exc:
        st.warning(f"데이터를 불러오는 중 문제가 발생했습니다: {exc}")

    return {"commands": [], "codes": []}