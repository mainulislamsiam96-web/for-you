code = []
code.append("import uuid")
code.append("from datetime import datetime")
code.append("")
code.append("PAIRS_PER_CARTON = 24")
code.append("")
code.append("def generate_invoice(parsed_order, inventory):")
code.append("    buyer = parsed_order.get('buyer_name', 'Unknown')")
code.append("    items = parsed_order.get('items', [])")
code.append("    warnings = list(parsed_order.get('warnings', []))")
code.append("    fulfilled = []")
code.append("    unfulfilled = []")
code.append("    for item in items:")
code.append("        sku = str(item.get('sku', '')).strip()")
code.append("        quantity = int(item.get('quantity', 0))")
code.append("        unit = item.get('unit', 'carton')")
code.append(
    "        pairs_needed = quantity * PAIRS_PER_CARTON if unit in ['carton','ctn'] else quantity")
code.append("        stock_info = inventory.lookup(sku)")
code.append("        if stock_info is None:")
code.append(
    "            unfulfilled.append({'sku':sku,'requested_pairs':pairs_needed,'available_pairs':0,'shortage_pairs':pairs_needed,'status':'invalid_sku'})")
code.append("            warnings.append(f'SKU {sku} not found.')")
code.append("            continue")
code.append("        available = stock_info['stock']")
code.append("        price = stock_info['price']")
code.append("        if available >= pairs_needed:")
code.append("            inventory.deduct(sku, pairs_needed)")
code.append(
    "            fulfilled.append({'sku':sku,'requested_qty':quantity,'fulfilled_pairs':pairs_needed,'unit':unit,'price_per_pair':price,'line_total':price*pairs_needed,'status':'available'})")
code.append("        elif 0 < available < pairs_needed:")
code.append("            shortage = pairs_needed - available")
code.append("            inventory.deduct(sku, available)")
code.append(
    "            fulfilled.append({'sku':sku,'requested_qty':quantity,'fulfilled_pairs':available,'unit':unit,'price_per_pair':price,'line_total':price*available,'status':'partially_available'})")
code.append(
    "            unfulfilled.append({'sku':sku,'requested_pairs':pairs_needed,'available_pairs':available,'shortage_pairs':shortage,'status':'partially_available'})")
code.append(
    "            warnings.append(f'SKU {sku}: needed {pairs_needed} pairs, only {available} available.')")
code.append("        else:")
code.append(
    "            unfulfilled.append({'sku':sku,'requested_pairs':pairs_needed,'available_pairs':0,'shortage_pairs':pairs_needed,'status':'out_of_stock'})")
code.append("    subtotal = sum(f['line_total'] for f in fulfilled)")
code.append("    return {")
code.append("        'invoice_id': f'VF-{uuid.uuid4().hex[:6].upper()}',")
code.append("        'buyer_name': buyer,")
code.append("        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),")
code.append("        'fulfilled_items': fulfilled,")
code.append("        'unfulfilled_items': unfulfilled,")
code.append(
    "        'totals': {'subtotal':subtotal,'fulfilled_item_count':len(fulfilled),'unfulfilled_item_count':len(unfulfilled),'total_items':len(items)},")
code.append("        'warnings': warnings")
code.append("    }")
code.append("")
code.append("def print_invoice(invoice):")
code.append("    print('\\n' + '='*55)")
code.append("    print(f'  VICTORY FOOTWEAR — INVOICE')")
code.append("    print(f\"  Invoice ID : {invoice['invoice_id']}\")")
code.append("    print(f\"  Buyer      : {invoice['buyer_name']}\")")
code.append("    print(f\"  Date       : {invoice['timestamp']}\")")
code.append("    print('='*55)")
code.append("    print('\\n  FULFILLED ITEMS:')")
code.append("    for item in invoice['fulfilled_items']:")
code.append(
    "        price_str = f\"{item['line_total']} tk\" if item['price_per_pair'] > 0 else 'price TBD'")
code.append(
    "        print(f\"  ✅ {item['sku']} — {item['fulfilled_pairs']} pairs ({price_str}) [{item['status']}]\")")
code.append("    if invoice['unfulfilled_items']:")
code.append("        print('\\n  MISSING ITEMS:')")
code.append("        for item in invoice['unfulfilled_items']:")
code.append(
    "            print(f\"  ❌ {item['sku']} — needed {item['requested_pairs']} pairs [{item['status']}]\")")
code.append(
    "    print(f\"\\n  Subtotal : {invoice['totals']['subtotal']} tk\")")
code.append(
    "    print(f\"  Fulfilled: {invoice['totals']['fulfilled_item_count']} items\")")
code.append(
    "    print(f\"  Missing  : {invoice['totals']['unfulfilled_item_count']} items\")")
code.append("    print('='*55)")

with open("invoice.py", "w", encoding="utf-8") as f:
    f.write("\n".join(code))

print("Done! invoice.py created successfully!")
