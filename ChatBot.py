import streamlit as st
from streamlit_option_menu import option_menu
import openai

# OpenAI API 키 설정
openai.api_key = st.secrets.get("openai", {}).get("api_key", "")

# 초기화 (기본 맛집, 축제 데이터 포함)
if "restaurant_list" not in st.session_state:
    st.session_state.restaurant_list = [
        {"name": "서산 한정식", "location": "충남 서산시", "specialty": "한정식", "image": "https://example.com/restaurant1.jpg"},
        {"name": "천안 떡갈비", "location": "충남 천안시", "specialty": "떡갈비", "image": "https://example.com/restaurant2.jpg"},
        {"name": "홍성 회센터", "location": "충남 홍성군", "specialty": "회", "image": "https://example.com/restaurant3.jpg"},
        {"name": "대전 청국장", "location": "충남 대전시", "specialty": "청국장", "image": "https://example.com/restaurant4.jpg"},
        {"name": "태안 해물탕", "location": "충남 태안군", "specialty": "해물탕", "image": "https://example.com/restaurant5.jpg"},
    ]

if "reservation_list" not in st.session_state:
    st.session_state.reservation_list = []

if "festivals" not in st.session_state:
    st.session_state.festivals = [
        {"name": "서산 해미읍성 문화제", "location": "서산 해미읍성", "date": "2024-05-10", "details": "서산 지역의 전통문화를 체험할 수 있는 축제입니다.", "image": "https://example.com/festival1.jpg"},
        {"name": "천안 독립기념관 축제", "location": "천안 독립기념관", "date": "2024-08-15", "details": "독립운동의 역사와 의미를 기리는 행사입니다.", "image": "https://example.com/festival2.jpg"},
        {"name": "태안 바다축제", "location": "태안 해변", "date": "2024-07-20", "details": "여름 바다와 함께하는 다양한 해양 스포츠와 문화 공연이 펼쳐집니다.", "image": "https://example.com/festival3.jpg"},
        {"name": "당진 벚꽃축제", "location": "당진시", "date": "2024-04-05", "details": "봄을 맞이해 벚꽃이 만개한 당진에서 펼쳐지는 축제입니다.", "image": "https://example.com/festival4.jpg"},
        {"name": "홍성 고추축제", "location": "홍성군", "date": "2024-06-10", "details": "홍성 특산물인 고추를 주제로 한 다양한 행사와 체험이 제공됩니다.", "image": "https://example.com/festival5.jpg"},
    ]

# 네비게이션 메뉴
selected = option_menu(
    menu_title=None,
    options=["메인", "맛집", "축제"],
    icons=["house", "utensils", "calendar"],
    default_index=0,
    orientation="horizontal",
)

# 1️⃣ 메인 화면
if selected == "메인":
    st.title("🎉 충남 맛집 & 축제 추천 시스템")
    st.write("축제 및 맛집과 관련된 정보를 확인하세요!")

    # 업로드된 이미지 대신 사용자가 제공한 이미지를 직접 포함
    image_url = "https://images.app.goo.gl/VKLrMeGCbJ7FhHF17"  # 웹상의 이미지 URL로 변경하거나, 로컬 경로로 변경
    st.image(image_url, caption="충남 지역에서 다양한 맛집과 축제를 즐겨보세요!", use_container_width=True)

# 2️⃣ 맛집 화면
elif selected == "맛집":
    st.title("📌 충남 맛집 리스트")
    st.write("아래에서 맛집 정보를 추가하거나 확인하세요.")
    
    # 맛집 정보 추가 섹션
    with st.expander("맛집 정보 추가하기"):
        name = st.text_input("맛집 이름")
        location = st.text_input("위치")
        specialty = st.text_input("대표 메뉴")
        image_file = st.file_uploader("맛집 이미지 업로드", type=["png", "jpg", "jpeg"])
        if st.button("맛집 추가"):
            if name and location and specialty and image_file:
                st.session_state.restaurant_list.append({
                    "name": name,
                    "location": location,
                    "specialty": specialty,
                    "image": image_file,
                })
                st.success(f"{name}이(가) 추가되었습니다!")
            else:
                st.error("모든 정보를 입력해주세요.")

    # 맛집 목록 표시
    st.subheader("맛집 목록")
    for restaurant in st.session_state.restaurant_list:
        st.write(f"**{restaurant['name']}**")
        st.write(f"위치: {restaurant['location']}")
        st.write(f"대표 메뉴: {restaurant['specialty']}")
        if restaurant['image']:
            st.image(restaurant['image'], caption=restaurant['name'], use_container_width=True)
        st.markdown("---")

    # 예약 시스템
    st.subheader("맛집 예약 시스템")
    restaurant_name = st.selectbox("예약할 맛집 선택", [r['name'] for r in st.session_state.restaurant_list])
    reservation_time = st.time_input("예약 시간")
    num_people = st.number_input("인원 수", min_value=1, max_value=20, value=1)

    if st.button("예약하기"):
        if restaurant_name and reservation_time and num_people:
            reservation = {
                "restaurant": restaurant_name,
                "time": reservation_time,
                "people": num_people,
            }
            st.session_state.reservation_list.append(reservation)
            st.success(f"{restaurant_name} 예약이 완료되었습니다!")
        else:
            st.error("모든 정보를 입력해주세요.")

    # 예약 목록 표시
    st.subheader("예약 내역")
    if st.session_state.reservation_list:
        for reservation in st.session_state.reservation_list:
            st.write(f"맛집: {reservation['restaurant']}")
            st.write(f"예약 시간: {reservation['time']}")
            st.write(f"인원 수: {reservation['people']}")
            st.markdown("---")
    else:
        st.write("예약된 내역이 없습니다.")

