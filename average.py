# with open("39033.bigwig", "rb") as binary_file:
#     # Seek position and read N bytes
#     binary_file.seek(0)  # Go to beginning
#     couple_bytes = binary_file.read(65)
#     print(couple_bytes)
# print(123)
import struct
import zlib
f = open("39033.bigwig", "rb")
data = f.read(36)
(magic, version, zoomLevels, chromosomeTreeOffset, fullDataOffset, fullIndexOffset,
	fieldCount, definedFieldCount
	) = struct.unpack("=IHHQQQHH", data)


data = f.read(20)
(autoSqlOffset, totalSummaryOffset, uncompressBufSize) = struct.unpack("=QQI", data)

data = f.read(8)
reserved= struct.unpack("Q", data)
reserved = reserved[0]

#64

zooms = []
for x in range(1,zoomLevels + 1):
	zoom = {}
	data = f.read(24)
	(reductionLevel, reserved, dataOffest, indexOffset) = struct.unpack("=IIQQ", data)
	zoom["level"] = x
	zoom["reductionLevel"] = reductionLevel
	zoom["reserved"] = reserved
	zoom["ldataOffest"] = dataOffest
	zoom["indexOffset"] = indexOffset
	zooms.append(zoom)

# 64 + zoomLevels * 24

data = f.read(40)
(basesCovered, minVal, maxVal, sumData, sumSquares) = struct.unpack("=Qdddd", data)

# data = f.read(8)
# basesCovered = int.from_bytes(data, byteorder = 'big', signed = False)
# data = f.read(8)
# minVal = int.from_bytes(data, byteorder = 'big', signed = False)
# data = f.read(8)
# maxVal = int.from_bytes(data, byteorder = 'big', signed = False)
# data = f.read(8)
# sumData = int.from_bytes(data, byteorder = 'big', signed = False)
# data = f.read(8)
# sumSquares = int.from_bytes(data, byteorder = 'big', signed = False)
# print("basesCovered: " + str(basesCovered))
# print("minVal: " + str(minVal))
# print("maxVal: " + str(maxVal))
# print("sumData: " + str(sumData))
# print("sumSquares: " + str(sumSquares))

# 64 + zoomLevels * 24 + 40

# tree header
data = f.read(4)
treeMagic = struct.unpack("=I", data)
treeMagic = treeMagic[0]

data = f.read(12)
(blockSize, keySize, valSize) = struct.unpack("=III", data)
data = f.read(16)
(itemCount, treeReserved) = struct.unpack("=QQ", data)


# parse 1 node
data = f.read(4)
(isLeaf, nodeReserved, count) = struct.unpack("BBH", data) 

node = []
for _ in range(0, count):
	key = ""
	for x in range(0, keySize):
		data = f.read(1)
		temp = struct.unpack("b", data) 
		if chr(temp[0]) != "\x00":
			key += chr(temp[0])
	data = f.read(8)
	(chromId, chromSize) = struct.unpack("II", data)
	node.append({"key": key, "chromId": chromId, "chromSize": chromSize})

# print header
# print("magic: " + hex(magic))
# print("version: " + hex(version))
# print("zoomLevels: " + str(zoomLevels))
# print("chromosomeTreeOffset: " + hex(chromosomeTreeOffset))
# print("fullDataOffset: " + hex(fullDataOffset))
# print("fullIndexOffset: " + hex(fullIndexOffset))
# print("fieldCount: " + hex(fieldCount))
# print("definedFieldCount: " + hex(definedFieldCount))
# print("autoSqlOffset: " + hex(autoSqlOffset))
# print("totalSummaryOffset: " + hex(totalSummaryOffset))
# print("uncompressBufSize: " + hex(uncompressBufSize))
# print("reserved: " + hex(reserved))
# for zoom in zooms
# 	print(zoom)
# print("basesCovered: " + hex(basesCovered))
# print("minVal: " + str(minVal))
# print("maxVal: " + str(maxVal))
# print("sumData: " + str(sumData))
# print("sumSquares: " + str(sumSquares))
# print("treeMagic: " + hex(treeMagic))
# print("blockSize: " + str(blockSize))
# print("keySize: " + str(keySize))
# print("valSize: " + str(valSize))
# print("itemCount: " + str(itemCount))
# print("reserved: " + str(treeReserved))
# print("isLeaf: " + str(isLeaf))
# print("nodeReserved: " + str(nodeReserved))
# print("count: " + str(count))
# for item in node:
# 	print(item)

