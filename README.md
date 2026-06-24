# cursor-tdd-cart

장바구니 할인 계산기 — Python 3.12, pytest 기반 Dual-Track TDD 프로젝트.

## 구조

- `src/cart.py` — Entity (순수 도메인 로직)
- `src/app.py` — Boundary (Flask 주문 폼)
- `tests/entity/` — 불변식(INV-*) 검증
- `tests/boundary/` — 입력/UI 계약(E-*, UC-*) 검증

## 실행

```bash
pip install -r requirements.txt
pytest -q
```