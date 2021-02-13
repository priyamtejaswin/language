#!/usr/bin/env python
"""
created at: Sat 13 Feb 2021 10:00:52 AM EST
created by: Priyam Tejaswin

From each training sample, read the Bio, and save a query string.
"""


import os
import plac
import re
import sys
from tqdm import tqdm


def create_wikibio_query(bio):
    sep = '<sep>'
    clean = []
    s, e = '', ''

    for word in bio.split():
        if len(re.findall(':', word)) != 1:
            continue

        key, val = word.split(':')
        if val != '<none>':
            match = re.search(r'_[0-9]+$', key)
            if match is None:
                # clean.append(key)
                clean.append(val)
                clean.append(sep)

                s = ''
                e = ''
            else:
                holder = key[:match.start()]
                if s:
                    if s == holder:
                        e += val + ' '
                    else:
                        # clean.append(s)
                        clean.append(e.strip())
                        clean.append(sep)

                        s = holder
                        e = val + ' '

                else:
                    s = holder
                    e = val + ' '

    if s:
        # clean.append(s)
        clean.append(e.strip())
        clean.append(sep)

    tokens = ' '.join(clean).strip(sep).strip()
    tokens = ' '.join(tokens.split()[:80])

    query = [t for t in tokens.split() if t != sep]
    return ' '.join(query)


@plac.pos('source_file', "Path to WikiBio input sources.")
@plac.pos('output_file', "Path to output queries file.")
def main(source_file, output_file):
    """
    source_file: WikiBio file. Each line has 1 bio.
    output_file: File with queries. Must be new.
    """
    assert os.path.exists(source_file), "%s does not exist."
    assert not os.path.exists(output_file), "%s already exists!"

    with open(source_file) as fp:
        queries = [create_wikibio_query(bio.strip()) for bio in tqdm(fp.readlines())]

    batch = []
    for q in tqdm(queries):
        batch.append(q)
        if len(batch) == 100000:
            with open(output_file, 'a') as fp:
                fp.write('\n'.join(batch) + '\n')
            batch = []

    if len(batch):
        with open(output_file, 'a') as fp:
            fp.write('\n'.join(batch) + '\n')

    print("Queries written to %s" % output_file)


if __name__ == '__main__':
    plac.call(main)

