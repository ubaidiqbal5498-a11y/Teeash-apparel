# -*- coding: utf-8 -*-
"""One-shot transform for Teeash Apparel premium redesign."""
from pathlib import Path
import re

ROOT = Path(r"C:\Users\DELL\Desktop\Teeash-apparel")
CSS = ROOT / "styles.css"
HTML = ROOT / "index.html"

# ---------- CSS tokens ----------
css = CSS.read_text(encoding="utf-8")
new_root = r'''/* ============================================================
   Teeash Apparel — Premium Modern Fashion
   Light luxury theme (Apple / Nike inspired)
   ============================================================ */

/* ---------- Brand tokens ---------- */
:root {
  --color-white: #FFFFFF;
  --color-soft-gray: #F5F5F5;
  --color-accent: #2563EB;
  --color-accent-hover: #1D4ED8;
  --color-accent-soft: rgba(37, 99, 235, 0.12);
  --color-text: #111827;
  --color-muted: #6B7280;
  --color-muted-soft: #9CA3AF;
  --color-surface: #F5F5F5;
  --color-surface-elevated: #FFFFFF;
  --color-border: rgba(17, 24, 39, 0.08);
  --color-border-strong: rgba(37, 99, 235, 0.28);
  --color-black: #111827;
  --color-gold: #2563EB;
  --color-gold-bright: #3B82F6;
  --color-gold-soft: rgba(37, 99, 235, 0.12);
  --shadow-card: 0 8px 28px rgba(17, 24, 39, 0.06);
  --shadow-card-hover: 0 16px 40px rgba(17, 24, 39, 0.10);
  --shadow-drawer: -12px 0 40px rgba(17, 24, 39, 0.12);
  --radius-card: 18px;
  --radius-btn: 999px;
  --radius-lg: 20px;
  --section-pad-y: 5.5rem;
  --section-pad-x: clamp(1.25rem, 4vw, 3.5rem);
  --max-width: 1240px;
  --font-family: "Manrope", "Poppins", system-ui, sans-serif;
  --font-display: "Cormorant Garamond", "Times New Roman", serif;
  --transition: 0.3s ease;
  --header-height: 4.5rem;
}'''

m = re.search(r":root\s*\{.*?\n\}", css, flags=re.S)
if not m:
    raise SystemExit("Could not find :root in CSS")
# Keep header comment before Brand tokens if present
pre = css[: m.start()]
# Strip old file header comment block at start
pre = re.sub(
    r"^/\* =+.*?Brand tokens ---------- \*/\s*",
    "",
    pre,
    count=1,
    flags=re.S,
)
css = new_root + "\n\n" + css[m.end() :]

# body base colors
css = css.replace(
    """body {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: var(--font-family);
  background-color: var(--color-black);
  color: var(--color-white);
  line-height: 1.65;
  letter-spacing: 0.01em;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}""",
    """body {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: var(--font-family);
  background-color: var(--color-white);
  color: var(--color-text);
  line-height: 1.65;
  letter-spacing: 0.01em;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}""",
)

css = css.replace(
    """::selection {
  background: var(--color-gold);
  color: var(--color-black);
}""",
    """::selection {
  background: var(--color-accent);
  color: var(--color-white);
}""",
)

