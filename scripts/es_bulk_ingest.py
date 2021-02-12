#!/usr/bin/env python
# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information


"""Script that indexes the English Wiki paragraphs to a local ES cluster."""
# https://github.com/elastic/elasticsearch-py/blob/master/examples/bulk-ingest/bulk-ingest.py


import os
import sys
import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk


def create_index(client):
    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index="wiki_blocks",
        ignore=400,
    )


def generate_actions(DATASET_PATH):
    """Reads the file and for each row
    yields a single document. This function is passed into the bulk()
    helper to create many documents in sequence.
    """
    with open(DATASET_PATH, mode="r") as f:
        for line in f:
            doc = {
                '_index': 'wiki_blocks',
                '_type': '_doc',
                'description': line.strip()
            }
            yield doc


def main():
    fpath = sys.argv[1]
    print("Input file path: %s" % fpath)
    assert os.path.exists(fpath), "Input file path does not exist."

    print("Calculating number of blocks in dataset...")
    with open(fpath) as fp:
        number_of_docs = 0
        for line in fp:
            number_of_docs += 1
    print("Number of docs: %d" % number_of_docs)

    client = Elasticsearch()
    print("Creating an index...")
    create_index(client)

    print("Indexing documents...")
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, action in streaming_bulk(
        client=client, index="wiki_blocks", actions=generate_actions(fpath),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, number_of_docs))


if __name__ == "__main__":
    main()
