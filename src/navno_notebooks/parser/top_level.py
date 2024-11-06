"""Parsere for topnivå dokumenttyper."""

import datetime
from typing import Any

from langchain_core.documents import Document

from .section import section_with_header


def content_page(content: dict[str, Any]) -> list[Document]:
    """Parser for 'no.nav.navno:content-page-with-sidemenus'.

    Args:
        content: JSON struktur
    Returns:
        Liste med dokumenter
    """
    # Hent ut metadata som gjelder hele siden
    metadata = {
        "path": content["_path"],
        "created": datetime.datetime.fromisoformat(content["createdTime"]),
        "last_modified": datetime.datetime.fromisoformat(content["modifiedTime"]),
        "language": content["language"],
        "ingress": content["data"].get("ingress", ""),
        "taxonomy": content["data"].get("taxonomy", []),
        "area": content["data"].get("area", []),
    }
    owner = content["data"].get("owner", [])
    if isinstance(owner, str):
        owner = [owner]
    metadata["owner"] = owner
    # Iterer over innholdet og hent ut dokumenter
    docs = []
    for section in content["page"]["regions"]["pageContent"]["components"]:
        sec_type = section["descriptor"]
        if sec_type == "no.nav.navno:section-with-header":
            docs.extend(section_with_header(section, metadata.copy()))
        elif sec_type == "no.nav.navno:uxsignals-widget":
            pass  # Ignorer med vilje
        else:
            raise NotImplementedError(f"Har ikke støtte for '{sec_type}'")
    return docs