# Append light theme + new component styles
OVERRIDE = r'''

/* ============================================================
   LIGHT LUXURY THEME + NEW COMPONENTS
   ============================================================ */

html { scroll-behavior: auto; }

body {
  background: var(--color-white);
  color: var(--color-text);
}

/* Pages (SPA-style views) */
.page {
  display: none;
  animation: pageIn 0.45s ease;
}
.page.is-active {
  display: block;
}
@keyframes pageIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.site-header {
  background: rgba(255, 255, 255, 0.86);
  border-bottom: 1px solid var(--color-border);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}
.site-header.is-scrolled {
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 8px 28px rgba(17, 24, 39, 0.06);
  border-bottom-color: var(--color-border);
}
.logo,
.site-header .logo {
  color: var(--color-text) !important;
  font-weight: 700;
  letter-spacing: 0.04em;
}
.nav-links a,
.site-header.is-scrolled .nav-links a {
  color: var(--color-muted) !important;
}
.nav-links a:hover,
.site-header.is-scrolled .nav-links a:hover {
  color: var(--color-text) !important;
}
.nav-links a.active,
.site-header.is-scrolled .nav-links a.active {
  color: var(--color-accent) !important;
}
.nav-icon-btn,
.site-header.is-scrolled .nav-icon-btn {
  border-color: var(--color-border) !important;
  background: var(--color-soft-gray) !important;
  color: var(--color-text) !important;
}
.nav-icon-btn:hover {
  background: var(--color-accent) !important;
  border-color: var(--color-accent) !important;
  color: #fff !important;
}
.nav-cta {
  background: var(--color-accent) !important;
  border-color: var(--color-accent) !important;
  color: #fff !important;
}
.nav-cta:hover {
  background: var(--color-accent-hover) !important;
  border-color: var(--color-accent-hover) !important;
  color: #fff !important;
}
.nav-toggle-bar {
  background: var(--color-text) !important;
}
.site-search {
  background: var(--color-white);
  border-bottom: 1px solid var(--color-border);
}
.site-search input {
  background: var(--color-soft-gray);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  border-radius: 14px;
}

.btn-primary {
  background: var(--color-accent) !important;
  border-color: var(--color-accent) !important;
  color: #fff !important;
}
.btn-primary:hover {
  background: var(--color-accent-hover) !important;
  border-color: var(--color-accent-hover) !important;
}
.btn-secondary,
.btn-outline {
  background: transparent !important;
  border: 1px solid var(--color-border-strong) !important;
  color: var(--color-text) !important;
}
.btn-secondary:hover,
.btn-outline:hover {
  background: var(--color-accent-soft) !important;
  border-color: var(--color-accent) !important;
  color: var(--color-accent) !important;
}
.btn-soft {
  background: var(--color-soft-gray) !important;
  color: var(--color-text) !important;
  border: 1px solid var(--color-border) !important;
}

.hero {
  background: linear-gradient(160deg, #F8FAFC 0%, #EEF2FF 48%, #F5F5F5 100%);
  color: var(--color-text);
  min-height: calc(100vh - var(--header-height));
  margin-top: var(--header-height);
}
.hero-overlay {
  background: linear-gradient(90deg, rgba(255,255,255,0.82) 0%, rgba(255,255,255,0.35) 55%, rgba(255,255,255,0.1) 100%) !important;
}
.hero-welcome,
.hero-subtitle,
.section-eyebrow {
  color: var(--color-accent) !important;
}
.hero-heading,
.hero-content h1 {
  color: var(--color-text) !important;
}
.hero-description {
  color: var(--color-muted) !important;
}
.scroll-indicator {
  display: none !important;
}

.categories,
.streetwear-collection,
.bestsellers,
.featured,
.featured-products,
.premium-collection,
.trust-badges,
.reviews,
.faq,
.about,
.brand-story,
.contact,
.checkout,
.about-page {
  background: var(--color-white);
  color: var(--color-text);
}
.bestsellers,
.featured-products,
.faq,
.trust-badges {
  background: var(--color-soft-gray);
}

.categories-header h2,
.streetwear-collection-header h2,
.bestsellers-header h2,
.premium-collection-header h2,
.featured-header h2,
.featured-products-header h2,
.brand-story-header h2,
.contact-header h2,
.checkout-header h2,
.about-content h2,
.about-page h2,
.reviews-header h2,
.faq-header h2 {
  color: var(--color-text) !important;
}
.categories-header p,
.streetwear-collection-header p,
.bestsellers-header p,
.premium-collection-header p,
.featured-header p,
.featured-products-header p,
.brand-story-header p,
.contact-header p,
.reviews-header p,
.faq-header p,
.about-page p {
  color: var(--color-muted) !important;
}

.category-card,
.streetwear-card,
.bestseller-card,
.premium-card,
.product-card,
.trust-card,
.review-card,
.faq-item,
.contact-card,
.checkout-summary,
.about-feature-card {
  background: var(--color-white) !important;
  border: 1px solid var(--color-border) !important;
  border-radius: var(--radius-card) !important;
  box-shadow: var(--shadow-card) !important;
  color: var(--color-text) !important;
  transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
}
.category-card:hover,
.streetwear-card:hover,
.bestseller-card:hover,
.premium-card:hover,
.product-card:hover,
.about-feature-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-card-hover) !important;
  border-color: var(--color-border-strong) !important;
}

.is-product-clickable {
  cursor: pointer;
}
.is-product-clickable:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 3px;
}

.streetwear-info h3,
.bs-info h3,
.premium-info h3,
.product-info h3,
.category-card h3 {
  color: var(--color-text) !important;
}
.streetwear-desc,
.bs-desc,
.product-desc,
.premium-category,
.streetwear-price,
.bs-price,
.product-price,
.premium-price {
  color: var(--color-muted) !important;
}
.streetwear-price,
.bs-price,
.product-price,
.premium-price {
  color: var(--color-text) !important;
  font-weight: 700;
}

.streetwear-actions,
.bs-actions,
.product-card .btn {
  display: none !important;
}

.product-label,
.bs-badge,
.premium-badge,
.product-modal-badge {
  background: var(--color-accent) !important;
  color: #fff !important;
}

.site-footer {
  background: #0B1220 !important;
  color: rgba(255,255,255,0.82) !important;
}
.footer-logo,
.footer-heading {
  color: #fff !important;
}
.footer-links a,
.footer-social a {
  color: rgba(255,255,255,0.7) !important;
}
.footer-links a:hover,
.footer-social a:hover {
  color: #93C5FD !important;
}

/* About page */
.about-page {
  margin-top: var(--header-height);
  padding-bottom: 4rem;
}
.about-hero {
  position: relative;
  min-height: 52vh;
  display: grid;
  place-items: end start;
  overflow: hidden;
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
}
.about-hero img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.about-hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(17,24,39,0.15), rgba(17,24,39,0.72));
}
.about-hero-content {
  position: relative;
  z-index: 1;
  padding: 3.5rem var(--section-pad-x);
  color: #fff;
  max-width: 720px;
}
.about-hero-content h1 {
  font-family: var(--font-display);
  font-size: clamp(2.4rem, 5vw, 4rem);
  line-height: 1.1;
  margin: 0.4rem 0 0.8rem;
}
.about-hero-content p {
  color: rgba(255,255,255,0.88) !important;
  font-size: 1.05rem;
}
.about-inner {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 3.5rem var(--section-pad-x) 0;
}
.about-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  margin: 2rem 0 3rem;
}
.about-feature-card {
  padding: 1.6rem 1.4rem;
}
.about-feature-card h3 {
  font-size: 1.15rem;
  margin-bottom: 0.45rem;
}
.about-feature-card p {
  color: var(--color-muted);
  font-size: 0.95rem;
}
.about-story {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 2.5rem;
  align-items: center;
  margin-bottom: 3.5rem;
}
.about-story img {
  width: 100%;
  border-radius: var(--radius-lg);
  aspect-ratio: 4/5;
  object-fit: cover;
  box-shadow: var(--shadow-card-hover);
}
.about-contact-panel {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 1.5rem;
  padding: 2rem;
  border-radius: var(--radius-lg);
  background: linear-gradient(145deg, #F8FAFC, #EEF2FF);
  border: 1px solid var(--color-border);
}
.about-social {
  display: flex;
  gap: 0.75rem;
  list-style: none;
  margin-top: 1rem;
}
.about-social a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.6rem;
  height: 2.6rem;
  border-radius: 999px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  text-decoration: none;
  transition: 0.25s ease;
}
.about-social a:hover {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: #fff;
}
@media (max-width: 900px) {
  .about-grid,
  .about-story,
  .about-contact-panel {
    grid-template-columns: 1fr;
  }
}

/* Product modal upgrades */
.product-modal-dialog {
  background: var(--color-white) !important;
  color: var(--color-text) !important;
  border-radius: var(--radius-lg) !important;
  box-shadow: var(--shadow-card-hover) !important;
  max-width: min(1080px, 94vw);
}
.product-modal-title,
#product-modal-title {
  color: var(--color-text) !important;
}
.product-modal-price {
  color: var(--color-accent) !important;
  font-size: 1.35rem;
  font-weight: 700;
}
.product-modal-desc,
.product-detail-block p,
.product-modal-note,
.product-modal-label {
  color: var(--color-muted) !important;
}
.product-detail-block h3 {
  color: var(--color-text) !important;
}
.product-modal-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-top: 0.5rem;
}
.product-modal-qty {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  margin: 0.75rem 0 1rem;
  padding: 0.35rem;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  width: fit-content;
  background: var(--color-soft-gray);
}
.product-modal-qty button {
  width: 2.1rem;
  height: 2.1rem;
  border: 0;
  border-radius: 999px;
  background: var(--color-white);
  color: var(--color-text);
  cursor: pointer;
  font-size: 1.1rem;
}
.product-modal-qty span {
  min-width: 1.5rem;
  text-align: center;
  font-weight: 600;
}
.product-modal-related {
  margin-top: 1.75rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--color-border);
}
.product-modal-related h3 {
  font-size: 1rem;
  margin-bottom: 0.85rem;
}
.related-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}
.related-card {
  border: 1px solid var(--color-border);
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  background: var(--color-soft-gray);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.related-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card);
}
.related-card img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}
.related-card p {
  padding: 0.55rem 0.65rem 0.7rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--color-text);
}
@media (max-width: 700px) {
  .product-modal-actions,
  .related-grid {
    grid-template-columns: 1fr;
  }
}

/* Cart drawer */
.cart-drawer {
  position: fixed;
  inset: 0;
  z-index: 1200;
  pointer-events: none;
}
.cart-drawer.is-open {
  pointer-events: auto;
}
.cart-drawer-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(17, 24, 39, 0.45);
  opacity: 0;
  transition: opacity 0.3s ease;
}
.cart-drawer.is-open .cart-drawer-backdrop {
  opacity: 1;
}
.cart-drawer-panel {
  position: absolute;
  top: 0;
  right: 0;
  width: min(420px, 100%);
  height: 100%;
  background: var(--color-white);
  box-shadow: var(--shadow-drawer);
  display: flex;
  flex-direction: column;
  transform: translateX(105%);
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}
.cart-drawer.is-open .cart-drawer-panel {
  transform: translateX(0);
}
.cart-drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.35rem;
  border-bottom: 1px solid var(--color-border);
}
.cart-drawer-header h2 {
  font-size: 1.15rem;
  font-weight: 700;
}
.cart-drawer-close {
  width: 2.4rem;
  height: 2.4rem;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  background: var(--color-soft-gray);
  cursor: pointer;
  font-size: 1.25rem;
  color: var(--color-text);
}
.cart-drawer-body {
  flex: 1;
  overflow: auto;
  padding: 1rem 1.25rem;
}
.cart-drawer-empty {
  text-align: center;
  color: var(--color-muted);
  padding: 2.5rem 1rem;
}
.cart-drawer-items {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}
.cart-drawer-item {
  display: grid;
  grid-template-columns: 76px 1fr;
  gap: 0.85rem;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 14px;
  background: var(--color-soft-gray);
}
.cart-drawer-item img {
  width: 76px;
  height: 95px;
  object-fit: cover;
  border-radius: 10px;
}
.cart-drawer-item h4 {
  font-size: 0.92rem;
  margin-bottom: 0.2rem;
}
.cart-drawer-item .meta {
  font-size: 0.78rem;
  color: var(--color-muted);
  margin-bottom: 0.45rem;
}
.cart-drawer-item-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}
.cart-drawer-footer {
  border-top: 1px solid var(--color-border);
  padding: 1.1rem 1.35rem 1.35rem;
  display: grid;
  gap: 0.55rem;
}
.cart-totals-row {
  display: flex;
  justify-content: space-between;
  color: var(--color-muted);
  font-size: 0.92rem;
}
.cart-totals-row.total {
  color: var(--color-text);
  font-weight: 700;
  font-size: 1.05rem;
  margin-top: 0.25rem;
}
.cart-drawer-actions {
  display: grid;
  gap: 0.55rem;
  margin-top: 0.55rem;
}
body.drawer-open,
body.modal-open {
  overflow: hidden;
}

.checkout {
  margin-top: var(--header-height);
}
.checkout-header h2,
.checkout .contact-card {
  color: var(--color-text);
}
.checkout input,
.checkout textarea,
.contact input,
.contact textarea {
  background: var(--color-white) !important;
  color: var(--color-text) !important;
  border: 1px solid var(--color-border) !important;
  border-radius: 14px !important;
}

.cart-toast {
  background: var(--color-white) !important;
  color: var(--color-text) !important;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card-hover);
}
.cart-toast-link {
  color: var(--color-accent) !important;
}

.whatsapp-float {
  background: #25D366 !important;
  color: #fff !important;
}

.bs-size,
.product-modal-sizes .bs-size {
  border-color: var(--color-border) !important;
  color: var(--color-text) !important;
  background: var(--color-white) !important;
}
.bs-size.is-active,
.product-modal-sizes .bs-size.is-active {
  background: var(--color-accent) !important;
  border-color: var(--color-accent) !important;
  color: #fff !important;
}

.media-skeleton::before {
  background: linear-gradient(90deg, #eee, #f7f7f7, #eee) !important;
}
'''

