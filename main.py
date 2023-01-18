import requests
import subprocess as sp
from setup import *

def downloadImages(rootSavePath):
	#this returns every date each picture was taken on
	dateResponse = requests.get('https://epic.gsfc.nasa.gov/api/enhanced/all')

	dateList = []
	for date in dateResponse.json():
		#since there are multiple pics of earth taken a day, there will be duplicate dates and we need to filter them out or we will make excess requests
		if date['date'] not in dateList:
			dateList.append(date['date'])

	if not os.path.isdir(rootSavePath):
		print(f'Creating path {rootSavePath}\n')
		sp.run(['mkdir', rootSavePath])
	else:
		print(f'Found existing directory for {rootSavePath}\n')

	for date in dateList:
		print(date)
		savePath = os.path.join(rootSavePath, date[0:4], date[5:7], date[8:10])
		
		#check if year folder exists
		if not os.path.isdir(os.path.join(rootSavePath, date[0:4])):
				print(f'Creating path {os.path.join(rootSavePath, date[0:4])}\n')
				sp.run(['mkdir', os.path.join(rootSavePath, date[0:4])])
		else:
			print(f'Found existing directory for {os.path.join(rootSavePath, date[0:4])}\n')

		#check if year/month folder exists
		if not os.path.isdir(os.path.join(rootSavePath, date[0:4], date[5:7])):
				print(f'Creating directory {os.path.join(rootSavePath, date[0:4], date[5:7])}\n')
				sp.run(['mkdir', os.path.join(rootSavePath, date[0:4], date[5:7])])
		else:
			print(f'Found existing directory for {os.path.join(rootSavePath, date[0:4], date[5:7])}\n')

		#check if year/month/day folder exists
		if not os.path.isdir(os.path.join(rootSavePath, date[0:4], date[5:7], date[8:10])):
				print(f'Creating path {os.path.join(rootSavePath, date[0:4], date[5:7], date[8:10])}\n')
				sp.run(['mkdir', os.path.join(rootSavePath, date[0:4], date[5:7], date[8:10])])
		else:
			print(f'Found existing directory for {os.path.join(rootSavePath, date[0:4], date[5:7], date[8:10])}, skipping this day\n')
			continue

		imageMetaDataResponse = requests.get(f'https://epic.gsfc.nasa.gov/api/natural/date/{date}')
		
		imageMetaDataResponseJson = imageMetaDataResponse.json()

		#iterating over every photo taken on the supplied day
		for imageNum, response in enumerate(imageMetaDataResponseJson):
			savePath = os.path.join(rootSavePath, date[0:4], date[5:7], date[8:10])
			imageName = response['image']

			URL = f'https://api.nasa.gov/EPIC/archive/natural/{date[0:4]}/{date[5:7]}/{date[8:10]}/png/{imageName}.png?api_key=BkFVBBcoSre33RhWShgaYdDD1wyFowS3hUx7QmUb'

			savePath =  os.path.join(savePath, str(imageNum) + '.png')
			cmd = f'curl -L -o {savePath} {URL}'
			print(f'{cmd}\n')
			#TODO: Chnage this to use requests to instead of SP, use this link: https://www.alixaprodev.com/2022/07/how-to-download-image-using-requests.html
			sp.run(['curl', '-L', '-o', savePath, URL])	




def main():
	rootSavePath = setup()	
	downloadImages(rootSavePath)


if __name__ == '__main__':
	main()