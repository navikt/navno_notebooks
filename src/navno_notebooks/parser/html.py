"""Parser metoder for JSON data med HTML innhold."""

from typing import Any


def parse_area(content: dict[str, Any]) -> str:
    """Parser for type 'no.nav.navno:html-area'."""
    # TODO: Parse 'data macro' her
    html: str = content["config"]["html"]["processedHtml"]
    return html