if "LIGHT LUXURY THEME + NEW COMPONENTS" not in css:
    css += OVERRIDE

CSS.write_text(css, encoding="utf-8")
print("CSS updated:", len(css))

# ---------- HTML transforms ----------
html = HTML.read_text(encoding="utf-8")

# Nav links
old_nav = '''      <ul class="nav-links">
        <li><a href="#home" class="nav-link active" data-nav>Home</a></li>
        <li><a href="#categories" class="nav-link" data-nav>Categories</a></li>
        <li><a href="#streetwear-collection" class="nav-link" data-nav>Collections</a></li>
        <li><a href="#new-arrivals" class="nav-link" data-nav>New Arrivals</a></li>
        <li><a href="#bestsellers" class="nav-link" data-nav>Best Sellers</a></li>
        <li><a href="#contact" class="nav-link" data-nav>Contact</a></li>
      </ul>'''

new_nav = '''      <ul class="nav-links">
        <li><a href="#home" class="nav-link active" data-nav data-page="home">Home</a></li>
        <li><a href="#categories" class="nav-link" data-nav data-page="categories">Categories</a></li>
        <li><a href="#collections" class="nav-link" data-nav data-page="collections">Collections</a></li>
        <li><a href="#about" class="nav-link" data-nav data-page="about">About</a></li>
      </ul>'''