# 3️⃣ 축제 화면
elif selected == "축제":
    st.title("🎉 충남 축제 리스트")
    st.write("아래에서 축제 정보를 추가하거나 확인하세요.")

    # 축제 상세보기 버튼 및 외부 URL 연결
    festival_url = f"https://8be5-121-152-252-96.ngrok-free.app/"
    st.markdown(f"[🌐 현재 추천하는 천안 축제 목록]({festival_url})", unsafe_allow_html=True)
    st.markdown("---")

    # 축제 정보 추가 섹션
    with st.expander("축제 정보 추가하기"):
        festival_name = st.text_input("축제 이름")
        festival_location = st.text_input("축제 장소")
        festival_date = st.date_input("축제 날짜")
        festival_details = st.text_area("축제 설명")
        festival_image = st.file_uploader("축제 이미지 업로드", type=["png", "jpg", "jpeg"])
        if st.button("축제 추가"):
            if festival_name and festival_location and festival_date and festival_details and festival_image:
                festival = {
                    "name": festival_name,
                    "location": festival_location,
                    "date": festival_date,
                    "details": festival_details,
                    "image": festival_image,
                }
                st.session_state.festivals.append(festival)
                st.success(f"{festival_name} 축제가 추가되었습니다!")
            else:
                st.error("모든 정보를 입력해주세요.")

    # 축제 목록 표시
    st.subheader("축제 목록")
    if st.session_state.festivals:
        for festival in st.session_state.festivals:
            st.write(f"**{festival['name']}**")
            st.write(f"장소: {festival['location']}")
            st.write(f"날짜: {festival['date']}")
            st.write(f"설명: {festival['details']}")
            if festival['image']:
                st.image(festival['image'], caption=festival['name'], use_container_width=True)
            st.markdown("---")
    else:
        st.write("등록된 축제가 없습니다.")

# 💬 오른쪽 하단 채팅 아이콘 및 챗봇 기능
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_chatgpt_response(user_input):
    # OpenAI API를 호출하여 답변을 가져옴
    response = openai.Completion.create(
        engine="text-davinci-003",  # 사용할 모델 이름
        prompt=user_input,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# 채팅 인터페이스
st.markdown("""
    <style>
    #chat-icon {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #4CAF50;
        color: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        text-align: center;
        font-size: 30px;
        line-height: 60px;
        cursor: pointer;
        z-index: 9999;
    }
    #chat-popup {
        position: fixed;
        bottom: 100px;
        right: 20px;
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 10px;
        width: 300px;
        padding: 20px;
        z-index: 10000;
        display: none;
    }
    </style>
    <div id="chat-icon" onclick="document.getElementById('chat-popup').style.display='block'">💬</div>
    <div id="chat-popup">
        <h4>💬 ChatGPT와 대화하기</h4>
        <input id="user-input" placeholder="질문을 입력하세요" style="width:100%; padding:5px; margin-bottom:10px;" />
        <button onclick="sendMessage()" style="width:100%; padding:5px;">전송</button>
        <div id="chat-output"></div>
    </div>
    <script>
    function sendMessage() {
        var userMessage = document.getElementById('user-input').value;
        var output = document.getElementById('chat-output');
        output.innerHTML += '<div><b>나:</b> ' + userMessage + '</div>';
        document.getElementById('user-input').value = '';
        output.scrollTop = output.scrollHeight;

        fetch('/send_message', {
            method: 'POST',
            body: JSON.stringify({ user_message: userMessage }),
        })
        .then(response => response.json())
        .then(data => {
            output.innerHTML += '<div><b>ChatGPT:</b> ' + data.answer + '</div>';
        });
    }
    </script>
""", unsafe_allow_html=True)
