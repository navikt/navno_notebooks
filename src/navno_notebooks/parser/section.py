"""Parsere for 'no.nav:navno:section-*'."""

import copy
from typing import Any

from langchain_core.documents import Document

HEADER_MAPPING = {
    "h1": "#",
    "h2": "##",
    "h3": "###",
    "h4": "####",
    "h5": "#####",
    "h6": "######",
}
"""Mapping fra HTML header type til Markdown header"""


def section_with_header(
    content: dict[str, Any], metadata: dict[str, Any] | None = None
) -> list[Document]:
    """Parse en 'no.nav.navno:section-with-header'.

    Args:
        content: JSON blob med innhold å parse
        metadata: Valgbar metadata å legge til på resultate av parsing

    Returns:
        Liste med dokumenter som representerer innholdet
    """
    assert content["descriptor"] == "no.nav.navno:section-with-header", (
        "Feil type for top-nivå JSON, forventet 'no.nav.navno:section-with-header' "
        f"fikk '{content['descriptor']}'"
    )
    # Ordne slik at metadata har formen som vi antar
    if not metadata:
        metadata = {}
    if "headers" not in metadata:
        metadata["headers"] = []
    # Legg til metadata som gjelder for denne seksjonen (kan bli overskrevet senere!)
    metadata["headers"].append((content["config"]["title"], "##"))
    metadata["anchor"] = content["config"]["anchorId"]
    # Liste med resultater å returnere
    results = []
    # Iterer over potensielle barn
    state = ""
    for sub_section in content["regions"]["content"]["components"]:
        if sub_section["type"] == "fragment":
            sub_section = sub_section["fragment"]
        sub_type = sub_section["descriptor"]
        if sub_type == "no.nav.navno:html-area":
            state += sub_section["config"]["html"]["processedHtml"]
        elif sub_type == "no.nav.navno:dynamic-header":
            if state:
                results.append(
                    Document(page_content=state, metadata=copy.deepcopy(metadata))
                )
                state = ""
            header = sub_section["config"]["title"]
            header_level = HEADER_MAPPING[sub_section["config"]["titleTag"]]
            # Hvis forrige header er samme nivå som den nye så erstatter vi
            if metadata["headers"][-1][1] == header_level:
                metadata["headers"].pop()
            metadata["headers"].append((header, header_level))
            metadata["anchor"] = sub_section["config"]["anchorId"]
    if state:
        results.append(Document(page_content=state, metadata=copy.deepcopy(metadata)))
    return results