if old_nav not in html:
    raise SystemExit("Nav block not found")
html = html.replace(old_nav, new_nav)

html = html.replace(
    '<a href="#checkout" class="nav-icon-btn cart-toggle" id="cart-toggle" aria-label="Go to checkout">',
    '<button type="button" class="nav-icon-btn cart-toggle" id="cart-toggle" aria-label="Open shopping cart">',
)
html = html.replace(
    '''          <span class="cart-count" id="cart-count" aria-hidden="true">0</span>
        </a>''',
    '''          <span class="cart-count" id="cart-count" aria-hidden="true">0</span>
        </button>''',
)

html = html.replace(
    '<a href="#premium-collection-title" class="nav-cta">Shop Now</a>',
    '<a href="#collections" class="nav-cta" data-nav data-page="collections">Shop Now</a>',
)

html = html.replace('<a class="skip-link" href="#home">Skip to content</a>',
                    '<a class="skip-link" href="#page-home">Skip to content</a>')

# Hero CTAs -> page nav
html = html.replace(
    '<a href="#streetwear-collection" class="btn btn-primary">Shop Collection</a>',
    '<a href="#collections" class="btn btn-primary" data-nav data-page="collections">Shop Collection</a>',
)
html = html.replace(
    '<a href="#new-arrivals" class="btn btn-secondary">New Arrivals</a>',
    '<a href="#collections" class="btn btn-secondary" data-nav data-page="collections">Explore Styles</a>',
)

