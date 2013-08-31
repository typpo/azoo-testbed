#!/usr/bin/env python

from boto.s3.connection import S3Connection
import multiprocessing
import sys
import os
import time
import aws_config
import fitsprocess
import util

RAW_DIR = 'raw'
PROCESSED_DIR = 'processed'

conn = S3Connection(aws_config.ACCESS_KEY, aws_config.SECRET_KEY)
bucket = conn.get_bucket('asteroidzoo')

print 'Loading all keys...'
fitskeys = [key for key in bucket.list() if key.name.endswith('arch.H')]
count = 0
total = len(fitskeys)

def process_key(key):
  count = total = 0
  #count += 1
  print 'Processing %s... (%d/%d)' % (key.name, count, total)

  raw_filepath = '%s/%s' % (RAW_DIR, key.name)
  processed_filepath = '%s/%s' % (PROCESSED_DIR, key.name)
  # Remove all spaces; hdcompress breaks on paths with spaces
  raw_filepath = raw_filepath.replace(' ', '_')

  util.make_dir_for_file(raw_filepath)

  key.get_contents_to_filename(raw_filepath)

  newfiles = fitsprocess.process(raw_filepath)
  for filepath in newfiles:
    key = bucket.new_key(filepath)
    key.set_contents_from_filename(filepath)
    os.remove(filepath)
  os.remove(raw_filepath)
  os.remove(raw_filepath.replace('arch.H', 'arch'))


#for key in fitskeys:
#  process_key(key)

pool = multiprocessing.Pool(multiprocessing.cpu_count())
pool.map(process_key, fitskeys[:1000])

#test = bucket.get_key('Test_Folder/Chelya_orb.png')
#test.set_canned_acl('public-read')
