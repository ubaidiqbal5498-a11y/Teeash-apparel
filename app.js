/* Teeash Apparel — app interactions (routing, modal, cart drawer) */
(function () {
  "use strict";

  /* ---------- Hero media ---------- */
  (function initHero() {
    var heroBg = document.getElementById("hero-bg");
    var video = document.querySelector(".hero-video");
    if (!heroBg || !video) return;

    function tryPlay() {
      heroBg.classList.add("is-video-ready");
      heroBg.classList.remove("is-fallback");
      var playPromise = video.play();
      if (playPromise && playPromise.catch) {
        playPromise.catch(function () {
          /* Autoplay may be blocked; muted + playsinline usually succeeds */
        });
      }
    }

    video.addEventListener("loadeddata", tryPlay);
    video.addEventListener("canplay", tryPlay);
    if (video.readyState >= 2) tryPlay();
    video.load();
  })();

  /* ---------- Page routing (no scroll navigation) ---------- */
  var header = document.getElementById("site-header");
  var toggle = document.getElementById("nav-toggle");
  var pages = {
    home: document.getElementById("page-home"),
    categories: document.getElementById("page-categories"),
    collections: document.getElementById("page-collections"),
    about: document.getElementById("page-about"),
    checkout: document.getElementById("page-checkout")
  };

  function closeMobileMenu() {
    if (!header || !toggle) return;
    header.classList.remove("is-menu-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open menu");
  }

  function showPage(name, options) {
    options = options || {};
    if (!pages[name]) name = "home";

    Object.keys(pages).forEach(function (key) {
      var panel = pages[key];
      if (!panel) return;
      var active = key === name;
      panel.classList.toggle("is-active", active);
      panel.hidden = !active;
      if (active) {
        panel.querySelectorAll(".reveal, .streetwear-card, .premium-card, .product-card, .bestseller-card").forEach(function (el) {
          el.classList.add("is-visible");
        });
      }
    });

    document.querySelectorAll("[data-page]").forEach(function (link) {
      link.classList.toggle("active", link.getAttribute("data-page") === name);
    });

    if (!options.keepScroll) {
      window.scrollTo(0, 0);
    }
    closeMobileMenu();

    if (name === "checkout") {
      var checkoutSection = document.getElementById("checkout");
      if (checkoutSection) {
        checkoutSection.hidden = false;
        checkoutSection.classList.add("is-visible", "is-checkout-open");
      }
    }

    try {
      history.replaceState({ page: name }, "", "#" + name);
    } catch (e) { /* ignore */ }
  }

  window.TeeashShowPage = showPage;

  document.querySelectorAll("[data-page]").forEach(function (link) {
    link.addEventListener("click", function (event) {
      var page = link.getAttribute("data-page");
      if (!page) return;
      event.preventDefault();
      showPage(page);
      var targetId = link.getAttribute("data-scroll-target");
      if (targetId) {
        window.setTimeout(function () {
          var el = document.getElementById(targetId);
          if (el) {
            var offset = header ? header.offsetHeight + 12 : 72;
            var top = el.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top: Math.max(0, top), behavior: "smooth" });
          }
        }, 60);
      }
    });
  });

  document.querySelectorAll(".shop-anchors a").forEach(function (link) {
    link.addEventListener("click", function (event) {
      var href = link.getAttribute("href") || "";
      if (href.charAt(0) !== "#") return;
      event.preventDefault();
      var el = document.getElementById(href.slice(1));
      if (!el) return;
      var offset = header ? header.offsetHeight + 12 : 72;
      var top = el.getBoundingClientRect().top + window.pageYOffset - offset;
      window.scrollTo({ top: Math.max(0, top), behavior: "smooth" });
    });
  });

  if (header) {
    function updateScrollState() {
      header.classList.toggle("is-scrolled", window.scrollY > 24);
    }
    updateScrollState();
    window.addEventListener("scroll", updateScrollState, { passive: true });
  }

  if (toggle && header) {
    toggle.addEventListener("click", function () {
      var isOpen = header.classList.toggle("is-menu-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      toggle.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
    });
  }

  /* Search */
  (function initSearch() {
    var searchToggle = document.getElementById("search-toggle");
    var searchForm = document.getElementById("site-search");
    var searchInput = document.getElementById("site-search-input");
    if (!searchToggle || !searchForm || !searchInput) return;

    searchToggle.addEventListener("click", function () {
      var isOpen = !searchForm.hidden;
      searchForm.hidden = isOpen;
      searchToggle.setAttribute("aria-expanded", isOpen ? "false" : "true");
      if (!isOpen) searchInput.focus();
    });

    searchForm.addEventListener("submit", function (event) {
      event.preventDefault();
      var query = searchInput.value.trim().toLowerCase();
      if (!query) return;

      showPage("collections");
          var titles = document.querySelectorAll(
            ".streetwear-info h3, .bs-info h3, .premium-info h3, .product-info h3, .catalog-info h3"
          );
      var match = null;
      titles.forEach(function (title) {
        if (!match && title.textContent.toLowerCase().indexOf(query) !== -1) {
          match = title.closest("li") || title;
        }
      });
      searchForm.hidden = true;
      searchToggle.setAttribute("aria-expanded", "false");
      if (match) {
        window.setTimeout(function () {
          match.scrollIntoView({ behavior: "smooth", block: "center" });
          if (match.classList.contains("is-product-clickable")) {
            match.focus();
          }
        }, 80);
      }
    });
  })();

  /* Reveal / counters */
  (function initReveal() {
    function revealAll(selector) {
      document.querySelectorAll(selector).forEach(function (el) {
        el.classList.add("is-visible");
      });
    }
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(
        function (entries, obs) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              obs.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.12 }
      );
      document.querySelectorAll(".reveal, .streetwear-card, .premium-card, .product-card, .bestseller-card").forEach(function (el, index) {
        if (!el.classList.contains("bestseller-card") && !el.classList.contains("streetwear-card")) {
          el.classList.add("reveal-card");
        }
        el.style.transitionDelay = (index % 8) * 0.05 + "s";
        observer.observe(el);
      });
    } else {
      revealAll(".reveal, .streetwear-card, .premium-card, .product-card, .bestseller-card");
    }

    document.querySelectorAll(".bestseller-card").forEach(function (card) {
      card.querySelectorAll(".bs-size").forEach(function (btn) {
        btn.addEventListener("click", function (event) {
          event.stopPropagation();
          card.querySelectorAll(".bs-size").forEach(function (b) { b.classList.remove("is-active"); });
          btn.classList.add("is-active");
        });
      });
      card.querySelectorAll(".bs-swatch").forEach(function (swatch) {
        swatch.addEventListener("click", function (event) {
          event.stopPropagation();
          card.querySelectorAll(".bs-swatch").forEach(function (s) { s.classList.remove("is-active"); });
          swatch.classList.add("is-active");
        });
      });
    });

    function animateCounter(el) {
      var target = parseFloat(el.getAttribute("data-target"), 10);
      var decimals = parseInt(el.getAttribute("data-decimals") || "0", 10);
      var suffix = el.getAttribute("data-suffix") || "";
      var start = null;
      function formatValue(value) {
        return (decimals > 0 ? value.toFixed(decimals) : Math.floor(value).toLocaleString()) + suffix;
      }
      function step(ts) {
        if (!start) start = ts;
        var progress = Math.min((ts - start) / 1600, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = formatValue(target * eased);
        if (progress < 1) window.requestAnimationFrame(step);
        else el.textContent = formatValue(target);
      }
      window.requestAnimationFrame(step);
    }

    var counters = document.querySelectorAll(".counter");
    var statsBlock = document.querySelector(".brand-stats");
    if (counters.length && statsBlock && "IntersectionObserver" in window) {
      var started = false;
      var statsObserver = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && !started) {
            started = true;
            counters.forEach(animateCounter);
            obs.unobserve(entry.target);
          }
        });
      }, { threshold: 0.35 });
      statsObserver.observe(statsBlock);
    }
  })();

  /* ---------- Product modal ---------- */
  var modal = document.getElementById("product-modal");
  var modalQty = 1;
  var currentProduct = null;
  var defaultImage = "assets/hero/male-tee.jpg";
  var galleryExtras = ["assets/hero/male-tee.jpg", "assets/hero/male-streetwear.jpg"];
  var sizes = ["S", "M", "L", "XL"];
  var colors = [
    { name: "Black", value: "#0B0B0B" },
    { name: "White", value: "#FFFFFF" },
    { name: "Olive", value: "#556B2F" },
    { name: "Navy", value: "#1B2A4A" },
    { name: "Grey", value: "#6B7280" },
    { name: "Beige", value: "#D6C3A8" }
  ];
  var lockedScrollY = 0;

  function textOf(root, selector) {
    var node = root ? root.querySelector(selector) : null;
    return node ? node.textContent.trim() : "";
  }

  function getProductFromCard(card) {
    if (!card) return null;
    var img = card.querySelector("img");
    var labelNode =
      card.querySelector(".product-label") ||
      card.querySelector(".bs-badge") ||
      card.querySelector(".premium-badge");
    var activeSize = card.querySelector(".bs-size.is-active");
    var activeColor = card.querySelector(".bs-swatch.is-active");
    return {
      name: textOf(card, "h3") || "Teeash Product",
      price:
        textOf(card, ".bs-price") ||
        textOf(card, ".streetwear-price") ||
        textOf(card, ".product-price") ||
        textOf(card, ".premium-price") ||
        "",
      description:
        textOf(card, ".bs-desc") ||
        textOf(card, ".streetwear-desc") ||
        textOf(card, ".product-desc") ||
        textOf(card, ".premium-category") ||
        "Premium Teeash Apparel piece.",
      image: img && img.getAttribute("src") ? img.getAttribute("src") : defaultImage,
      alt: img && img.getAttribute("alt") ? img.getAttribute("alt") : "Product image",
      label: labelNode ? labelNode.textContent.trim() : "",
      selectedSize: activeSize ? activeSize.textContent.trim() : "M",
      selectedColor: activeColor
        ? activeColor.getAttribute("title") || activeColor.getAttribute("aria-label") || "Black"
        : "Black",
      material: "Premium cotton blend with a soft handfeel, durable stitching, and a refined everyday finish."
    };
  }

  function renderGallery(product) {
    var imageEl = document.getElementById("product-modal-image");
    var thumbsEl = document.getElementById("product-modal-thumbs");
    if (!thumbsEl || !imageEl) return;
    var images = [product.image].concat(galleryExtras.filter(function (src) { return src !== product.image; }));
    thumbsEl.innerHTML = "";
    images.forEach(function (src, index) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "product-thumb" + (index === 0 ? " is-active" : "");
      btn.innerHTML = '<img src="' + src + '" alt="">';
      btn.addEventListener("click", function () {
        imageEl.src = src;
        thumbsEl.querySelectorAll(".product-thumb").forEach(function (el) { el.classList.remove("is-active"); });
        btn.classList.add("is-active");
      });
      thumbsEl.appendChild(btn);
    });
  }

  function renderOptions(product) {
    var sizesEl = document.getElementById("product-modal-sizes");
    var colorsEl = document.getElementById("product-modal-colors");
    sizesEl.innerHTML = "";
    sizes.forEach(function (size) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "bs-size" + (size === product.selectedSize ? " is-active" : "");
      btn.textContent = size;
      btn.addEventListener("click", function () {
        sizesEl.querySelectorAll(".bs-size").forEach(function (el) { el.classList.remove("is-active"); });
        btn.classList.add("is-active");
      });
      sizesEl.appendChild(btn);
    });

    colorsEl.innerHTML = "";
    colors.forEach(function (color) {
      var swatch = document.createElement("button");
      swatch.type = "button";
      swatch.className = "bs-swatch" + (color.name === product.selectedColor ? " is-active" : "");
      swatch.style.setProperty("--swatch", color.value);
      swatch.title = color.name;
      swatch.setAttribute("aria-label", color.name);
      swatch.addEventListener("click", function () {
        colorsEl.querySelectorAll(".bs-swatch").forEach(function (el) { el.classList.remove("is-active"); });
        swatch.classList.add("is-active");
      });
      colorsEl.appendChild(swatch);
    });
  }

  function renderRelated(currentName) {
    var wrap = document.getElementById("related-products");
    if (!wrap) return;
    wrap.innerHTML = "";
    var cards = Array.prototype.slice.call(document.querySelectorAll(".is-product-clickable"));
    var related = cards.filter(function (card) {
      return textOf(card, "h3") !== currentName;
    }).slice(0, 3);

    related.forEach(function (card) {
      var img = card.querySelector("img");
      var name = textOf(card, "h3");
      var el = document.createElement("article");
      el.className = "related-card";
      el.innerHTML =
        '<img src="' + (img ? img.src : defaultImage) + '" alt="' + name.replace(/"/g, "&quot;") + '">' +
        "<p>" + name + "</p>";
      el.addEventListener("click", function () {
        openModal(getProductFromCard(card));
      });
      wrap.appendChild(el);
    });
  }

  function setQty(value) {
    modalQty = Math.max(1, value);
    var qtyEl = document.getElementById("product-modal-qty-value");
    if (qtyEl) qtyEl.textContent = String(modalQty);
  }

  function openModal(product) {
    if (!modal || !product) return;
    currentProduct = product;
    setQty(1);
    document.getElementById("product-modal-title").textContent = product.name;
    document.getElementById("product-modal-price").textContent = product.price;
    document.getElementById("product-modal-desc").textContent = product.description;
    var imageEl = document.getElementById("product-modal-image");
    imageEl.src = product.image;
    imageEl.alt = product.alt;

    var badgeEl = document.getElementById("product-modal-badge");
    if (badgeEl) {
      badgeEl.hidden = !product.label;
      badgeEl.textContent = product.label || "";
    }
    var fabricEl = document.getElementById("product-modal-fabric");
    if (fabricEl) fabricEl.textContent = product.material;
    var deliveryEl = document.getElementById("product-modal-delivery");
    if (deliveryEl) {
      deliveryEl.textContent = "Orders ship in 24 hours. Standard delivery 3–5 business days. Easy exchanges within 14 days.";
    }

    renderGallery(product);
    renderOptions(product);
    renderRelated(product.name);

    lockedScrollY = window.scrollY || 0;
    modal.hidden = false;
    document.body.classList.add("modal-open");
    document.body.style.top = "-" + lockedScrollY + "px";
    void modal.offsetWidth;
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-open");
    document.body.style.top = "";
    window.scrollTo(0, lockedScrollY);
    window.setTimeout(function () {
      if (!modal.classList.contains("is-open")) modal.hidden = true;
    }, 300);
  }

  window.TeeashOpenProduct = openModal;
  window.TeeashCloseProduct = closeModal;

  document.querySelectorAll(".is-product-clickable").forEach(function (card) {
    card.addEventListener("click", function (event) {
      if (event.target.closest("a, button")) return;
      openModal(getProductFromCard(card));
    });
    card.addEventListener("keydown", function (event) {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openModal(getProductFromCard(card));
      }
    });
  });

  if (modal) {
    modal.querySelectorAll("[data-close-modal]").forEach(function (el) {
      el.addEventListener("click", closeModal);
    });
  }

  var qtyMinus = document.getElementById("qty-minus");
  var qtyPlus = document.getElementById("qty-plus");
  if (qtyMinus) qtyMinus.addEventListener("click", function () { setQty(modalQty - 1); });
  if (qtyPlus) qtyPlus.addEventListener("click", function () { setQty(modalQty + 1); });

  /* ---------- Cart drawer ---------- */
  var STORAGE_KEY = "teeash-cart";
  var cart = [];
  var drawer = document.getElementById("cart-drawer");
  var countEl = document.getElementById("cart-count");
  var drawerItems = document.getElementById("cart-drawer-items");
  var drawerEmpty = document.getElementById("cart-drawer-empty");
  var checkoutItems = document.getElementById("checkout-items");
  var checkoutEmpty = document.getElementById("checkout-empty");
  var checkoutTotal = document.getElementById("checkout-total");
  var checkoutForm = document.getElementById("checkout-form");
  var checkoutNote = document.getElementById("checkout-note");
  var SHIPPING_FLAT = 5;

  function parsePrice(text) {
    var value = parseFloat(String(text).replace(/[^0-9.]/g, ""), 10);
    return isNaN(value) ? 0 : value;
  }
  function formatMoney(amount) {
    return "$" + amount.toFixed(2);
  }
  function itemKey(item) {
    return [item.name, item.size || "", item.color || ""].join("|");
  }
  function loadCart() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      cart = raw ? JSON.parse(raw) : [];
      if (!Array.isArray(cart)) cart = [];
    } catch (e) {
      cart = [];
    }
  }
  function saveCart() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(cart)); } catch (e) { /* ignore */ }
  }
  function getCount() {
    return cart.reduce(function (sum, item) { return sum + item.quantity; }, 0);
  }
  function getSubtotal() {
    return cart.reduce(function (sum, item) { return sum + item.price * item.quantity; }, 0);
  }
  function getShipping() {
    return cart.length ? SHIPPING_FLAT : 0;
  }
  function getGrandTotal() {
    return getSubtotal() + getShipping();
  }

  function getActiveSize(root) {
    var el = root.querySelector(".bs-size.is-active, .product-modal-sizes .bs-size.is-active");
    return el ? el.textContent.trim() : "";
  }
  function getActiveColor(root) {
    var el = root.querySelector(".bs-swatch.is-active, .product-modal-colors .bs-swatch.is-active");
    if (!el) return "";
    return el.getAttribute("title") || el.getAttribute("aria-label") || "";
  }

  function getProductFromModal(qty) {
    if (!modal || !modal.classList.contains("is-open")) return null;
    var title = document.getElementById("product-modal-title");
    var priceNode = document.getElementById("product-modal-price");
    var image = document.getElementById("product-modal-image");
    var priceText = priceNode ? priceNode.textContent.trim() : "";
    return {
      name: title ? title.textContent.trim() : "Teeash Product",
      price: parsePrice(priceText),
      priceText: priceText || formatMoney(parsePrice(priceText)),
      image: image && image.getAttribute("src") ? image.getAttribute("src") : defaultImage,
      size: getActiveSize(modal),
      color: getActiveColor(modal),
      quantity: qty || 1
    };
  }

  function openDrawer() {
    if (!drawer) return;
    drawer.hidden = false;
    document.body.classList.add("drawer-open");
    void drawer.offsetWidth;
    drawer.classList.add("is-open");
    drawer.setAttribute("aria-hidden", "false");
  }

  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove("is-open");
    drawer.setAttribute("aria-hidden", "true");
    document.body.classList.remove("drawer-open");
    window.setTimeout(function () {
      if (!drawer.classList.contains("is-open")) drawer.hidden = true;
    }, 320);
  }

  function renderItemList(targetEl, forCheckout) {
    if (!targetEl) return;
    targetEl.innerHTML = "";
    cart.forEach(function (item, index) {
      var li = document.createElement("li");
      li.className = forCheckout ? "checkout-item" : "cart-drawer-item";
      var sizeLabel = item.size || "—";
      var colorLabel = item.color || "—";
      var lineTotal = item.price * item.quantity;
      if (forCheckout) {
        li.innerHTML =
          '<img class="checkout-item-image" src="' + item.image + '" alt="' + item.name.replace(/"/g, "&quot;") + '">' +
          '<div class="checkout-item-info">' +
            '<h4 class="checkout-item-name">' + item.name + "</h4>" +
            '<p class="checkout-item-meta">Color: ' + colorLabel + " · Size: " + sizeLabel + "</p>" +
            '<div class="checkout-item-row">' +
              '<div class="checkout-item-qty">' +
                '<button type="button" class="cart-qty-btn" data-qty-minus="' + index + '" aria-label="Decrease">−</button>' +
                "<span>" + item.quantity + "</span>" +
                '<button type="button" class="cart-qty-btn" data-qty-plus="' + index + '" aria-label="Increase">+</button>' +
              "</div>" +
              '<p class="checkout-item-total">' + formatMoney(lineTotal) + "</p>" +
            "</div>" +
            '<button type="button" class="cart-item-remove" data-remove="' + index + '">Remove</button>' +
          "</div>";
      } else {
        li.innerHTML =
          '<img src="' + item.image + '" alt="' + item.name.replace(/"/g, "&quot;") + '">' +
          "<div>" +
            "<h4>" + item.name + "</h4>" +
            '<p class="meta">Color: ' + colorLabel + " · Size: " + sizeLabel + "</p>" +
            '<div class="cart-drawer-item-row">' +
              '<div class="checkout-item-qty">' +
                '<button type="button" class="cart-qty-btn" data-qty-minus="' + index + '" aria-label="Decrease">−</button>' +
                "<span>" + item.quantity + "</span>" +
                '<button type="button" class="cart-qty-btn" data-qty-plus="' + index + '" aria-label="Increase">+</button>' +
              "</div>" +
              "<strong>" + formatMoney(lineTotal) + "</strong>" +
            "</div>" +
            '<button type="button" class="cart-item-remove" data-remove="' + index + '">Remove</button>' +
          "</div>";
      }
      targetEl.appendChild(li);
    });
  }

  function renderCart() {
    if (countEl) countEl.textContent = String(getCount());
    if (drawerEmpty) drawerEmpty.hidden = cart.length > 0;
    if (checkoutEmpty) checkoutEmpty.hidden = cart.length > 0;
    renderItemList(drawerItems, false);
    renderItemList(checkoutItems, true);

    var subtotal = getSubtotal();
    var shipping = getShipping();
    var total = getGrandTotal();
    var subEl = document.getElementById("cart-subtotal");
    var shipEl = document.getElementById("cart-shipping");
    var totalEl = document.getElementById("cart-drawer-total");
    if (subEl) subEl.textContent = formatMoney(subtotal);
    if (shipEl) shipEl.textContent = cart.length ? formatMoney(shipping) : "$0.00";
    if (totalEl) totalEl.textContent = formatMoney(total);
    if (checkoutTotal) checkoutTotal.textContent = formatMoney(total);
  }

  function addToCart(product) {
    if (!product || !product.name) return;
    var incoming = {
      name: product.name,
      price: product.price,
      priceText: product.priceText || formatMoney(product.price),
      image: product.image || defaultImage,
      size: product.size || "",
      color: product.color || "",
      quantity: product.quantity || 1
    };
    var key = itemKey(incoming);
    var existing = cart.find(function (item) { return itemKey(item) === key; });
    if (existing) existing.quantity += incoming.quantity;
    else cart.push(incoming);
    saveCart();
    renderCart();
  }

  function updateQuantity(index, delta) {
    if (!cart[index]) return;
    cart[index].quantity += delta;
    if (cart[index].quantity <= 0) cart.splice(index, 1);
    saveCart();
    renderCart();
  }
  function removeItem(index) {
    cart.splice(index, 1);
    saveCart();
    renderCart();
  }

  function flashToast(message) {
    var toast = document.getElementById("cart-toast");
    var toastText = document.getElementById("cart-toast-text");
    if (!toast || !toastText) return;
    toastText.textContent = message || "Added to cart";
    toast.hidden = false;
    toast.classList.add("is-visible");
    window.setTimeout(function () {
      toast.classList.remove("is-visible");
      window.setTimeout(function () {
        if (!toast.classList.contains("is-visible")) toast.hidden = true;
      }, 280);
    }, 2400);
  }

  function handleListClick(event) {
    var target = event.target;
    if (!(target instanceof Element)) return;
    if (target.hasAttribute("data-qty-plus")) {
      updateQuantity(parseInt(target.getAttribute("data-qty-plus"), 10), 1);
    } else if (target.hasAttribute("data-qty-minus")) {
      updateQuantity(parseInt(target.getAttribute("data-qty-minus"), 10), -1);
    } else if (target.hasAttribute("data-remove")) {
      removeItem(parseInt(target.getAttribute("data-remove"), 10));
    }
  }

  if (drawerItems) drawerItems.addEventListener("click", handleListClick);
  if (checkoutItems) checkoutItems.addEventListener("click", handleListClick);

  var addCartBtn = document.getElementById("product-modal-cart");
  if (addCartBtn) {
    addCartBtn.addEventListener("click", function (event) {
      event.preventDefault();
      var product = getProductFromModal(modalQty);
      if (!product) return;
      addToCart(product);
      closeModal();
      openDrawer();
      flashToast("Added to cart");
    });
  }

  var buyNowBtn = document.getElementById("product-modal-buy");
  if (buyNowBtn) {
    buyNowBtn.addEventListener("click", function (event) {
      event.preventDefault();
      var product = getProductFromModal(modalQty);
      if (!product) return;
      addToCart(product);
      closeModal();
      closeDrawer();
      showPage("checkout");
    });
  }

  var cartToggle = document.getElementById("cart-toggle");
  if (cartToggle) {
    cartToggle.addEventListener("click", function (event) {
      event.preventDefault();
      openDrawer();
    });
  }

  if (drawer) {
    drawer.querySelectorAll("[data-close-drawer]").forEach(function (el) {
      el.addEventListener("click", closeDrawer);
    });
  }

  var continueBtn = document.getElementById("cart-continue-btn");
  if (continueBtn) continueBtn.addEventListener("click", closeDrawer);

  var checkoutBtn = document.getElementById("cart-checkout-btn");
  if (checkoutBtn) {
    checkoutBtn.addEventListener("click", function () {
      closeDrawer();
      showPage("checkout");
    });
  }

  var toastOpen = document.getElementById("cart-toast-open");
  if (toastOpen) {
    toastOpen.addEventListener("click", function () {
      openDrawer();
    });
  }

  if (checkoutForm) {
    checkoutForm.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!cart.length) {
        if (checkoutNote) {
          checkoutNote.hidden = false;
          checkoutNote.textContent = "Please add a product before placing your order.";
        }
        return;
      }
      if (checkoutNote) {
        checkoutNote.hidden = false;
        checkoutNote.textContent = "Thank you. Your order has been received and is ready for payment processing.";
      }
      checkoutForm.reset();
      cart = [];
      saveCart();
      renderCart();
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    if (drawer && drawer.classList.contains("is-open")) closeDrawer();
    else if (modal && modal.classList.contains("is-open")) closeModal();
  });

  /* Image skeletons */
  document.querySelectorAll([
    ".streetwear-image-wrap",
    ".premium-image-wrap",
    ".bs-image-wrap",
    ".category-card",
    ".brand-story-media",
    ".about-media",
    ".about-hero",
    ".product-modal-media"
  ].join(",")).forEach(function (wrap) {
    var img = wrap.querySelector("img");
    if (!img) return;
    wrap.classList.add("media-skeleton");
    function markLoaded() { wrap.classList.add("is-loaded"); }
    if (img.complete && img.naturalWidth > 0) markLoaded();
    else {
      img.addEventListener("load", markLoaded);
      img.addEventListener("error", markLoaded);
    }
  });



  /* Signature Tee Lab showcase */
  (function initTeeLab() {
    var shirt = document.getElementById("tee-shirt");
    if (!shirt) return;
    var styleLabel = document.getElementById("tee-lab-style");
    var colorLabel = document.getElementById("tee-lab-color");
    var rec = document.getElementById("tee-lab-rec");
    var style = "oversized";
    var colorName = "Black";

    function updateRec() {
      var map = {
        oversized: "strong street silhouette",
        classic: "clean everyday essential",
        boxy: "modern drop-shoulder energy"
      };
      if (rec) {
        rec.textContent =
          "Recommended: " +
          style.charAt(0).toUpperCase() + style.slice(1) +
          " in " + colorName + " — " + (map[style] || "signature Teeash fit") + ".";
      }
      if (styleLabel) styleLabel.textContent = style.charAt(0).toUpperCase() + style.slice(1);
      if (colorLabel) colorLabel.textContent = colorName;
      shirt.setAttribute("data-fit", style);
    }

    document.querySelectorAll(".tee-pill").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".tee-pill").forEach(function (b) { b.classList.remove("is-active"); });
        btn.classList.add("is-active");
        style = btn.getAttribute("data-style") || "oversized";
        updateRec();
      });
    });

    document.querySelectorAll(".tee-swatch").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".tee-swatch").forEach(function (b) { b.classList.remove("is-active"); });
        btn.classList.add("is-active");
        var c = btn.getAttribute("data-color") || "#111827";
        colorName = btn.getAttribute("data-name") || "Black";
        shirt.style.setProperty("--tee-color", c);
        var mark = shirt.querySelector(".tee-mark");
        if (mark) {
          mark.style.color = (colorName === "Ivory") ? "rgba(17,24,39,0.28)" : "rgba(255,255,255,0.35)";
        }
        updateRec();
      });
    });

    shirt.style.setProperty("--tee-color", "#111827");
    updateRec();
  })();

  loadCart();
  renderCart();

  var initial = (location.hash || "#home").replace("#", "");
  if (!pages[initial]) initial = "home";
  showPage(initial, { keepScroll: true });
})();
