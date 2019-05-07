#!/usr/bin/python
# -*- coding: UTF-8 -*-
import apache_beam as beam
import six

def count_ones(word_ones):
  (word, ones) = word_ones
  return (word, sum(ones))

def format_result(word_count):
  (word, count) = word_count
  return '%s: %d' % (word, count)

if __name__ == '__main__':
    PROJECT='ixq-web'
    BUCKET='test-njajsdnkjsdnxzm'

    argv = [
        '--project={0}'.format(PROJECT),
        '--runner=DataflowRunner',
        '--save_main_session',
        '--staging_location=gs://{0}/staging/'.format(BUCKET),
        '--temp_location=gs://{0}/staging/'.format(BUCKET),
        #'--streaming=True'
    ]
    pipeline = beam.Pipeline(argv=argv)

    lines = pipeline | beam.io.ReadStringsFromPubSub(
        subscription='projects/ixq-web/subscriptions/mysub')

    counts = (lines
            | 'split' >> (beam.ParDo(WordExtractingDoFn())
                          .with_output_types(six.text_type))
            | 'pair_with_one' >> beam.Map(lambda x: (x, 1))
            | beam.WindowInto(window.FixedWindows(15, 0))
            | 'group' >> beam.GroupByKey()
            | 'count' >> beam.Map(count_ones))

    output = counts | 'format' >> beam.Map(format_result)
    output | beam.io.WriteStringsToPubSub('projects/ixq-web/topics/hello')

    pipeline.run().wait_until_finish()
