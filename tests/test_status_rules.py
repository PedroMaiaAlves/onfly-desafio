"""Testes fornecidos: regras de status."""

from helpers import run_cli


def test_status_rules_exclude_cancelled_and_no_show(tmp_path):
    """Somente CONFIRMED entra nos totais financeiros."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "status": "CONFIRMED", "amount": "100.00"},
            {"reservation_id": "R-2", "status": "CANCELLED", "amount": "50.00"},
            {"reservation_id": "R-3", "status": "NO_SHOW", "amount": "20.00"},
        ],
    )
    assert report["summary"]["total_reservations"] == 3
    assert report["summary"]["confirmed_reservations"] == 1
    assert report["summary"]["cancelled_reservations"] == 1
    assert report["summary"]["no_show_reservations"] == 1
    assert report["summary"]["total_amount_brl"] == "100.00"
    assert report["summary"]["total_room_nights"] == 1

def test_only_confirmed_status_is_billable(tmp_path):
    """Status diferentes de CONFIRMED não entram nos totais faturáveis."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "hotel_id": "H01",
                "status": "CONFIRMED",
                "amount": "100.00",
            },
            {
                "reservation_id": "R-2",
                "hotel_id": "H02",
                "status": "PENDING",
                "amount": "900.00",
            },
        ],
    )

    assert report["summary"]["total_reservations"] == 2
    assert report["summary"]["confirmed_reservations"] == 1
    assert report["summary"]["total_room_nights"] == 1
    assert report["summary"]["total_amount_brl"] == "100.00"
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01"]
