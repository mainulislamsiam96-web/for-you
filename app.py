# app.py
# Flask web server for Victory Footwear Order Agent UI
# Place this file inside your jj folder alongside all other .py files
#
# Run with:  python app.py
# Then open: http://localhost:5000

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import glob

from order_parser import parse_order
from inventory import InventoryManager, load_inventory_from_excel
from invoice import generate_invoice
from reporter import DailyReporter

# ── Setup ──────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder='.')
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Auto-find the latest Excel file in the jj folder
def find_latest_excel():
    files = sorted(glob.glob(os.path.join(BASE_DIR, 'Stock*.xlsx')), reverse=True)
    return files[0] if files else None

excel_path = find_latest_excel()
inv = InventoryManager(load_inventory_from_excel(excel_path)) if excel_path else None
reporter = DailyReporter()

print(f"✅ Inventory loaded from: {excel_path}" if excel_path else "⚠️  No Excel file found.")
if inv:
    total = len(inv.stock)
    in_stock = sum(1 for v in inv.stock.values() if v['stock'] > 0)
    print(f"   {in_stock}/{total} SKUs have stock.")

# ── Routes ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'app_ui.html')


@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    """Return full inventory as JSON."""
    if not inv:
        return jsonify({'error': 'No inventory loaded'}), 500
    items = []
    for sku, data in inv.stock.items():
        items.append({
            'sku': sku,
            'stock': data['stock'],
            'price': data['price'],
            'name': data.get('name', '')
        })
    return jsonify({'items': items, 'total': len(items)})


@app.route('/api/inventory/update', methods=['POST'])
def update_inventory():
    """Add or update a single item in inventory."""
    data = request.json
    sku   = str(data.get('sku', '')).strip()
    stock = int(data.get('stock', 0))
    price = float(data.get('price', 0))
    name  = data.get('name', '')

    if not sku:
        return jsonify({'error': 'SKU required'}), 400

    if not inv:
        return jsonify({'error': 'No inventory loaded'}), 500

    is_new = sku not in inv.stock
    inv.stock[sku] = {'stock': stock, 'price': price, 'name': name}
    return jsonify({'ok': True, 'sku': sku, 'action': 'created' if is_new else 'updated'})


@app.route('/api/parse', methods=['POST'])
def parse_message():
    """Parse a WhatsApp order message with Groq AI."""
    data = request.json
    message = data.get('message', '')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    try:
        parsed = parse_order(message)
        return jsonify(parsed)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/invoice', methods=['POST'])
def create_invoice():
    """Parse a message and build a full invoice in one step."""
    data = request.json
    message = data.get('message', '')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    if not inv:
        return jsonify({'error': 'No inventory loaded'}), 500

    try:
        parsed  = parse_order(message)
        invoice = generate_invoice(parsed, inv)
        reporter.record(invoice)

        # Save invoice JSON to disk
        fname = os.path.join(BASE_DIR, f"invoice_{invoice['invoice_id']}.json")
        import json
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(invoice, f, indent=2, ensure_ascii=False)

        return jsonify(invoice)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/report', methods=['GET'])
def get_report():
    """Return today's daily report."""
    return jsonify(reporter.generate_report())


@app.route('/api/upload-stock', methods=['POST'])
def upload_stock():
    """Accept a new Excel file and reload inventory."""
    global inv, excel_path
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    f = request.files['file']
    if not f.filename.endswith('.xlsx'):
        return jsonify({'error': 'Only .xlsx files accepted'}), 400

    save_path = os.path.join(BASE_DIR, f.filename)
    f.save(save_path)
    excel_path = save_path

    try:
        inv = InventoryManager(load_inventory_from_excel(save_path))
        total   = len(inv.stock)
        in_stock = sum(1 for v in inv.stock.values() if v['stock'] > 0)
        print(f"✅ Reloaded inventory: {in_stock}/{total} SKUs from {f.filename}")
        return jsonify({'ok': True, 'file': f.filename, 'total_skus': total, 'in_stock': in_stock})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Run ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n🚀 Victory Footwear Agent UI")
    print("   Open your browser → http://localhost:5000\n")
    app.run(debug=True, port=5000)
