"""Verktøy for å jobbe med sitemap til en nettside."""

import datetime

import httpx
from pydantic import BaseModel, Field, HttpUrl
from yarl import URL


class Site(BaseModel):
    """En side fra en sitemap.xml."""

    loc: HttpUrl = Field(description="Full URL til siden")
    lastmod: datetime.datetime | None = Field(
        None, description="Datoen når siden sist ble endret"
    )


async def parse_sitemap(url: str | URL) -> list[Site]:
    """Tolk en sitemap.xml og returner en liste av sider funnet.

    Args:
        url: Nettsiden å hente sitemap fra. Må være fullstendig med skjema.

    Returns:
        Liste med sider funnet i sitemap-et.
    """
    import xml.etree.ElementTree as ET

    if isinstance(url, str):
        url = URL(url)
    if not url.path.endswith("sitemap.xml"):
        url = url.with_path(f"{url.path}/sitemap.xml")
    async with httpx.AsyncClient() as client:
        raw_sitemap = (await client.get(str(url))).raise_for_status()
    sitemap = ET.fromstring(raw_sitemap.text)
    assert sitemap.tag.endswith(
        "urlset"
    ), f"Bare 'urlset' sitemap støttes, fant: {sitemap.tag}"
    result = []
    for site in sitemap:
        assert site.tag.endswith("url"), f"Ukjent tag for side: {site.tag}"
        loc: str
        lastmod: datetime.datetime | None = None
        for child in site:
            if child.tag.endswith("loc") and child.text:
                loc = child.text
            elif child.tag.endswith("lastmod") and child.text:
                lastmod = datetime.datetime.fromisoformat(child.text)
        result.append(Site(loc=loc, lastmod=lastmod))  # type: ignore[arg-type]
    return result
