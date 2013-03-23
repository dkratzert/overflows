#! python
#-*- coding: utf-8 -*-

#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  <dkratzert@gmx.de> wrote this file. As long as you retain this notice you
#  can do whatever you want with this stuff. If we meet some day, and you think
#  this stuff is worth it, you can buy me a beer in return Daniel Kratzert.
#  ----------------------------------------------------------------------------

 
 
 
import sys, os
import fnmatch
import re
from math import pi, radians, degrees
from optparse import OptionParser



	
def sortedlistdir(dir):
	"""sorts the file list"""
	l = os.listdir(dir)
	l.sort()
	return l
 

 
################################################################################################# 

def read_header(path):    
	"""loop through files, print out values"""
	
	file = None
	occ = False
	
	for file in sortedlistdir(path):
		if fnmatch.fnmatch(file, '*[!matrix]*_??_*.sfrm'): #first frame of every run in dir
			fpath = os.path.join(path, file)
			#print file
			try:
				file = open(fpath,'rb')
				#file.close()
			except IOError:
				raise UserInputException('%s does not exist' % file)

			file = open(fpath,'rb')
			header = {}
			
			
			for n in range(96):
				l = file.read(80)
				a = l[:8]
				header[a] = l[8:]
  
			try:
				maxi = int(header['MAXIMUM:'].split()[0])
			except:
				raise Exception("Cannot read in the Bruker data file \
				%s because the header field MAXIMUM: can not be parsed." % file)

			try:	
				elaps = header['ELAPSDR:'].split()
			except:
				raise Exception("Cannot read in the Bruker data file \
				%s because the header field ELAPSDR: can not be parsed." % file)
			
			try:		
				theta = header['ANGLES :'].split()
			except:
				raise Exception("Cannot read in the Bruker data file \
				%s because the header field ANGLES : can not be parsed." % file)	
			
			try:		
				time = header['CUMULAT:'].split()
			except:
				raise Exception("Cannot read in the Bruker data file \
				%s because the header field ELAPSDR: can not be parsed." % file)	
			
			
			time = round(float(time[0]),0)
			theta2 = round(float(theta[0]),0)-360
						
			if len(elaps[:]) > 2:
				if maxi > 120000:
					print "Overflow", maxi, "in", fpath, "2theta =", theta2, "grad", "zeit =", time
					occ = True
			file.close()
	
	if occ != True:
		print "No overflows"
 
if __name__ == "__main__":
	path = '.'
	read_header(path)
	
	