# Remove scroll indicator
html = re.sub(
    r'\s*<a href="#categories" class="scroll-indicator"[\s\S]*?</a>\s*',
    "\n",
    html,
    count=1,
)

# Remove action button groups from product cards
html = re.sub(
    r'\s*<div class="streetwear-actions">[\s\S]*?</div>\s*(?=</div>\s*</li>)',
    "\n            </div>\n",
    html,
)
html = re.sub(
    r'\s*<div class="bs-actions">[\s\S]*?</div>\s*(?=</div>\s*</li>)',
    "\n            </div>\n",
    html,
)
html = re.sub(
    r'\s*<a href="#" class="btn btn-primary">View Product</a>\s*',
    "\n",
    html,
)
html = re.sub(
    r'\s*<button type="button" class="btn btn-outline js-view-details">View Details</button>\s*',
    "\n",
    html,
)

# Make product cards clickable (add class + role)
for cls in ("streetwear-card", "bestseller-card", "premium-card", "product-card"):
    html = html.replace(
        f'class="{cls}"',
        f'class="{cls} is-product-clickable" tabindex="0" role="button" aria-label="View product details"',
    )

# Wrap pages: insert after <main>
html = html.replace(
    "  <main>\n",
    '  <main>\n    <div class="page is-active" id="page-home" data-page-panel="home">\n',
    1,
)

