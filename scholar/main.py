#!/usr/bin/env python
#
# Driver code the the Publications stuff:
from functions import scholarly_citation_count
from download import download_recent_citations
from convert_to_md import convert_to_markdown

local_dir='./publications'

# If override is set to true then will re-download publications that are already downloaded (e.g. to update citations
# for a publication

total_num_pubs, total_num_citations = scholarly_citation_count()
download_recent_citations(local_dir, override_current_downloads=False)
convert_to_markdown(total_num_pubs, total_num_citations, local_dir)
