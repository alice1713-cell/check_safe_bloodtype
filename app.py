import streamlit as st
import pandas as pd

# 1. 데이터 구조 (리스트): 환자 혈액형별 수혈 가능한 혈액형 리스트
all_blood_types = ["A형", "B형", "O형", "AB형"]
type_a_safe = ["A형", "O형"]
type_b_safe = ["B형", "O형"]
type_o_safe = ["O형"]
type_ab_safe = ["A형", "B형", "O형", "AB형"]


# 2. 함수 (def): 환자의 혈액형과 필요 수혈량을 받아 수혈 가능 리스트, 안내 문구, 위험도 점수 반환
def check_blood(blood_type, amount):
    # 기본 위험도 점수 계산 (수혈량 100mL당 2점으로 기본 설정 예시)
    risk_score = int(amount / 50)

    # 3. 조건문 (if-elif-else): 혈액형별 수혈 가능 리스트 및 주의 메시지 설정
    if blood_type == "O형":
        safe_list = type_o_safe
        guide_msg = "희귀 수혈 주의 (O형만 수혈 가능)"
    elif blood_type == "AB형":
        safe_list = type_ab_safe
        guide_msg = "전 혈액형 수혈 가능"
    elif blood_type == "A형":
        safe_list = type_a_safe
        guide_msg = "동일 혈액형(A형) 및 O형 수혈 가능"
    else:
        safe_list = type_b_safe
        guide_msg = "동일 혈액형(B형) 및 O형 수혈 가능"

    # 추가 조건: 대량 출혈(1000mL 이상) 시 위험도 점수 +30점 가산
    if amount >= 1000:
        risk_score += 30

    return safe_list, guide_msg, risk_score


# --- Streamlit 웹 화면 구성 ---
st.title("🩸 맞춤형 혈액형 수혈 판별 & 위험도 가이드")
st.write("응급 상황 시 환자의 혈액형과 필요 수혈량을 입력하여 안전한 수혈 가이드를 확인하세요.")

st.divider()

# (1) 혈액형 선택 (드롭다운) & (2) 필요 수혈량 입력 (슬라이더)
selected_blood = st.selectbox("1. 환자의 혈액형을 선택하세요:", all_blood_types)
blood_amount = st.slider("2. 필요 수혈량을 입력하세요 (mL):", min_value=100, max_value=2000, value=400, step=100)

# 분석하기 버튼
if st.button("수혈 가능 여부 분석하기"):
    # 함수 실행
    safe_blood_list, status_message, danger_score = check_blood(selected_blood, blood_amount)

    st.subheader("📋 분석 결과")

    # 수도코드 5) 조건 판단: O형이고 1000mL 이상이면 긴급 경고 출력
    if selected_blood == "O형" and blood_amount >= 1000:
        st.error(f"🚨 [긴급 경고] O형 대량 출혈 환자입니다! ({status_message})")
    elif blood_amount >= 1000:
        st.warning(f"⚠️ [대량 출혈 주의] {selected_blood} 환자는 {', '.join(safe_blood_list)} 혈액을 수혈받을 수 있습니다. ({status_message})")
    else:
        st.info(f"ℹ️ {selected_blood} 환자는 {', '.join(safe_blood_list)} 혈액을 수혈받을 수 있습니다. ({status_message})")

    # (강조 수치) 응급 위험도 점수 Metric 표시
    st.metric(label="응급 위험도 점수", value=f"{danger_score}점", delta="1000mL 이상 대량출혈 가산점 포함" if blood_amount >= 1000 else "일반 수혈 범위")

    # 4. 반복문 (for): 전체 혈액형 리스트를 순회하며 테이블(표) 데이터 생성
    table_data = []
    for donor in all_blood_types:
        if donor in safe_blood_list:
            availability = "가능"
            if donor == selected_blood:
                reason = "같은 혈액형으로 응집 반응 없이 안전"
            else:
                reason = "응집원이 없어 수혈 가능 (안전)"
        else:
            availability = "불가능"
            reason = "환자의 항체와 반응하여 응집 위험"

        # 표의 한 줄(행) 추가
        table_data.append({
            "수혈 혈액형": donor,
            "가능 여부": availability,
            "면역 반응 설명": reason
        })

    # 테이블(표) 형태로 화면에 출력
    st.write("### 🧬 수혈 가능 혈액형 목록")
    df = pd.DataFrame(table_data)
    st.table(df)
