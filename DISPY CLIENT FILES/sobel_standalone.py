import picamera
def greyscaleImage(image)
    from PIL import Image
    image.convert('L')

import picamera.array
import time
import io
import PIL
from PIL import Image

stream = io.BytesIO()

with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)
    camera.capture(stream, format='jpeg')
stream.seek(0)
image = Image.open(stream)
start = time.time_ns()
image.convert('L')
mid = time.time_ns()
seq = list(image.getdata())
end = time.time_ns()
time1 = (mid-start)/1000000000
time2 = (end-mid)/1000000000
print(time1)
print(time2)
print(seq)