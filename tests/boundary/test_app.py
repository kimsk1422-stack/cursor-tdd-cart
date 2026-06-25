"""Boundary 계약 RED — UC-1 · UC-2 · UE-1 (Track A).

Arrange / Act / Assert 뼈대만 갖춘 실패 테스트.
구현(`src/app.py`)은 GREEN 단계에서 작성한다.
"""

import pytest

from src.app import app


@pytest.fixture
def client():
    return app.test_client()


# ── UC-1: GET / → 200, 본문에 qty 입력 폼 ─────────────────────────────────


@pytest.mark.boundary
def test_uc_1_index_has_qty_input(client):
    """UC-1: GET / → status 200 이고 본문에 name=\"qty\" 입력이 있다."""
    # Act
    response = client.get("/")  # UC-1

    # Assert
    assert response.status_code == 200  # UC-1
    assert 'name="qty"' in response.get_data(as_text=True)  # UC-1


# ── UC-2: POST /calc → 본문에 final_total 결과 ─────────────────────────────


@pytest.mark.boundary
def test_uc_2_calc_vip_shows_final_total(client):
    """UC-2: POST /calc (price·qty·vip) → 본문에 51300 이 있다."""
    # Act
    response = client.post(
        "/calc",
        data={"price": "60000", "qty": "1", "vip": "on"},
    )  # UC-2

    # Assert
    assert "51300" in response.get_data(as_text=True)  # UC-2


# ── UE-1: qty가 숫자가 아니면 400 ─────────────────────────────────────────


@pytest.mark.boundary
def test_ue_1_calc_non_numeric_qty_returns_400(client):
    """UE-1: POST /calc qty=\"abc\" → status 400."""
    # Act
    response = client.post(
        "/calc",
        data={"price": "60000", "qty": "abc"},
    )  # UE-1

    # Assert
    assert response.status_code == 400  # UE-1
