A dead simple MJPEG (motion JPEG) streaming video client in Python using
only the standard library.

Example:

```python
for jpegdata in mjpegc.MJPEGClient("http://camera.example.com/mjpegstream"):
    print "Found a JPEG-encoded frame %d bytes long." % len(jpegdata)
```
