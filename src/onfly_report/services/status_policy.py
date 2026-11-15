"""Política de status das reservas."""

from __future__ import annotations

def is_billable(status: str) -> bool:
    """Indica se a reserva entra nos totais financeiros e de noites."""
    return status == "CONFIRMED" ## reformulado a função is_billable, para aceitar somente os casos em que o status é confirmed, refatoração aplicada após o caso de teste em que qualquer status diferente de no show e canceled, foram confirmados erroneamente
