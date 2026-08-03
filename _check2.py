from pathlib import Path
h = Path(r"C:\Users\DELL\Desktop\Teeash-apparel\index.html").read_text(encoding="utf-8")
c = Path(r"C:\Users\DELL\Desktop\Teeash-apparel\styles.css").read_text(encoding="utf-8")
for k in ["cat-tshirts", "cat-trousers", "cat-jeans", "cat-tracksuits", "social-icon", "home-bestsellers-title", "catalog-card", "PROFESSIONAL STOREFRONT"]:
    src = h if k != "PROFESSIONAL STOREFRONT" else c
    print(k, src.count(k) if k == "catalog-card" or k == "social-icon" else (k in src))
