import sys
import os.path
def setup():
	rootSavePath = sys.argv[1]

	if not os.path.isdir(rootSavePath):
		print(f'{rootSavePath} does not exist')
		exit(0)
	

	return rootSavePath
