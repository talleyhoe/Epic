from setup import *
import requests
import os.path
import subprocess as sp
#get the file name using the api
#use wget to download the image

def main():
	setup()
	#print('hello world\n')
	URL = 'https://epic.gsfc.nasa.gov/archive/natural/'
	savePath = 'Images/'

	response = requests.get('https://api.nasa.gov/EPIC/api/natural/images?api_key=BkFVBBcoSre33RhWShgaYdDD1wyFowS3hUx7QmUb')
	jsonResponse = response.json()
	
	imageName = jsonResponse[0]['image']
	date = jsonResponse[0]['date']
	year = date[0:4]
	month = date[5:7]
	day = date[8:10]

	URL +=  f'{year}/{month}/{day}/png/{imageName}.png'

	cmd = f'curl -L -o {savePath+year+month+day} {URL}'
	print(f'{cmd}\n')
	sp.run(['curl', '-L', '-o', savePath+year+month+day, URL])


if __name__ == '__main__':
	main()