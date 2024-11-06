"""Tester for innhenting av metadata."""

import pytest
from yarl import URL

from navno_notebooks.metadata import Metadata, fetch_metadata


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/sykepenger", "/dagpenger", "/oyeprotese"])
async def test_fetch(path: str) -> None:
    """Test at å hente metadata for kjente stier fungerer."""
    metadata: Metadata
    i = 0
    async for meta in fetch_metadata([URL(path)], follow_redirect=False):
        metadata = meta.metadata[0]
        assert not meta.could_not_reach, "Alle sider skal nåes!"
        i += 1
    assert i == 1, "Itererte flere ganger enn forventet!"
    assert metadata, "Fikk ikke metadata"
    assert metadata.path == path, "Forventer samme sti!"


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/sykepeng", "/dagger", "/yeprotse"])
async def test_fetch_error(path: str) -> None:
    """Test at å hente metadata for ødelagte stier ikke fungerer."""
    cnr = []
    i = 0
    async for meta in fetch_metadata([URL(path)], follow_redirect=False):
        assert not meta.metadata
        cnr = meta.could_not_reach
        i += 1
    assert i == 1, "Itererte flere ganger enn forventet!"
    assert cnr, "Stier kunne nåes?"


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/rullestol-scooter"])
async def test_fetch_redirect(path: str) -> None:
    """Test at å hente metadata for stier som omdirigerer fungerer."""
    metadata: Metadata
    i = 0
    async for meta in fetch_metadata([URL(path)], follow_redirect=True):
        if meta.metadata:
            metadata = meta.metadata[0]
        assert not meta.could_not_reach, "Alle sider skal nåes!"
        i += 1
    # NOTE: Med omdirigering så forventer vi at det tar 2 runder å hente metadata
    assert i == 2, "Itererte flere ganger enn forventet!"
    assert metadata, "Fikk ikke metadata"
    assert metadata.path != path, "Forventer ikke samme sti!"


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/rullestol-scooter"])
async def test_fetch_redirect_errors(path: str) -> None:
    """Test at å hente metadata for stier som omdirigerer ikke gir resultat om vi ikke tillater omdirigering."""
    cnr = []
    i = 0
    async for meta in fetch_metadata([URL(path)], follow_redirect=False):
        assert not meta.metadata
        cnr = meta.could_not_reach
        i += 1
    assert i == 1, "Itererte flere ganger enn forventet!"
    assert cnr, "Forventet at omdirigering ikke etterfølges!"
