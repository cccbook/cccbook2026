mermaid.initialize({
  startOnLoad: false,
  securityLevel: "loose",
  flowchart: { useMaxWidth: true },
  sequence: { useMaxWidth: true },
  gantt: { useMaxWidth: true }
});

function mzScale(view, factor) {
  const canvas = view.querySelector(".mz-canvas");
  const svg = canvas.querySelector("svg");
  if (!svg) return;
  const z = Math.min(8, Math.max(0.5, (parseFloat(svg.style.zoom) || 1) * factor));
  svg.style.zoom = z;
}

function mzReset(view) {
  const svg = view.querySelector(".mz-canvas svg");
  if (svg) svg.style.zoom = 1;
}

function mzRender(view) {
  const src = view.querySelector(".mz-src");
  const canvas = view.querySelector(".mz-canvas");
  if (!src || !canvas) return;
  const dark = document.body.getAttribute("data-md-color-scheme") === "slate";
  mermaid.render("mz-" + Math.random().toString(36).slice(2, 8), src.textContent).then(
    ({ svg }) => {
      canvas.innerHTML = svg;
      canvas.querySelector("svg").style.zoom = 1;
    },
    (err) => {
      canvas.innerHTML = "";
      const pre = document.createElement("pre");
      pre.classList.add("mz-error");
      pre.textContent = src.textContent;
      canvas.appendChild(pre);
      console.warn("mermaid render failed:", err);
    }
  );
}

document$.subscribe(() => {
  document.querySelectorAll(".mz-view").forEach((view) => {
    if (view.dataset.mzInit) return;
    view.dataset.mzInit = "1";
    mzRender(view);

    view.querySelectorAll(".mz-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const action = btn.dataset.mz;
        if (action === "in") mzScale(view, 1.25);
        else if (action === "out") mzScale(view, 1 / 1.25);
        else mzReset(view);
      });
    });

    const canvas = view.querySelector(".mz-canvas");
    canvas.addEventListener("wheel", (e) => {
      if (!(e.ctrlKey || e.metaKey)) return;
      e.preventDefault();
      mzScale(view, e.deltaY < 0 ? 1.1 : 1 / 1.1);
    }, { passive: false });
  });
});

new MutationObserver(() => {
  document.querySelectorAll(".mz-view").forEach(mzRender);
}).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
