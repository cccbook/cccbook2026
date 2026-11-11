"""自動生成 MkDocs 導覽 (SUMMARY.md) 與各分類書目總覽頁 (catalog/)"""
import posixpath
import re
from pathlib import Path

import mkdocs_gen_files

CATEGORIES = ["電腦", "歷史", "傳記", "數學", "物品", "小說", "得獎"]
ROOT = Path(__file__).resolve().parent
SKIP_NAMES = {"todo.md", "prompts.md", "prompt.md", "list.md"}
SKIP_PREFIX = ("session-", ".")


def natural_key(name: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def keep(path: Path) -> bool:
    if path.name in SKIP_NAMES or path.name.startswith(SKIP_PREFIX):
        return False
    if any(part.startswith(("_", ".")) for part in path.parts):
        return False
    return True


def description(readme: Path) -> str:
    try:
        for line in readme.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith(("#", "!", "[", "<", ">", "|", "```")):
                continue
            text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
            text = re.sub(r"[*_`]", "", text)
            if text:
                return text[:80] + ("…" if len(text) > 80 else "")
    except Exception:
        pass
    return ""


def write_generated_index(item: Path, children: list[Path]):
    """為沒有 README.md 的目錄生成虛擬 index.md，避免站內連結 404"""
    index_path = item / "index.md"
    with mkdocs_gen_files.open(index_path, "w", encoding="utf-8") as f:
        f.write(f"# {item.name}\n\n")
        if not children:
            f.write("（本目錄尚無內容）\n")
            return
        for child in children:
            if child.is_dir():
                child_index = "README.md" if (child / "README.md").exists() else "index.md"
                f.write(f"- [{child.name}]({child.name}/{child_index})\n")
            else:
                f.write(f"- [{child.stem}]({child.name})\n")


def write_nav_item(nav_file, item: Path, depth: int):
    indent = "    " * depth
    if item.is_dir():
        readme = item / "README.md"
        label = item.name
        has_readme = readme.exists()
        link = posixpath.join(item.as_posix(), "README.md") if has_readme else posixpath.join(item.as_posix(), "index.md")
        children = sorted(
            [p for p in item.iterdir() if keep(p) and p.is_dir()], key=lambda p: natural_key(p.name)
        ) + sorted(
            [p for p in item.iterdir() if keep(p) and p.is_file() and p.suffix == ".md"],
            key=lambda p: natural_key(p.name),
        )
        if not has_readme:
            write_generated_index(item, children)
        nav_file.write(f"{indent}- [{label}]({link})\n")
        for child in children:
            write_nav_item(nav_file, child, depth + 1)
    else:
        label = item.stem
        nav_file.write(f"{indent}- [{label}]({item.as_posix()})\n")


def collect_books(category: Path):
    books = []
    for path in sorted(category.rglob("README.md")):
        if not keep(path):
            continue
        book_dir = path.parent
        chapters = [p for p in book_dir.rglob("*.md") if keep(p) and p.name != "README.md"]
        books.append((book_dir, len(chapters)))
    return books


def write_catalog(category: Path, category_name: str):
    books = collect_books(category)
    out_path = Path("catalog") / f"{category_name}.md"
    with mkdocs_gen_files.open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# {category_name}（共 {len(books)} 本）\n\n")
        for book_dir, n_chapters in books:
            readme = book_dir / "README.md"
            rel = posixpath.relpath(readme.as_posix(), "catalog")
            desc = description(readme)
            f.write(f"- [{book_dir.name}]({rel})")
            if desc:
                f.write(f"\n  > {desc}")
            f.write("\n")
    return out_path


def main():
    with mkdocs_gen_files.open("SUMMARY.md", "w", encoding="utf-8") as nav_file:
        nav_file.write("- [首頁](README.md)\n")
        nav_file.write("- [搜尋](search.md)\n")
        for name in CATEGORIES:
            category = Path(name)
            if not category.is_dir():
                continue
            catalog_path = write_catalog(category, name)
            nav_file.write(f"- [{name}]({catalog_path.as_posix()})\n")
            children = sorted(
                [p for p in category.iterdir() if keep(p) and p.is_dir()],
                key=lambda p: natural_key(p.name),
            ) + sorted(
                [p for p in category.iterdir() if keep(p) and p.is_file() and p.suffix == ".md"],
                key=lambda p: natural_key(p.name),
            )
            if not (category / "README.md").exists():
                write_generated_index(category, children)
            for child in children:
                write_nav_item(nav_file, child, 1)


main()
