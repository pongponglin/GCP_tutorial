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
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.transforms.trigger import AfterProcessingTime, AccumulationMode

def run(argv = None):
    ######################### setting #########################
    parser = argparse.ArgumentParser()
    #parser.add_argument(
    #    '--input_topic', required=True,
    #    help='Input PubSub topic of the form "/topics/<PROJECT>/<TOPIC>".')
    parser.add_argument(
        '--output_table', required=True,
        help=
        ('Output BigQuery table for results specified as: PROJECT:DATASET.TABLE '
         'or DATASET.TABLE.'))
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True

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
    QUERY = "SELECT COUNT(ap) as num, COUNT(DISTINCT(mac)) as user FROM `testdataset.test_table10`"

    with beam.Pipeline(argv=pipeline_args) as pipeline:
        (
        pipeline | 'ReadingPubSub:UserLog' >> beam.io.Read(beam.io.BigQuerySource(query=QUERY, use_standard_sql=True))
                 | beam.WindowInto(beam.window.FixedWindows(1 * 60))
                 | 'UploadBQ' >> beam.io.WriteToBigQuery(known_args.output_table,
                        schema='num:INTEGER,user:INTEGER',
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
        )





    #with beam.Pipeline(argv=pipeline_args) as pipeline:
    #    (
    #    pipeline | 'ReadingPubSub:UserLog' >> beam.io.Read(beam.io.BigQuerySource(query=QUERY, use_standard_sql=True))
    #             | beam.WindowInto(beam.window.FixedWindows(1 * 60),
    #                            trigger=AfterProcessingTime(3 * 60),
    #                            accumulation_mode=AccumulationMode.DISCARDING )
    #             | 'UploadBQ' >> beam.io.WriteToBigQuery(known_args.output_table,
    #                    schema='num:INTEGER,user:INTEGER',
    #                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
    #                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
    #    )

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
    ## 創一個 testtopic 的 PubSub topic
    ## python Window_BigQuery_training.py    --runner DataflowRunner       --project ixq-web    --job_name windowtraining    --temp_location gs://test-njajsdnkjsdnxzm/tmp        --output_table "testdataset.training_windowbq"       --streaming
