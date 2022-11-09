# SPECFEM Website

This is the website repository.
Feel free to contribute and add content to the site!


---
## Contributing to the website 

Each of the website pages is written using Markdown. To learn more about Markdown, follow [this tutorial](https://www.markdowntutorial.com/) or look up specific syntax [here](https://www.markdownguide.org/basic-syntax/). 

To make changes you can [fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repository and then [open a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) when you are ready to add your contributions to the site. We recommend testing your changes locally first, before opening a Pull Request, to ensure everything is just how you wanted! Details of the repository layout are given below, as well as a guide on how to check your updated version. 



---
### Repository layout: 
The layout modifications are controlled by:
- _layouts/default.html
- assets/css/style.scss




### Testing your changes locally 
* To test your changes locally, use Ruby, Jekyll, and Bundler. You can install these using 
``` 
$ gem install jekyll bundler 
```
This may not work on Mac. If so, then a work-around is given below. Next we need to run the following command: 

```
$ bundle install
```

Once you have got Jekyll and Bundler installed, you are now all setup to view any changes you make to the website. Each time you want to view your most recent version run:
```
$ bundle exec jekyll serve
```  
This will generate a server address (```http://127.0.0.1:4000```). Navigate to this server address in your favourite web browser and your newly-updated SPECFEM website should be viewable in all its glory! 




---
### Installing gems on Mac
* Macs ship with their own verison of Ruby that you are not able to edit. This can make installing Gems a bit more difficult. An easy work around for this is to first install a separate version of Ruby using [Homebrew](https://brew.sh/): 
```
$ brew install ruby 
```

Now you have your own version of Ruby, you will want to run the command 
```
$ export GEM_HOME="$HOME/.gem"
```
and also add this command to your shell configuration (either your ~/.zshrc or ~/.bash_profile depending on the shell you use). Don't forget to make sure these updates to your config file are activated by running ```$ source ~/.zshrc``` or  ```$ source ~/.bash-profile```. You should now have a working version of Ruby that you can use to install. Finally we can run our install command 
``` 
$ gem install jekyll bundler &&  bundle install
```

