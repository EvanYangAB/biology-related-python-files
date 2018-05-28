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
	) = struct.unpack("IHHQQQHH", data)


data = f.read(20)
(autoSqlOffset, totalSummaryOffset, uncompressBufSize) = struct.unpack("QQI", data)

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

zooms = []
for x in range(1,zoomLevels + 1):
	zoom = {}
	data = f.read(24)
	(reductionLevel, reserved, dataOffest, indexOffset) = struct.unpack("IIQQ", data)
	zoom["level"] = x
	zoom["reductionLevel"] = reductionLevel
	zoom["reserved"] = reserved
	zoom["ldataOffest"] = dataOffest
	zoom["indexOffset"] = indexOffset
	zooms.append(zoom)
print(zooms)

data = f.read(40)
(basesCovered, minVal, maxVal, sumData, sumSquares) = struct.unpack("QQQQQ", data)
print("basesCovered: " + str(basesCovered))
print("minVal: " + str(minVal))
print("maxVal: " + str(maxVal))
print("sumData: " + str(sumData))
print("sumSquares: " + str(sumSquares))

data = f.read(4)
treeMagic = struct.unpack("I", data)
print("treeMagic: " + hex(treeMagic[0]))