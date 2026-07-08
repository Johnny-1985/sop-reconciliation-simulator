# AI Multi-Agent S&OP Platform — SPEC.md (v1.0)

## 1. 프로젝트 목적

**포트폴리오/이직용 데모.** 실사용 목적이 아니라, 채용 담당자·면접관에게 "이 사람은 AI를 잘 쓰는 사람이 아니라, S&OP 실무를 깊이 이해하고 그것을 AI로 재현할 수 있는 사람"이라는 인상을 주는 것이 유일한 성공 기준이다.

타겟 롤: Sales Planning / Demand Planning / IBP Manager (Team Lead~Senior), 장기적으로 Director.

**핵심 메시지 (GitHub README 한 줄):**
> "Multi-Agent AI platform simulating real-world S&OP demand-supply reconciliation meetings."

## 2. 핵심 컨셉

S&OP 회의에서 가장 보편적이고 누구나 이해하는 긴장 구도를 재현한다: **Sales(수요 극대화) vs Procurement/Supply(실행 가능성)**. 이 갈등을 Harmonizer(=Integrated Planning Manager 페르소나)가 중재해 하나의 합의된 계획으로 수렴시킨다.

이 페르소나 설계는 의도적이다 — Harmonizer의 역할이 실제 작성자(John)의 현업 직무와 동일하므로, 인터뷰에서 "이 프로젝트가 곧 제 업무입니다"라는 설명이 자연스럽게 성립한다.

```
[Synthetic Data: 태양광 제품별 월별 수요/공급 시나리오]
              │
              ▼
   ┌─────────────────────┐
   │  Sales Demand Agent  │  "시장 기회 관점" — 수요 상향, 신규 물량 확보 주장
   └─────────────────────┘
              │  주장 + 근거
              ▼
   ┌─────────────────────┐
   │ Supply/Procurement   │  "실행 가능성 관점" — 리드타임, MOQ, 생산능력 제약 반박
   │  Agent               │
   └─────────────────────┘
              │  주장 + 반박 근거
              ▼
   ┌─────────────────────┐
   │     Harmonizer        │  두 입장을 검토해 최종 합의안 + 근거 + 트레이드오프 도출
   │ (Integrated Planning  │
   │  Manager persona)      │
   └─────────────────────┘
              │
              ▼
   [Executive Summary: 최종 계획 수치 + 결정 근거 + 리스크]
```

## 3. Phase 1 범위 (최소 기능)

**포함:**
- Agent 2개 (Sales Demand Agent, Supply/Procurement Agent) + 간단 Harmonizer
- 단일 시나리오 데모 (Synthetic 태양광 데이터 1세트, 예: 특정 국가 모듈/인버터 월별 수요-공급 갭)
- 2라운드 이내 토론 (Agent 1 주장 → Agent 2 반박 → Harmonizer 결론), 무한 루프 없음
- Executive Summary 자동 생성 (최종 합의 수치, 핵심 근거 3가지, 리스크 1~2가지)
- 인터랙티브 데모 UI (대화형으로 각 Agent 발언이 채팅 버블처럼 순차 표시)

**Phase 1에서 제외 (Phase 2/3로 이연):**
- Finance Agent, Marketing Agent 등 추가 관점
- Reviewer Agent (자동 품질 검증 루프)
- Orchestrator/Managing Editor 레이어
- 다중 시나리오 비교, 사용자 정의 데이터 업로드
- 실시간 외부 데이터 연동 (뉴스레터 프로젝트와 달리 이 프로젝트는 시뮬레이션이므로 불필요)

## 4. Synthetic 데이터 설계

실제 회사 데이터는 사용 불가하므로, 태양광 업계 구조를 참고한 가상 데이터를 직접 생성한다.

**가상 회사:** "SunArc Solar" (가상 태양광 제조사, 유럽 시장 판매)

**데이터 스키마 (예시):**

