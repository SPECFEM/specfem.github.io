## Scholar directory

This dir contains some functions (```functions.py```) and a driver code (```main.py```) to download 20 publications from the [Specfem Software Google Scholar](https://scholar.google.com/citations?user=bvjzHdUAAAAJ). These can then be automatically transferred to a HTML/MD format for addition to the website.

### To do: 
<u> Downloading from website </u>

- [ ] Allow user to specify 20 most recent or 20 most cited publications
- [x] Correctly deal with unicode special characters
- [ ] Look into taking more than 20 publications? 
- [ ] Extract link to the paper?

<u> Adding to SPECFEM.org </u>

- [x] Write script to convert yaml files to correct style for website
- [ ] Look into Cron job to automatically update every few weeks.
