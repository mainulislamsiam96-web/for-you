# inventory.py
# Reads YOUR real stock from the Excel file automatically.

import pandas as pd
import os


def load_inventory_from_excel(filepath: str) -> list[dict]:
    """
    Reads Victory Footwear stock Excel file and returns
    a clean list of all products with SKU, stock, price.
    """
    df = pd.read_excel(filepath, sheet_name="Vic-Stock", header=None)
    inventory = []

    for _, row in df.iterrows():
        try:
            article = str(row[1]).strip()
            stock   = row[7]
            status  = str(row[9]).strip() if pd.notna(row[9]) else ""
            price   = row[10] if pd.notna(row[10]) else 0.0

            # Skip headers, totals, empty rows
            if article in ["nan", "Article No :", "Previous Page", ""]:
                continue
            if not pd.notna(stock):
                continue

            inventory.append({
                "sku":   article,
                "stock": int(stock),
                "price": float(price) if str(price) not in ["nan","0","0.0"] else 0.0
            })
        except Exception:
            continue

    return inventory


class InventoryManager:
    """
    Your warehouse in code.
    Knows every product, its stock (in pairs), and price.
    """

    def __init__(self, inventory_data: list[dict]):
        self.stock = {}
        for item in inventory_data:
            sku = str(item["sku"]).strip()
            self.stock[sku] = {
                "stock": int(item.get("stock", 0)),
                "price": float(item.get("price", 0.0))
            }

    def lookup(self, sku: str) -> dict | None:
        """Check a SKU. Returns stock + price or None if not found."""
        sku = str(sku).strip()
        return dict(self.stock[sku]) if sku in self.stock else None

    def deduct(self, sku: str, qty: int):
        """Remove pairs from stock after an order is fulfilled."""
        sku = str(sku).strip()
        if sku in self.stock:
            self.stock[sku]["stock"] = max(0, self.stock[sku]["stock"] - qty)

    def set_price(self, sku: str, price: float):
        """Set or update the price for a SKU."""
        sku = str(sku).strip()
        if sku in self.stock:
            self.stock[sku]["price"] = price

    def get_available_skus(self) -> list[str]:
        """Return list of all SKUs that have stock > 0."""
        return [sku for sku, info in self.stock.items() if info["stock"] > 0]

    def show_all(self, available_only: bool = True):
        """Print the current stock table."""
        print("\n" + "="*55)
        print("   VICTORY FOOTWEAR — CURRENT STOCK")
        print("="*55)
        count = 0
        for sku, info in self.stock.items():
            if available_only and info["stock"] == 0:
                continue
            price_str = f"{info['price']} tk" if info["price"] > 0 else "price not set"
            print(f"  {sku:<20} {info['stock']:>6} pairs   {price_str}")
            count += 1
        print(f"{'='*55}")
        print(f"  Total available SKUs: {count}")
        print("="*55 + "\n")
