import html
import re

# GitHub 風格的行內數學: $`...`$
GFM_CODE_MATH = re.compile(r"\$`(.+?)`\$", re.DOTALL)

# GitHub 風格的區塊數學: ```math ... ```
GFM_MATH_FENCE = re.compile(
    r"^[ \t]*```math[^\S\n]*\n(.*?)[ \t]*```\s*$",
    re.MULTILINE | re.DOTALL,
)


def on_page_markdown(markdown, page, config, files):
    markdown = GFM_CODE_MATH.sub(lambda m: "$" + m.group(1) + "$", markdown)
    markdown = GFM_MATH_FENCE.sub(lambda m: "$$\n" + m.group(1) + "\n$$", markdown)
    return markdown


def fence_mermaid(source, language, cls, options=None, md=None, **kwargs):
    code = html.escape(source)
    return (
        '<div class="mz-view">'
        '<div class="mz-bar">'
        '<button type="button" class="mz-btn" data-mz="in" title="放大 (Ctrl+滾輪)">+</button>'
        '<button type="button" class="mz-btn" data-mz="out" title="縮小">−</button>'
        '<button type="button" class="mz-btn" data-mz="fit" title="重設大小">1:1</button>'
        '</div>'
        f'<div class="mz-canvas"><pre class="mz-src" hidden>{code}</pre></div>'
        '</div>'
    )


def on_config(config, **kwargs):
    opts = (config.get("mdx_configs") or {}).get("pymdownx.superfences") or {}
    for fence in opts.setdefault("custom_fences", []):
        if fence.get("name") == "mermaid":
            fence["format"] = fence_mermaid
    return config