# Close home page before categories, open categories
html = html.replace(
    '    <!-- Shop by Category -->\n    <section class="categories reveal" id="categories"',
    '''    </div><!-- /page-home -->

    <div class="page" id="page-categories" data-page-panel="categories" hidden>
    <!-- Shop by Category -->
    <section class="categories reveal" id="categories"''',
    1,
)

# Close categories before streetwear, open collections
html = html.replace(
    '    <!-- Featured Collections — Premium Streetwear -->\n    <section class="streetwear-collection reveal" id="streetwear-collection"',
    '''    </div><!-- /page-categories -->

    <div class="page" id="page-collections" data-page-panel="collections" hidden>
    <!-- Featured Collections — Premium Streetwear -->
    <section class="streetwear-collection reveal" id="streetwear-collection"''',
    1,
)

# Find end of contact section / before </main> to close collections and add about + keep checkout outside pages carefully
# Structure desired:
# page-home: hero
# page-categories: categories
# page-collections: streetwear through faq (not checkout/contact)
# page-about: new about (includes contact info)
# checkout stays as separate page panel

# Close collections before checkout, then checkout as own page, then about page
# Currently order: ... faq, checkout, contact, </main>

html = html.replace(
    '    <!-- Checkout / Payment -->\n    <section class="checkout reveal" id="checkout"',
    '''    </div><!-- /page-collections -->

    <div class="page" id="page-checkout" data-page-panel="checkout" hidden>
    <!-- Checkout / Payment -->
    <section class="checkout reveal" id="checkout"''',
    1,
)

# Replace contact section with about page that includes contact, close checkout page before it
contact_start = html.find('    <!-- Contact -->\n    <section class="contact reveal" id="contact"')
if contact_start < 0:
    contact_start = html.find('<section class="contact reveal" id="contact"')
main_end = html.find("  </main>")
if contact_start < 0 or main_end < 0:
    raise SystemExit("Could not locate contact/main end")

