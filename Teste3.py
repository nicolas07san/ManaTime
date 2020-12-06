import base64
import zlib

# Background
with open('data/images/background.png', 'rb') as imageFile:
    image = base64.b85encode(imageFile.read())
    print(image)

compressed = base64.b85encode(zlib.compress(image, 9))

imagetxt = open('background.txt', 'wb')
imagetxt.write(compressed)
imagetxt.close()

read_file = open('background.txt', 'rb').read()

decompressed = zlib.decompress(base64.b85decode(read_file))

dimg = open('imagetosave.png', 'wb')
dimg.write(base64.b85decode(decompressed))
dimg.close()

'''
# Mapa

text = open('data/map.txt', 'rb').read()

tcompressed = base64.b64encode(zlib.compress(text, 9))

ctext = open('data/mapc.txt', 'wb')
ctext.write(tcompressed)
ctext.close()

tread_file = open('data/mapc.txt', 'rb').read()

tdecompressed = zlib.decompress(base64.b64decode(tread_file))

dtxt = open('data/mapd.txt', 'w')
dtxt.write(base64.b64decode(tdecompressed))
dtxt.close()
'''