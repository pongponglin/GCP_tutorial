from __future__ import absolute_import

import logging
import argparse
import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions

'''Normalize pubsub string to json object'''
# Lines look like this:
# {'datetime': '2017-07-13', 'mac': 'FC:FC:48:AE:F6:94', 'status': 1}

#def parse_pubsub(line):
#    import json
#    record = json.loads(line)
#    return (record['mac']), (record['status']), (record['datetime'])




def run(argv=None):

    class Process(beam.DoFn):
        def process(self, element):
            from ast import literal_eval
            element = literal_eval(element)
            dict_ = {}
            dict_['mac'.encode('utf-8')] = element['mac'].encode('utf-8')
            dict_['status'.encode('utf-8')] = int(element['status'])
            dict_['datetime'.encode('utf-8')] = element['datetime'].encode('utf-8')
            yield dict_

    """Build and run the pipeline."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_topic', required=True,
        help='Input PubSub topic of the form "/topics/<PROJECT>/<TOPIC>".')
    parser.add_argument(
        '--output_table', required=True,
        help=
        ('Output BigQuery table for results specified as: PROJECT:DATASET.TABLE '
         'or DATASET.TABLE.'))
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True
    #pipeline_options.view_as(StandardOptions).project = 'PSBQ_example'

    with beam.Pipeline(argv=pipeline_args) as p:
    # Read the pubsub topic into a PCollection.
        lines = ( p | beam.io.ReadStringsFromPubSub(known_args.input_topic)
                    | "JSON row to dict" >> beam.ParDo(Process())
                    | beam.io.WriteToBigQuery(
                        known_args.output_table,
                        schema='mac:STRING,status:INTEGER,datetime:STRING',
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
                )

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()

    #python psbq.py \
    #  --runner DataflowRunner \
    #  --project ixq-web \
    #  --temp_location gs://test-njajsdnkjsdnxzm/tmp/ \
    #  --input_topic "projects/ixq-web/topics/hello" \
    #  --output_table "testdataset.test_table5" \
    #  --streaming
