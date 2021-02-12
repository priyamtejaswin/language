#!/usr/bin/env python
"""
created at: Fri 12 Feb 2021 07:37:47 AM EST
created by: Priyam Tejaswin

Extracts content from the Blocks Tfr file.
"""


import os
import plac
from tqdm import tqdm
import tensorflow as tf


@plac.pos('tfr_path', "Path to Tf Records file.")
@plac.pos('output_path', "Path to store text. Must be new.")
def main(tfr_path, output_path):
    print("TFRecords path: %s" % tfr_path)
    print("Output path: %s" % output_path)
    assert os.path.exists(tfr_path), "TFRecords path is bad."
    assert not os.path.exists(output_path), "Output path already exists!"

    dataset = tf.data.TFRecordDataset([tfr_path])
    c = 0
    total = 0
    towrite = []
    for row in tqdm(dataset):
        total += 1
        text = row.numpy().strip().lower()
        text = str(text, 'utf-8')
        towrite.append(text)
        c += 1

        if c == 100000:
            with open(output_path, 'a') as fp:
                fp.write('\n'.join(towrite) + '\n')

            c = 0
            towrite = []

    if towrite:
        with open(output_path, 'a') as fp:
            fp.write('\n'.join(towrite) + '\n')

    print("Done. Written %d blocks to %s" % (total, output_path))


if __name__ == '__main__':
    plac.call(main)