# parsing data
# full data offset jumps to dataCount
data = f.seek(fullDataOffset)
data = f.read(4)
dataCount = struct.unpack("I", data)
print(dataCount)

data = f.seek(fullIndexOffset)
data = f.read(48)
(rMagic, rBlockSize, rItemCount, rStartChromIx, rStartBase, rEndChromIx, rEndBase,
	rEndFileOffset, rItemsPerSlot, rReserved) = struct.unpack("IIQIIIIQII", data)
print("(rMagic, rBlockSize, rItemCount, rStartChromIx, rStartBase, rEndChromIx, rEndBase, rEndFileOffset, rItemsPerSlot, rReserved)")
print((rMagic, rBlockSize, rItemCount, rStartChromIx, rStartBase, rEndChromIx, rEndBase,
	rEndFileOffset, rItemsPerSlot, rReserved))
print(fullIndexOffset + 48)
# read 1 r tree node
def readRtreeNode(offset):
	f.seek(offset)
	data = f.read(4)
	(rIsLeaf, rReserved, rCount) = struct.unpack("BBH", data)
	print((rIsLeaf, rReserved, rCount))
	if rIsLeaf:
		data = f.read(32)
		(rStartChromIx, rStartBase, rEndChromIx, rEndBase, rdataOffset, rDataSize) = struct.unpack("IIIIQQ", data)
		return {"rIsLeaf": rIsLeaf, "rReserved": rReserved, "rCount": rCount, "rStartChromIx": rStartChromIx, "rStartBase": rStartBase, "rEndChromIx": rEndChromIx, "rEndBase": rEndBase, "rdataOffset": rdataOffset, "rDataSize": rDataSize, "nextOff": offset + 32}
	else:
		data = f.read(24)
		(rStartChromIx, rStartBase, rEndChromIx, rEndBase, rdataOffset) = struct.unpack("IIIIQ", data)
		return {"rIsLeaf": rIsLeaf, "rReserved": rReserved, "rCount": rCount, "rStartChromIx": rStartChromIx, "rStartBase": rStartBase, "rEndChromIx": rEndChromIx, "rEndBase": rEndBase, "rdataOffset": rdataOffset, "nextOff": offset + 24}

print(readRtreeNode(fullIndexOffset + 48))
print(readRtreeNode(fullIndexOffset + 48 + 24))
print(readRtreeNode(583410880))
print(readRtreeNode(583423176))

data = f.seek(713)
data = f.read(4373)
decom = zlib.decompress(data)
header = decom[:24]

print(struct.unpack("IIIIIBBH", header))
print(struct.unpack("IIf", decom[24:36]))
print(struct.unpack("IIf", decom[36:48]))

def aveBigWig(f, chrmzone, startIndex, endIndex):
	f.seek(0)
	data = f.read(36)
	(magic, version, zoomLevels, chromosomeTreeOffset, fullDataOffset, fullIndexOffset,
		fieldCount, definedFieldCount) = struct.unpack("=IHHQQQHH", data)
	f.seek(chromosomeTreeOffset)
	data = f.read(4)
	chrmId = -1
	(isLeaf, nodeReserved, count) = struct.unpack("BBH", data) 
	for _ in range(0, count):
		key = ""
		for x in range(0, keySize):
			data = f.read(1)
			temp = struct.unpack("b", data) 
			if chr(temp[0]) != "\x00":
				key += chr(temp[0])
		data = f.read(8)
		(chromId, chromSize) = struct.unpack("II", data)
		if key == chrmzone:
			chrmId = chromId
	if chrmId == -1:
		print("error")
		exit() # need to handle error
	offset = fullIndexOffset
	while 1:
		node = readRtreeNode(offset)
		layerSize = node[rCount]
		for _ in xrange(1,rCount):
			if node[rEndChromIx] >= chrmId && node[rStartChromIx] <= chrmId:
				break;
			else:
				node = readRtreeNode(node[nextOff])
		if node[rIsLeaf] == 1:
			break




def readBioFile(file, chrmzone, startIndex, endIndex):
	f = open(file, "rb")
	if struct.unpack("I", f.read(4))[0] == int("0x888FFC26", 0):
	 	aveBigWig(f, chrmzone, startIndex, endIndex)
	f.close()


