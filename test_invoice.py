import json
from order_parser import parse_order
from inventory import InventoryManager, load_inventory_from_excel
from invoice import generate_invoice, print_invoice

# Load real stock
EXCEL_PATH = r"E:\PROJECT 01 (ORDER PROCESS)\jj\Stock Goods -06-05-2026.xlsx"
inv = InventoryManager(load_inventory_from_excel(EXCEL_PATH))

# Test order message
message = """
Karim Brothers
8-4021 x 5 ctn
8-6021 x 2 ctn
9999 x 1 ctn
"""

print("Parsing order...")
parsed = parse_order(message)

print("Generating invoice...")
invoice = generate_invoice(parsed, inv)

print_invoice(invoice)
print("\nFull JSON:")
print(json.dumps(invoice, indent=2))
