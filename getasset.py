#!/usr/bin/env python

import dz
import click


@click.command()
@click.option('--baseurl', required=True, help='Base URL of the Digizuite DAM Center.')
@click.option('--username', required=True, default='System', help='API-capable Digizuite username; defaults to System.')
@click.option('--password', required=True, help='Password for the provided username.')
@click.option('--assetid', required=True, help='Unique asset ID.')
def main(baseurl, username, password, assetid):
    """A Digizuite API client which imports a hierarchy into a tree field."""

    # Create a Client instance
    dzClient = dz.Client(baseurl, username, password)

    # Ask the Client to get this asset record
    asset = dzClient.getAssetURL(assetid)
    print(asset)

if __name__ == '__main__':
    main()
