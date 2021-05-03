from multiprocessing.shared_memory import SharedMemory
from multiprocessing.managers import SharedMemoryManager
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import current_process, cpu_count, Process
from datetime import datetime
import numpy as np
import pandas as pd
import tracemalloc
import time
import sys
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

def getFile(file):
    wordsInFile = []
    for line in file:
        splitList = line.split()
        for i in splitList:
            wordsInFile.append(i)
    file.close()
    return wordsInFile
# Python program for implementation of MergeSort
def mergeSort(arr):
    if len(arr) > 1:
         # Finding the mid of the array
        mid = len(arr)//2
        # Dividing the array elements
        L = arr[:mid]
        # into 2 halves
        R = arr[mid:]
        # Sorting the first half
        mergeSort(L)
        # Sorting the second half
        mergeSort(R)
        i = j = k = 0
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def getSize(filename):
    st = os.stat(filename)
    return st.st_size

def work_with_shared_memory(shm_name, shape, dtype, i):
    print(f'With SharedMemory: {current_process()}')
    # Locate the shared memory by its name
    shm = SharedMemory(shm_name)
    # Create the np.recarray from the buffer of the shared memory
    np_array = np.recarray(shape=shape, dtype=dtype, buf=shm.buf)
    mergeSort(np_array[(i-1)*(np_array.size/cpu_count()):i*(np_array.size/cpu_count())])
    return np.nansum(np_array.val)


def work_no_shared_memory(np_array: np.recarray):
    print(f'No SharedMemory: {current_process()}')
    # Without shared memory, the np_array is copied into the child process
    mergeSort(np_array)
    return np.nansum(np_array.val)


if __name__ == "__main__":

    # User file input
    fileName = input("Enter File Name: ")
    file = open(fileName, "r")
    # Display file size in KB or MB (whichever looks better)
    numBytes = getSize(fileName)
    if (numBytes < 1e6):
        print(f"file size = {getSize(fileName)/1e3}KB")
    else:
        print(f"file size = {getSize(fileName)/1e6}MB")

    # Make a large data frame with date, float and character columns
    a = getFile(file)
    #df = pd.DataFrame(a)
    #Convert into numpy recarray to preserve the dtypes
    np_array = np.array(a)
    #del df
    shape, dtype = np_array.shape, np_array.dtype

    # With shared memory
    # Start tracking memory usage
    tracemalloc.start()
    start_time = time.time()
    with SharedMemoryManager() as smm:
        # Create a shared memory of size numBytes
        shm = smm.SharedMemory(sys.getsizeof(np_array))

        # Create a np.recarray using the buffer of shm
        shm_np_array = np.recarray(shape=shape, dtype=dtype, buf=shm.buf)
        # Copy the data into the shared memory
        np.copyto(shm_np_array, np_array)

        # Spawn some processes to do some work
        with ProcessPoolExecutor(cpu_count()) as exe:
            fs = [exe.submit(work_with_shared_memory, shm.name, shape, dtype, i)
                  for i in range(cpu_count())]
            for _ in as_completed(fs):
                pass
    # Check memory usage
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage {current/1e6}MB; Peak: {peak/1e6}MB")
    print(f'Time elapsed: {time.time()-start_time:.2f}s')
    tracemalloc.stop()

    # Without shared memory
    tracemalloc.start()
    start_time = time.time()
    mergeSort(np_array)

    # Check memory usage
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage {current/1e6}MB; Peak: {peak/1e6}MB")
    print(f'Time elapsed: {time.time()-start_time:.2f}s')
    tracemalloc.stop()

    file.close()