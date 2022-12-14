import urllib.request
import matplotlib.pyplot as plt
import numpy as np
import yaml
from scholarly import scholarly

def scholarly_citation_count():
    # Get data:
    data = scholarly.search_author_id('bvjzHdUAAAAJ')
    scholarly.fill(data, sections=['publications'])


    # Get total number of citations:
    total_num_pubs = len(data['publications'])
    total_num_citations = data['citedby']

    return total_num_pubs, total_num_citations


def _get_annual_citations(s):
    # Works out the citations per calendar year from the HTML string
    annual_cite_yr = []
    annual_cite    = []

    u = 0
    while u!=-1:

        # Find year:
        u = s.find("gsc_oci_g_t")
        if u != -1:
            s = s[u:]
            u = s.find(">")
            s = s[u+1:]
            annual_cite_yr.append( int(s[:s.find('</span>')]))

    # Now scrape number of citations per year
    for n in range(len(annual_cite_yr)):
        searchstr = '<span class="gsc_oci_g_al">'
        u = s.find(searchstr)
        if u!=-1:
            s = s[u+len(searchstr):]
            u = s.find('</span>')
            num = s[ : u]
            s = s[u:]
        else:
            num = 0

        annual_cite.append(int(num))

    return np.array([annual_cite_yr, annual_cite])




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
    if field == 'Title':
        field = _get_title(html)
        return field
    else:
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


        # Get yearly citations if citations exist:
        if np.logical_and(field == 'Citations', field_value!='n/a'):
            yearly_stats = _get_annual_citations(html)
            field_value = [field_value, yearly_stats]

    return field_value


def get_unique_paper_codes(landingpage, linkstr):
    # Takes in the HTML code from the landing page
    # Link required to navigate to individual publication page

    # Create a list of the paper link hrefs
    paper_links = []
    unit = 0
    while unit != -1:
        unit = landingpage.find(linkstr)
        tmp  = landingpage[unit + len(linkstr):]

        terminate = tmp.find('"')
        paper_links.append(tmp[:terminate])
        landingpage = landingpage[terminate:]

    paper_links = paper_links[:-1]

    # Get unique list values:
    paper_links = list(set(paper_links))
    return paper_links


def _get_title(s):
    # Retreives paper title from HTML string
    # First we need to locate the title roughly:
    search_str = '<div id="gsc_oci_title">'
    s = s[s.find(search_str)+len(search_str):]

    if s[:2] == '<a': # probably linking a href:
        s= s[2:]
        s = s[s.find('>')+1:]
        title = s[:s.find('</a>')]
    else:
        title = s[:s.find('</div>')]
    return title




def parse_citation(linkstr, pub, localdir):
    # Driver to extract publication based on a GS unique code
    # Link string - the GS link prefix
    # pub         - Unique GS code
    # localdir    - output directory
    citation = {}

    # Create HTTP link to the individual publication part of scholar
    url = f"https://scholar.google.com{linkstr}{pub}"
    url = _fix_amp(url)

    # Gather the HTML code from that publication
    html = _get_HTML(url)
    html = html[html.find('<div id="gsc_oci_title">'):]

    # Store for citation:
    citation["Unique GS"] = pub
    citation["url"]       = url

    # Extract important fields and print:
    FIELD = ['Title', 'Authors', 'Journal', 'Volume', 'Issue', 'Publication date', 'Citations']
    for field in FIELD:
        val = search_field_in_html(field, html)
        # Format YAML
        citation = _add_val_to_YAML(field, val, citation)


    # Output
    print('Written to YAML: \n', citation)

    # Create YAML file:
    with open(f"{localdir}/{citation['Unique GS']}.yml", 'w') as outfile:
        yaml.dump(citation, outfile, default_flow_style=False)



def _add_val_to_YAML(field, val, citation):
    # Adds a specific value and field (e.g. Year: 2020) to the citation dictionary
    if field == 'Citations':
        # process total and annual citations
        if val == 'n/a':
            citation["Total citations"] = val
        else:
            citation["Total citations"] = val[0][1:]

            # Get number of years:
            ann_dict = {}
            annuals = np.array(val[1])
            for i in range(np.shape(annuals)[1]):
                ann_dict[f"{annuals[0, i]}"] = f"{annuals[1, i]}"
                # CREATING THE YAML FILE

            # Add ann_dict to Yaml dictionary
            citation["Yearly citations"] = ann_dict

    else:
        citation[str(field)] = val
    return citation




def get_total_citations_for_specfem(html, localdir):
    # Gets the statistics for the whole specfem software citations:

    html = html[html.find('<div class="gsc_md_hist_b">'):]


    years = []
    u = 0
    while u!=-1 :
        searchstr = '<span class="gsc_g_t" style="right:'
        u = html.find(searchstr)
        html = html[u+len(searchstr):]

        html = html[html.find('>')+1:]
        if u != -1:
            years.append(html[:html.find('<')])

    cites = {}
    # Now get number of citations:
    for n in range(len(years)):
        searchstr = '<span class="gsc_g_al">'
        html = html[html.find(searchstr)+len(searchstr):]

        cites[years[n]] = html[:html.find('<')]


    # Write this to YAML:
    with open(f"{localdir}/total_citations_per_year.yml", 'w') as outfile:
        yaml.dump(cites, outfile, default_flow_style=False)





def plot_citations_graph(localdir):
    # Takes total citations data and makes a bar chart:

    # Read YAML:
    with open(f"{localdir}/total_citations_per_year.yml", 'r') as file:
        data = np.array((list(yaml.safe_load(file).items()))).astype(int)

    fs = 14

    fig, ax = plt.subplots(figsize=(10,4.5))
    fig.set_tight_layout(True)
    ax.bar(data[:,0], data[:,1], align='center', tick_label=data[:,0].astype(str), color='darkslategrey')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('Year', fontsize=fs)
    ax.set_ylabel('Number of citations for\npapers using SPECFEM', fontsize=fs)
    plt.savefig('./total_citations_per_year.jpg')
