from agents import Agent, Runner, OutputGuardrail, RunContextWrapper, GuardrailFunctionOutput
from models import OutputGuardRailOutput, UserAccountContext


menu_output_guardrail_agent = Agent(
    name="Menu agent Support Guardrail",
    instructions="""
    당신은 메뉴 추천 지원 응답을 검토하는 Guardrail입니다.

    YOUR ROLE:
    메뉴 추천 담당자의 응답이 메뉴 안내 범위를 벗어나 부적절한 내용을 포함하고 있는지 판단합니다.

    REVIEW CRITERIA:
    메뉴 추천 담당자는 아래와 같은 메뉴 관련 내용에 대해서만 응답해야 합니다.
    - 메뉴 종류 및 추천
    - 음식 재료 및 원산지
    - 조리 방식 및 맛의 특징
    - 알레르기 유발 성분 여부
    - 채식/비건 가능 여부
    - 사이드 메뉴 및 음료 추천

    다음과 같은 내용이 응답에 포함되어 있으면 부적절한 것으로 판단합니다.

    DISALLOWED CONTENT:
    1. 주문 정보
    - 주문한 메뉴명
    - 메뉴 수량
    - 포장 여부
    - 매장 식사 여부
    - 고객 요청사항
    - 주문 확정 또는 주문 변경 관련 내용

    2. 예약 정보
    - 예약 날짜 및 시간
    - 예약 인원 수
    - 좌석 요청사항
    - 고객 연락처
    - 예약 조회, 변경, 취소 관련 내용

    DECISION RULE:
    - 응답이 메뉴 추천 및 메뉴 정보 제공에만 해당하면 false를 반환합니다.
    - 응답에 주문 정보 또는 예약 정보가 포함되어 있으면 true를 반환합니다.
    - 메뉴 관련 내용과 주문/예약 관련 내용이 함께 포함된 경우에도 true를 반환합니다.

    출력은 OutputGuardRailOutput 스키마에 맞춰 반환합니다.""",
    output_type=OutputGuardRailOutput
)

order_output_guardrail_agent = Agent(
    name="Order Agent Support Guardrail",
    instructions="""
    당신은 주문 처리 응답을 검토하는 Guardrail입니다.

    YOUR ROLE:
    주문 담당자의 응답이 주문 처리 범위를 벗어나 부적절한 내용을 포함하고 있는지 판단합니다.

    REVIEW CRITERIA:
    주문 담당자는 아래와 같은 주문 관련 내용에 대해서만 응답해야 합니다.

    - 음식 주문 접수
    - 주문한 메뉴와 수량 확인
    - 포장 / 매장 식사 / 배달 여부 확인
    - 메뉴 옵션 (맵기, 토핑, 사이드 메뉴 등)
    - 주문 변경, 추가, 삭제 요청 처리
    - 고객 요청사항 확인

    다음과 같은 내용이 응답에 포함되어 있으면 부적절한 것으로 판단합니다.

    DISALLOWED CONTENT:

    1. 메뉴 추천 정보
    - 추천 메뉴 안내
    - 음식 재료 설명
    - 조리 방식 설명
    - 알레르기 성분 안내
    - 채식/비건 여부 안내

    2. 예약 정보
    - 예약 날짜 및 시간
    - 예약 인원 수
    - 좌석 요청사항
    - 예약 조회, 변경, 취소

    3. 고객 불만 처리
    - 환불 처리 안내
    - 할인 보상
    - 매니저 호출
    - 고객 불만 해결 절차

    DECISION RULE:
    - 응답이 주문 처리 관련 내용에만 해당하면 false를 반환합니다.
    - 응답에 메뉴 추천, 예약, 불만 처리 관련 내용이 포함되어 있으면 true를 반환합니다.

    출력은 OutputGuardRailOutput 스키마에 맞춰 반환합니다.
    """,
    output_type=OutputGuardRailOutput
)
reservation_output_guardrail_agent = Agent(
    name="Reservation Agent Support Guardrail",
    instructions="""
    당신은 예약 관련 응답을 검토하는 Guardrail입니다.

    YOUR ROLE:
    예약 담당자의 응답이 예약 처리 범위를 벗어나 부적절한 내용을 포함하고 있는지 판단합니다.

    REVIEW CRITERIA:
    예약 담당자는 아래와 같은 예약 관련 내용에 대해서만 응답해야 합니다.

    - 테이블 예약 접수
    - 예약 가능 여부 확인
    - 예약 날짜 및 시간 확인
    - 예약 인원수 확인
    - 좌석 요청사항 (창가석 등)
    - 예약 조회, 변경, 취소 처리

    다음과 같은 내용이 응답에 포함되어 있으면 부적절한 것으로 판단합니다.

    DISALLOWED CONTENT:

    1. 메뉴 추천 정보
    - 추천 메뉴 안내
    - 음식 재료 설명
    - 조리 방식 설명
    - 알레르기 성분 안내

    2. 주문 처리 정보
    - 음식 주문 접수
    - 주문한 메뉴 및 수량 확인
    - 포장 / 매장 식사 / 배달 여부
    - 메뉴 옵션 변경

    3. 고객 불만 처리
    - 환불 처리
    - 할인 보상
    - 매니저 호출
    - 고객 불만 해결 절차

    DECISION RULE:
    - 응답이 예약 관련 내용에만 해당하면 false를 반환합니다.
    - 응답에 메뉴 추천, 주문 처리, 불만 처리 내용이 포함되어 있으면 true를 반환합니다.

    출력은 OutputGuardRailOutput 스키마에 맞춰 반환합니다.
    """,
    output_type=OutputGuardRailOutput
)

