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
