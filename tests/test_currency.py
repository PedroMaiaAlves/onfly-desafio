"""Testes fornecidos: câmbio para BRL."""

from helpers import run_cli


def test_currency_conversion_to_brl(tmp_path):
    """Multiplica o valor pela taxa, sem inverter a operação."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "currency": "BRL", "amount": "100.00"},
            {"reservation_id": "R-2", "currency": "USD", "amount": "100.00"},
        ],
    )
    assert report["summary"]["total_amount_brl"] == "642.00"

def test_currency_conversion_to_brl_with_amount_equals_zero(tmp_path):
    """Testando a conversão de valor quando o amount informado for zero"""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "currency": "BRL", "amount": "0"},
            {"reservation_id": "R-2", "currency": "USD", "amount": "100.00"},
        ],
    )
    assert report["summary"]["total_amount_brl"] == "542.00"

def test_currency_conversion_preserves_decimal_precision(tmp_path):
    """A conversão usa Decimal e arredonda half-up somente na serialização."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "currency": "USD",
                "amount": "0.75",
            }
        ],
    )

    assert report["summary"]["total_amount_brl"] == "4.07"
