import re
import urllib.request
from collections import Counter

html = open(r"C:\Users\DELL\Desktop\Teeash-apparel\index.html", encoding="utf-8").read()
print("Product Image placeholder:", "Product Image" in html)
ids = re.findall(r"images.unsplash.com/photo-([a-z0-9-]+)", html)
print("count", len(ids))
dupes = [(k, v) for k, v in Counter(ids).items() if v > 1]
print("dupes", dupes if dupes else "none")
urls = re.findall(r'https://images\.unsplash\.com/photo-[a-z0-9-]+\?[^"\s]+', html)
fail = []
for u in sorted(set(urls)):
    try:
        with urllib.request.urlopen(u, timeout=25) as r:
            if r.status != 200:
                fail.append((r.status, u))
    except Exception as e:
        fail.append((str(e)[:80], u))
print("unique urls", len(set(urls)))
print("fails", len(fail))
for f in fail:
    print(f)
for i, x in enumerate(ids, 1):
    print(i, x)
