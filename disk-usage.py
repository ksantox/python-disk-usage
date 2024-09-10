#!/usr/bin/python
import os
import sys
import pandas

def getDirectorySize(directory, generateCsv = False):
    if not os.path.isdir(directory) or directory == '/' or directory == '.':
        print('Provided argument is not a valid directory.')
        return

    total = 0
    paths = []
    usage = []

    for entry in os.scandir(directory):
        try:
            if entry.is_dir(follow_symlinks=False):
                currDirSize = getDirectorySize(entry.path)
                total += currDirSize
                
                paths.append(entry.path)
                usage.append(currDirSize)

                if not generateCsv:
                    readableSize = humanReadableSize(currDirSize)
                    print(f'{entry.path}: {readableSize}')
            else:
                total += entry.stat(follow_symlinks=False).st_size
        except Exception as error:
            print(f'Exception: {error}')
            total += 0

    if generateCsv:
        generateReport(paths, usage)

    return total

def generateReport(paths, usage):
    readableSizes = [humanReadableSize(size) for size in usage]
    usageDict = { 'Directory': paths, 'Usage': readableSizes }

    dataFrame = pandas.DataFrame(usageDict)
    dataFrame.to_csv('disk_usage.csv')

def humanReadableSize(totalSize):
    if totalSize == 0:
        return "0B"
    
    sizeUnits = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while totalSize >= 1024 and i < len(sizeUnits) - 1:
        totalSize /= 1024
        i += 1

    return f"{totalSize:.2f} {sizeUnits[i]}"

def main():
    if len(sys.argv) < 2:
        print('No directory provided')
        return

    directory = sys.argv[1]
    generateCsv = sys.argv[2] == 'true' if len(sys.argv) >= 3 else False

    totalSize = getDirectorySize(directory, generateCsv)
    readableSize = humanReadableSize(totalSize)
    print(f'Total size is: {readableSize}')

if __name__ == '__main__':
    main()
