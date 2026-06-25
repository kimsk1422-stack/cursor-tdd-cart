"""subtotal 계약 RED 스켈레톤 — INV-1, E-1, E-2 (Track B).

Arrange / Act / Assert 뼈대만 갖춘 실패 테스트.
구현(`src/cart.py`)은 GREEN 단계에서 작성한다.
"""

import pytest

from src.cart import subtotal


# ── INV-1: subtotal(items) == Σ(price × qty) ────────────────────────────────


@pytest.mark.entity
def test_inv_1_subtotal_single_line():
    """INV-1-a: subtotal(items) == Σ(price × qty) — 단일 라인."""
    # Arrange
    items = [{"price": 1_000, "qty": 1}]
    expected = 1_000

    # Act
    actual = subtotal(items)  # INV-1

    # Assert
    assert actual == expected  # INV-1


@pytest.mark.entity
def test_inv_1_subtotal_multiple_lines():
    """INV-1-b: subtotal(items) == Σ(price × qty) — 다중 라인 (인터뷰 사례)."""
    # Arrange
    items = [
        {"price": 12_000, "qty": 3},
        {"price": 30_000, "qty": 1},
    ]
    expected = 66_000

    # Act
    actual = subtotal(items)  # INV-1

    # Assert
    assert actual == expected  # INV-1


@pytest.mark.entity
def test_inv_1_subtotal_empty_cart():
    """INV-1-c: subtotal(items) == Σ(price × qty) — 빈 장바구니."""
    # Arrange
    items = []
    expected = 0

    # Act
    actual = subtotal(items)  # INV-1

    # Assert
    assert actual == expected  # INV-1


# ── E-1: items is None → TypeError ──────────────────────────────────────────


@pytest.mark.entity
def test_e_1_subtotal_none_raises_type_error():
    """E-1-a: items is None → TypeError."""
    # Arrange
    items = None

    # Act / Assert
    with pytest.raises(TypeError):  # E-1
        subtotal(items)  # E-1


# ── E-2: price 또는 qty 음수 → ValueError, 인덱스 포함 ───────────────────────


@pytest.mark.entity
def test_e_2_subtotal_negative_qty_raises_value_error_with_index():
    """E-2-a: qty 음수 → ValueError, 인덱스 포함."""
    # Arrange
    items = [{"price": 1_000, "qty": -1}]

    # Act / Assert
    with pytest.raises(ValueError, match=r"0"):  # E-2
        subtotal(items)  # E-2


@pytest.mark.entity
def test_e_2_subtotal_negative_price_raises_value_error_with_index():
    """E-2-b: price 음수 → ValueError, 인덱스 포함."""
    # Arrange
    items = [{"price": -500, "qty": 2}]

    # Act / Assert
    with pytest.raises(ValueError, match=r"0"):  # E-2
        subtotal(items)  # E-2


@pytest.mark.entity
def test_e_2_subtotal_negative_at_later_index():
    """E-2-c: 후행 인덱스 음수 → ValueError, 해당 인덱스 포함."""
    # Arrange
    items = [
        {"price": 1_000, "qty": 1},
        {"price": 2_000, "qty": -3},
    ]

    # Act / Assert
    with pytest.raises(ValueError, match=r"1"):  # E-2
        subtotal(items)  # E-2
