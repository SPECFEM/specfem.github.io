#!/usr/bin/env python
#
# converts publication list to markdown text
import yaml
from copy import copy
import os
import fileinput
import numpy as np

import pandas as pd
from functions import plot_citations_graph

calendar = {1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'}

def convert_to_markdown(total_pub_no, total_cites, local_dir='./publications/'):

    # Update total citations button in index.md via citations_button in _INCLUDES
    for line in fileinput.input('../_includes/citation_button.html', inplace=1):
        if "{% assign num_pubs=" in line:
            linestr = '{% assign num_pubs=' + str(total_pub_no) + '%}'
            print( linestr.rstrip() )
        elif "{% assign num_cites=" in line:
            linestr = '{% assign num_cites=' + str(total_cites) + '%}'
            print(linestr.rstrip())
        else:
            print(line.rstrip())


    files = os.listdir(local_dir)

    files.remove('total_citations_per_year.yml')
    files.remove('total_citations.yml')

    P_dict = {}
    dates  = []
    for GS_unique in files:

        with open(f"{local_dir}/{GS_unique}", 'r') as file:
            tmp_pub = yaml.safe_load(file)
        P_dict[GS_unique[:-4]] = copy(tmp_pub) # -4 removes the .yml from the name

        # Sort out date:
        date = tmp_pub['Publication date']
        separator = date.find('/')
        year  = date[:separator]

        # Check month doesnt also include year:
        month = date[separator + 1:]
        u = month.find('/')
        if u!= -1:
            month = month[:u]

        dates.append([int(month), int(year), tmp_pub["Unique GS"]])

    # Sort publications by date:
    sorted_by_date = pd.DataFrame(dates, columns=['Month', 'Year', 'UniqueGS']).sort_values(by=['Year', 'Month'], ascending=False).to_numpy()

    # Create graph for website
    plot_citations_graph(localdir=local_dir)

    # Now write to MD:

    # first we want to remove the current stuff:
    f = open("../publications.md", "r+")
    f.truncate(0)

    # Markdown formatting stuff
    f.write('''---
    layout: default
    title: Publications
    description: Publications using SPECFEM\n---\n''')

    # Title
    f.write('\n')
    f.write('# Publications:\n')
    # Introduction
    f.write('The open-source development of the SPECFEM codes has allowed researchers across the globe to apply them in various fields of study. Below shows the citation count of journal articles that utilised the SPECFEM codes. Seminal papers relating to the development of, and theory behind, SPECFEM can be found on the [Training page](training.md).  \n')
    # Add the image/bargraph
    f.write("![title](scholar/total_citations_per_year.jpg)\n\n")

    f.write('## Recent publications using SPECFEM:\n')
    f.write('#### Here we list some recent publications using some of the SPECFEM codes. A larger, albeit possibly non-exhaustive, list of publications can be found on our [<span class="fas fa-external-link-alt"></span> Google Scholar](https://scholar.google.com/citations?hl=en&user=bvjzHdUAAAAJ&view_op=list_works&sortby=pubdate).')
    f.write('\n')
    f.write('\n')

    # publication list
    for i in range(20):
        code = sorted_by_date[i,2]
        pub  = P_dict[code]
        url  = pub['url']
        md_link = '(' + url + '){:style="color: gray;" target="_blank"}'

        #print("md_link: ",md_link)

        f.write(f"<i><b>{pub['Title']}</b></i>  \n")
        f.write(f"{pub['Authors']}   \n")
        f.write(f'[<span style="color:grey"><span class="fas fa-external-link-alt"></span> Published in {calendar[sorted_by_date[i,0]]} {sorted_by_date[i,1]}</span>]' + md_link + '\n')
        f.write('\n')
    f.close()

    print('Completed conversion to Markdown.')

if __name__ == "__main__":
    convert_to_markdown()