| 필드 | 설명 | 예시 |
|---|---|---|
| product | 제품군 | Module (Q.TRON 유사), Inverter (HYB G3 유사), Battery (B5.1-X 유사) |
| market | 판매 국가 | Italy, Germany, Poland, France |
| month | 계획 월 | 2026-08 ~ 2026-12 |
| sales_forecast_request | Sales가 요청하는 물량 | 12,000 units |
| current_supply_capacity | 생산/조달 가능 물량 | 8,500 units |
| lead_time_weeks | 리드타임 (정상 기준 2~4개월/8~16주) | 10주 |
| moq | 최소발주단위 | 1,000 units |
| unit_cost | 단가 | €0.117/W |
| inventory_on_hand | 현재고 | 2,300 units |
| target_inventory_level | 적정재고 (1.5개월치 수요 기준) | sales_forecast_request × 1.5 |
| inventory_gap | 현재고 - 적정재고 (양수=과잉, 음수=부족) | -1,155 |
| product_lifecycle_stage | established / new_launch | new_launch |
| launch_month | 신제품 출시 월 (established는 null) | 2026-10 |

**단위 규칙:** 모듈은 수량(장) 입력 후 POWERCLASS(Wp) × 수량 ÷ 10⁶ = MWp로 환산. 인버터·ESS는 대수(units) 그대로 사용.

**적정재고 로직:** 적정재고 = 해당 월 수요(sales_forecast_request) × 1.5개월. 재고가 이 수준을 초과하면(inventory_gap 양수) Procurement Agent가 추가 생산에 신중해야 하고, 미달이면(음수) 공급 확대 근거가 강해진다.

**신제품 출시 처리:** product_lifecycle_stage가 "new_launch"인 경우 과거 판매 추세가 없으므로, Sales Agent는 유사 제품 유추/시장 규모 추정(market sizing)에 근거해 예측하며, Harmonizer는 이를 더 높은 불확실성으로 간주해 보수적 결정 + 빠른 재검토 주기를 권고하도록 설계했다 (자세한 로직은 AGENT_PROMPTS.md 참조).

이 스키마는 실제 SPEC 작성 시 `synthetic_data.json` 또는 `.xlsx`로 구현하며, 5개 시나리오(수요 급증/공급 차질/재고 과잉/모듈 배분/신제품 출시)를 미리 만들어 데모에서 선택 가능하게 한다.

## 5. Agent 설계 (Phase 1)

### 5.1 Sales Demand Agent
- **입장:** 시장 기회 극대화, 고객 이탈 방지, 매출 성장
- **논거 소스:** sales_forecast_request, 시장 트렌드, 경쟁사 동향(가상)
- **시스템 프롬프트 방향:** "당신은 공격적인 영업 계획 담당자입니다. 데이터를 기반으로 왜 이 물량이 필요한지, 확보하지 못했을 때의 비즈니스 리스크(고객 이탈, 경쟁사 점유율 상승)를 설득력 있게 주장하세요."

### 5.2 Supply/Procurement Agent
- **입장:** 실행 가능성, 비용 효율성, 리스크 관리
- **논거 소스:** current_supply_capacity, lead_time_weeks, moq, unit_cost
- **시스템 프롬프트 방향:** "당신은 신중한 공급망 담당자입니다. 데이터를 기반으로 요청된 물량이 왜 실행 어려운지(리드타임, MOQ, 생산능력), 대안(부분 승인, 일정 조정)을 제시하세요."

### 5.3 Harmonizer
- **입장:** 중립적 의사결정자 (Integrated Planning Manager 페르소나)
- **역할:** 두 Agent의 주장을 요약 → 트레이드오프 분석 → 최종 합의 수치 결정 → 근거 3줄 요약
- **출력 형식:** Executive Summary (최종 계획, Key Rationale, Risk Flag)

## 6. 기술 아키텍처 (Phase 1)

포트폴리오 데모 목적에 맞춰 **Claude Artifact 기반 인터랙티브 웹 데모**로 구현한다 (별도 백엔드 호스팅 불필요, 빠른 완성 우선).

