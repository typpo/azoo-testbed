#!/usr/bin/env python

import sys
import os
import f2n
import pyfits

OUTPUT_DIR = 'processed'
FRAME_SIZE = 512    # in pixels
IMAGE_HEIGHT = 4096
IMAGE_WIDTH = 4110
OVERLAP_RATIO = .11

def decompress(filepath):
  os.system('hdecompress %s' % filepath)
  return filepath.replace('arch.H', 'arch')

def get_cropped_image(filepath, xmin, xmax, ymin, ymax):
  im = f2n.fromfits(filepath)      # TODO don't read the file each time
  im.crop(xmin, xmax, ymin, ymax)
  return im

def process_cropped_frame(im, filename, framenum):
  # TODO save raw images

  # Make log scaled image - png
  im.makepilimage('log', negative=False)
  im.tonet('%s/%s-%d-scaled.png' % (OUTPUT_DIR, filename, framenum))

  # Make negative log scaled image - png
  im.makepilimage('log', negative=True)
  im.tonet('%s/%s-%d-negative.png' % (OUTPUT_DIR, filename, framenum))


def process(compressed_filepath):
  filepath = decompress(compressed_filepath)
  filename = os.path.splitext(filepath)[0]

  xmin = ymin = 0
  xmax = ymax = FRAME_SIZE
  num_frames = 0

  # Crop image into multiple overlapping frames
  overlap_px_delta = (1.-OVERLAP_RATIO) * FRAME_SIZE
  # TODO assumes perfect fit - do we ever deal with edges?
  while xmax < IMAGE_WIDTH:
    while ymax < IMAGE_HEIGHT:
      num_frames += 1
      im_frame = get_cropped_image(filepath, xmin, xmax, ymin, ymax)
      process_cropped_frame(im_frame, filename, num_frames)

      ymax += overlap_px_delta
      ymin += overlap_px_delta
    xmax += overlap_px_delta
    xmin += overlap_px_delta


if __name__ == "__main__":
  if len(sys.argv) > 1:
    process(sys.argv[1])
  else:
    print 'usage: process filepath.arch.H'
