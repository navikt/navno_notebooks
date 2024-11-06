"""Tester for sitemap funksjonalitet."""

import pytest

from navno_notebooks.sitemap import parse_sitemap


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "site", ["https://www.nav.no", "https://www.digdir.no/sitemap.xml?page=1"]
)
async def test_parse(site: str) -> None:
    """Test at vi kan laste inn kjente sitemap."""
    sitemap = await parse_sitemap(site)
    assert sitemap, "Fikk tom liste fra sitemap!"
