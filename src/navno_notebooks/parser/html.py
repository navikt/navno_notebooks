"""Parser metoder for JSON data med HTML innhold."""

from typing import Any

from bs4 import BeautifulSoup

from .macros import parse_macros


def parse_area(content: dict[str, Any]) -> str:
    """Parser for type 'no.nav.navno:html-area'."""
    # TODO: Parse 'data macro' her
    html: str = content["config"]["html"]["processedHtml"]
    if macros := parse_macros(content["config"]["html"]["macros"]):
        soup = BeautifulSoup(html, "lxml")
        editor_macros = soup.find_all("editor-macro")
        for macro in editor_macros:
            ref = macro.attrs["data-macro-ref"]
            if replacement := macros.get(ref):
                macro.replace_with(replacement)
            else:
                macro.extract()
        return str(soup)
    return html
