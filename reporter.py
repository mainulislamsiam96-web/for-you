from datetime import datetime

class DailyReporter:
    def __init__(self):
        self.invoices = []

    def record(self, invoice: dict):
        self.invoices.append(invoice)

    def generate_report(self) -> dict:
        buyer_map = {}
        for inv in self.invoices:
            name = inv['buyer_name']
            if name not in buyer_map:
                buyer_map[name] = {
                    'buyer_name': name,
                    'invoice_count': 0,
                    'total_value': 0.0,
                    'fulfilled_items': 0,
                    'missing_items': 0,
                    'invoice_ids': [],
                    'missing_skus': []
                }
            b = buyer_map[name]
            b['invoice_count'] += 1
            b['total_value'] += inv['totals']['subtotal']
            b['fulfilled_items'] += inv['totals']['fulfilled_item_count']
            b['missing_items'] += inv['totals']['unfulfilled_item_count']
            b['invoice_ids'].append(inv['invoice_id'])
            for u in inv['unfulfilled_items']:
                b['missing_skus'].append({
                    'sku': u['sku'],
                    'shortage_pairs': u['shortage_pairs'],
                    'status': u['status']
                })
        total_revenue = sum(inv['totals']['subtotal'] for inv in self.invoices)
        return {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'total_buyers': len(buyer_map),
            'total_invoices': len(self.invoices),
            'total_revenue': total_revenue,
            'buyers': list(buyer_map.values())
        }

    def print_report(self):
        report = self.generate_report()
        print('\n' + '='*55)
        print('  VICTORY FOOTWEAR — DAILY REPORT')
        print(f"  Date       : {report['report_date']}")
        print(f"  Generated  : {report['generated_at']}")
        print('='*55)
        print(f"  Total Buyers  : {report['total_buyers']}")
        print(f"  Total Invoices: {report['total_invoices']}")
        print(f"  Total Revenue : {report['total_revenue']} tk")
        print('\n  BUYER BREAKDOWN:')
        for b in report['buyers']:
            print(f"  {b['buyer_name']}")
            print(f"    Invoices : {b['invoice_count']}")
            print(f"    Revenue  : {b['total_value']} tk")
            print(f"    Fulfilled: {b['fulfilled_items']} items")
            print(f"    Missing  : {b['missing_items']} items")
            if b['missing_skus']:
                print(f"    Missing SKUs:")
                for s in b['missing_skus']:
                    print(f"      ❌ {s['sku']} — {s['shortage_pairs']} pairs [{s['status']}]")
        print('='*55)