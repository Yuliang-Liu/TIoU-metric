import glob
from shapely.geometry import *

Origin_file = 'YOUR_ORIGIN_FILE/'
Output_file = 'SORTED_FILE/'

files = glob.glob(Origin_file+'*.txt')
files.sort()

for i in files:
	print('Pros ' + i)
	out = i.replace(Origin_file, Output_file)
	fin = open(i, 'r').readlines()
	fout = open(out, 'w')
	for line in fin:
		cors = line.strip().split(',')
		assert(len(cors) %2 == 0), 'cors invalid.'
		pts = [(int(cors[j]), int(cors[j+1])) for j in xrange(0,len(cors),2)]
		try:
			pgt = Polygon(pts)
		except Exception as e:
			print('Not a valid polygon.', pgt)
			continue
		
		if not pgt.is_valid: 
		        print('GT polygon has intersecting sides.', pts)
		        continue
			
		pRing = LinearRing(pts)
		if pRing.is_ccw:
			pts.reverse()
		outstr= ''
		for ipt  in pts[:-1]:
			outstr += (str(int(ipt[0]))+','+ str(int(ipt[1]))+',')
		outstr += (str(int(pts[-1][0]))+','+ str(int(pts[-1][1])))
		fout.writelines(outstr+'\n')
	fout.close()
