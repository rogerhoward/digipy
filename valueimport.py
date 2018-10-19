#!/usr/bin/env python

import dz
import click


@click.command()
@click.option('--file', required=True, type=click.Path(exists=True), help='Path to import file. See README for format.')
@click.option('--field', required=True, type=int, help='ID of field to import into.')
@click.option('--baseurl', required=True, help='Base URL of the Digizuite DAM Center.')
@click.option('--username', required=True, default='System', help='API-capable Digizuite username; defaults to System.')
@click.option('--password', required=True, help='Password for the provided username.')
def main(file, field, baseurl, username, password):
    """A Digizuite API client which imports a value list into a controlled field."""

    # Create a Client instance
    dzClient = dz.Client(baseurl, username, password)

    # Ask the Client to import the terms file
    dzClient.importValuesToField(file, field)

if __name__ == '__main__':
    main()

