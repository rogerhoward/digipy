#!/usr/bin/env python

import dz
import click
from urllib.parse import urljoin


def mode_switch(ctx, param, value):
    print(ctx, param, value)





@click.group()
@click.pass_context
@click.option('--baseurl', required=True, prompt='Please enter the base URL for a Digizuite DAM Center', default='https://damcenter.com', help='Base URL of the Digizuite DAM Center.')
@click.option('--username', required=True, prompt='Please enter the API username', default='System', help='API username')
@click.option('--password', required=True, prompt='Please enter the API user password', help='API password.')
def cli(ctx, baseurl, username, password):
    dzClient = dz.Client(baseurl, username, password)

    ctx.ensure_object(dict)
    ctx.obj['client'] = dzClient


@cli.command()
@click.pass_context
def GenerateAndPopulateAllSearches(ctx):
    """
    GenerateAndPopulateAllSearches is...
    """
    c = ctx.obj['client']

    template = '/apiproxy/JobService.js?accesskey={apikey}&method=GenerateAndPopulateAllSearches'.format({'apikey': c.apikey})
    print(template)
    print('GenerateAndPopulateAllSearches is running', c.BASE_URL)


@cli.command()
@click.pass_context
def GenerateAndPopulateAllSearchesForProduct(ctx):
    template = '/apiproxy/JobService.js?accesskey={apikey}&method=GenerateAndPopulateAllSearchesForProduct&productGuid={product}'


@cli.command()
@click.pass_context
def PopulateAllSearches(ctx):
    template = '/apiproxy/JobService.js?accesskey={apikey}&method=PopulateAllSearches'

if __name__ == '__main__':
    cli(obj={})