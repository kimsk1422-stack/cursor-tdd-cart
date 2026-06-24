# tests/entity/test_cart.py
# [INV-1] 장바구니 상품의 소계(subtotal)는 수량 * 단가여야 한다.

def test_cart_subtotal_calculation():
    # 단가 1000원짜리 상품을 3개 담았을 때 소계는 3000원이어야 함
    price = 1000
    quantity = 3

    # 아직 실제 코드가 없으므로 아래 호출은 실패(RED)해야 정상입니다.
    from src.cart import calculate_subtotal
    assert calculate_subtotal(price, quantity) == 3000