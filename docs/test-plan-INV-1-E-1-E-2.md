# 테스트 플랜 — INV-1 · E-1 · E-2

| 항목 | 내용 |
|------|------|
| 대상 함수 | `src/cart.py` → `subtotal(items)` |
| 계약 출처 | [README.md](../README.md) 계약 ID 표 |
| 관련 PRD | [docs/PRD.md](PRD.md) (발견 근거·OOS 참조) |
| 문서 버전 | 2026-06-24 |
| TDD 단계 | RED 준비 — 실패 테스트 작성 전 설계 |

---

## 1. 범위

본 문서는 아래 세 계약에 대한 **RED 단계 테스트 설계**만 다룬다. 구현(GREEN)·리팩터링은 포함하지 않는다.

| ID | 계약 | 계층 | 검증 대상 |
|----|------|------|-----------|
| **INV-1** | `subtotal(items) == Σ(price × qty)` | Entity | 유효 입력 시 소계 합산 |
| **E-1** | `items is None` → `TypeError` | Boundary* | `subtotal` 진입점 검증 |
| **E-2** | `price` 또는 `qty` 음수 → `ValueError`, **인덱스 포함** | Boundary* | `subtotal` 진입점 검증 |

> **Boundary\*** (README): Flask UI가 아니라 **도메인 함수 `subtotal` 진입점**에서 수행하는 입력 검증이다. 따라서 테스트 파일 위치는 `tests/entity/` 이다. (`src/cart.py`만 import)

---

## 2. 전제 · 데이터 모델

### 2.1 `items` 형식

`items`는 **라인 목록**이다. 각 라인은 `price`(단가, int)와 `qty`(수량, int)를 갖는다.

```python
# 테스트·구현에서 공통으로 쓸 표현 (dict)
{"price": 12_000, "qty": 3}
```

- 빈 장바구니: `[]` — INV-1만 해당 (`0` 반환). E-1·E-2 범위 밖(별도 계약 없음).
- **본 플랜에서 다루지 않음**: `qty == 0`, `price == 0`, 빈 dict, 키 누락 — ID 없음 → 테스트 추가 금지.

### 2.2 검증 순서 (구현 가이드 · GREEN 시 참고)

`subtotal` 내부 권장 순서:

1. **E-1** — `items is None` → 즉시 `TypeError`
2. **E-2** — 각 인덱스 `i`에 대해 `price < 0` 또는 `qty < 0` → `ValueError` (메시지에 `i` 포함)
3. **INV-1** — `Σ(price × qty)` 반환

RED 단계에서는 검증 순서와 무관하게 **각 계약을 독립 테스트**로 고정한다.

### 2.3 근거 사례 (INV-1)

| 근거 | 입력 | 기대 `subtotal` |
|------|------|-----------------|
| 인터뷰 2024-03-12 | A 3개 × 12,000 + B 1개 × 30,000 | `66_000` |
| 주문 #1107 (소계만) | 단일 라인 60,000 × 1 | `60_000` |
| 주문 #1042 (소계만) | 단일 라인 48,000 × 1 | `48_000` |

### 2.4 근거 사례 (E-2)

| 근거 | 입력 | 기대 |
|------|------|------|
| CS 클레임 — 수량 -1 | `qty: -1` | `ValueError`, 0원으로 조용히 계산하지 않음 |

README 계약상 **음수 `price`** 도 E-2에 포함한다 (PRD OOS-005와 상이 — README·`cart.py` SSOT 우선).

---

## 3. 범위 외 (테스트 작성 금지)

| 항목 | 이유 |
|------|------|
| 할인·VIP·`final_total` | INV-2~4, 별도 플랜 |
| `items` 빈 목록·HTTP 500 | README E-1/E-2에 없음 (PRD E-002는 Boundary Flask) |
| `qty == 0`, `price == 0` | 계약 ID 없음 |
| `items`가 list가 아닌 타입 | 계약 ID 없음 |
| 예외 메시지 **문구** 고정 | E-2는 **인덱스 포함**만 계약; 정확한 문자열은 고정하지 않음 |
| `TypeError` / `ValueError` 외 예외 | 계약 ID 없음 |

---

## 4. 테스트 파일 · 명명

| 항목 | 값 |
|------|-----|
| 경로 | `tests/entity/test_subtotal.py` |
| import | `from src.cart import subtotal` |
| 마커 | `@pytest.mark.entity` (전체) |
| 함수 docstring / 주석 | 계약 ID 명시: `# INV-1`, `# E-1`, `# E-2` |

```bash
pytest tests/entity/test_subtotal.py -q   # 본 플랜만
pytest tests/entity -q                    # Entity 전체
pytest -q                                 # 전체 (작업 종료 시)
```

---

## 5. RED 테스트 케이스

TDD 권장 작성 순서: **가장 단순한 실패 → 점진 확장**. 아래 `RED-n` 순서를 따른다.

### 5.1 INV-1 — 소계 합산

| ID | RED 순서 | 테스트명 (권장) | 입력 `items` | 기대 |
|----|----------|-----------------|--------------|------|
| INV-1-a | 1 | `test_subtotal_single_line` | `[{"price": 1_000, "qty": 1}]` | `1_000` |
| INV-1-b | 2 | `test_subtotal_multiple_lines` | `[{"price": 12_000, "qty": 3}, {"price": 30_000, "qty": 1}]` | `66_000` |
| INV-1-c | 3 | `test_subtotal_empty_cart` | `[]` | `0` |