about_page = r'''    </div><!-- /page-checkout -->

    <div class="page" id="page-about" data-page-panel="about" hidden>
      <section class="about-page" id="about" aria-label="About Teeash Apparel">
        <div class="about-hero">
          <img src="https://images.unsplash.com/photo-1558171813-4c088753af8f?auto=format&fit=crop&w=1600&q=80" alt="Teeash Apparel brand story">
          <div class="about-hero-overlay" aria-hidden="true"></div>
          <div class="about-hero-content">
            <p class="section-eyebrow" style="color:#93C5FD">Our Story</p>
            <h1>Modern fashion with lasting confidence.</h1>
            <p>Teeash Apparel crafts premium men’s essentials for everyday style — refined fits, quality fabrics, and a clean contemporary aesthetic.</p>
          </div>
        </div>

        <div class="about-inner">
          <div class="about-story">
            <div>
              <p class="section-eyebrow">Brand Story</p>
              <h2>Designed for the modern man.</h2>
              <p>Born from a love of clean silhouettes and elevated streetwear, Teeash brings international fashion standards to everyday wardrobes. Every piece is curated for comfort, durability, and effortless style.</p>
              <p style="margin-top:0.9rem">Our mission is simple: make premium fashion accessible, wearable, and consistently refined — from first look to long-term favorite.</p>
            </div>
            <img src="https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?auto=format&fit=crop&w=900&h=1100&q=80" alt="Premium Teeash apparel collection">
          </div>

          <p class="section-eyebrow">Why Teeash</p>
          <h2>What we stand for</h2>
          <div class="about-grid">
            <article class="about-feature-card">
              <h3>Premium Quality</h3>
              <p>Carefully selected fabrics and precise stitching for pieces that look sharp and feel better wear after wear.</p>
            </article>
            <article class="about-feature-card">
              <h3>Fast Delivery</h3>
              <p>Orders move quickly from our studio to your door — with reliable tracking and easy updates.</p>
            </article>
            <article class="about-feature-card">
              <h3>Customer Satisfaction</h3>
              <p>Friendly support, easy exchanges, and a fit-focused experience designed around you.</p>
            </article>
            <article class="about-feature-card">
              <h3>Modern Fashion</h3>
              <p>Minimal, athletic, and street-ready styles inspired by global fashion capitals.</p>
            </article>
            <article class="about-feature-card">
              <h3>Our Mission</h3>
              <p>To elevate everyday menswear with timeless design, honest quality, and confident simplicity.</p>
            </article>
            <article class="about-feature-card">
              <h3>Thoughtful Details</h3>
              <p>From soft handfeel cotton to refined finishing, every detail is intentional.</p>
            </article>
          </div>

          <div class="about-contact-panel" id="contact">
            <div>
              <p class="section-eyebrow">Contact</p>
              <h2>Let’s talk style.</h2>
              <p>Reach out for orders, collaborations, or styling advice. We’re here to help you build a wardrobe that feels premium every day.</p>
              <p style="margin-top:1rem"><strong>Email:</strong> contact@teeashapparel.com</p>
              <p><strong>Phone:</strong> +92 XXX XXXXXXX</p>
              <p><strong>Location:</strong> Karachi, Pakistan</p>
            </div>
            <div>
              <h3 style="margin-bottom:0.4rem">Follow Teeash</h3>
              <p style="color:var(--color-muted)">Stay inspired with new drops and styling ideas.</p>
              <ul class="about-social" aria-label="Social media">
                <li><a href="https://www.facebook.com/" target="_blank" rel="noopener noreferrer" aria-label="Facebook">f</a></li>
                <li><a href="https://www.instagram.com/" target="_blank" rel="noopener noreferrer" aria-label="Instagram">in</a></li>
                <li><a href="https://wa.me/" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">wa</a></li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </div><!-- /page-about -->

'''

# Remove old about + brand-story? Keep brand story inside collections.
# Remove only the contact section (replaced by about page contact)
# Find contact section end - it's before </main>
contact_section = html[contact_start:main_end]
# Ensure we close checkout page - contact_start should be after checkout section
html = html[:contact_start] + about_page + html[main_end:]

# Update modal body for qty / buy now / related
old_modal_btn = '''          <button type="button" class="btn btn-primary js-add-to-cart" id="product-modal-cart">Add to Cart</button>
          <p class="product-modal-note">Select your size and color, then continue to checkout.</p>
        </div>
      </div>
    </div>
  </div>'''

