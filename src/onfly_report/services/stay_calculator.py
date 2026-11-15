"""Cálculo de noites ocupadas."""

from __future__ import annotations

from datetime import date

def calculate_room_nights(checkin: date, checkout: date, rooms: int) -> int:
    """Calcula noites de quarto: diferença de dias (não inclusiva) vezes quartos."""
    if(checkout < checkin):
        raise ValueError(
            "A data de saída não pode ser anterior a data de entrada"
        )

    return (checkout - checkin).days * rooms ##pegando agora a diferença em dias considerando o mês e não apenas a data
