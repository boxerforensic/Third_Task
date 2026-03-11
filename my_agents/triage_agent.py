import streamlit as st
from agents import (
    Agent,
    RunContextWrapper,
    input_guardrail,
    Runner,
    GuardrailFunctionOutput,
    handoff,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.extensions import handoff_filters
from models import UserAccountContext, InputGuardRailOutput, HandoffData
from my_agents.menu_agent import menu_agent
from my_agents.reservation_agent import reservation_agent
from my_agents.order_agent import order_agent
from my_agents.compaints_agent import complaints_agent


input_guardrail_agent = Agent(
    name="Input Guardrail Agent",
    instructions="""
   사용자의 요청이 메뉴정보, 재료, 알레르기에 대한 정보, 주문에 대한 확인 정보, 음식점 테이블 예약 정보 등 음식점에서 예약하고 음식을 주문하고 날짜를 확인하는 등의  주제에서 벗어난 요청은 처리하지 마십시오. 요청이 주제에서 벗어난 경우, 처리 사유를 명시하십시오. 특히 대화 초반에는 사용자와 간단한 대화를 나눌 수 있지만, 메뉴정보, 재료, 알레르기에 대한 정보, 주문에 대한 확인 정보, 음식점 테이블 예약 정보 등과 관련이 없는 요청에는 응대하지 마십시오.
""",
    output_type=InputGuardRailOutput,
)


@input_guardrail
async def off_topic_guardrail(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
    input: str,
):
    result = await Runner.run(
        input_guardrail_agent,
        input,
        context=wrapper.context,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_off_topic,
    )


def dynamic_triage_agent_instructions(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
):
    return f"""
    {RECOMMENDED_PROMPT_PREFIX}


    당신은 고객 지원 담당자입니다. 고객의 주문 예약, 예약테이블, 예약된 인원수 메뉴 특이사항에만 답변해야 합니다.
    고객의 이름을 불러야 합니다.
    
    예약한 고객의 이름  {wrapper.context.name}.
    예약한 고객이 주문한 메뉴  {wrapper.context.menu}.
    예약한 고객의 예약 테이블 번호  {wrapper.context.table_number}.
    예약한 고객의 예약 시간  {wrapper.context.Reservation_time}.
    예약한 고객의 예약된 인원수  {wrapper.context.Number_of_people_reserved}.
    예약한 고객의 전화번호  {wrapper.context.Number_of_people_reserved}.
    예약한 고객의 특이사항 {wrapper.context.significant}
    
    YOUR MAIN JOB: Classify the customer's issue and route them to the right specialist.
    
    ISSUE CLASSIFICATION GUIDE:
    
   🔹 MENU AGENT - 다음과 같은 경우 여기로 연결:

        - 메뉴 종류, 가격, 구성 관련 질문
        - 음식 재료, 원산지, 조리 방식 문의
        - 알레르기 유발 성분, 채식/비건 여부 확인
        - 맵기 정도, 추천 메뉴, 사이드 메뉴 안내

    🔹 ORDER AGENT - 다음과 같은 경우 여기로 연결:

        - 음식 주문 접수 및 주문 내용 확인
        - 메뉴 추가, 변경, 삭제 요청
        - 포장 / 매장식사 / 배달 여부 확인
        - 주문 수량, 옵션, 요청사항 전달

    🔹 RESERVATION AGENT - 다음과 같은 경우 여기로 연결:

        - 테이블 예약 접수 및 예약 가능 여부 확인
        - 예약 날짜, 시간, 인원수 변경 요청
        - 예약 조회, 취소, 재확인
        - 좌석 요청, 창가석 여부, 특별 요청사항 접수
    
    🔹 Complaints AGENT - 다음과 같은 경우 여기로 연결:

        - 고객의 불만을 공감하며 인정
        - 해결책 제시(환불, 할인, 매니저 소환)
        - 고객의 심각한 불만에 대해 단계적으로 해결해 나간다.
       
    분류 절차:

        1. 고객의 문제를 경청합니다.
        2. 분류가 불분명한 경우 추가 질문을 합니다.
        3. 위의 네 가지 범주 중 하나로 분류합니다.
        4. 고객을 담당 부서로 연결하는 이유를 설명합니다. "[specific issue]를 해결해 드릴 수 있는 [category] 전문가에게 연결해 드리겠습니다."
        5. 적절한 전문가 상담원에게 연결합니다.    
    
    SPECIAL HANDLING:
        - 여러 문제: 가장 긴급한 문제부터 처리하고, 나머지는 후속 조치를 위해 기록해 두십시오.
        - 불분명한 문제: 배정 전에 1~2개의 질문을 통해 명확히 하십시오.
    """


def handle_handoff(
    wrapper: RunContextWrapper[UserAccountContext],
    input_data: HandoffData,
):

    with st.sidebar:
        st.write(
            f"""
            Handing off to {input_data.to_agent_name}
            Reason: {input_data.reason}
            Issue Type: {input_data.issue_type}
            Description: {input_data.issue_description}
        """
        )


def make_handoff(agent):

    return handoff(
        agent=agent,
        on_handoff=handle_handoff,
        input_type=HandoffData,
        input_filter=handoff_filters.remove_all_tools,
    )


triage_agent = Agent(
    name="Triage Agent",
    instructions=dynamic_triage_agent_instructions,
    input_guardrails=[
        off_topic_guardrail,
    ],
    # tools=[
    #     technical_agent.as_tool(
    #         tool_name="Technical Help Tool",
    #         tool_description="Use this when the user needs tech support."
    #     )
    # ]
    handoffs=[
        make_handoff(menu_agent),
        make_handoff(reservation_agent),
        make_handoff(order_agent),
        make_handoff(complaints_agent)
    ],
)