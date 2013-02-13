
import sys, os
import Image, ImageDraw
import copy


if len(sys.argv) < 2:
    sys.exit('Usage: %s filename_HR' % sys.argv[0])
filename_HR = sys.argv[1]
#filename_LR = sys.argv[2]


img = Image.open(filename_HR)
pixels = img.load()
draw = ImageDraw.Draw(img)


def drawVLine(l, color):
	for j in range(img.size[1]):
		pixels[l,j] = color

def drawHLine(l, color):
	for i in range(img.size[0]):
		pixels[i,l] = color



#rectangle = [x1,y1, x2,y2]
def detectVLine(rectangle):
	vZone = list()

	inContent = False

	for j in range(rectangle[1], rectangle[3]):
		blankLine = True
		
		for i in range(rectangle[0], rectangle[2]):
			if(pixels[i,j][0] < 250):
				blankLine = False
				
		#if(blankLine):
			#drawHLine(j, (0, 100, 255))
		
		if(inContent & blankLine):
			inContent = False
			vZone.append(j)
			#drawHLine(j, (255, 100, 0))
		elif (not (inContent) and not (blankLine)):
			inContent = True
			vZone.append(j)
			#drawHLine(j, (100, 255, 0))
	return vZone


vZone = detectVLine([0,0,img.size[0],img.size[1]])
#vZone = [133, 162, 182, 205, 207, 244, 269, 293, 295, 312, 314, 331, 396, 415, 418, 1001, 1007, 1025, 1027, 1047, 1048, 1067, 1069, 1088, 1090, 1108, 1110, 1128, 1131, 1336, 1338, 1339, 1341, 1361, 1362, 1382, 1383, 1402, 1403, 1423, 1424, 1442, 1445, 1463, 1466, 1484, 1486, 1505]

#print vZone



#delete too small vertical zone
def deleteSmallVerticalZone(vZone):
	vZoneShort = list()
	e = 0
	while e < len(vZone) :
		nStart = e
		nEnd = e+1
		#print nStart, nEnd, "=|=>", vZone[nEnd] - vZone[nStart]
		#a zone should be bigger than
		while(nEnd < len(vZone) and vZone[nEnd] - vZone[nStart] < 20):
			#print nStart, nEnd, "=X=>", vZone[nEnd] - vZone[nStart]
			nEnd = nEnd +2
		
		#2 zones canno't be too close
		#print nSvZonevZonetart, nEnd, "=)=>", vZone[nEnd+1] - vZone[nEnd]
		while(nEnd+1 < len(vZone) and vZone[nEnd+1] - vZone[nEnd] < 20):
			#print nStart, nEnd, "=*=>", vZone[nEnd+1] - vZone[nEnd]
			nEnd = nEnd +2
		
		vZoneShort.append((vZone[nStart], vZone[nEnd]))

		e = nEnd+1
	return vZoneShort

vZone = deleteSmallVerticalZone(vZone)
#vZone = [(133, 162), (182, 244), (269, 331), (396, 1505)]

#print vZone


#for e in range(0, len(vZone)):
	#drawHLine(vZone[e][0], (255, 100, 0))
	#drawHLine(vZone[e][1], (100, 255, 0))
	

#foreach vZone we determine hZones
#from these vZones we create rectangle
#these rectangles are find in the good order
def makeRectangles():
	curRect = [0,0,0,0]
	zones = list()
	for e in range(0, len(vZone)):
		inContent = False
		curRect[1] = vZone[e][0]
		curRect[3] = vZone[e][1]
		zonesH = list()
		
		for i in  range(img.size[0]):
			blankLine = True
			
			for j in range(vZone[e][0], vZone[e][1]):
				if(pixels[i,j][0] < 250):
					blankLine = False
					
			if(inContent & blankLine):
				inContent = False
				curRect[2] = i
				if(len(zonesH)>0):
					tempRect = zonesH.pop()
					if(curRect[0] - tempRect[2] < 20):
						curRect[0] = tempRect[0]
						curRect[1] = tempRect[1]
					else:
						zonesH.append(tempRect)
				zonesH.append(copy.copy(curRect))
			elif (not (inContent) and not (blankLine)):
				inContent = True
				curRect[0] = i
		
		#print zonesH
		for e in range(0, len(zonesH)):
			zones.append(zonesH[e])
	return zones

zones = makeRectangles()
#zones = [[239, 133, 1037, 162], [331, 182, 556, 244], [705, 182, 959, 244], [300, 269, 588, 331], [719, 269, 946, 331], [112, 396, 614, 1505], [662, 396, 1164, 1505]]
#print zones


f = open(filename_HR + '.html','w')
f.write('<!DOCTYPE html>\n<html><head></head><body>\n')
nf = 0

for e in range(0, len(zones)):
	#print "--------------------------------------"
	#draw.rectangle(zones[e], outline="Blue")
	#print zones[e]
	zones[e][1] -= 5
	zones[e][3] += 5
	#print zones[e]
	vl = detectVLine(zones[e])
	#draw.rectangle(zones[e], outline="Blue")
	#print vl
	i = 0
	while i < len(vl)-1:
		#draw.rectangle( [zones[e][0], vl[i], zones[e][2], vl[i+1]], outline="Pink")
		fn = filename_HR+'image'+str(nf)+'.png'
		fn_bn = os.path.basename(fn)
		f.write('<img style="width:100%" src="'+fn_bn+'" /><br />\n')
		img.crop([zones[e][0], vl[i], zones[e][2], vl[i+1]]).save(fn)
		nf +=1
		i = i+2
	

f.write('\n</body></html>')

#img.show()








