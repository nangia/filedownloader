import requests
from urllib.request import urlopen, URLError
from abc import ABC, abstractmethod
import pandas as pd

class Downloader(ABC):
    # Inherit from this class and override the methods gen_url_fname() and __init__. The latter to initialize anything
    # that you need to. gen_url_fname() should yield a tuple (fname, url) - fname being the file name to which the URL
    # should be written to. 
    @abstractmethod
    def gen_url_fname(self):
        pass

    @abstractmethod 
    def __init__(self):
        pass
    
    def download_file(self, url, local_filename, headers={'User-agent': 'Mozilla/5.0'}):
        with requests.get(url, stream=True, headers=headers) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)
        return local_filename

    def go(self):
        for fname, url in self.gen_url_fname():
            print(fname, url)
            try:
                print(f"Downloading {url} as {fname}")
                self.download_file(url, fname)
            except requests.exceptions.HTTPError as exc:
                print(f"Error downloading {url}")
                print(url, exc)

# Download prabuddha bharata magazines from 2003 to 2021
class PrabuddhaBharataYearDownloader(Downloader):
    year_begin = 0
    year_end = 0
    
    def __init__(self):
        self.year_begin = 2003
        self.year_end = 2003
        
    
    def gen_url_fname(self):
        # example URL https://advaitaashrama.org/pb/2003/122003.pdf
        for year in range(self.year_begin, self.year_end + 1):
            for month in range(1, 13):
                # return a tuple with (year, URL, filename)
                url = f"https://advaitaashrama.org/pb/{year:04}/{month:02}{year:04}.pdf"
                fname = f"{year:04}-{month:02}-pb.pdf"
                yield fname, url

# Downloader for files mentioned in an xls file (File, URL) in sheet URL
class ExcelSheetDownloader(Downloader):
    excel_filename = ""
    df = None
    
    def __init__(self):
        self.excel_filename = "download_sample.xlsx"
        converter_dic = {'File' : str, 'URL': str}
        self.df = pd.read_excel(self.excel_filename, sheet_name="URL", converters=converter_dic)
    
    def gen_url_fname(self):
        self.df = self.df.reset_index()  # make sure indexes pair with number of rows
        for index, row in self.df.iterrows():
            yield row['File'], row['URL']


if __name__ == "__main__":
    excel_downloader = ExcelSheetDownloader()
    excel_downloader.go()