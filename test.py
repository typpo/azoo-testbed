#!/usr/bin/env python

import sys
import pyfits
import png
import binascii

hdulist = pyfits.open('fits.fits')
print hdulist.info()

im = hdulist[0]
'''
print im
im.header['ZIMAGE'] = 'T'
im.header['ZCMPTYPE'] = 'HCOMPRESS_1'
im.header['ZBITPIX'] = 16
im.header['ZNAXIS'] = 2
im.header['ZNAXIS1'] = 4110
im.header['ZNAXIS2'] = 4096

#im.update_header()

hdulist.writeto('poop.fits', clobber=True)
'''

print len(im.data)

hdulist.writeto('uncompressed.fits', clobber=True)
sys.exit(1)

IMAGE_WIDTH = 2000

f = open('fits.fits', 'rb')
headerbytes = f.read(8000)

bytes = 0
pixelcount = 0
rows = []
flatpixels = []
more = True
out_data = open('data.data', 'wb')
while more:
  row = []
  for px in range(IMAGE_WIDTH):
    pixel = f.read(2)  # 2 bytes per pixel
    if pixel == '':
      print 'EOF. %d bytes, %d pixelcount' % (bytes, pixelcount)
      print 'Done.'
      more = False
      break
    out_data.write(pixel)
    bytes += 2
    pixelcount += 1
    hexstr = ''.join(["{0:x}".format(ord(b)) for b in pixel])
    intval = int(hexstr, 16)
    row.append(intval)
    flatpixels.append(intval)
    #print binascii.hexlify(pixel)
    #print intval
  rows.append(row)

sys.exit(1)
out_data.close()

out = open('png.png', 'w')
w = png.Writer(IMAGE_WIDTH, len(rows), greyscale=True, bytes_per_sample=2)
#w.write(out, rows)
w.write_array(out, flatpixels)

"""
hdulist = pyfits.open('fits.fits')

im = hdulist[0]
im.update_header()
im.size = bytes
"""
