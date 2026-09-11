export function initNavbar() {
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const menuClose = document.querySelector("[data-menu-close]");
  const siteMenu = document.querySelector("[data-site-menu]");
  const menuOverlay = document.querySelector("[data-menu-overlay]");

  if (!menuToggle || !siteMenu || !menuOverlay) return;

  const menuLinks = siteMenu.querySelectorAll("a");

  function setMenuState(isOpen) {
    menuToggle.setAttribute("aria-expanded", String(isOpen));
    menuToggle.setAttribute("aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");
    siteMenu.setAttribute("aria-hidden", String(!isOpen));
    siteMenu.classList.toggle("translate-x-full", !isOpen);
    siteMenu.classList.toggle("translate-x-0", isOpen);
    menuOverlay.classList.toggle("pointer-events-none", !isOpen);
    menuOverlay.classList.toggle("opacity-0", !isOpen);
    menuOverlay.classList.toggle("pointer-events-auto", isOpen);
    menuOverlay.classList.toggle("opacity-100", isOpen);
    document.body.classList.toggle("overflow-hidden", isOpen);
  }

  menuToggle.addEventListener("click", () => {
    const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
    setMenuState(!isOpen);
  });

  menuOverlay.addEventListener("click", () => setMenuState(false));
  menuClose?.addEventListener("click", () => setMenuState(false));
  menuLinks.forEach((link) => link.addEventListener("click", () => setMenuState(false)));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setMenuState(false);
  });
}
