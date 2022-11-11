# Script downloads and prints 20 most recent citations on the SPECFEM google scholar

# Current issues:
# - Fix UNICODE characters in names
# - Get titles of the papers
from functions import _get_HTML, _fix_amp, search_field_in_html, get_unique_paper_codes


# SPECFEM SCHOLAR LANDING PAGE ADDRESS
landingpage = _get_HTML("https://scholar.google.com/citations?view_op=list_works&hl=en&hl=en&user=bvjzHdUAAAAJ&sortby=pubdate")

# Get unique GS identifies for each paper on the SPECFEM page
paper_links = get_unique_paper_codes(landingpage)

# Loop for each publication found on the page (will only get first 20 at the moment):
for i in range(len(paper_links)):
    print()
    print("-------------------------------------------------------")
    print()

    # Create HTTP link to the individual publication part of scholar
    pub = paper_links[i]
    url = f"https://scholar.google.com{linkstr}{pub}"
    url = _fix_amp(url)

    # Gather the HTML code from that publication
    html = _get_HTML(url)
    html = html[html.find('<div id="gsc_oci_title">'):]

    # Extract important fields and print:
    FIELD = ['Authors', 'Journal', 'Volume', 'Issue', 'Publication date', 'Citations']
    for field in FIELD:

        field_value = search_field_in_html(field, html)
        print(f"{field}: {field_value}")