"""Parsing av macro fra JSON."""

from typing import Any

from bs4 import BeautifulSoup, Tag


def parse_macros(content: list[dict[str, Any]]) -> dict[str, Tag]:
    """Tolk macro strukturen og gi tilbake en mapping over verdier.

    Args:
        content: JSON struktur med macro-er
    Returns:
        Mapping som mapper fra macro ID til verdi macro kan erstattes med
    """
    result = dict()
    for macro in content:
        name = macro["name"]
        ref = macro["ref"]
        if name == "product-card-mini":
            result[ref] = _product_card(macro)
        else:
            raise NotImplementedError(f"Støtter ikke macro: {name}")
    return result


def _product_card(content: dict[str, Any]) -> Tag:
    """Tolk 'product-card-mini' macro."""
    for card in content["config"]:
        data = content["config"][card]
        if page := data.get("targetPage"):
            return BeautifulSoup(
                f"<a href=\"https://www.nav.no{page['_path']}\">{page['displayName']}</a>"
            ).a
    raise RuntimeError(f"Klarte ikke å lage lenke for product-card {content['ref']}")
