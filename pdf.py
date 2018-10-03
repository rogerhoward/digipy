#!/usr/bin/env python

import PyPDF2
import dz
import click
from itertools import chain


def unique_words(text):
    return set([word.strip() for word in text.split()])

def getPDFText(path):
    # filename = 'enter the name of the file here' 
    #open allows you to read the file
    pdfFileObj = open(path,'rb')
    #The pdfReader variable is a readable object that will be parsed
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #discerning the number of pages will allow us to parse through all #the pages
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    #The while loop will read each page
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()

    return ' '.join(unique_words(text))



@click.command()
@click.argument('path')
def main(path):
    """A Digizuite API client which imports a hierarchy into a tree field."""

    # Create a Client instance
    # dzClient = dz.Client(baseurl, username, password)

    # Ask the Client to get this asset record
    # asset = dzClient.getAssetURL(assetid)
    # print(asset)

    text = getPDFText(path)
    print(text)

if __name__ == '__main__':
    main()

