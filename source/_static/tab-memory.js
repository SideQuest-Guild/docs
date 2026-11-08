// Makes a reader's synced-tab pick (OS, installer, io, ...) follow them across
// pages *and* across visits.
//
// sphinx-design's own sd_tabs.js already keeps same-group tabs in sync on one
// page, and remembers the pick for the rest of that browser tab in
// sessionStorage, under the key `sphinx-design-tab-id-<group>`. It reads that
// key on DOMContentLoaded, and a `?group=key` URL param always wins over it.
//
// sessionStorage does not survive a new tab or a new visit, so without this
// script the pick resets each time. This script runs before DOMContentLoaded
// (plain <script>, no `defer`/`type=module`), so it can seed sessionStorage
// from localStorage first:
//
// 1. On load, copy each `sphinx-design-tab-id-*` key from localStorage into
//    sessionStorage, so the latest pick made in any browser tab wins. This
//    never overrides a `?group=key` URL param: sd_tabs.js applies that after
//    DOMContentLoaded, once it has already read whatever is in sessionStorage.
// 2. On every click of a tab label, save the pick to localStorage too, so the
//    next page and the next visit start from it.
//
// Storage can throw (private browsing, storage turned off); then the page
// just behaves like plain sphinx-design.
(() => {
  const PREFIX = "sphinx-design-tab-id-";

  try {
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(PREFIX)) {
        sessionStorage.setItem(key, localStorage.getItem(key));
      }
    }
  } catch {
    return;
  }

  document.addEventListener("click", (event) => {
    if (!(event.target instanceof Element)) {
      return;
    }
    const label = event.target.closest(".sd-tab-label[data-sync-group]");
    const group = label?.dataset.syncGroup;
    const id = label?.dataset.syncId;
    if (group && id) {
      try {
        localStorage.setItem(PREFIX + group, id);
      } catch {
        // Storage refused: the pick still holds for this browser tab.
      }
    }
  });
})();
