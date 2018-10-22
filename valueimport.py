#!/usr/bin/env python

import dz
import click

baseurl_default = 'https://dam.acme.com'


@click.command()
@click.option('--baseurl', required=True, help='Base URL of the Digizuite DAM Center.', prompt='Enter a URL to a DAM Center instance', default=baseurl_default)
@click.option('--username', required=True, default='System', help='API-capable Digizuite username; defaults to System.', prompt='Enter a username for the DAM Center')
@click.option('--password', required=True, help='Password for the provided username.', prompt='Enter the MD5 hash of the password for the user you previously entered')
@click.option('--field', required=True, type=int, help='ID of field to import into.', prompt='Enter the Metadata field label ID for the field to import values into')
@click.option('--field_type', required=True, type=click.Choice(['combo', 'tree']), help='Type of field to import into.', prompt='Enter combo|tree to determine what type of import to perform')
@click.option('--file', required=True, type=click.Path(exists=True), help='Path to import file. See README for format.', prompt="Enter a valid path to a data file for import")
def main(baseurl, username, password, field, field_type, file):
    """A Digizuite API client which imports a value list into a controlled field."""

    #Check for defaults
    if baseurl == baseurl_default:
        print('Please enter a non-default value for baseurl')
        return False

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
