# Utility to download a series of URLs

This is just a small utility to download a series of URLs. 

Two example non-abstract classes exist.

## ExcelSheetDownloader

Use this class to download a series of URLs listed in an XLS file.

## PrabuddhaBharataYearDownloader

Use this class to download Prabuddha Bharata from 2003 to 2021. 

# How to extend this further?

Write your own downloader class which inherts from class Downloader. Override the methods gen_url_fname() and __init__(). The latter to initialize anything that you need to. gen_url_fname() should yield a tuple (fname, url) - fname being the file name to which the URL should be written to.