**assert 패턴**

```python
# INV-1
assert subtotal(items) == expected
```

**RED 시 기대 실패**: `NotImplementedError` (현재 스텁) 또는 잘못된 합.

---

### 5.2 E-1 — `items is None`

| ID | RED 순서 | 테스트명 (권장) | 입력 | 기대 |
|----|----------|-----------------|------|------|
| E-1-a | 4 | `test_subtotal_none_raises_type_error` | `None` | `pytest.raises(TypeError)` |

**assert 패턴**

```python
# E-1
with pytest.raises(TypeError):
    subtotal(None)
```

**주의**

- `TypeError`만 계약. 메시지 내용은 검증하지 않는다.
- `subtotal([])` 와 혼동하지 않는다 — 빈 목록은 INV-1-c.

---

### 5.3 E-2 — 음수 `price` / `qty`, 인덱스 포함

| ID | RED 순서 | 테스트명 (권장) | 입력 `items` | 기대 |
|----|----------|-----------------|--------------|------|
| E-2-a | 5 | `test_subtotal_negative_qty_raises_value_error_with_index` | `[{"price": 1_000, "qty": -1}]` | `ValueError`, 메시지에 `"0"` 또는 `0` |
| E-2-b | 6 | `test_subtotal_negative_price_raises_value_error_with_index` | `[{"price": -500, "qty": 2}]` | `ValueError`, 메시지에 `"0"` 또는 `0` |
| E-2-c | 7 | `test_subtotal_negative_at_later_index` | `[{"price": 1_000, "qty": 1}, {"price": 2_000, "qty": -3}]` | `ValueError`, 메시지에 `"1"` 또는 `1` |

**assert 패턴**

```python
# E-2 — 인덱스 포함만 계약
with pytest.raises(ValueError, match=r"0"):  # 또는 str(index) in str(exc.value)
    subtotal([{"price": 1_000, "qty": -1}])
```

**주의**

- **0원 반환 금지** — CS 클레임(수량 -1 → 화면 0원) 회귀 방지.
- 여러 라인 중 **첫 번째 위반 인덱스**만 검증해도 충분 (계약은 “인덱스 포함”이지 “모든 위반 보고”가 아님).
- E-2-c는 인덱스 `1`이 메시지에 들어가는지로 다중 라인을 구분한다.

---

## 6. RED → GREEN 체크리스트

### RED (tests/ 만 수정)

- [ ] `tests/entity/test_subtotal.py` 생성
- [ ] INV-1-a → c 순으로 테스트 추가, `pytest -q` 실행 시 **실패** 확인
- [ ] E-1-a 추가, 실패 확인
- [ ] E-2-a → c 추가, 실패 확인
- [ ] `assert True`, `pytest.skip`, 예외 삼키기 **사용 안 함**
- [ ] 커밋 메시지 예: `test: add RED tests for INV-1, E-1, E-2`

### GREEN (`src/cart.py` 최소 구현)

- [ ] E-1: `items is None` 분기 + `# E-1` 주석
- [ ] E-2: 음수 검사 루프 + `# E-2` 주석
- [ ] INV-1: 합산 반환 + `# INV-1` 주석
- [ ] `pytest -q` **전부 통과**
- [ ] 커밋 메시지 예: `feat: implement subtotal for INV-1, E-1, E-2`

### REFACTOR (선택 · 본 플랜 이후)

- [ ] 구조 변경과 동작 변경 **분리 커밋**
- [ ] 리팩터 전후 `pytest -q` 동일 통과

---

## 7. 추적 매트릭스

| 계약 ID | 테스트 ID | 테스트 함수 (권장명) | 구현 위치 (`subtotal` 내) |
|---------|-----------|----------------------|---------------------------|
| INV-1 | INV-1-a | `test_subtotal_single_line` | 합산 로직 |
| INV-1 | INV-1-b | `test_subtotal_multiple_lines` | 합산 로직 |
| INV-1 | INV-1-c | `test_subtotal_empty_cart` | 합산 로직 |
| E-1 | E-1-a | `test_subtotal_none_raises_type_error` | `None` 검사 |
| E-2 | E-2-a | `test_subtotal_negative_qty_raises_value_error_with_index` | 음수 검사 |
| E-2 | E-2-b | `test_subtotal_negative_price_raises_value_error_with_index` | 음수 검사 |
| E-2 | E-2-c | `test_subtotal_negative_at_later_index` | 음수 검사 |

---

## 8. 관련 문서

| 문서 | 역할 |
|------|------|
| [README.md](../README.md) | 계약 ID SSOT (INV-1, E-1, E-2) |
| [AGENTS.md](../AGENTS.md) | RED/GREEN/REFACTOR 규칙, 디렉터리 구조 |
| [docs/PRD.md](PRD.md) | MomTest 근거, OOS, 후속 계약(INV-2~4 등) |

---

*본 문서는 `subtotal` 첫 사이클(INV-1 · E-1 · E-2) RED 테스트 설계용입니다.*
