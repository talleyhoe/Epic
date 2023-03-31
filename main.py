import requests
from tqdm import tqdm

from setup import *

DEBUG = 0

def dprint(*args, **kwargs):
    """Print only if global DEBUG is true"""
    # global DEBUG
    if DEBUG:
        print(*args, **kwargs)

def eprint(*args, **kwargs):
    """Print to stderr instead of stdout"""
    print(*args, file=sys.stderr, **kwargs)


def addFiletype(filePath: str):
    """Try to guess an image's file type and rename the file."""
    try:
        imgType = filetype.guess(filePath).mime.split('/')[-1]
    except:
        imgType = 'png'
    # This just replaces any filetypes (existing or not) with the new type
    new_path = '.'.join((os.path.splitext(filePath)[0], imgType))
    try:
        os.rename(filePath, new_path)
        return 0
    except Exception as err:
        eprint("Couldn't rename file at path {}".format(filePath))
        eprint(err)
        return 1

def getSaveDir(rootSavePath, year, month, day):
    """Return a date based folder to save images in."""
    return os.path.join(rootSavePath, year, month, day)

def getSavePath(rootSavePath, year, month, day, id):
    """Return an image's save path."""
    ext = '.png'
    fileName = str(id) + ext
    return os.path.join(
            getSaveDir(rootSavePath, year, month, day), 
            fileName)
    

def getDateList():
    """Return a unique list of dates where EPIC took photos"""
    dateResponse = requests.get('https://epic.gsfc.nasa.gov/api/enhanced/all')

    dateList = []
    for date in dateResponse.json():
        # since there are multiple pics of earth taken a day, there will be 
        # duplicate dates and we need to filter them out or we will make excess 
        # requests
        if date['date'] not in dateList:
            dateList.append(date['date'])

    return dateList

# Note: this could avoid redundancy issues if dateList is implemented with 
#       a nodal structure. Luckily, the queries aren't big
def setupDirs(rootSavePath, dateList):
    """
    Parse a unique list of dates that contain images. Create subdirectories
    to store EPIC images in. Should not be called directly. 

    Keyword arguments:
    rootSavePath -- base directory all images will be saved in 
    dateList -- unique list of dates generated from genDateList()
    """
    print("Preparing directories...")
    for date in dateList:
        year  = date[0: 4]
        month = date[5: 7] 
        day   = date[8:10]
        savePath = os.path.join(rootSavePath, year, month, day)
        os.makedirs(savePath, exist_ok=True)
        

def genDownloadManifest(rootSavePath):
    """
    Call getDateList, setup appropriate folders, get daily image manifest from 
    EPIC, and put together a list of download requests. Will prune out any 
    requests that already have a matching file at their save location

    Keyword arguments:
    rootSavePath -- base directory all images will be saved in 
    
    Return:
    manifest -- a list of 2 item hash maps of the form [{path, url}, ...]
    """
    dateList = getDateList()
    setupDirs(rootSavePath, dateList)

    metaDataUrl = "https://epic.gsfc.nasa.gov/api/natural/date/{}"
    imageUrl = "https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png"

    manifest = []

    print("Generating manifest...")
    for date in tqdm(dateList):
        year  = date[0: 4]
        month = date[5: 7] 
        day   = date[8:10]
        imageMetaDataResponse = requests.get(metaDataUrl.format(date)).json()
        for imageNum, response in enumerate(imageMetaDataResponse):
            savePath = getSavePath(rootSavePath, year, month, day, imageNum)
            dprint("Path: {}, Result {}".format(savePath, os.path.exists(savePath)))
            if not os.path.exists(savePath):
                webId = response['image']
                requestStruct = {
                        "path": savePath,
                        "url": imageUrl.format(year, month, day, webId)
                    }
                manifest.append(requestStruct)
    return manifest

    
def downloadImage(imageMap, apiKey):
    """ 
    Download an image from a source url. 

    Keyword arguments:
    imageMap -- a hash map of the form {path, url}
    """
    imgPath = imageMap.get('path')
    imgUrl  = imageMap.get('url')
    try:
        params = {'api_key': apiKey}
        response = requests.get(imgUrl, params=params)
    except Exception as err:
        if DEBUG:
            eprint(f"ERROR: Can't request image url: {imgUrl}")
            eprint(err)
        return -1

    remainingRequests = int(response.headers.get("x-ratelimit-remaining"))

    if response.status_code == 200:
        with open(imgPath, 'wb') as img:
            img.write(response.content)
        addFiletype(imgPath)
    else:
        eprint("ERROR: Status code {} for url {}."
               .format(response.status_code, imgUrl))
    return remainingRequests


# Threading goes here
def downloadImages(rootSavePath, apiKey):
    print("Downloading images...")

    # Generates file structure and return files to download
    manifest = genDownloadManifest(rootSavePath)
    for imageMap in tqdm(manifest):
        remainingRequests = downloadImage(imageMap, apiKey)
        if remainingRequests < 1:
            eprint("Exceeded API Limit")
            sys.exit(0)

    

def main():
    rootSavePath = setup()  
    apiKey = "BkFVBBcoSre33RhWShgaYdDD1wyFowS3hUx7QmUb"
    downloadImages(rootSavePath, apiKey)
    print("Done!")


if __name__ == '__main__':
    main()
