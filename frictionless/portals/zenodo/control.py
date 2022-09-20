from __future__ import annotations
import attrs
import os
from typing import Optional, List
from ...dialect import Control


DEFAULT_FORMATS = ["csv", "tsv", "xlsx", "xls", "jsonl", "ndjson"]
BASE_URL = "https://zenodo.org/api/"


@attrs.define(kw_only=True)
class ZenodoControl(Control):
    """Zenodo control representation"""

    type = "zenodo"

    # State

    all_versions: Optional[int] = None
    """Show (true or 1) or hide (false or 0) all versions of records."""

    apikey: Optional[str] = os.environ.get("ZENODO_ACCESS_TOKEN", None)
    """The access token to authenticate to the github API. It is required 
    to write files to github repo. 
    For reading, it is optional however using apikey increases the api 
    access limit from 60 to 5000 requests per hour. To write, access 
    token has to have write repository access.
    """

    base_url: Optional[str] = BASE_URL
    """Endpoint for zenodo. By default it is set to live site. For testing(only write), we can 
    pass url of sandbox for example, https://sandbox.zenodo.org/api. Sandbox doesnot work for
    reading."""

    bounds: Optional[str] = None
    """Return records filtered by a geolocation bounding box. 
    (Format bounds=143.37158,-38.99357,146.90918,-37.35269)"""

    communities: Optional[str] = None
    """Return records that are part of the specified communities. (Use of community identifier)."""

    deposition_id: Optional[int] = None
    """Id of the deposition resource. Deposition resource is the state of a resource for 
    uploading and editing records on Zenodo."""

    doi: Optional[str] = None
    """Digital Object Identifier(DOI). When the deposition is published, a unique DOI is registered by 
    Zenodo. This is only for the published depositions."""

    formats: Optional[List[str]] = DEFAULT_FORMATS
    """Formats instructs plugin to only read specified types of files. By default it is set to 
    'csv,xls,xlsx'.
    """

    name: Optional[str] = None
    """Custom name for a catalog or a package. Default name is 'catalog' or 'package'"""

    metafn: Optional[str] = None
    """Metadata file path for deposition resource. Deposition resource is used for uploading 
    and editing records on Zenodo."""

    page: Optional[str] = None
    """Page number for pagination."""

    rcustom: Optional[str] = None
    """Return records containing the specified custom keywords. (Format custom=[field_name]:field_value)"""

    record: Optional[str] = None
    """Unique identifier of a record. We can use it find the specific record while creating a 
    package or a catalog. For example, 7078768"""

    rtype: Optional[str] = None
    """Return records of the specified type. (Publication, Poster, Presentation…)"""

    search: Optional[str] = None
    """Search query containing one or more search keywords and qualifiers to filter the repositories. 
    For example, 'windows+label:bug+language:python'."""

    size: Optional[int] = None
    """Number of results to return per page."""

    sort: Optional[str] = None
    """Sort order (bestmatch or mostrecent). Prefix with minus to change form 
    ascending to descending (e.g. -mostrecent)"""

    status: Optional[str] = None
    """Filter result based on the deposit status (either draft or published)"""

    subtype: Optional[str] = None
    """Return records that are part of the specified communities. (Use of community identifier)."""

    tmp_path: Optional[str] = None
    """Temp path to create intermediate package/resource file/s to upload to the zenodo instance"""

    # Metadata

    metadata_profile_patch = {
        "properties": {
            "all_versions": {"type": "integer"},
            "apikey": {"type": "string"},
            "base_url": {"type": "string"},
            "bounds": {"type": "string"},
            "communities": {"type": "string"},
            "deposition_id": {"type": "integer"},
            "doi": {"type": "string"},
            "formats": {"type": "array"},
            "name": {"type": "string"},
            "page": {"type": "string"},
            "rcustom": {"type": "string"},
            "record": {"type": "string"},
            "rtype": {"type": "string"},
            "search": {"type": "string"},
            "size": {"type": "integer"},
            "sort": {"type": "string"},
            "status": {"type": "string"},
            "subtype": {"type": "string"},
            "tmp_path": {"type": "string"},
        },
    }
