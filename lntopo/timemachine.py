import sys
import time
from .common import DatasetFile
import click
import networkx as nx
from .parser import ChannelAnnouncement, ChannelUpdate, NodeAnnouncement
from tqdm import tqdm
from datetime import datetime
import json
from networkx.readwrite import json_graph


@click.group()
def timemachine():
    pass


@timemachine.command()
@click.argument("dataset", type=DatasetFile())
@click.argument("timestamp", type=int, required=False)
# @click.option('--fmt', type=click.Choice(['dot', 'gml', 'graphml', 'json'], case_sensitive=False))
def restore(dataset, timestamp=None):
    """Restore reconstructs the network topology at a specific time in the past.

    Restore replays gossip messages from a dataset and reconstructs
    the network as it would have looked like at the specified
    timestamp in the past. The network is then printed to stdout using
    the format specified with `--fmt`.

    """
    if timestamp is None:
        timestamp =    time.time()

    scid_list = []

    for m in tqdm(dataset, desc="Replaying gossip messages"):
        if isinstance(m, ChannelAnnouncement):
            scid_list.append(m.short_channel_id)

    with open('all_public_scid.json', 'w') as outfile:
        # Write the list to the file as a JSON object
        json.dump(scid_list, outfile)