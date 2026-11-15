"""Testes fornecidos: noites de quarto na virada de mês."""

import pytest

from helpers import run_cli


def test_nights_across_month_boundary(tmp_path):
    """A diferença de datas considera a virada de mês, não o dia do mês."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-01-30",
                "checkout_date": "2025-02-02",
                "rooms": "1",
            }
        ],
    )
    assert report["summary"]["total_room_nights"] == 3

def test_nights_same_day(tmp_path):
    """Testando Checkin e Checkout no mesmo dia"""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-01-30",
                "checkout_date": "2025-01-30",
                "rooms": "1",
            }
        ],
    )
    assert report["summary"]["total_room_nights"] == 0

def test_checkout_before_checkin(tmp_path):
    """Testando Checkout na data anterior ao Checkin"""
    with pytest.raises(
        AssertionError,
        match="A data de saída não pode ser anterior a data de entrada",
    ):
        run_cli(
            tmp_path,
            [
                {
                    "reservation_id": "R-1",
                    "checkin_date": "2025-01-30",
                    "checkout_date": "2025-01-29",
                    "rooms": "1",
                }
            ],
        )
