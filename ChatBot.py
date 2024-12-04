import streamlit as st
import os
import openai
import pandas as pd
from datetime import datetime

# OpenAI API 키 설정
openai.api_key = st.secrets["openai"]["api_key"]

# 맛집 데이터 샘플
restaurant_list = [
    {"name": "백제불고기", "location": "공주시", "specialty": "불고기"},
    {"name": "서산해물탕", "location": "서산시", "specialty": "해물탕"},
    {"name": "아산칼국수", "location": "아산시", "specialty": "칼국수"},
    {"name": "논산비빔밥", "location": "논산시", "specialty": "비빔밥"},
    {"name": "당진초밥", "location": "당진시", "specialty": "초밥"},
]

# 예약 데이터를 저장할 DataFrame
if "reservations" not in st.session_state:
    st.session_state.reservations = pd.DataFrame(columns=["name", "restaurant", "date", "time", "people"])

# 앱 제목
st.title("충남 맛집 추천 & 예약 시스템 + 챗봇 🍴🤖")

# 1️⃣ 맛집 리스트 출력
st.header("📌 충남 지역 맛집 리스트")
for restaurant in restaurant_list:
    st.markdown(f"- **{restaurant['name']}** (위치: {restaurant['location']}, 대표메뉴: {restaurant['specialty']})")

# 2️⃣ 예약 섹션
st.header("📅 예약하기")
with st.form("reservation_form"):
    name = st.text_input("예약자 이름")
    restaurant = st.selectbox("예약할 맛집", [r["name"] for r in restaurant_list])
    date = st.date_input("예약 날짜", min_value=datetime.now().date())
    time = st.time_input("예약 시간")
    people = st.number_input("인원 수", min_value=1, step=1)
    submitted = st.form_submit_button("예약하기")
    if submitted:
        # 예약 정보 저장
        new_reservation = pd.DataFrame({
            "name": [name],
            "restaurant": [restaurant],
            "date": [date],
            "time": [time],
            "people": [people]
        })
        st.session_state.reservations = pd.concat([st.session_state.reservations, new_reservation], ignore_index=True)
        st.success(f"{name}님, {restaurant}에 예약이 완료되었습니다!")

# 예약 정보 조회
st.header("🔍 예약 정보 조회")
if not st.session_state.reservations.empty:
    st.dataframe(st.session_state.reservations)
else:
    st.write("현재 예약 내역이 없습니다.")

# 3️⃣ 챗봇 섹션
st.header("💬 ChatGPT와 대화하기")
user_input = st.text_input("궁금한 점을 입력하세요:")
if st.button("질문하기"):
    if user_input:
        try:
            # 최신 모델 호출 방식 (ChatGPT 모델)
            response = openai.Completion.create(
                model="gpt-3.5-turbo",  # 사용할 모델을 gpt-3.5-turbo로 변경
                prompt=f"사용자의 질문: {user_input}\n답변:",
                max_tokens=150,
                temperature=0.7
            )
            # 챗봇의 응답을 추출하여 출력
            answer = response['choices'][0]['text'].strip()
            st.write(f"🤖 ChatGPT 답변: {answer}")
        except Exception as e:
            st.error(f"오류 발생: {e}")
    else:
        st.warning("질문을 입력해주세요!")
