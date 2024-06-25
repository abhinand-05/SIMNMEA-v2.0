# A quick subroutine to count the number of lines in a given file name.
# 1 = get number of lines
# 2 = get content
# 3 = get content as list
import sys
def readTextFile(getWhat, fileToRead):
	# Get and return only the number of 
	if(getWhat == 1):
		with open(fileToRead) as f:
			for i, l in enumerate(f):
				pass
			return i + 1

	# Get and return each line of the provided static sentence file in one chunk
	elif(getWhat == 2):
		toSend = ''
		with open(fileToRead) as f:
			fileContent = [line.rstrip() for line in f]
		for each in fileContent:
			toSend = toSend + each + "\n"
		return toSend.strip('\n')

	# Get and return the entire content as a list
	elif(getWhat == 3):
		toSend = ''
		with open(fileToRead) as f:
			fileContent = [line.rstrip() for line in f]
		return fileContent

	# else -- Just in case
	else:
		print ('''Yikes, something's wrong. Unknown read text-file parameter!\
                1 = get number of lines\
                2 = get content\
                3 = get content as list''')
		sys.exit()

# Read the file that has all the static sentences (read by readTextFile func
#	with parameter '2' to indicate read the entire content of the file).
#	staticSentences holds the entire chunk of static sentences read from the
#	file.