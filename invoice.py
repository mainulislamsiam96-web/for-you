import uuid
from datetime import datetime

PAIRS_PER_CARTON = 24

def generate_invoice(parsed_order, inventory):
    buyer = parsed_order.get('buyer_name', 'Unknown')
    items = parsed_order.get('items', [])
    warnings = list(parsed_order.get('warnings', []))
    fulfilled = []
    unfulfilled = []
    for item in items:
        sku = str(item.get('sku', '')).strip()
        quantity = int(item.get('quantity', 0))
        unit = item.get('unit', 'carton')
        pairs_needed = quantity * PAIRS_PER_CARTON if unit in ['carton','ctn'] else quantity
        stock_info = inventory.lookup(sku)
        if stock_info is None:
            unfulfilled.append({'sku':sku,'requested_pairs':pairs_needed,'available_pairs':0,'shortage_pairs':pairs_needed,'status':'invalid_sku'})
            warnings.append(f'SKU {sku} not found.')
            continue
        available = stock_info['stock']
        price = stock_info['price']
        if available >= pairs_needed:
            inventory.deduct(sku, pairs_needed)
            fulfilled.append({'sku':sku,'requested_qty':quantity,'fulfilled_pairs':pairs_needed,'unit':unit,'price_per_pair':price,'line_total':price*pairs_needed,'status':'available'})
        elif 0 < available < pairs_needed:
            shortage = pairs_needed - available
            inventory.deduct(sku, available)
            fulfilled.append({'sku':sku,'requested_qty':quantity,'fulfilled_pairs':available,'unit':unit,'price_per_pair':price,'line_total':price*available,'status':'partially_available'})
            unfulfilled.append({'sku':sku,'requested_pairs':pairs_needed,'available_pairs':available,'shortage_pairs':shortage,'status':'partially_available'})
            warnings.append(f'SKU {sku}: needed {pairs_needed} pairs, only {available} available.')
        else:
            unfulfilled.append({'sku':sku,'requested_pairs':pairs_needed,'available_pairs':0,'shortage_pairs':pairs_needed,'status':'out_of_stock'})
    subtotal = sum(f['line_total'] for f in fulfilled)
    return {
        'invoice_id': f'VF-{uuid.uuid4().hex[:6].upper()}',
        'buyer_name': buyer,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'fulfilled_items': fulfilled,
        'unfulfilled_items': unfulfilled,
        'totals': {'subtotal':subtotal,'fulfilled_item_count':len(fulfilled),'unfulfilled_item_count':len(unfulfilled),'total_items':len(items)},
        'warnings': warnings
    }

def print_invoice(invoice):
    print('\n' + '='*55)
    print(f'  VICTORY FOOTWEAR — INVOICE')
    print(f"  Invoice ID : {invoice['invoice_id']}")
    print(f"  Buyer      : {invoice['buyer_name']}")
    print(f"  Date       : {invoice['timestamp']}")
    print('='*55)
    print('\n  FULFILLED ITEMS:')
    for item in invoice['fulfilled_items']:
        price_str = f"{item['line_total']} tk" if item['price_per_pair'] > 0 else 'price TBD'
        print(f"  ✅ {item['sku']} — {item['fulfilled_pairs']} pairs ({price_str}) [{item['status']}]")
    if invoice['unfulfilled_items']:
        print('\n  MISSING ITEMS:')
        for item in invoice['unfulfilled_items']:
            print(f"  ❌ {item['sku']} — needed {item['requested_pairs']} pairs [{item['status']}]")
    print(f"\n  Subtotal : {invoice['totals']['subtotal']} tk")
    print(f"  Fulfilled: {invoice['totals']['fulfilled_item_count']} items")
    print(f"  Missing  : {invoice['totals']['unfulfilled_item_count']} items")
    print('='*55)