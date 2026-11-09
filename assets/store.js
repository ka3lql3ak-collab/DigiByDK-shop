// Checkout links. Paste the product link from Payhip (or Gumroad / Stripe) between the quotes.
// Leave it empty ("") until the checkout is ready; the button then shows a "coming soon" note instead.
const CHECKOUT = {
  glowup: "",
};

document.querySelectorAll("[data-product]").forEach((btn) => {
  const url = CHECKOUT[btn.dataset.product];
  if (url) {
    btn.href = url;
    btn.target = "_blank";
    btn.rel = "noopener";
  } else {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const msg = document.getElementById("buy-msg");
      if (msg) msg.hidden = false;
    });
  }
});
