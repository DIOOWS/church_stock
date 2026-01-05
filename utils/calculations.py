import math
from utils.db import fetch_table


def get_inventory_map():
    inv = fetch_table("inventory")
    return {x["product_id"]: float(x["quantity"]) for x in inv}


def compute_mountable_for_basket(basket_type_id):
    """
    Mantido para compatibilidade com páginas antigas.
    Retorna:
    - mountable (int)
    - limiting_product_id (uuid)
    """
    items = fetch_table("basket_type_items", {"basket_type_id": basket_type_id})
    inv_map = get_inventory_map()

    if not items:
        return 0, None

    possible = []
    limiting_product = None
    limiting_value = None

    for it in items:
        pid = it["product_id"]
        req = float(it["quantity_required"])
        stock = inv_map.get(pid, 0.0)
        if req <= 0:
            continue
        val = stock / req
        possible.append(val)

        if limiting_value is None or val < limiting_value:
            limiting_value = val
            limiting_product = pid

    mountable = math.floor(min(possible)) if possible else 0
    return mountable, limiting_product


def analyze_basket(basket_type_id):
    """
    Mantido para outras telas (Tipos de Cesta).
    Retorna:
    - completas: número de cestas completas montáveis
    - faltas_proxima: dict {produto_id: falta} para montar +1 cesta
    - checklist: lista de dicts com status de cada item
    """
    items = fetch_table("basket_type_items", {"basket_type_id": basket_type_id})
    inv_map = get_inventory_map()

    if not items:
        return 0, {}, []

    # 1) calcular completas
    ratios = []
    for it in items:
        pid = it["product_id"]
        req = float(it["quantity_required"])
        stock = inv_map.get(pid, 0.0)
        ratios.append(stock / req)

    completas = math.floor(min(ratios)) if ratios else 0

    # 2) calcular sobras e faltas
    faltas_proxima = {}
    checklist = []

    for it in items:
        pid = it["product_id"]
        req = float(it["quantity_required"])
        stock = inv_map.get(pid, 0.0)

        usado = completas * req
        sobra = stock - usado

        if sobra < req:
            falta = req - sobra
            faltas_proxima[pid] = float(falta)

        checklist.append({
            "product_id": pid,
            "required": req,
            "stock": stock,
            "used_for_full": usado,
            "remaining": sobra,
            "ok_for_next": sobra >= req,
            "missing_for_next": max(0.0, req - sobra)
        })

    return completas, faltas_proxima, checklist


def basket_summary(basket_type_id):
    """
    FUNÇÃO NOVA PARA O DASHBOARD:
    Retorna:
    - completas (int) => quantas cestas disponíveis (montáveis)
    - limitante_nome (str) => item que trava a próxima cesta
    - falta_para_mais_1 (float) => quanto falta do item limitante
    """
    items = fetch_table("basket_type_items", {"basket_type_id": basket_type_id})
    products = fetch_table("products")
    prod_map = {p["id"]: p["name"] for p in products}

    inv_map = get_inventory_map()

    if not items:
        return 0, "-", 0

    # calcular completas
    ratios = []
    for it in items:
        pid = it["product_id"]
        req = float(it["quantity_required"])
        stock = inv_map.get(pid, 0.0)
        ratios.append(stock / req)

    completas = math.floor(min(ratios)) if ratios else 0

    # calcular faltante apenas do ITEM LIMITANTE (para +1 cesta)
    limitante_pid = None
    limitante_falta = 0

    for it in items:
        pid = it["product_id"]
        req = float(it["quantity_required"])
        stock = inv_map.get(pid, 0.0)

        usado = completas * req
        sobra = stock - usado

        if sobra < req:
            falta = req - sobra
            # pega o maior faltante (mais crítico)
            if falta > limitante_falta:
                limitante_falta = falta
                limitante_pid = pid

    limitante_nome = prod_map.get(limitante_pid, "-") if limitante_pid else "-"
    return completas, limitante_nome, round(limitante_falta, 2)
