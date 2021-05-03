# Shared Memory vs. Non-Shared Memory

## Overview

The objective of this project was to compare the use of shared memory and non-shared memory in data processing. For this implementation only summation and sorting operations were used for data processing. The shared memory used multithreading to concurrently sort the data throughout the memory, and the non-shared memory only used the main thread to sort. 

## Code Structure

The only two files that are relavent are the `shared_mem_ex.py` and `shared_mem_ex_customfile.py`. `shared_mem_ex.py` performs summing up randomly generated data that is stored in the memory. `shared_mem_ex_customfile.py` sorts a custom input file using merge sort, where the custom input file was a `.txt` book file. Only the shared memory section of the code is breifly explained below because the non-shared memory just runs the data processing on a single thread.

### Shared Memory Code

The shared memory code takes in the data and stores it into a memory buffer, which will be used throughout all of the different threads that are utilized. Once the data is stored in the memory buffer, a loop is used to perform the data processing operation over a given section of the memory, therefore all of the data will be sorted at the same time. A python library designed for getting the number of availiable threads is used, so all of the availiable threads are utilized.

```
with ProcessPoolExecutor(cpu_count()) as exe:
  fs = [exe.submit(work_with_shared_memory, shm.name, shape, dtype, i)
        for i in range(cpu_count())]
  for _ in as_completed(fs):
    pass
```
                
## Results and Analysis

Below are a couple of the visual results that are outputted after running the code:

![Small File Results](https://github.com/cglosner/SharedMemory/blob/main/smallFile.PNG)
![Large File Results](https://github.com/cglosner/SharedMemory/blob/main/mediumFile.PNG)

Next, is a plot of the general trend of running the program against various file sizes:

![Graphical Results](https://github.com/cglosner/SharedMemory/blob/main/plot.png)

As you can see from the results, there was a significant speed up in by using the shared memory compared to using the non-shared memory, but there was also a need for more memory and cores to obtain that time speed up.
