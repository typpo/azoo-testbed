#!/usr/bin/env python

import sys
import os
import f2n
import pyfits
import json
import util

OUTPUT_DIR = 'processed'
RAW_DIR = 'raw'
FRAME_SIZE = 512    # in pixels
IMAGE_HEIGHT = 4096
IMAGE_WIDTH = 4110
OVERLAP_RATIO = .11

def decompress(filepath):
  os.system('hdecompress "%s"' % filepath)
  return filepath.replace('arch.H', 'arch')

def get_cropped_image(filepath, xmin, xmax, ymin, ymax):
  im = f2n.fromfits(filepath)      # TODO don't read the file each time
  im.crop(xmin, xmax, ymin, ymax)
  return im

def process_cropped_frame(im, filename, framenum):
  # Make log scaled image - png
  im.makepilimage('log', negative=False)
  scaled_path = '%s/%s-%d-scaled.png' % (OUTPUT_DIR, filename, framenum)
  im.tonet(scaled_path)

  # Make negative log scaled image - png
  im.makepilimage('log', negative=True)
  negative_path = '%s/%s-%d-negative.png' % (OUTPUT_DIR, filename, framenum)
  im.tonet(negative_path)

  return {
      'scaled_path': scaled_path,
      'negative_path': negative_path,
      }


def process(compressed_filepath):
  filepath = decompress(compressed_filepath)
  filename = os.path.splitext(filepath)[0]
  if filename.startswith(RAW_DIR):
    # this is ugly - output dir should be one of the inputs
    filename = filename.replace('%s/' % RAW_DIR, '')

  util.make_dir_for_file('%s/%s' % (OUTPUT_DIR, filename))

  xmin = ymin = 0
  xmax = ymax = FRAME_SIZE
  num_frames = 0

  # Crop image into multiple overlapping frames
  overlap_px_delta = (1.-OVERLAP_RATIO) * FRAME_SIZE
  # TODO assumes perfect fit - do we ever deal with edges?
  metadatas = []
  while xmax < IMAGE_WIDTH:
    while ymax < IMAGE_HEIGHT:
      num_frames += 1
      im_frame = get_cropped_image(filepath, xmin, xmax, ymin, ymax)
      metadata = process_cropped_frame(im_frame, filename, num_frames)

      metadata['crop'] = {
          'xmin': xmin,
          'xmax': xmax,
          'ymin': ymin,
          'ymax': ymax,
          }
      metadatas.append(metadata)
      ymax += overlap_px_delta
      ymin += overlap_px_delta
    xmax += overlap_px_delta
    xmin += overlap_px_delta

    f = open('%s/%s.json' % (OUTPUT_DIR, filename), 'w')
    f.write(json.dumps({
      'processed_images': metadatas,
      'original_path': compressed_filepath
      }, indent=2))
    f.close()


if __name__ == "__main__":
  if len(sys.argv) > 1:
    process(sys.argv[1])
  else:
    print 'usage: process filepath.arch.H'
