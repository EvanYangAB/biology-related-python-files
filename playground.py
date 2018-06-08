import struct
import zlib

def readRtreeNode(f, offset, isLeaf):
    f.seek(offset)
    data = f.read(4)
    (rIsLeaf, rReserved, rCount) = struct.unpack("BBH", data)
    if isLeaf:
        data = f.read(32)
        (rStartChromIx, rStartBase, rEndChromIx, rEndBase, rdataOffset, rDataSize) = struct.unpack("IIIIQQ", data)
        return {"rIsLeaf": rIsLeaf, "rReserved": rReserved, "rCount": rCount, "rStartChromIx": rStartChromIx, "rStartBase": rStartBase, "rEndChromIx": rEndChromIx, "rEndBase": rEndBase, "rdataOffset": rdataOffset, "rDataSize": rDataSize, "nextOff": offset + 32}
    else:
        data = f.read(24)
        (rStartChromIx, rStartBase, rEndChromIx, rEndBase, rdataOffset) = struct.unpack("IIIIQ", data)
        return {"rIsLeaf": rIsLeaf, "rReserved": rReserved, "rCount": rCount, "rStartChromIx": rStartChromIx, "rStartBase": rStartBase, "rEndChromIx": rEndChromIx, "rEndBase": rEndBase, "rdataOffset": rdataOffset, "nextOff": offset + 24}

# read 1 r tree head node
def readRtreeHeadNode(f, offset):
    f.seek(offset)
    data = f.read(4)
    (rIsLeaf, rReserved, rCount) = struct.unpack("BBH", data)
    return readRtreeNode(f, offset, rIsLeaf)

f = open("39033.bigwig", "rb")
# f = open("dummy_var_sample.bigwig", "rb")
# f = open("test_fixedStep.bigwig", "rb")
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
# print("chromosomeTreeOffset: " + str(chromosomeTreeOffset))
# print("fullDataOffset: " + hex(fullDataOffset))
# print("fullIndexOffset: " + hex(fullIndexOffset))
# print("fieldCount: " + hex(fieldCount))
# print("definedFieldCount: " + hex(definedFieldCount))
# print("autoSqlOffset: " + hex(autoSqlOffset))
# print("totalSummaryOffset: " + hex(totalSummaryOffset))
# print("uncompressBufSize: " + hex(uncompressBufSize))
# print("reserved: " + hex(reserved))
for zoom in zooms:
  print(zoom)
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
#    print(item)

# parsing data
# full data offset jumps to dataCount
# data = f.seek(fullDataOffset)
# data = f.read(4)
# dataCount = struct.unpack("I", data)
# print(dataCount)

# data = f.seek(fullIndexOffset)
# data = f.read(48)
# (rMagic, rBlockSize, rItemCount, rStartChromIx, rStartBase, rEndChromIx, rEndBase,
#     rEndFileOffset, rItemsPerSlot, rReserved) = struct.unpack("IIQIIIIQII", data)
# print("(rMagic, rBlockSize, rItemCount, rStartChromIx, rStartBase, rEndChromIx, rEndBase, rEndFileOffset, rItemsPerSlot, rReserved)")
# print((rMagic, rBlockSize, rItemCount, rStartChromIx, rStartBase, rEndChromIx, rEndBase,
#     rEndFileOffset, rItemsPerSlot, rReserved))
# print(fullIndexOffset + 48)

# print(readRtreeHeadNode(f, fullIndexOffset + 48))
# print(readRtreeNode(f, fullIndexOffset + 48 + 32, 1))
# print(readRtreeHeadNode(f, 583410880))
# print(readRtreeNode(f, 583423176, 1))
# print(readRtreeNode(f, 583423208, 1))
# print(readRtreeNode(f, 583423240, 1))
# f.seek(713)
# data = f.read(4373)



# data = f.seek(587232696)
# data = f.read(2939)
# decom = zlib.decompress(data)
# header = decom[:24]

# print(struct.unpack("IIIIIBBH", header))
# # for bedGraph
# print(struct.unpack("IIf", decom[24:36]))
# print(struct.unpack("IIf", decom[36:48]))

#for varStep
# print(struct.unpack("If", decom[24:32]))
# print(struct.unpack("If", decom[32:40]))
# print(struct.unpack("If", decom[40:48]))

#for fixStep
# print(struct.unpack("f", decom[24:28]))
# print(struct.unpack("f", decom[28:32]))
# print(struct.unpack("f", decom[32:36]))

f.seek(676939587)
data = f.read(48)
(rMagic, rBlockSize, rItemCount, rStartChromIx, rStartBase, rEndChromIx, rEndBase,
    rEndFileOffset, rItemsPerSlot, rReserved) = struct.unpack("IIQIIIIQII", data)
print("(rMagic, rBlockSize, rItemCount, rStartChromIx, rStartBase, rEndChromIx, rEndBase, rEndFileOffset, rItemsPerSlot, rReserved)")
print((rMagic, rBlockSize, rItemCount, rStartChromIx, rStartBase, rEndChromIx, rEndBase,
    rEndFileOffset, rItemsPerSlot, rReserved))

print(readRtreeHeadNode(f, 676939587 + 48))

print(readRtreeHeadNode(f, 676945783))

data = f.seek(587232696)
data = f.read(2939)
decom = zlib.decompress(data)



print(struct.unpack("4I4f", decom[0:32]))