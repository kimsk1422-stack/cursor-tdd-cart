"""Boundary 계층 — Flask 주문 폼 (Track A / Use Cases).

ECB 역할:
- Boundary: HTTP 요청/응답, 입력 검증, HTML 폼 렌더링.
- Entity(`src.cart.final_total`)에 할인 계산을 위임한다.
  Boundary는 할인 공식·문턱·VIP 순서를 재구현하지 않는다.

계약(Contracts):
UC-1  GET / → 200, 본문에 qty·price·VIP 입력 폼 포함
UC-2  POST /calc (price·qty·vip) → 본문에 final_total 결과 표시
UE-1  qty가 숫자가 아니면 400 + 에러 메시지

폼 필드 SSOT: price, qty, vip(checkbox) — POST action=/calc
"""

from flask import Flask, request

from src.cart import final_total

app = Flask(__name__)


@app.get("/")
def index():
    return (
        '<form action="/calc" method="post">'
        '<input name="price" type="text">'
        '<input name="qty" type="text">'
        '<input name="vip" type="checkbox">'
        '<button type="submit">Calc</button>'
        '</form>'
    ), 200  # UC-1


@app.post("/calc")
def calc():
    qty_raw = request.form.get("qty", "")
    try:
        qty = int(qty_raw)
    except ValueError:
        return "qty must be a number", 400  # UE-1

    price = int(request.form.get("price", "0"))
    is_vip = request.form.get("vip") == "on"

    total = final_total([{"price": price, "qty": qty}], is_vip=is_vip)  # UC-2
    return str(total), 200  # UC-2
