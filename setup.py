import sys
import os.path

def setup():
    """Handle and parse save path for downloads from argv"""
    rootSavePath = sys.argv[1]

    # Handle argv path creation
    if not os.path.isdir(rootSavePath):
        print(f"'{rootSavePath}' does not exist.") 
        mkdir_ans = input("Would you like to create the directory? (y/n)")
        if (mkdir_ans.lower() == 'y' | mkdir_ans.lower() == 'yes'):
            os.makedirs(rootSavePath)
        else:
            sys.exit(1)
    

    return rootSavePath
