from order_parser import parse_order
from inventory import InventoryManager, load_inventory_from_excel
from invoice import generate_invoice
from reporter import DailyReporter

EXCEL_PATH = r"E:\PROJECT 01 (ORDER PROCESS)\jj\Stock Goods -06-05-2026.xlsx"
inv = InventoryManager(load_inventory_from_excel(EXCEL_PATH))

reporter = DailyReporter()

# 3 different orders from 3 different buyers
orders = [
    "Karim Brothers\n8-4021 x 5 ctn\n8-6021 x 2 ctn",
    "Rahim Store\n8-7028 x 3 ctn\n9999 x 1 ctn",
    "Sumon Enterprise\n3-6335 x 4 ctn\n8-4028 x 2 ctn\n0000 x 1 ctn",
]

for msg in orders:
    parsed = parse_order(msg)
    invoice = generate_invoice(parsed, inv)
    reporter.record(invoice)
    print(f"✅ Recorded invoice for {invoice['buyer_name']}")

reporter.print_report()
