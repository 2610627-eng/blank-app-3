import pandas as pd
import streamlit as column
import streamlit as st

# 1. 초기화 및 세션 상태 설정 (웹 페이지가 새로고침되어도 주문 내역 유지)
menu_list = ["부대찌개", "제육볶음", "된장찌개", "떡볶이 세트"]
price_list = [12000, 14000, 13000, 10000]

if "order_list" not in st.session_state:
    st.session_state.order_list = []
if "total_price" not in st.session_state:
    st.session_state.total_price = 0

# 웹 앱 제목
st.title("🍲 한식 밀키트 무인 키오스크")
st.subheader("직원의 도움 없이 간편하게 메뉴를 선택하고 결제하세요!")
st.write("---")

# 2. 메뉴판 출력 (st.dataframe 활용)
st.write("### 📋 메뉴판")
menu_df = pd.DataFrame(
    {"메뉴명": menu_list, "가격(원)": [f"{p:,}" for p in price_list]},
    index=[1, 2, 3, 4],
)
st.dataframe(menu_df, use_container_width=True)

# 3. 주문 선택 및 추가 (스트림릿 위젯 활용)
st.write("### 🛒 메뉴 선택")
selected_menu = st.selectbox(
    "원하시는 밀키트를 선택하세요:",
    options=menu_list,
    index=0,
)

# 수량 선택
quantity = st.number_input("수량을 선택하세요:", min_value=1, max_value=10, value=1)

# '장바구니 담기' 버튼
if st.button("장바구니에 담기", type="primary"):
    idx = menu_list.index(selected_menu)
    price = price_list[idx] * quantity

    # 장바구니 추가
    st.session_state.order_list.append(
        {"메뉴": selected_menu, "수량": quantity, "금액": price}
    )
    st.session_state.total_price += price
    st.toast(f"🛒 {selected_menu} {quantity}개가 장바구니에 담겼습니다!")

st.write("---")

# 4. 현재 장바구니 내역 및 결제하기
st.write("### 🧾 나의 장바구니")

if st.session_state.order_list:
    # 현재까지 담은 주문 출력
    order_df = pd.DataFrame(st.session_state.order_list)
    st.dataframe(order_df, use_container_width=True)

    # 총 결제 금액
    st.metric(label="총 결제 금액", value=f"{st.session_state.total_price:,} 원")

    # 결제 여부 선택 인터페이스
    st.write("#### 결제를 진행하시겠습니까?")
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("Yes (결제)"):
            st.success("🎉 결제가 완료되었습니다. 맛있는 식사 되세요!")
            # 초기화
            st.session_state.order_list = []
            st.session_state.total_price = 0

    with col2:
        if st.button("No (취소)"):
            st.error("❌ 메뉴 주문이 취소되었습니다. 처음부터 다시 선택해주세요.")
            # 초기화
            st.session_state.order_list = []
            st.session_state.total_price = 0
else:
    st.info("장바구니가 비어 있습니다. 메뉴를 선택하고 담아주세요.")