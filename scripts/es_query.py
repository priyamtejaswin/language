#!/usr/bin/env python
"""
created at: Sat 13 Feb 2021 02:30:17 AM EST
created by: Priyam Tejaswin

Script and function for querying the local ES cluster.
"""


from elasticsearch import Elasticsearch
import os
import plac
import sys
from tqdm import tqdm


def retrieve(es, qs, topk=5):
    """
    Retrieve `topk` docs for the query string `qs`.
    `es` is the Elasticsearch object.
    """
    assert isinstance(topk, int) and topk > 0
    query = {
                "more_like_this" : {
                    "fields" : ["description"],
                    "like" : qs,
                    "min_term_freq" : 1,
                    "min_doc_freq" : 1
                }
            }

    response = es.search(index='wiki_blocks', body={'query': query}, size=topk)
    hits = response['hits']['hits']
    return [x['_source']['description'] for x in hits]


@plac.pos('queries_file', "Path to list of queries.")
@plac.pos('output_file', "Path to dump the retrieved results and line numbers.")
def main(queries_file, output_file):
    """
    Sequentially query the ES cluster and save results.
    `output_file` will contain the docs.
    `output_file + '.nbs'` will have number of docs per query.
    """
    assert os.path.exists(queries_file), "%s is not valid." % queries_file
    assert not os.path.exists(output_file), "%s already exists!" % output_file

    es = Elasticsearch()
    numqs = 0
    with open(queries_file) as fp:
        for line in fp:
            numqs += 1

    progbar = tqdm(unit='queries', total=numqs)
    answers, indices = [], []
    ix = 0
    with open(queries_file) as fp:
        for line in fp:
            qs = line.strip()
            hits = retrieve(es, qs)

            answers.extend(hits)
            ix += len(hits)
            indices.append(ix)

            if len(indices) == 10000:
                with open(output_file, 'a') as fp:
                    fp.write('\n'.join(answers) + '\n')
                with open(output_file + '.nbs', 'a') as fp:
                    fp.write('\n'.join([str(_) for _ in indices]) + '\n')

                answers, indices = [], []

            progbar.update(1)

    if indices:
        with open(output_file, 'a') as fp:
            fp.write('\n'.join(answers) + '\n')
        with open(output_file + '.nbs', 'a') as fp:
            fp.write('\n'.join([str(_) for _ in indices]) + '\n')

    print("Done. Check %s and the `.nbs` file for results." % output_file)


if __name__ == '__main__':
    plac.call(main)

