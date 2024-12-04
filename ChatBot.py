import streamlit as st
import openai
import pandas as pd
from datetime import datetime

# OpenAI API 키 설정
openai.api_key = st.secrets["openai"]["api_key"]

# 맛집 및 축제 데이터 샘플
restaurant_list = [
    {"name": "백제불고기", "location": "공주시", "specialty": "불고기"},
    {"name": "서산해물탕", "location": "서산시", "specialty": "해물탕"},
    {"name": "아산칼국수", "location": "아산시", "specialty": "칼국수"},
    {"name": "논산비빔밥", "location": "논산시", "specialty": "비빔밥"},
    {"name": "당진초밥", "location": "당진시", "specialty": "초밥"},
]

festival_list = [
    {"location": "공주시", "festival": "백제문화제", "date": "9월 말 ~ 10월 초"},
    {"location": "서산시", "festival": "해미읍성 역사문화축제", "date": "10월 중순"},
    {"location": "아산시", "festival": "아산 성웅이순신 축제", "date": "5월 초"},
    {"location": "논산시", "festival": "논산 딸기축제", "date": "3월 중순"},
    {"location": "당진시", "festival": "기지시줄다리기축제", "date": "4월 중순"},
]

# 예약 데이터를 저장할 DataFrame
if "reservations" not in st.session_state:
    st.session_state.reservations = pd.DataFrame(columns=["name", "restaurant", "date", "time", "people"])

# 앱 제목
st.title("충남 맛집 추천 & 예약 시스템 + 지역 축제 정보 🍴🎉🤖")

# 1️⃣ 맛집 리스트 출력
st.header("📌 충남 지역 맛집 및 축제 리스트")
for restaurant in restaurant_list:
    matching_festival = next((f for f in festival_list if f["location"] == restaurant["location"]), None)
    st.markdown(f"### **{restaurant['name']}**")
    st.write(f"- **위치:** {restaurant['location']}")
    st.write(f"- **대표메뉴:** {restaurant['specialty']}")
    if matching_festival:
        st.write(f"🎉 **축제 정보:** {matching_festival['festival']} (개최 시기: {matching_festival['date']})")

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
            # 최신 API 호출 방식
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions about restaurants and festivals."},
                    {"role": "user", "content": user_input},
                ],
            )
            # ChatGPT 응답 출력
            answer = response["choices"][0]["message"]["content"]
            st.write(f"🤖 ChatGPT 답변: {answer}")
        except openai.OpenAIError as e:
            st.error(f"OpenAI API 오류 발생: {e}")
        except Exception as e:
            st.error(f"알 수 없는 오류 발생: {e}")
    else:
        st.warning("질문을 입력하세요!")
