import sys
import struct
import numpy as np
import timeit

"""1. Variables, Their Binary Representation, Bits, Bytes and Memory Requirements
"""
# Finding number of bytes
print(f"There are {np.int8().itemsize} bytes in int8")
print(f"There are {np.int32().itemsize} bytes in int32")
print(f"There are {np.uint32().itemsize} bytes in uint32")
print(f"There are {np.int64().itemsize} bytes in int64")
print(f"There are {np.float32().itemsize} bytes in float32")
print(f"There are {np.float64().itemsize} bytes in float64")


print("")
#using sys.getsizeof()
print(f"There are {sys.getsizeof(np.int8())} bytes in int8")
print(f"There are {sys.getsizeof(np.int32())} bytes in int32")
print(f"There are {sys.getsizeof(np.uint32())} bytes in uint32")
print(f"There are {sys.getsizeof(np.int64())} bytes in int64")
print(f"There are {sys.getsizeof(np.float32())} bytes in float32")
print(f"There are {sys.getsizeof(np.float64())} bytes in float64")

print("")
# min and max values
print(f"The min is {np.iinfo(np.int8).min} and the max is {np.iinfo(np.int8).max}")
print(f"The min is {np.iinfo(np.int32).min} and the max is {np.iinfo(np.int32).max}")
print(f"The min is {np.iinfo(np.uint32).min} and the max is {np.iinfo(np.uint32).max}")
print(f"The min is {np.iinfo(np.int64).min} and the max is {np.iinfo(np.int64).max}")
print(f"The min is {np.finfo(np.float32).min} and the max is {np.finfo(np.float32).max}")
print(f"The min is {np.finfo(np.float64).min} and the max is {np.finfo(np.float32).min}")


print("")
#binary form
print(f"Binary form for 8 is {bin(8)}")
print(f"Binary form for 127 is {bin(127)}")
print(f"Binary form for 128 is {bin(128)}")
print(f"Binary form for 255 is {bin(255)}")
print(f"Binary form for -255 is {bin(-255)}")
print(f"Binary form for -255 is {bin(struct.unpack('!I', struct.pack('!f', 1.125))[0])}")


print()
#determine, using the .bit_length() the smallest data type you could use to store the above values.
print(f"8: {int.bit_length(8)} bits")
print(f"127: {int.bit_length(127)} bits")
print(f"128: {int.bit_length(128)} bits")
print(f"255: {int.bit_length(255)} bits")
print(f"-255: {int.bit_length(-255)} bits")
print(f"-255: {int.bit_length((struct.unpack('!I', struct.pack('!f', 1.125))[0]))} bits")


"""2. Estimating Arithmetic Intensity"""
#Estimate the Arithmetic Intensity of the problem if it is performed using 8-bit integers
#𝑦[𝑖]=𝑎⋅𝑥[𝑖]+𝑏
# 2 FLOPS (multiplying array of size N by a --> results in a single array, then adding that value to b)
# 3 bytes of memory operations (𝑥[𝑖] followed by 𝑎⋅𝑥[𝑖] then followed by 𝑎⋅𝑥[𝑖]+𝑏) - 3 operations 1 byte per
# Therefore Arthmetic Intensity is 2/3

#Estimate the Arithmetic Intensity of the problem if it is performed using single precision floating point values.
# 2 FLOPS (multiplying array of size N by a --> results in a single array, then adding that value to b)
# 12 bytes of memory operations (𝑥[𝑖] followed by 𝑎⋅𝑥[𝑖] then followed by 𝑎⋅𝑥[𝑖]+𝑏) - 3 operations 4 byte per
# Therefore Arthmetic Intensity is 2/12 = 1/6

#Estimate the Arithmetic Intensity if performed in double precision.
# 2 FLOPS (multiplying array of size N by a --> results in a single array, then adding that value to b)
# 24 bytes of memory operations (𝑥[𝑖] followed by 𝑎⋅𝑥[𝑖] then followed by 𝑎⋅𝑥[𝑖]+𝑏) - 3 operations 8 byte per
# Therefore Arthmetic Intensity is 2/24 = 1/12

#Given the Roofline plot in Figure 2.2 of Notebook 2.1:, how would the compute time for each of the above case compare to that of double precision?
# Both 8-bit and single-precision are computer bound, but double precision is memory bound


"""Restructuring an Algorithm"""
# 𝑦[𝑖]=𝑎[𝑖]⋅𝑥[𝑖]+𝑏⋅𝑥[𝑖]+𝑏 .
# Estimate the Arithmetic Intensity of the problem if it is performed in single precision as expressed above.
# Number of operations for array of size N: N[(2N+1)+1+1+1]. 2N+1 is array multiplcation's summation, +1 for the
# addition, +1 for the multiplcation between b and the array, +1 for the addition at the end. Then multiplied by N
# for the size of the array therefore:
# N(2N+5) FLOPS
# 16 bytes of memory operation (𝑎[𝑖]⋅𝑥[𝑖], 𝑏⋅𝑥[𝑖], 𝑎[𝑖]⋅𝑥[𝑖]+𝑏⋅𝑥[𝑖], 𝑎[𝑖]⋅𝑥[𝑖]+𝑏⋅𝑥[𝑖]+𝑏). 4 operations 4 bytes each
# Arithmetic Intensity of (2N^2 + 5N)/16

#Compare the Arithmetic Intensity if you instead factorise the problem as evaluate it as
# 𝑦[𝑖]=(𝑎[𝑖]+𝑏)𝑥[𝑖]+𝑏
# Number of operations, assuming i=1, (𝑎[𝑖]+𝑏) is 1. Multiplying by 𝑥[𝑖] would be 2N + 2, then adding b is one
# Therefore FLOPS is 2N + 4
# 12 bytes of memory
# Arithmetic Intensity of (2N+4)/12 = (N+2)/6


# Use %timeit to test the performance of both implementions for arrays sizes of 100, 1000, 10000 elements.
array100 = np.array(np.zeros(100),np.float32)
array1000 = np.array(np.zeros(100),np.float32)
array10000 = np.array(np.zeros(100),np.float32)

print(timeit.timeit(array100))
print(timeit.timeit(array1000))
print(timeit.timeit(array10000))


