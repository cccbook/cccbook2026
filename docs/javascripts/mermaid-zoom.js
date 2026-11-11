(function () {
  "use strict";

  function currentScheme() {
    return document.body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "default";
  }

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose",
    theme: currentScheme(),
    flowchart: { useMaxWidth: true },
    sequence: { useMaxWidth: true },
    gantt: { useMaxWidth: true }
  });

  // mermaid.render() 不可併發呼叫（會互相衝突導致
  // "Cannot read properties of null" 錯誤），用佇列序列化。
  var mzQueue = [];
  var mzRunning = false;

  function mzSchedule(job) {
    mzQueue.push(job);
    if (!mzRunning) mzRunNext();
  }

  function mzRunNext() {
    var job = mzQueue.shift();
    if (!job) {
      mzRunning = false;
      return;
    }
    mzRunning = true;
    Promise.resolve()
      .then(job)
      .catch(function (e) {
        console.warn("mermaid job failed:", e);
      })
      .then(mzRunNext);
  }

  function mzApplyZoom(view, z) {
    var svg = view.querySelector(".mz-canvas svg");
    if (!svg) return;
    z = Math.min(8, Math.max(0.5, z));
    var cur = parseFloat(svg.style.zoom) || 1;
    // mermaid 的 svg 寬度是 100% / max-width 限制，CSS zoom 會被抵銷；
    // 先凍結基準寬度為 px，讓 zoom 真正改變視覺大小。
    if (svg.style.width === "") {
      var w = svg.getBoundingClientRect().width / cur;
      if (w > 0) svg.style.width = w + "px";
    }
    if (svg.dataset.mzMaxWidth === undefined) {
      svg.dataset.mzMaxWidth = svg.style.maxWidth || "";
    }
    svg.style.maxWidth = "none";
    svg.style.zoom = z;
  }

  function mzScale(view, factor) {
    var svg = view.querySelector(".mz-canvas svg");
    if (!svg) return;
    mzApplyZoom(view, (parseFloat(svg.style.zoom) || 1) * factor);
  }

  function mzReset(view) {
    var svg = view.querySelector(".mz-canvas svg");
    if (!svg) return;
    svg.style.zoom = 1;
    svg.style.maxWidth = svg.dataset.mzMaxWidth || "";
    svg.style.width = "";
  }

  function mzRender(view) {
    var srcEl = view.querySelector(".mz-src");
    var canvas = view.querySelector(".mz-canvas");
    if (!srcEl || !canvas) return;
    var source = srcEl.textContent;
    if (!source.trim()) return;

    // 已成功繪製且沒有待重繪（配色變更）→ 跳過
    if (view.dataset.mzState === "done" && !view.dataset.mzDirty) return;
    if (view.dataset.mzState === "rendering") {
      // 正在繪製中又收到重繪要求（例如配色切換）→ 繪完後再排一次
      view.dataset.mzDirty = "1";
      return;
    }
    view.dataset.mzState = "rendering";

    mzSchedule(function () {
      var dark = document.body.getAttribute("data-md-color-scheme") === "slate";
      mermaid.initialize({
        startOnLoad: false,
        securityLevel: "loose",
        theme: dark ? "dark" : "default",
        flowchart: { useMaxWidth: true },
        sequence: { useMaxWidth: true },
        gantt: { useMaxWidth: true }
      });
      return mermaid
        .render("mz-" + Math.random().toString(36).slice(2, 8), source)
        .then(function (result) {
          // 只移除舊圖與錯誤訊息，保留 .mz-src（重繪需要它）
          Array.prototype.slice.call(canvas.children).forEach(function (child) {
            if (child !== srcEl) child.remove();
          });
          var holder = document.createElement("div");
          holder.innerHTML = result.svg;
          var el = holder.firstElementChild;
          if (el) {
            el.style.zoom = 1;
            canvas.appendChild(el);
          }
          view.dataset.mzState = "done";
          view.dataset.mzTheme = dark ? "dark" : "default";
          if (view.dataset.mzDirty) {
            delete view.dataset.mzDirty;
            mzRender(view);
          }
        })
        .catch(function (err) {
          view.dataset.mzState = "done";
          var msg = err && err.message ? err.message : String(err);
          console.warn("mermaid render failed:", err);
          var pre = canvas.querySelector(".mz-error");
          if (!pre) {
            pre = document.createElement("pre");
            pre.classList.add("mz-error");
            canvas.appendChild(pre);
          }
          pre.textContent = "[mermaid 繪圖失敗] " + msg + "\n\n" + source;
          if (view.dataset.mzDirty) {
            delete view.dataset.mzDirty;
            mzRender(view);
          }
        });
    });
  }

  function mzInit(view) {
    if (view.dataset.mzInit) return;
    view.dataset.mzInit = "1";
    mzRender(view);

    // 事件委派：按鈕與滾輪縮放
    view.addEventListener("click", function (e) {
      var btn = e.target.closest ? e.target.closest(".mz-btn") : null;
      if (!btn || !view.contains(btn)) return;
      var action = btn.dataset.mz;
      if (action === "in") mzScale(view, 1.25);
      else if (action === "out") mzScale(view, 1 / 1.25);
      else mzReset(view);
    });

    var canvas = view.querySelector(".mz-canvas");
    if (canvas) {
      canvas.addEventListener("wheel", function (e) {
        if (!(e.ctrlKey || e.metaKey)) return;
        e.preventDefault();
        mzScale(view, e.deltaY < 0 ? 1.1 : 1 / 1.1);
      }, { passive: false });
    }
  }

  document$.subscribe(function () {
    document.querySelectorAll(".mz-view").forEach(mzInit);
  });

  // 只在配色真的切換時重繪（初始化時的屬性套用不觸發）
  var mzLastScheme = document.body.getAttribute("data-md-color-scheme");
  new MutationObserver(function () {
    var scheme = document.body.getAttribute("data-md-color-scheme");
    if (scheme === mzLastScheme) return;
    mzLastScheme = scheme;
    document.querySelectorAll(".mz-view").forEach(function (view) {
      view.dataset.mzDirty = "1";
      mzRender(view);
    });
  }).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
})();
