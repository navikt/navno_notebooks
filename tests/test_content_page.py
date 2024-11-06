"""Tester for parsing av sider med type 'no.nav.navno:content-page-with-sidemenus'."""

import re

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
    for doc in docs:
        for first_h, second_h in zip(
            doc.metadata["headers"], doc.metadata["headers"][1:]
        ):
            assert first_h[1] != second_h[1], "To like headere skal ikke forekomme"
        assert not re.search(
            r"editor-macro", doc.page_content
        ), "Det skal ikke eksistere macro etter parsing"
