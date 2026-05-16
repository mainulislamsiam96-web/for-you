# test_parser.py
# Tests the AI order parser with real messy WhatsApp messages

import json
from order_parser import parse_order

# Test messages — realistic WhatsApp orders
messages = [

    # Clean English order
    """
    Karim Brothers
    8-4021 x 5 ctn
    8-6021 x 2 ctn
    """,

    # Bangla words for quantity
    """
    Rahim Store
    8-7028 tin carton
    8-4028 dui ctn
    5-60167 panch carton
    """,

    # Messy mixed format
    """
    bhai
    Sumon Enterprise order:
    8-4021 - 3
    3-6335 x 10
    5-9761 2 ctn
    """,
]

for i, msg in enumerate(messages, 1):
    print(f"\n{'='*50}")
    print(f"TEST {i} — Raw Message:")
    print(msg.strip())
    print(f"\nParsed Result:")
    result = parse_order(msg)
    print(json.dumps(result, indent=2, ensure_ascii=False))
