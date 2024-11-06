"""Parser metoder for JSON data med HTML innhold."""

from typing import Any

from bs4 import BeautifulSoup


def parse_area(content: dict[str, Any]) -> str:
    """Parser for type 'no.nav.navno:html-area'."""
    # TODO: Parse 'data macro' her
    html: str = content["config"]["html"]["processedHtml"]
    soup = BeautifulSoup(html, "lxml")
    editor_macros = soup.find_all("editor-macro")
    for macro in editor_macros:
        name = macro.attrs["data-macro-name"]
        if name == "product-card-mini":
            macro.extract()
        else:
            raise NotImplementedError(f"Mangler støtte for macro av type: {name}")
    return str(soup)
