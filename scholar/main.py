#!/usr/bin/env python
#
# Driver code the the Publications stuff:

from download import download_recent_citations
from convert_to_md import convert_to_markdown

local_dir='./publications'

# If override is set to true then will re-download publications that are already downloaded (e.g. to update citations
# for a publication
download_recent_citations(local_dir, override_current_downloads=False)
convert_to_markdown(local_dir)