```
[React Artifact - 단일 파일]
   ├─ Synthetic 시나리오 선택 UI
   ├─ "Run S&OP Debate" 버튼
   ├─ fetch() → api.anthropic.com/v1/messages (Claude API 직접 호출)
   │     ├─ Call 1: Sales Demand Agent 응답 생성
   │     ├─ Call 2: Supply/Procurement Agent 응답 생성 (Call 1 결과를 컨텍스트로 전달)
   │     └─ Call 3: Harmonizer 최종 결론 생성 (Call 1+2 결과를 컨텍스트로 전달)
   ├─ 채팅 버블 UI로 순차 렌더링 (Sales → Procurement → Harmonizer)
   └─ Executive Summary 카드 (최종 수치 + 근거 + 리스크)
```

**⚠️ 중요한 기술적 제약:** Claude Artifact의 API 직접 호출 기능은 claude.ai 내에서만 동작한다. 이 데모를 **GitHub 포트폴리오에 공개 배포**하려면 별도 백엔드(예: Vercel serverless function + API 키)가 필요하다. Phase 1에서는 claude.ai Artifact로 빠르게 완성하고, GitHub에는 스크린 레코딩(GIF)과 코드를 함께 올리는 방식으로 우회한다. 실제 공개 배포는 Phase 2 이후 검토.

## 7. Phase 로드맵

| Phase | 내용 | 상태 |
|---|---|---|
| Phase 1 | Agent 2개 + 간단 Harmonizer, 단일 시나리오, Claude Artifact 데모 | 완료 |
| Phase 2 | Finance Agent 추가(원가·마진·손실처리 관점), 판매 부진/데드스탁 청산 방향성 로직 | 진행 중 (Finance Agent + 조건부 오케스트레이션 완료) |
| Phase 2 (계속) | 결과 히스토리 저장, 시나리오 선택 유지, 백엔드 프록시로 공개 배포 | 보류 |
| Phase 3 | Reviewer Agent(품질 검증), 실행 가능한 What-if 파라미터 조정 UI | 보류 |

**Phase 2 데드스탁/판매 부진 로직 (구현 완료):**
- 트리거 조건: `inventory_gap`이 **2개월 이상 연속 양수**(재고 과잉)인 경우 `dead_stock_trigger_month`에 첫 트리거 월이 자동 기록됨 (build_data.py에서 계산).
- 트리거가 있는 시나리오에서만 **Finance Agent가 조건부로 소집**되어 hold/markdown/write-off 3가지 옵션의 월간 재고보유비용(연 18% 가정)을 비교 제시.
- Harmonizer는 Finance의 제안을 그대로 받아들이거나 뒤집을 수 있으며, 뒤집을 경우 그 이유를 `pricing_decision.rationale`에 명시 — 이 역시 승인자 뷰에서 강조 표시됨.
- 시나리오 C(Germany Oversupply)가 9월에 정확히 트리거되는 것을 검증 완료.

## 8. 포트폴리오 서사 (인터뷰용)

- **한 줄 피치:** "실제 S&OP 회의에서 벌어지는 Sales-Supply 갈등 조정 과정을 AI 멀티에이전트로 시뮬레이션한 프로젝트. Harmonizer 로직은 제가 Q CELLS EU 클러스터에서 실제로 수행하는 의사결정 프레임워크를 반영했습니다."
- **차별화 포인트:** "AI를 쓸 줄 아는 사람"이 아니라 "S&OP 갈등 구조 자체를 설계할 수 있는 사람"이라는 증거.
- **다음 질문 대비:** 면접관이 "왜 Finance Agent는 없나요?"라고 물으면 → "Phase 1은 가장 핵심적인 Demand-Supply 긴장에 집중했고, Finance는 Phase 2 로드맵에 있습니다"라고 답변 가능하도록 로드맵을 문서에 명시해둔다.

---

*버전 히스토리: v1.0 (최초 작성) — Phase 1 범위 확정, Agent 2개 구조, Synthetic 데이터 스키마 초안*
