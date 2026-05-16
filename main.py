import json
import os
from order_parser import parse_order
from inventory import InventoryManager, load_inventory_from_excel
from invoice import generate_invoice, print_invoice
from reporter import DailyReporter

EXCEL_PATH = r'E:\PROJECT 01 (ORDER PROCESS)\jj\Stock Goods -14-05-2026.xlsx'


def run_agent():
    print('='*55)
    print('  VICTORY FOOTWEAR — SALES ORDER AGENT')
    print('='*55)
    print('Loading inventory...')
    inv = InventoryManager(load_inventory_from_excel(EXCEL_PATH))
    print('Inventory loaded! 74 products ready.')
    reporter = DailyReporter()
    all_invoices = []
    print('\nPaste WhatsApp order messages below.')
    print('Type DONE when finished. Type REPORT for daily report.\n')
    while True:
        print('-'*55)
        lines = []
        print('Enter order (press Enter twice when done):')
        while True:
            line = input()
            if line.strip() == '':
                break
            if line.strip().upper() == 'DONE':
                print('\nSession ended.')
                reporter.print_report()
                report = reporter.generate_report()
                with open('daily_report.json', 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                print('\nDaily report saved to daily_report.json')
                return
            if line.strip().upper() == 'REPORT':
                reporter.print_report()
                break
            lines.append(line)
        if not lines:
            continue
        message = '\n'.join(lines)
        print('\nParsing order with AI...')
        parsed = parse_order(message)
        print(f"Buyer: {parsed.get('buyer_name', 'Unknown')}")
        print(f"Items found: {len(parsed.get('items', []))}")
        print('Generating invoice...')
        invoice = generate_invoice(parsed, inv)
        print_invoice(invoice)
        reporter.record(invoice)
        all_invoices.append(invoice)
        with open(f"invoice_{invoice['invoice_id']}.json", 'w', encoding='utf-8') as f:
            json.dump(invoice, f, indent=2, ensure_ascii=False)
        print(f"Invoice saved to invoice_{invoice['invoice_id']}.json")


if __name__ == '__main__':
    run_agent()
