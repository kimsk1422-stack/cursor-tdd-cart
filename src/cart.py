"""장바구니 할인 계산 — Entity 계층 (Track B / Domain).

계약(Contracts):
INV-1 subtotal == Σ(price*qty)
INV-2 amount>=50000 → round(*0.9) / <50000 그대로 (경계 포함)
INV-3 문턱할인 후 VIP면 round(*0.95). 순서 문턱→VIP 고정
INV-4 0 <= final_total <= subtotal (할인은 금액을 늘리지 않는다)
E-1   items is None → TypeError
E-2   price/qty 음수 → ValueError(인덱스 포함)
"""

THRESHOLD = 50000  # INV-2 문턱 금액 (SSOT)


def _validate_line_items(items):
    for index, item in enumerate(items):
        price = item["price"]
        qty = item["qty"]
        if price < 0 or qty < 0:
            raise ValueError(f"negative price or qty at index {index}")  # E-2


def subtotal(items):
    if items is None:
        raise TypeError  # E-1
    _validate_line_items(items)  # E-2
    total = 0
    for item in items:
        total += item["price"] * item["qty"]  # INV-1
    return total  # INV-1


def apply_threshold_discount(amount):
    # TODO(INV-2): 경계 포함(>=) 10% 할인, 반올림
    raise NotImplementedError


def final_total(items, is_vip=False):
    # TODO(INV-3): 문턱할인 → (VIP면) 5% 추가, 순서 고정
    # TODO(INV-4): 결과가 subtotal 을 넘지 않음을 보장하는 위치
    raise NotImplementedError
