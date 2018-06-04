import pyBigWig
bw = pyBigWig.open("39033.bigwig")
print(bw.intervals())