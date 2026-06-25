# Cart Discount TDD Practice

## 목적

이 프로젝트는 **장바구니 할인 계산 로직**을 TDD(Test-Driven Development) 방식으로 구현하는 연습 프로젝트입니다.

모든 테스트와 구현은 **계약 ID**(INV-*, E-*)를 기준으로 추적합니다. 계약 ID는 테스트와 구현을 잇는 "추적의 못"이며, 사람 개발자와 AI 코딩 에이전트가 함께 참고하는 프로젝트 지도입니다.

상세 발견 근거와 제품 요구사항은 [docs/PRD.md](docs/PRD.md)를 참조하세요.
첫 사이클(`subtotal`) 테스트 설계·케이스는 [docs/test-plan-INV-1-E-1-E-2.md](docs/test-plan-INV-1-E-1-E-2.md)를 참조하세요.

**현재 단계:** GREEN 완료 — `src/cart.py`의 `subtotal` 최소 구현으로 `tests/entity/test_subtotal.py` 7건 통과.

## 핵심 원칙

- **ID에 없는 동작은 만들지 않는다.** 계약 표에 정의되지 않은 기능·예외·할인 정책은 구현하지 않습니다.
- **테스트가 먼저다.** 구현보다 실패하는 테스트가 항상 앞섭니다.
- **RED → GREEN → REFACTOR** 순서를 따릅니다.
  - RED: `tests/`만 수정. `src/`는 건드리지 않습니다.
  - GREEN: 실패를 통과시키는 최소 구현만 `src/`에 추가합니다.
  - REFACTOR: 전부 통과한 뒤에만 구조를 개선합니다.
- **과잉 구현을 금지한다.** 요청·계약에 없는 기능을 미리 만들지 않습니다.

## 계약 ID 목록

| ID    | 계약(불변식 / 에러)                                                 | 근거 레벨 | 계층        |
| ----- | ------------------------------------------------------------ | ----- | --------- |
| INV-1 | `subtotal(items) == Σ(price × qty)`                          | —     | Entity    |
| INV-2 | `amount ≥ 50000 → round(amount×0.9)` / `< 50000 → 그대로` 경계 포함 | L1    | Entity    |
| INV-3 | `final = 문턱할인 적용 후, VIP면 round(×0.95)`. 순서 문턱→VIP 고정         | L2    | Entity    |
| INV-4 | 모든 입력에서 `0 ≤ final_total ≤ subtotal`. 할인은 금액을 늘리지 않는다        | L3    | Entity    |
| E-1   | `items is None → TypeError`                                  | L0    | Boundary* |
| E-2   | `price` 또는 `qty`가 음수 → `ValueError`, 인덱스 포함                  | L0    | Boundary* |

## 계약 ID 설명

### INV-1

장바구니 소계(`subtotal`)는 각 상품의 `price × qty`를 모두 더한 값과 같아야 합니다.

### INV-2

금액이 50,000원 이상이면 `round(amount × 0.9)`로 10% 문턱 할인을 적용하고, 50,000원 미만이면 할인 없이 그대로 둡니다. 경계값(50,000원)은 포함합니다.

### INV-3

최종 금액은 문턱 할인을 먼저 적용한 뒤, VIP 회원이면 `round(× 0.95)`를 추가 적용합니다. 적용 순서는 **문턱 → VIP**로 고정됩니다.

### INV-4

모든 유효 입력에서 최종 결제 금액(`final_total`)은 0 이상이며 소계(`subtotal`)를 초과하지 않습니다. 할인은 금액을 늘리지 않습니다.

### E-1

`items`가 `None`이면 `TypeError`를 발생시킵니다.

### E-2

`price` 또는 `qty`가 음수이면 `ValueError`를 발생시키며, 오류 메시지에 해당 항목의 인덱스를 포함합니다.

## 계층 의미

### Entity

`src/cart.py`에 위치하며, **순수 도메인 계산 로직**을 담당합니다. 소계·문턱 할인·VIP 할인·최종 금액 등 INV-* 계약을 구현합니다. Flask 등 Boundary 계층을 import 하지 않습니다.

