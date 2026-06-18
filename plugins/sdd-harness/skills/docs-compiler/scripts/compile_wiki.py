#!/usr/bin/env python3
"""Offline Zero-Dependency Static Documentation Wiki Compiler.

Scans a 'docs/' directory recursively, translates Markdown to HTML, extracts
Mermaid blocks, computes relative depths, and generates a portable documentation
portal browsable locally via file:// scheme.
"""

import os
import re
import shutil
import sys

try:
    import markdown
except ImportError:
    print("Error: The 'markdown' library is required. Install it via:")
    print("  pip install markdown")
    sys.exit(1)


def clean_and_create_dir(directory):
    """Safely recreates a clean directory."""
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def get_markdown_files(docs_dir):
    """Recursively finds all markdown files under docs_dir."""
    md_files = []
    for root, _, files in os.walk(docs_dir):
        for f in files:
            if f.endswith(".md"):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, docs_dir)
                md_files.append((full_path, rel_path))
    return md_files


def compute_depth_prefix(rel_path):
    """Computes the depth offset prefix to return to the root directory.

    Example:
      'index.md' -> './'
      'sdd/epic/feat.md' -> '../../'
    """
    parts = rel_path.split(os.sep)
    depth = len(parts) - 1
    if depth == 0:
        return "./"
    return "../" * depth


def parse_mermaid_blocks(content):
    """Translates standard mermaid fenced code blocks into HTML wrapper tags."""
    pattern = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)
    return pattern.sub(r'<pre class="mermaid">\1</pre>', content)


def build_sidebar_html(md_files, active_rel_path):
    """Generates a hardcoded hierarchical HTML list representing the sidebar."""
    depth_prefix = compute_depth_prefix(active_rel_path)
    html_lines = ["<ul>"]

    # Organize files by groupings
    groups = {"General": [], "Specifications": [], "ADRs": []}

    for full, rel in sorted(md_files):
        # Target HTML file path mirroring the MD path
        html_rel = rel[:-3] + ".html"
        title = os.path.splitext(os.path.basename(rel))[0].replace("_", " ").replace("-", " ").title()

        if rel == "index.md":
            title = "Home"
            groups["General"].insert(0, (html_rel, title))
        elif "sdd/" in rel:
            groups["Specifications"].append((html_rel, title))
        elif "adr/" in rel:
            groups["ADRs"].append((html_rel, title))
        else:
            groups["General"].append((html_rel, title))

    # Write out groups
    for group_name, items in groups.items():
        if not items:
            continue
        html_lines.append(f'<li class="nav-group">{group_name}</li>')
        for html_rel, title in items:
            href = depth_prefix + html_rel.replace(os.sep, "/")
            # Mark active
            active_class = ' class="active"' if html_rel == active_rel_path[:-3] + ".html" else ""
            html_lines.append(f'<li><a href="{href}"{active_class}>{title}</a></li>')

    html_lines.append("</ul>")
    return "\n".join(html_lines)


def find_project_root(start_dir):
    """Traverses upwards from start_dir to locate the project workspace root.

    Locates root by detecting the presence of '.agents' or '.git' directories.
    """
    current = os.path.abspath(start_dir)
    while True:
        if os.path.exists(os.path.join(current, ".agents")) or os.path.exists(os.path.join(current, ".git")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return os.getcwd()
        current = parent


def main():
    # Workspace layout paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = find_project_root(script_dir)
    
    docs_dir = os.path.join(workspace_root, "docs")
    output_dir = os.path.join(workspace_root, ".docs_build")
    templates_dir = os.path.join(script_dir, "../templates")

    # Check directories
    if not os.path.exists(docs_dir):
        # If docs folder is empty, scaffold a basic index.md
        os.makedirs(docs_dir)
        with open(os.path.join(docs_dir, "index.md"), "w") as f:
            f.write("# Welcome to your local Spec-Driven Development Wiki!\n\nStart editing specs in `docs/sdd/`.")

    clean_and_create_dir(output_dir)

    # 1. Copy style.css to output
    shutil.copy(os.path.join(templates_dir, "style.css"), os.path.join(output_dir, "style.css"))

    # 2. Read base layout
    with open(os.path.join(templates_dir, "template.html"), "r") as f:
        template_html = f.read()

    # 3. Process all MD files
    md_files = get_markdown_files(docs_dir)

    for full_path, rel_path in md_files:
        # Read original content
        with open(full_path, "r") as f:
            raw_content = f.read()

        # Translate Mermaid code blocks
        processed_content = parse_mermaid_blocks(raw_content)

        # Convert MD markup to HTML
        # Enforce extensions for clean tables and smart lists
        compiled_content = markdown.markdown(
            processed_content,
            extensions=["tables", "fenced_code", "nl2br"]
        )

        # Compute relative root offset path
        relative_prefix = compute_depth_prefix(rel_path)

        # Build sidebar matching active path
        sidebar_html = build_sidebar_html(md_files, rel_path)

        # Title formatting
        page_title = os.path.splitext(os.path.basename(rel_path))[0].replace("_", " ").replace("-", " ").title()
        if rel_path == "index.md":
            page_title = "Home"

        # Merge placeholders in template
        output_html = template_html.replace("{{title}}", page_title)
        output_html = output_html.replace("{{relative_path}}", relative_prefix)
        output_html = output_html.replace("{{sidebar}}", sidebar_html)
        output_html = output_html.replace("{{content}}", compiled_content)

        # Write out HTML file
        output_file_path = os.path.join(output_dir, rel_path[:-3] + ".html")
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        with open(output_file_path, "w") as f:
            f.write(output_html)

        print(f"Compiled: {rel_path} -> {os.path.relpath(output_file_path, workspace_root)}")

    print("\nWiki compilation complete! Local Documentation Portal is ready.")
    print(f"Open in your browser: file://{os.path.join(output_dir, 'index.html')}")


if __name__ == "__main__":
    main()
