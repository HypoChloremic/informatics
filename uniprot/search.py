import requests, sys
import xml.etree.ElementTree as ET
import json
import functools
from requests.models import Response
import argparse

class Uniprot:

    def gene_search(
                self,
                genes:list=["MYL2"], 
            ):
        """Performs gene search on the uniprot api

        Keyword Arguments:
            
            gene:list, will be included in the gene search. 

        Returns:
            
            responseBody:str

        """
        try: 
            assert isinstance(genes, list)
        except AssertionError as e:
            e.args += ("[genes] argument needs to be type(list)", )
            raise
            

        self.genes = genes

        self.requestURL = f"https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&gene={'%2C%20'.join(genes)}&organism=human"
        
        r = requests.get(self.requestURL, headers={ "Accept" : "application/json"})
        
        if not r.ok:
            r.raise_for_status()
            sys.exit()

        self.responseBody = r.text
        self.data = json.loads(self.responseBody)

        return self.responseBody
    
    def _assert_data(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                assert self.data
            except AssertionError as e:
                raise (AssertionError, "self.data is not defined. You have not performed a search to instantiate the object.")
            
            returned = func(self, *args, **kwargs)
            return returned

        return wrapper

    @_assert_data
    def extract_info(
                self,
                main_key:str,
                sub_key:str,
                data_key:str,
            ):
        """Will extract info from the response head
        
        Arguments:

            key:str

        """

        extracted_info = {}
        for i in range(len(self.data)):
            try:
                gene_key = self.data[i]['gene'][0]['name']['value']
                if self.data[i][main_key][0]["type"] == sub_key:
                    extracted_info[gene_key] = [self.data[i][main_key][0][data_key]]
                    print("success")
            except KeyError as e:
                print(f"Could not find <{main_key}> and <{sub_key}>\n{e}")
        
        return extracted_info
    
    @_assert_data
    def extract_function(self, main_key="comments", sub_key="FUNCTION", data_key="text"):
        extracted_info = {}
        for i in range(len(self.data)):
            try:
                gene_key = self.data[i]['gene'][0]['name']['value']
                if self.data[i][main_key][0]["type"] == sub_key:
                    extracted_info[gene_key] = self.data[i][main_key][0][data_key][0]['value']
                    print("success")
            except KeyError as e:
                print(f"Could not find <{main_key}> and <{sub_key}>\n{e}")
        
        return extracted_info

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--genes', default=None, type=str, help="", nargs="+")
        args = parser.parse_args()
        genes = args.genes
    except Exception as e:
        genes = ["MYL2", "APOE", "PAX7"]
        
    uni = Uniprot()
    uni.gene_search(genes=genes)
    output = uni.extract_function()
    for k in output:
        print("\n\n", k, "\n\n", "\tValue:\n", output[k])
