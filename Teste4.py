import base64
import zlib

# Background
with open('data/images/background.png', 'rb') as imageFile:
    image = base64.b85encode(imageFile.read())
    print(image)

compressed = zlib.compress(image, 9)

imagetxt = open('data/images/background.txt', 'wb')
imagetxt.write(compressed)
imagetxt.close()

read_file = open('data/images/background.txt', 'rb').read()

decompressed = zlib.decompress(read_file)

dimg = open('data/images/backgroundD.png', 'wb')
dimg.write(base64.b85decode(decompressed))
dimg.close()