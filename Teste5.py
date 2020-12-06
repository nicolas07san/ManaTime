import sys
import zlib

with open('data/images/backgroundD.png', 'rb') as imageFile:
    compressed = zlib.compress((imageFile.read()), 9)

imagetxt = open('background.txt', 'wb')
imagetxt.write(compressed)
imagetxt.close()

read_file = open('background.txt', 'rb').read()

decompressed = zlib.decompress(read_file)

dimg = open('backgroundD.png', 'wb')
dimg.write(decompressed)
dimg.close()

print('Comprimido', (sys.getsizeof(compressed)))

print('Descomprimido', (sys.getsizeof(decompressed)))