from pathlib import Path

html_path = Path(r"C:\Users\DELL\Desktop\Teeash-apparel\index.html")
html = html_path.read_text(encoding="utf-8")
start = html.find("  <!-- Small scripts:")
end = html.find("  </script>", start)
if start < 0 or end < 0:
    raise SystemExit("script not found")
end = end + len("  </script>")
replacement = '  <script src="app.js" defer></script>'
html = html[:start] + replacement + html[end:]
html = html.replace("<h3>Fabric &amp; Quality</h3>", "<h3>Material</h3>")
html_path.write_text(html, encoding="utf-8")
print("OK", len(html))
