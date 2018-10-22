#!/usr/bin/env python

import dz
import click
from urllib.parse import urljoin
import requests

baseurl_default = 'https://dam.acme.com'

products = {'DC': '3AD2C82D-EE80-40CD-A404-8D1AD124639D',
            'MM': 'F10ABF14-6FB1-4515-A16A-0C6C02376989',
            'ACCC': '2350F493-D4AB-48AE-AC07-562242104035',
            'MSOC': '726D5F54-C5FF-4F78-B931-167DAAAE389B',
            'DFS': 'AC045BF0-C538-4397-BC13-EF6A61DF6A82',
            'VP': 'F77A0B88-F80A-45CE-A5B9-65B6E7817FBE',
            }
product_choices = products.keys()

def getEndpoint(url, params):
    r = requests.request("GET", url, params=params)
    return r.status_code, r.text



@click.group()
@click.pass_context
@click.option('--baseurl', required=True, help='Base URL of the Digizuite DAM Center.', prompt='Enter a URL to a DAM Center instance', default=baseurl_default)
@click.option('--username', required=True, prompt='Please enter the API username', default='System', help='API username')
@click.option('--password', required=True, prompt='Please enter the API user password', help='API password.')
def cli(ctx, baseurl, username, password):
    #Check for defaults
    if baseurl == baseurl_default:
        print('Please enter a non-default value for baseurl')
        return False

    dzClient = dz.Client(baseurl, username, password)
    ctx.ensure_object(dict)
    ctx.obj['client'] = dzClient


@cli.command()
@click.pass_context
def regenall(ctx):
    """
    Regenerate and repopulate all searches in all products.
    """
    c = ctx.obj['client']
    if not c.login:
        return False

    r = requests.request("GET", urljoin(c.BASE_URL, '/apiproxy/JobService.js'), params={'accesskey': c.login, 'method': 'GenerateAndPopulateAllSearches'})
    print(r.status_code, r.text)

    if r.status_code == 200:
        return True
    else:
        return False


@cli.command()
@click.pass_context
@click.option('--product', required=True, type=click.Choice(product_choices), prompt='Please enter the product GUID', default='DC', help='the product GUID')
def regenone(ctx, product):
    """
    Regenerate and repopulate all searches in a single product
    """

    global products

    c = ctx.obj['client']
    if not c.login:
        return False

    product_guid = products[product]

    r = requests.request("GET", urljoin(c.BASE_URL, '/apiproxy/JobService.js'), params={'accesskey': c.login, 'method': 'GenerateAndPopulateAllSearchesForProduct', 'productGuid': product_guid})
    print(r.status_code, r.text)

    if r.status_code == 200:
        return True
    else:
        return False


@cli.command()
@click.pass_context
def repopall(ctx):
    """
    Repopulate all searches in all products
    """
    c = ctx.obj['client']
    if not c.login:
        return False

    r = requests.request("GET", urljoin(c.BASE_URL, '/apiproxy/JobService.js'), params={'accesskey': c.login, 'method': 'PopulateAllSearches'})
    print(r.status_code, r.text)

    if r.status_code == 200:
        return True
    else:
        return False

if __name__ == '__main__':
    cli(obj={})