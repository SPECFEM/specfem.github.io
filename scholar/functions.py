import urllib.request

def _get_HTML(url):
    # Extracts the HTML from a url
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    HTTP = mybytes.decode("unicode_escape")
    fp.close()

    return HTTP


def _fix_amp(s):
    # Fixes the formatting of the Ampersands in the url strings
    u = 0
    while u != -1:
        u = s.find('&amp;')
        if u > -1:
            s = s[:u] + '&' + s[u + 5:]

    return s


def search_field_in_html(field, html):
    # Search for specific field (e.g. Citation, Authors etc) in the HTML code.
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


def get_unique_paper_codes(landingpage):
    # Takes in the HTML code from the landing page

    # Link required to navigate to individual publication page
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
    return paper_links

