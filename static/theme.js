(() => {
  const STORAGE_KEY = "sms-theme";

  const getStoredTheme = () => {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch {
      return null;
    }
  };

  const storeTheme = (theme) => {
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch {
      // ignore storage write issues
    }
  };

  const preferredTheme = () => {
    const storedTheme = getStoredTheme();
    if (storedTheme === "light" || storedTheme === "dark") {
      return storedTheme;
    }
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  };

  const applyTheme = (theme) => {
    document.documentElement.setAttribute("data-theme", theme);
    const toggles = document.querySelectorAll("[data-theme-toggle]");
    toggles.forEach((toggleButton) => {
      const icon = toggleButton.querySelector("i");
      const label = toggleButton.querySelector("span");
      toggleButton.setAttribute(
        "aria-label",
        theme === "dark" ? "Switch to light mode" : "Switch to dark mode",
      );
      if (icon) {
        icon.className =
          theme === "dark" ? "bi bi-sun-fill" : "bi bi-moon-stars-fill";
      }
      if (label) {
        label.textContent = theme === "dark" ? "Light" : "Dark";
      }
    });
  };

  const initTheme = () => {
    const theme = preferredTheme();
    applyTheme(theme);

    document.querySelectorAll("[data-theme-toggle]").forEach((toggleButton) => {
      toggleButton.addEventListener("click", () => {
        const currentTheme =
          document.documentElement.getAttribute("data-theme") || "light";
        const nextTheme = currentTheme === "dark" ? "light" : "dark";
        applyTheme(nextTheme);
        storeTheme(nextTheme);
      });
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initTheme);
  } else {
    initTheme();
  }
})();
