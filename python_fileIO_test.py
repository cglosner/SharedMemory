import os

def sortFile(fileName, opNum):
    file = open(fileName, "r")
    wordsInFile = []
    for line in file:
        splitList = line.split()
        for i in splitList:
            wordsInFile.append(i)
    file.close()
    wordsInFile.sort()

    outName = "result" + str(opNum) + ".txt"
    outputFile = open(outName, "w")
    for i in wordsInFile:
        outputFile.writelines(i)
        outputFile.writelines(" ")
    outputFile.close()

def getSize(filename):
    st = os.stat(filename)
    return st.st_size

if __name__ == "__main__":
    fileName = input("Enter File Name: ")
    numBytes = getSize(fileName)
    if (numBytes < 1e6):
        print(f"file size = {getSize(fileName)/1e3}KB")
    else:
        print(f"file size = {getSize(fileName)/1e6}MB")

    for i in range(10):
        sortFile(fileName, i)