new_modal_btn = '''          <div class="product-modal-group">
            <p class="product-modal-label">Quantity</p>
            <div class="product-modal-qty" id="product-modal-qty">
              <button type="button" id="qty-minus" aria-label="Decrease quantity">−</button>
              <span id="product-modal-qty-value">1</span>
              <button type="button" id="qty-plus" aria-label="Increase quantity">+</button>
            </div>
          </div>

          <div class="product-modal-actions">
            <button type="button" class="btn btn-primary js-add-to-cart" id="product-modal-cart">Add to Cart</button>
            <button type="button" class="btn btn-outline" id="product-modal-buy">Buy Now</button>
          </div>
          <p class="product-modal-note">Select size and color, then add to cart or buy now.</p>

          <div class="product-modal-related" id="product-modal-related">
            <h3>Related Products</h3>
            <div class="related-grid" id="related-products"></div>
          </div>
        </div>
      </div>
    </div>
  </div>'''

if old_modal_btn not in html:
    raise SystemExit("Modal button block not found")
html = html.replace(old_modal_btn, new_modal_btn)

# Insert cart drawer before cart toast
drawer = r'''
  <!-- Slide-in shopping cart drawer -->
  <div class="cart-drawer" id="cart-drawer" hidden aria-hidden="true">
    <div class="cart-drawer-backdrop" data-close-drawer></div>
    <aside class="cart-drawer-panel" role="dialog" aria-modal="true" aria-labelledby="cart-drawer-title">
      <div class="cart-drawer-header">
        <h2 id="cart-drawer-title">Your Cart</h2>
        <button type="button" class="cart-drawer-close" data-close-drawer aria-label="Close cart">&times;</button>
      </div>
      <div class="cart-drawer-body">
        <p class="cart-drawer-empty" id="cart-drawer-empty">Your cart is empty.</p>
        <ul class="cart-drawer-items" id="cart-drawer-items"></ul>
      </div>
      <div class="cart-drawer-footer">
        <div class="cart-totals-row"><span>Subtotal</span><strong id="cart-subtotal">$0.00</strong></div>
        <div class="cart-totals-row"><span>Shipping</span><strong id="cart-shipping">$0.00</strong></div>
        <div class="cart-totals-row total"><span>Total</span><strong id="cart-drawer-total">$0.00</strong></div>
        <div class="cart-drawer-actions">
          <button type="button" class="btn btn-primary" id="cart-checkout-btn">Checkout</button>
          <button type="button" class="btn btn-outline" id="cart-continue-btn">Continue Shopping</button>
        </div>
      </div>
    </aside>
  </div>

'''

html = html.replace(
    '  <div class="cart-toast" id="cart-toast"',
    drawer + '  <div class="cart-toast" id="cart-toast"',
    1,
)

html = html.replace(
    '<a href="#checkout" class="cart-toast-link">View Checkout</a>',
    '<button type="button" class="cart-toast-link" id="cart-toast-open">View Cart</button>',
)

# Footer links to page nav
html = html.replace('<a href="#home" class="footer-logo">Teeash Apparel</a>',
                    '<a href="#home" class="footer-logo" data-nav data-page="home">Teeash Apparel</a>')
html = html.replace('<li><a href="#categories">Categories</a></li>',
                    '<li><a href="#categories" data-nav data-page="categories">Categories</a></li>')
html = html.replace('<li><a href="#streetwear-collection">Featured Collections</a></li>',
                    '<li><a href="#collections" data-nav data-page="collections">Collections</a></li>')
html = html.replace('<li><a href="#new-arrivals">New Arrivals</a></li>',
                    '<li><a href="#collections" data-nav data-page="collections">New Arrivals</a></li>')
html = html.replace('<li><a href="#bestsellers">Best Sellers</a></li>',
                    '<li><a href="#collections" data-nav data-page="collections">Best Sellers</a></li>')
html = html.replace('<li><a href="#contact">Contact Us</a></li>',
                    '<li><a href="#about" data-nav data-page="about">About &amp; Contact</a></li>')

HTML.write_text(html, encoding="utf-8")
print("HTML updated:", len(html))
print("Done transform stage 1")
