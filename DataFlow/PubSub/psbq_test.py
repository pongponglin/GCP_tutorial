import logging
import argparse
import apache_beam as beam
import time
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions

def run(argv = None):

    ######################### setting #########################
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

    ######################## function ########################
    def function_json_df(element):
        import pandas as pd
        import numpy as np
        from pandas.io.json import json_normalize
        import json
        import requests
        import datetime as dt
        from datetime import datetime as ddt
        js = json.loads(element)
        data = json_normalize(js)
        assoc = [] ; mac = [] ; rssi = [] ; tm = [] ; ap = [] ; hw = [] ; time = []
        for j in range(len(data['results'])):
            if pd.isnull(data['results'][j]):
                continue
            for i in range (len(data['results'][j][0]['sta'])):
                mac.extend([data['results'][j][0]['sta'][0]['mac']]*len(data['results'][j][0]['sta'][i]['assoc']))
                ap.extend([data['results'][j][0]['ap']]*len(data['results'][j][0]['sta'][i]['assoc']))
                hw.extend([data['results'][j][0]['hw']]*len(data['results'][j][0]['sta'][i]['assoc']))
                time.extend([data['results'][j][0]['time']]*len(data['results'][j][0]['sta'][i]['assoc']))
                assoc.extend(data['results'][j][0]['sta'][i]['assoc'])
                rssi.extend(data['results'][j][0]['sta'][i]['rssi'])
                tm.extend(data['results'][j][0]['sta'][i]['tm'])

        DATA = pd.DataFrame(np.column_stack([ap,hw,time,assoc,mac,rssi,tm]),
                  columns =  ['ap','hw','time','assoc','mac','rssi','tm'])

        DATA['rssi'] = pd.to_numeric( DATA['rssi'])

        for item in range(DATA.shape[0]):
            each_log = DATA.iloc[item,].to_dict()
            yield each_log



    ########################### run ##########################
    with beam.Pipeline(argv=pipeline_args) as pipeline:
        (
        pipeline | 'ReadingPubSub:UserLog' >> beam.io.ReadStringsFromPubSub(known_args.input_topic)
                 | 'Transform' >> beam.FlatMap(lambda item : function_json_df(element = item))
                 | 'UploadBQ' >> beam.io.WriteToBigQuery(known_args.output_table,
                        schema='ap:STRING,hw:STRING,time:STRING,assoc:STRING,mac:STRING,rssi:INTEGER,tm:STRING',
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
        )

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()

    # python psbq_test.py \
    #  --runner DataflowRunner \
    #  --project ixq-web \
    #  --temp_location gs://test-njajsdnkjsdnxzm/tmp/ \
    #  --input_topic "projects/ixq-web/topics/Next" \
    #  --output_table "testdataset.test_table10" \
    #  --streaming

    #python psbq_test.py       --runner DataflowRunner       --project aiii-wifi       --temp_location gs://aiii-wifi.appspot.com/tmp       --input_topic "projects/aiii-wifi/topics/userLogs"       --output_table "msd_wifi.userlog"       --streaming
