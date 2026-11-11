# 搜尋

<link rel="stylesheet" href="/cccbook2026/pagefind/pagefind-ui.css">
<script src="/cccbook2026/pagefind/pagefind-ui.js"></script>

<div id="pagefind-search"></div>

<script>
window.addEventListener('DOMContentLoaded', () => {
  new PagefindUI({
    element: '#pagefind-search',
    showSubResults: true,
    showImages: false,
    translations: {
      placeholder: '搜尋全站書籍內容…',
      clear_search: '清除',
      load_more: '載入更多結果',
      search_label: '搜尋本站',
      zero_results: '找不到「[SEARCH_TERM]」相關內容',
      many_results: '找到 [COUNT] 筆「[SEARCH_TERM]」結果',
      one_result: '找到 [COUNT] 筆「[SEARCH_TERM]」結果',
      searching: '正在搜尋「[SEARCH_TERM]」…'
    }
  });
});
</script>

!!! tip "快速鍵"

    按 <kbd>Ctrl</kbd>+<kbd>K</kbd>（macOS 為 <kbd>⌘</kbd>+<kbd>K</kbd>）也可跳到本頁搜尋。

## Google 全文檢索（備援）

若站內搜尋找不到，也可以用 Google 搜尋本站：

<!-- 
取得 Google Programmable Search Engine ID 後
（https://programmablesearchengine.google.com ，限定搜尋 cccbook.github.io/cccbook2026），
將下方註解打開並取代 YOUR_CSE_ID 即可啟用：

<script async src="https://cse.google.com/cse.js?cx=YOUR_CSE_ID"></script>
<div class="gcse-search"></div>
-->

<form action="https://www.google.com/search" method="get" target="_blank">
  <input type="hidden" name="q" value="site:cccbook.github.io/cccbook2026">
  <input type="text" name="q" placeholder="用 Google 搜尋本站…" size="40">
  <button type="submit">搜尋</button>
</form>