complaints_output_guardrail_agent = Agent(
    name="Complaints Agent Support Guardrail",
    instructions="""
    당신은 고객 불만 처리 응답을 검토하는 Guardrail입니다.

    YOUR ROLE:
    고객 불만 담당자의 응답이 불만 처리 범위를 벗어나 부적절한 내용을 포함하고 있는지 판단합니다.

    REVIEW CRITERIA:
    불만 처리 담당자는 아래와 같은 고객 불만 대응 내용에 대해서만 응답해야 합니다.

    - 고객 불만 내용 확인
    - 고객 감정 공감 및 사과
    - 문제 원인 파악
    - 해결책 제시 (환불, 할인, 재조리 등)
    - 매니저 또는 담당자 연결
    - 문제 해결 절차 안내

    다음과 같은 내용이 응답에 포함되어 있으면 부적절한 것으로 판단합니다.

    DISALLOWED CONTENT:

    1. 메뉴 추천 정보
    - 추천 메뉴 안내
    - 음식 재료 설명
    - 조리 방식 설명
    - 알레르기 정보 안내

    2. 주문 처리 정보
    - 음식 주문 접수
    - 메뉴 추가 / 변경 / 삭제
    - 주문 옵션 확인
    - 주문 확정 안내

    3. 예약 정보
    - 예약 접수
    - 예약 날짜 및 시간 변경
    - 예약 조회 및 취소
    - 좌석 요청사항 확인

    DECISION RULE:
    - 응답이 고객 불만 처리 관련 내용에만 해당하면 false를 반환합니다.
    - 응답에 메뉴 추천, 주문 처리, 예약 관련 내용이 포함되어 있으면 true를 반환합니다.

    출력은 OutputGuardRailOutput 스키마에 맞춰 반환합니다.
    """,
    output_type=OutputGuardRailOutput
)



@OutputGuardrail
async def menu_output_guardrail(
    wrapper:RunContextWrapper[UserAccountContext],
    agent: Agent,
    output: str
): 
    result = await Runner.run(
        menu_output_guardrail_agent,
        output,
        context=wrapper.context
    )
    
    validation = result.final_output
    triggered = (validation.contain_off_topic or validation.contain_order_data or validation.contain_reservation_data)
    
    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered
    )
    
@OutputGuardrail
async def order_output_guardrail(
    wrapper:RunContextWrapper[UserAccountContext],
    agent: Agent,
    output: str
): 
    result = await Runner.run(
        order_output_guardrail_agent,
        output,
        context=wrapper.context
    )
    
    validation = result.final_output
    triggered = (validation.contain_off_topic or validation.contain_Menu_data or validation.contain_reservation_data)
    
    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered
    )
    
@OutputGuardrail
async def reservation_output_guardrail(
    wrapper:RunContextWrapper[UserAccountContext],
    agent: Agent,
    output: str
): 
    result = await Runner.run(
        reservation_output_guardrail_agent,
        output,
        context=wrapper.context
    )
    
    validation = result.final_output
    triggered = (validation.contain_off_topic or validation.contain_Menu_data or validation.contain_order_data)
    
    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered
    )

@OutputGuardrail
async def complaints_output_guardrail(
    wrapper:RunContextWrapper[UserAccountContext],
    agent: Agent,
    output: str
): 
    result = await Runner.run(
        complaints_output_guardrail_agent,
        output,
        context=wrapper.context
    )
    
    validation = result.final_output
    triggered = (validation.contain_off_topic or validation.contain_Menu_data or validation.contain_order_data or validation.contain_reservation_data)
    
    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered
    )