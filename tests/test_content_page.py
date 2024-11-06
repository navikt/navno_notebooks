"""Tester for parsing av sider med type 'no.nav.navno:content-page-with-sidemenus'."""

import httpx
import pytest

from navno_notebooks.parser import content_page


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/oyeprotese", "/dagpenger", "/sykepenger"])
async def test_parse_content_page(path: str) -> None:
    """Test parsing av 'no.nav.navno:content-page-with-sidemenus'."""
    async with httpx.AsyncClient() as client:
        json = (
            (await client.get(f"https://www.nav.no/_next/data/latest/{path}.json"))
            .raise_for_status()
            .json()
        )
    docs = content_page(json["pageProps"]["content"])
    assert docs, "Forventet at vi fikk ut minst ett dokument fra parsing"
