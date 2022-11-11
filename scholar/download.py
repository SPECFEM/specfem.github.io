# Script downloads and prints 20 most recent citations on the SPECFEM google scholar

# Current issues:
# - Fix UNICODE characters in names
# - Get titles of the papers

import urllib.request


def _get_HTML(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    HTTP = mybytes.decode("unicode_escape")
    fp.close()

    return HTTP


def _fix_amp(s):
    u = 0
    while u != -1:
        u = s.find('&amp;')
        if u > -1:
            s = s[:u] + '&' + s[u + 5:]

    return s


def search_field_in_html(field, html):
    if field == 'Citations':
        search_str = f'Cited by'
        termination = '</a>'
    else:
        search_str = f'<div class="gsc_oci_field">{field}</div><div class="gsc_oci_value">'
        termination = '</div>'

    indx = html.find(search_str)

    if indx == -1:
        field_value = 'n/a'
    else:
        html_field = html[indx + len(search_str):]
        field_value = html_field[:html_field.find(termination)]

    return field_value




# SPECFEM SCHOLAR LANDING PAGE ADDRESS
landingpage = _get_HTML("https://scholar.google.com/citations?view_op=list_works&hl=en&hl=en&user=bvjzHdUAAAAJ&sortby=pubdate")
linkstr = '/citations?view_op=view_citation&amp;hl=en&amp;oe=ASCII&amp;user=bvjzHdUAAAAJ&amp;sortby=pubdate&amp;citation_for_view=bvjzHdUAAAAJ:'


# Create a list of the paper link hrefs 
paper_links = []
unit = 0
while unit != -1:
    unit = landingpage.find(linkstr)
    tmp = landingpage[unit + len(linkstr):]

    terminate = tmp.find('"')
    paper_links.append(tmp[:terminate])
    landingpage = landingpage[terminate:]

paper_links = paper_links[:-1]

# Get unique list values:
paper_links = list(set(paper_links))


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