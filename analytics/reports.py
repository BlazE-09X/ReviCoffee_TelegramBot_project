from database.models import get_connection


def get_discrepancy_summary(days: int = 30) -> dict:
    """Сводка по расхождениям за период."""
    with get_connection() as conn:
        rows = conn.execute(f"""
            SELECT 
                i.name AS item_name,
                i.unit,
                i.price_per_unit,
                SUM(ar.discrepancy) AS total_discrepancy,
                COUNT(ar.id) AS audit_count
            FROM audit_records ar
            JOIN items i ON i.id = ar.item_id
            WHERE ar.audit_date >= datetime('now', '-{days} days')
            GROUP BY ar.item_id
            ORDER BY total_discrepancy ASC
        """).fetchall()

    result = []
    total_loss_value = 0.0

    for row in rows:
        loss_value = abs(row["total_discrepancy"]) * row["price_per_unit"] if row["total_discrepancy"] < 0 else 0
        total_loss_value += loss_value
        result.append({
            "item_name": row["item_name"],
            "unit": row["unit"],
            "total_discrepancy": row["total_discrepancy"],
            "audit_count": row["audit_count"],
            "loss_value": loss_value,
        })

    return {"items": result, "total_loss_value": total_loss_value}


def get_staff_summary(days: int = 30) -> list[dict]:
    """Сводка расхождений по сотрудникам (нейтрально, без выводов)."""
    with get_connection() as conn:
        rows = conn.execute(f"""
            SELECT 
                staff_name,
                COUNT(*) AS audit_count,
                SUM(CASE WHEN discrepancy < 0 THEN 1 ELSE 0 END) AS shortage_count,
                AVG(discrepancy) AS avg_discrepancy
            FROM audit_records
            WHERE audit_date >= datetime('now', '-{days} days')
            GROUP BY staff_name
        """).fetchall()

    return [dict(row) for row in rows]