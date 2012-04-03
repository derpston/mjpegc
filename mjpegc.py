import httplib
import urlparse

class MJPEGClient:
    """An iterable producing JPEG-encoded video frames from an MJPEG stream URL."""

    def __init__(self, url):
        self._url = urlparse.urlparse(url)

        h = httplib.HTTP(self._url.netloc)
        h.putrequest('GET', self._url.path)  
        h.endheaders()  
        errcode, errmsg, headers = h.getreply()  

        if errcode == 200:
            self._fh = h.getfile()
        else:
            raise RuntimeError("HTTP %d: %s" % (errcode, errmsg))

    def __iter__(self): 
        """Yields JPEG-encoded video frames."""

        # TODO: handle chunked encoding delimited by marker instead
        # of content-length.

        while True:
            length = None
            while True:
                line = self._fh.readline()

                if line.startswith("Content-Length: "):
                    length = int(line.split(" ")[1])

                # Look for an empty line, signifying the end of the headers.
                if length is not None and line == "\r\n":
                    break

            yield self._fh.read(length)

if __name__ == "__main__":
    import Image
    import StringIO
    import sys

    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s http://camera.example.com/mjpegstream" % sys.argv[0]
        raise SystemExit

    for jpegdata in MJPEGClient(sys.argv[1]):
        frame = Image.open(StringIO.StringIO(jpegdata))
        print "%d bytes, %dx%d pixels" % (len(jpegdata), frame.size[0], frame.size[1])

