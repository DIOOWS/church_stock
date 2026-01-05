from utils.db import fetch_table, update_row, insert_row
from datetime import datetime


def add_stock(product_id, qty, movement_type="entrada", reference=None):
    inv = fetch_table("inventory", {"product_id": product_id})
    current = float(inv[0]["quantity"]) if inv else 0.0
    new_qty = current + float(qty)

    if inv:
        update_row(
            "inventory",
            {"product_id": product_id},
            {"quantity": new_qty, "updated_at": datetime.utcnow().isoformat()}
        )
    else:
        insert_row("inventory", {"product_id": product_id, "quantity": new_qty})

    insert_row("stock_movements", {
        "product_id": product_id,
        "qty_change": float(qty),
        "movement_type": movement_type,
        "reference": reference
    })


def register_delivery(family_id, leader_id, basket_type_id, quantity, recipient_name, notes=None):
    """
    Registra entrega completa e baixa o estoque automaticamente.
    """
    delivery = insert_row("deliveries", {
        "family_id": family_id,
        "leader_id": leader_id,
        "basket_type_id": basket_type_id,
        "quantity": int(quantity),
        "notes": notes
    })[0]

    items = fetch_table("basket_type_items", {"basket_type_id": basket_type_id})
    for it in items:
        product_id = it["product_id"]
        req = float(it["quantity_required"])
        total_to_remove = req * int(quantity)
        add_stock(product_id, -total_to_remove, movement_type="saida_cesta", reference=f"Entrega {delivery['id']}")

    return delivery


def quick_basket_checkout(basket_type_id, quantity, reference="Baixa rápida - Dashboard"):
    """
    Baixa estoque com base na receita da cesta SEM registrar entrega (modo rápido).
    """
    items = fetch_table("basket_type_items", {"basket_type_id": basket_type_id})

    if not items:
        raise Exception("Esta cesta não tem itens cadastrados. Cadastre a receita primeiro.")

    for it in items:
        product_id = it["product_id"]
        req = float(it["quantity_required"])
        total_to_remove = req * int(quantity)
        add_stock(product_id, -total_to_remove, movement_type="saida_cesta", reference=reference)
