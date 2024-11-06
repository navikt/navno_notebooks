"""Aksessere metadata om sider på nav.no."""

import asyncio
import datetime
import uuid
from itertools import batched
from typing import AsyncGenerator

import httpx
from pydantic import BaseModel, Field
from yarl import URL


class Metadata(BaseModel):
    """Metadata om innholdet i JSON data til sider på nav.no."""

    id: uuid.UUID = Field(
        description="Unik ID for elementet, merk at denne forandrer seg når siden oppdateres"
    )
    path: str = Field(description="Stien som data-en representerer")
    type: str = Field(description="Nettside type")
    created: datetime.datetime = Field(description="Når ble siden opprettet")
    modified: datetime.datetime = Field(description="Når ble siden sist endret")
    title: str = Field(description="Tittel på nettsiden")
    language: str = Field(description="Språket på nettsiden")


class CouldNotReach(BaseModel):
    """Sider som ikke kunne nåes."""

    path: str = Field(description="Stien som ikke kunne nåes")
    reason: str = Field(description="Hvorfor kunne den ikke nåes")
    status_code: int | None = Field(None, description="HTTP status kode hvis mulig")


class MetadataYield(BaseModel):
    """Generert metadata."""

    metadata: list[Metadata] = []
    could_not_reach: list[CouldNotReach] = []


async def fetch_metadata(
    sites: list[URL], batch_size: int = 10, follow_redirect: bool = True
) -> AsyncGenerator[MetadataYield, None]:
    """Hent metadata fra 'Nav.no' om ønskede sider.

    Args:
        sites: URL eller path til en side å hente metadata fra.
        batch_size: Antall sider å prosessere samtidig.
        follow_redirect: Hvis siden omdirigerer, skal dette følges?

    Returns:
        Liste med metadata for sider.
    """
    to_fetch = sites[:]  # Lag en kopi slik at vi kan destruktivt jobbe på listen
    result = []
    could_not_reach = []
    async with httpx.AsyncClient() as client:
        while to_fetch:
            redirects: list[URL] = []
            for site_batch in batched(to_fetch, n=batch_size):
                batch_data = await asyncio.gather(
                    *[
                        client.get(
                            f"https://www.nav.no/_next/data/latest{site.path}.json"
                        )
                        for site in site_batch
                    ]
                )
                for resp, site in zip(batch_data, site_batch):
                    if resp.status_code != 200:
                        could_not_reach.append(
                            CouldNotReach(
                                path=site.path,
                                reason="HTTP error",
                                status_code=resp.status_code,
                            )
                        )
                        continue
                    json = resp.json()["pageProps"]
                    if "__N_REDIRECT" in json:
                        if follow_redirect:
                            redirects.append(site.with_path(json["__N_REDIRECT"]))
                        else:
                            could_not_reach.append(
                                CouldNotReach(
                                    path=site.path,
                                    reason="Siden omdirigerte",
                                    status_code=None,
                                )
                            )
                        continue
                    content = json["content"]
                    meta = Metadata(
                        id=uuid.UUID(content["_id"]),
                        path=content["_path"],
                        title=content["displayName"],
                        type=content["type"],
                        created=datetime.datetime.fromisoformat(content["createdTime"]),
                        modified=datetime.datetime.fromisoformat(
                            content["modifiedTime"]
                        ),
                        language=content["language"],
                    )
                    result.append(meta)
                yield MetadataYield(metadata=result, could_not_reach=could_not_reach)
            to_fetch.clear()
            if follow_redirect and redirects:
                to_fetch.extend(redirects)
