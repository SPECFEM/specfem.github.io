# Script downloads and prints 20 most recent citations on the SPECFEM google scholar
import os
from functions import _get_HTML,  get_unique_paper_codes, parse_citation, get_total_citations_for_specfem

# Current issues:
# - Fix UNICODE characters in names


def download_recent_citations(local_dir='./publications', override_current_downloads=False):


    # SPECFEM SCHOLAR LANDING PAGE ADDRESS HTML LINKS:
    landingpage = _get_HTML("https://scholar.google.com/citations?view_op=list_works&hl=en&hl=en&user=bvjzHdUAAAAJ&sortby=pubdate")
    linkstr     = '/citations?view_op=view_citation&amp;hl=en&amp;oe=ASCII&amp;user=bvjzHdUAAAAJ&amp;sortby=pubdate&amp;citation_for_view=bvjzHdUAAAAJ:'


    # Get unique GS identifies for each paper on the SPECFEM GS landing page
    paper_links = get_unique_paper_codes(landingpage, linkstr)


    get_total_citations_for_specfem(landingpage, local_dir)

    # Loop for each publication found on the page (will only get first 20 at the moment):
    for i in range(len(paper_links)):
    #for i in range(1):

        # unique GS code
        pub = paper_links[i]

        # Check if we have already downloaded this:
        if os.path.exists(f"{local_dir}/{pub}.yml"):
            if override_current_downloads:
                print(f"{pub} already exists but redownloading.")
                parse_citation(linkstr, pub, local_dir)
            else:
                print(f"{pub} already exists. Not re-downloading.")
        else:
            parse_citation(linkstr, pub, local_dir)

if __name__ == "__main__":
    download_recent_citations()