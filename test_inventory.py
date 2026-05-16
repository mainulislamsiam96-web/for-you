# test_inventory.py
# Tests the inventory system using YOUR real Excel stock file.

from inventory import InventoryManager, load_inventory_from_excel

# ── STEP 1: Load your real Excel file ──────────────────────
# Change this path to where your Excel file actually is:
EXCEL_PATH = EXCEL_PATH = r"E:\PROJECT 01 (ORDER PROCESS)\jj\Stock Goods -06-05-2026.xlsx"

print("Loading your real stock file...")
inventory_data = load_inventory_from_excel(EXCEL_PATH)
print(f"✅ Loaded {len(inventory_data)} products from Excel\n")

# ── STEP 2: Create the inventory manager ───────────────────
inv = InventoryManager(inventory_data)

# ── STEP 3: Show all available stock ───────────────────────
inv.show_all(available_only=True)

# ── STEP 4: Test looking up a real SKU ─────────────────────
test_sku = "8-4021"
result = inv.lookup(test_sku)
print(f"Lookup '{test_sku}': {result}")

# ── STEP 5: Test looking up a SKU that doesn't exist ───────
fake_sku = "9999"
result = inv.lookup(fake_sku)
print(f"Lookup '{fake_sku}': {result}")   # should print: None

# ── STEP 6: Test deducting stock (simulating an order) ─────
print(f"\nOrder: 24 pairs of {test_sku}...")
before = inv.lookup(test_sku)["stock"]
inv.deduct(test_sku, 24)
after = inv.lookup(test_sku)["stock"]
print(f"  Stock before: {before} pairs")
print(f"  Stock after:  {after} pairs")
print(f"  Difference:   {before - after} pairs ✅")

# ── STEP 7: Show available SKUs list ───────────────────────
available = inv.get_available_skus()
print(f"\nAll SKUs with stock > 0: {len(available)} items")
print("First 10:", available[:10])