### Boundary*

입력 검증 경계에 가까운 규칙(E-*)을 정의합니다. 본 실습에서는 도메인 함수 **진입점**에서 해당 검증을 수행합니다.

## 예상 파일 구조

```text
.
├── README.md
├── docs/
│   ├── PRD.md
│   └── test-plan-INV-1-E-1-E-2.md
├── src/
│   └── cart.py
└── tests/
    └── entity/
        └── test_subtotal.py
```

## 진행 체크리스트 — INV-1 · E-1 · E-2

대상: `src/cart.py` → `subtotal(items)` · 테스트: `tests/entity/test_subtotal.py`  
상세 케이스·assert 패턴·OOS는 [docs/test-plan-INV-1-E-1-E-2.md](docs/test-plan-INV-1-E-1-E-2.md) §5~6 참조.

### RED (`tests/` 만 수정 · `src/` 금지)

- [x] `tests/entity/test_subtotal.py` 생성
- [x] **INV-1-a** — `test_inv_1_subtotal_single_line` (단일 라인 → `1_000`)
- [x] **INV-1-b** — `test_inv_1_subtotal_multiple_lines` (다중 라인 → `66_000`)
- [x] **INV-1-c** — `test_inv_1_subtotal_empty_cart` (빈 장바구니 → `0`)
- [x] **E-1-a** — `test_e_1_subtotal_none_raises_type_error` (`None` → `TypeError`)
- [x] **E-2-a** — `test_e_2_subtotal_negative_qty_raises_value_error_with_index` (음수 `qty`, 인덱스 `0`)
- [x] **E-2-b** — `test_e_2_subtotal_negative_price_raises_value_error_with_index` (음수 `price`, 인덱스 `0`)
- [x] **E-2-c** — `test_e_2_subtotal_negative_at_later_index` (후행 인덱스 `1`)
- [x] 각 테스트에 `@pytest.mark.entity`, docstring·주석에 계약 ID 명시
- [x] `pytest -q` 실행 시 **7건 실패** 확인 (`NotImplementedError`)
- [x] `assert True` · `pytest.skip` · 예외 삼키기 **사용 안 함** (지속 준수)
- [x] 커밋: `test: add RED tests for INV-1, E-1, E-2`

### GREEN (`src/cart.py` 최소 구현)

`subtotal` 내부 권장 순서: **E-1 → E-2 → INV-1** (테스트 플랜 §2.2)

- [x] **E-1** — `items is None`이면 `TypeError` + `# E-1` 주석
- [x] **E-2** — 각 인덱스 `i`에서 `price < 0` 또는 `qty < 0`이면 `ValueError`(메시지에 `i` 포함) + `# E-2` 주석
- [x] **INV-1** — `Σ(price × qty)` 반환 + `# INV-1` 주석
- [x] `pytest tests/entity/test_subtotal.py -q` **7건 전부 통과**
- [x] `pytest -q` **전부 통과**
- [x] 커밋: `feat: implement subtotal for INV-1, E-1, E-2`

### REFACTOR (본 사이클 이후 · 선택)

- [ ] 구조 변경과 동작 변경 **분리 커밋**
- [ ] 리팩터 전후 `pytest -q` 동일 통과

## TDD 진행 순서 (전체)

1. **RED** — 계약 ID별로 실패하는 테스트를 작성합니다.
2. **GREEN** — 해당 ID를 만족하는 최소 구현을 추가합니다. 구현 줄에 계약 ID 주석을 단다.
3. **REFACTOR** — 테스트가 모두 통과한 상태에서 구조를 개선합니다. 리팩터링 전후로 동작이 동일한지 확인합니다.

## 테스트 실행

```bash
pytest -q
```

`-q`는 quiet mode로, 테스트 결과를 간략하게 출력합니다.

## 구현 금지 사항

- 할인 정책 추가 금지
- 쿠폰, 세금, 배송비, 포인트 기능 추가 금지
- ID에 없는 예외 처리 추가 금지
- UI, CLI, DB, API 코드 추가 금지
