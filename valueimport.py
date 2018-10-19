#!/usr/bin/env python

import dz
import click


@click.command()
@click.option('--baseurl', required=True, help='Base URL of the Digizuite DAM Center.')
@click.option('--username', required=True, default='System', help='API-capable Digizuite username; defaults to System.')
@click.option('--password', required=True, help='Password for the provided username.')
@click.option('--field', required=True, type=int, help='ID of field to import into.')
@click.option('--type', required=True, type=click.Choice(['combo', 'tree']), help='Type of field to import into.')
@click.option('--file', required=True, type=click.Path(exists=True), help='Path to import file. See README for format.')
def main(baseurl, username, password, field, field_type, file):
    """A Digizuite API client which imports a value list into a controlled field."""

    # Create a Client instance
    dzClient = dz.Client(baseurl, username, password)

    if field_type == 'combo':
        # Ask the Client to import a flat list of labels and values
        dzClient.importFlatValues(file, field)
    elif field_type == 'tree':
        # Ask the Client to import a hierarchical list of labels
        dzClient.importTreeValues(file, field)

if __name__ == '__main__':
    main()
