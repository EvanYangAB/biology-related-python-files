# with open("39033.bigwig", "rb") as binary_file:
#     # Seek position and read N bytes
#     binary_file.seek(0)  # Go to beginning
#     couple_bytes = binary_file.read(65)
#     print(couple_bytes)
# print(123)
import struct
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

print("magic: " + hex(magic))
print("version: " + hex(version))
print("zoomLevels: " + str(zoomLevels))
print("chromosomeTreeOffset: " + hex(chromosomeTreeOffset))
print("fullDataOffset: " + hex(fullDataOffset))
print("fullIndexOffset: " + hex(fullIndexOffset))
print("fieldCount: " + hex(fieldCount))
print("definedFieldCount: " + hex(definedFieldCount))
print("autoSqlOffset: " + hex(autoSqlOffset))
print("totalSummaryOffset: " + hex(totalSummaryOffset))
print("uncompressBufSize: " + hex(uncompressBufSize))
print("reserved: " + hex(reserved))

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
	print(zoom)

# 64 + zoomLevels * 24

data = f.read(40)
(basesCovered, minVal, maxVal, sumData, sumSquares) = struct.unpack("=QQQQQ", data)
print("basesCovered: " + hex(basesCovered))
print("minVal: " + hex(minVal))
print("maxVal: " + hex(maxVal))
print("sumData: " + hex(sumData))
print("sumSquares: " + hex(sumSquares))
print("binary raw data:")
print(data)
print("===")

# 64 + zoomLevels * 24 + 40

# tree header
data = f.read(4)
treeMagic = struct.unpack("=I", data)
treeMagic = treeMagic[0]
print("treeMagic: " + hex(treeMagic))
data = f.read(12)
(blockSize, keySize, valSize) = struct.unpack("=III", data)
print("blockSize: " + str(blockSize))
print("keySize: " + str(keySize))
print("valSize: " + str(valSize))
data = f.read(16)
(itemCount, treeReserved) = struct.unpack("=QQ", data)
print("itemCount: " + str(itemCount))
print("reserved: " + str(treeReserved))

# parse 1 node
data = f.read(4)
(isLeaf, nodeReserved, count) = struct.unpack("BBH", data) 
print("isLeaf: " + str(isLeaf))
print("nodeReserved: " + str(nodeReserved))
print("count: " + str(count))
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


for item in node:
	print(item)

data = f.read(4)
dataCount = struct.unpack("I", data)
dataCount = dataCount[0]
print("dataCount: " + str(dataCount))

# read one data block
data = f.read(4)
print(struct.unpack("I", data))
data = f.read(4)
print(struct.unpack("I", data))
data = f.read(4)
print(struct.unpack("I", data))
data = f.read(4)
print(struct.unpack("I", data))
data = f.read(4)
print(struct.unpack("I", data))
data = f.read(1)
print(struct.unpack("B", data))


# (chromId, chromStart, chromEnd, itemStep, itemSpan, t_ype, reserved, itemCount) = struct.unpack("IIIIIBBH", data)
# dataBlock = {"chromId": chromId, "chromStart": chromStart, "chromEnd": chromEnd, 
# 	"itemStep": itemStep, "itemSpan": itemSpan, "type": t_ype, "reserved": reserved, "itemCount": itemCount}
# print(dataBlock)
