#!/usr/bin/python
# -*- coding: UTF-8 -*-
import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions

import argparse
import json

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_subscription', help=('Input PubSub subscription of the form '
          '"projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."'))
    parser.add_argument(
      '--output_table', required=True,
      help=
      ('Output BigQuery table for results specified as: PROJECT:DATASET.TABLE '
       'or DATASET.TABLE.'))
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True
    pipeline_options.view_as(StandardOptions).project = 'PSBQ_example'
    pipeline = beam.Pipeline(options=pipeline_options)

    message = (pipeline
                | 'Reading PubSub' >> beam.io.ReadFromPubSub(subscription=known_args.input_subscription)
                | beam.WindowInto(window.FixedWindows(2, 0))
                | 'Transform' >> beam.FlatMap(lambda item : json.loads(item))
                | 'UploadBQ' >> beam.io.WriteToBigQuery('test_table4', 'testdataset', 'ixq-web', schema='a:INTEGER,b:STRING'))

    pipeline.run().wait_until_finish()

if __name__ == '__main__':
    run()
