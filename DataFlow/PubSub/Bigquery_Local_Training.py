#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import argparse ## 處理 shell 上 python input 的參數，但在local處理上並不會用到
import apache_beam as beam
import time
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions

def run(argv = None):
    ######################### setting #########################
    #parser = argparse.ArgumentParser()
    #parser.add_argument(
    #    '--input_topic', required=True,
    #    help='Input PubSub topic of the form "/topics/<PROJECT>/<TOPIC>".')
    #parser.add_argument(
    #    '--output_table', required=True,
    #    help=
    #    ('Output BigQuery table for results specified as: PROJECT:DATASET.TABLE '
    #     'or DATASET.TABLE.'))
    #known_args, pipeline_args = parser.parse_known_args(argv)

    #pipeline_options = PipelineOptions(pipeline_args)
    #pipeline_options.view_as(SetupOptions).save_main_session = True
    #pipeline_options.view_as(StandardOptions).streaming = True

    ######################## function ########################
    def function_processing(element):
        from ast import literal_eval
        element = literal_eval(element)
        dict_ = {}
        dict_['col1'.encode('utf-8')] = element['col1'].encode('utf-8')
        dict_['col2'.encode('utf-8')] = int(element['col2'])*5
        dict_['col3'.encode('utf-8')] = element['col3'].encode('utf-8')
        yield dict_


    ########################### run ##########################
    with beam.Pipeline(argv=['--project=ixq-web']) as pipeline:
        (
        pipeline | 'ReadingPubSub:UserLog' >> beam.io.ReadFromText('./ReadText_dictionary.txt')
                 | 'Transform' >> beam.FlatMap(lambda item : function_processing(element = item))
                 | 'UploadBQ' >> beam.io.WriteToBigQuery('training_psbq', 'testdataset', 'ixq-web',
                        schema='col1:STRING,col2:INTEGER,col3:STRING',
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
        )

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()

    ## python Bigquery_Local_Training.py
