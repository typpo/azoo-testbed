#!/usr/bin/env python

import sys
import os
import f2n
import pyfits

#hdulist = pyfits.open('fits.fits')
#hdulist = pyfits.open('01_12DEC08_FL0802_0001.fits')

def decompress(filepath):
  os.system('hdecompress %s' % filepath)
  return filepath.replace('arch.H', 'arch')

def process(compressed_filepath):
  filepath = decompress(compressed_filepath)

  im = f2n.fromfits(filepath)
  im.makepilimage('lin', negative=False)
  im.tonet('nettest.png')

if __name__ == "__main__":
  if len(sys.argv) > 1:
    process(sys.argv[1])
  else:
    print 'usage: process filepath.arch.H'
