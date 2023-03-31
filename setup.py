import sys
import os.path

def setup():
    """Handle and parse save path for downloads from argv"""
    rootSavePath = os.path.abspath(sys.argv[1])

    # Handle argv path creation
    if not os.path.isdir(rootSavePath):
        print(f"'{rootSavePath}' does not exist.") 
        mkdir_ans = input("Would you like to create the directory? (y/n)\n")
        if ( (mkdir_ans.lower() == 'y') or (mkdir_ans.lower() == 'yes') ):
            print(f'Creating path {rootSavePath}\n')
            os.makedirs(rootSavePath)
        else:
            sys.exit(1)
    else:
        print(f'Found existing directory for {rootSavePath}\n')

    return rootSavePath
