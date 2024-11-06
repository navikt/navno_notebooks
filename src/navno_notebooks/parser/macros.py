"""Parsing av macro fra JSON."""

import re
from typing import Any

from bs4 import BeautifulSoup, Tag


def parse_macros(content: list[dict[str, Any]]) -> dict[str, Tag | str]:
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
        elif name == "global-value-with-math":
            result[ref] = _global_value_math(macro)
        elif name == "video":
            pass  # Ignore med vilje
        else:
            raise NotImplementedError(f"Støtter ikke macro: {name} ({ref})")
    return result


def _product_card(content: dict[str, Any]) -> Tag:
    """Tolk 'product-card-mini' macro."""
    for card in content["config"]:
        data = content["config"][card]
        if page := data.get("targetPage"):
            return BeautifulSoup(
                f"<a href=\"https://www.nav.no{page['_path']}\">{page['displayName']}</a>",
                "lxml",
            ).a
    raise RuntimeError(f"Klarte ikke å lage lenke for product-card {content['ref']}")


def _global_value_math(content: dict[str, Any]) -> str:
    """Tolk 'global-value-with-math' macro."""
    for math in content["config"]:
        data = content["config"][math]
        if expr := data.get("expression"):
            full_expr = re.sub(
                r"\$(\d)+", lambda m: str(data["variables"][int(m.group(1)) - 1]), expr
            )
            return str(eval(full_expr))
    raise RuntimeError(f"Fant ikke matte uttrykk i {content['ref']}")
