# Project-03
## Ebay Scraper

This is a repository for project 03, scraping from ebay 

This is the [link](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03) to the project instructions. 

This `ebay-dl.py` file contians the `name` of ebay items. It also contains the `price` of these items. Some other tags include:`free returns`, `items sold`, `status`, and `shipping`. 

The program uses `argparse` library to get a search from the command line, `requests` library to download first 10 webpages from the search, `Beautiful Soup` or `bs4` to extract all of the items, and a `json` library to save the list as a `json` file. 

## Arguments

Specify the desired item into the command line. For example, add 'pen' to the end of the `ebay-dl.py` file path as such:

```$ python3 ebay-dl.py pen``` 

For a search term with multiple words, such as "water park", the command line should have the desired search in quotations:

```$ python3 ebay-dl.py "water bottles"```


## Files Generated 

I generated 3 different json files (pens.json, toys.json and water bottles.json) that are uploaded to the repository. 

As explained above, the json files are generated by:

```$ python3 ebay-dl.py pen ```

```$ python3 ebay-dl.py "water bottles"```

```$ python3 ebay-dl.py toys```




