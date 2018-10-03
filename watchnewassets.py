#!/usr/bin/env python

# python watchnewassets.py C:\Users\rho\Desktop\watch_test
# python watchnewassets.py C:\Users\rho\Desktop\watch_test --baseurl="http://acme.dzrho.com" --username="System" --password="b7aef055d80a47feb8f715740d15d37c"

# .\watchnewassets.exe C:\Storage\acme.dzrho.com\DMM\Assets --baseurl="http://acme.dzrho.com" --username="System" --password="b7aef055d80a47feb8f715740d15d37c"


import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
import os
import click
import gv
import dz

GOOGLE_VISION_API_KEY = os.environ.get('GOOGLE_VISION_API_KEY', None)
DZ_CLIENT = None

class Watcher:
    DIRECTORY_TO_WATCH = None

    def __init__(self, path):
        self.DIRECTORY_TO_WATCH = path
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    def get_asset_id(self, path):
        assetid = os.path.basename(path).split("_")[0]
        print("assetid", assetid)
        return assetid

    def check_name(self, path):
        # basename = os.path.splitext(os.path.basename(path))[0]
        # if basename.endswith('_2'):
        if path.endswith('_2.jpg'):
            return True
        else:
            return False

    # @staticmethod
    def on_any_event(self, event):
        global DZ_CLIENT

        if event.is_directory:
            return None

        elif event.event_type == 'created' and self.check_name(event.src_path):
            # Take any action here when a file is first created.

            print("created: ", event.src_path)
            assetid = self.get_asset_id(event.src_path)

            print("assetidx: ", assetid)

            # Ask the Client to get this asset record
            displayid, asseturl = DZ_CLIENT.getAssetURL(assetid)
            print(asseturl)

            c = gv.GoogleVision(GOOGLE_VISION_API_KEY, asseturl)
            kw = c.keywords()
            print(kw)

            DZ_CLIENT.setKeywords(displayid, '10438', kw)





@click.command()
@click.argument('path')
@click.option('--baseurl', required=True, help='Base URL of the Digizuite DAM Center.')
@click.option('--username', required=True, default='System', help='API-capable Digizuite username; defaults to System.')
@click.option('--password', required=True, help='Password for the provided username.')
def watch(path, baseurl, username, password):

    global DZ_CLIENT

    # Create a Client instance
    DZ_CLIENT = dz.Client(baseurl, username, password)

    w = Watcher(path)
    w.run()


if __name__ == "__main__":
    watch()