import array
import math
import csv
import sys


# count the numbers of emails that the file have
def countEntries(file):
    f = open(file)
    count = 0
    for row in f:
        count += 1
    f.close()

    if math.ceil(numberOfBitsInTheFilter(count, 0.0000001) / (-numberOfHashFunctions(count, 0.0000001) / math.log(
            1 - math.exp(math.log(0.0000001) / numberOfHashFunctions(count, 0.0000001))))) == count:
        return count
    return count + 1


# Calculates the number of bits needed in the filter
def numberOfBitsInTheFilter(N, P):  # 'N' is the number of items in the filter and 'P' the probability of false positive
    return math.ceil((N * math.log(P)) / (math.log(1 / (pow(2, math.log(2))))))


# Calculates the number of hash functions needed
def numberOfHashFunctions(N, P):  # 'n' is the number of items in the filter and 'p' the probability of false positive
    M = numberOfBitsInTheFilter(N, P)
    K = round((M/N) * math.log(2))  # 'k' is the number of hash functions
    return K


# set to one the bit of the position the hash function returns passing the email
def add(arrayBit, item, K, M):
    count = 1
    while count < K:
        index = hash(str(item) + str(count)) % M
        setBit(arrayBit, index)
        count += 1


# checks if the given item(email) is in the db verifying if the bit of the given position is set to 1
# If all positions that returns are set to one it will return True, else it will return false
def check(arrayBit, item, K, M):
    count = 0
    while count < K:
        index = hash(str(item) + str(count)) % M
        result = testBit(arrayBit, index)
        if result == 0:
            return False
        count += 1
    return True


# ------------------------ BIT ARRAYS METHODS ------------------------
# creates a array of bits passing the size of the array
def makeBitArray(bitSize, fill=0):
    intSize = int(bitSize) >> 5                   # number of 32-bit integers
    if int(bitSize) & 31:                         # if bitSize != (32 * n) add
        intSize += 1                         # a record for stragglers
    if fill == 1:
        fill = 4294967295                    # all bits set
    else:
        fill = 0                             # all bits cleared

    bitArray = array.array('I')              # 'I' = unsigned 32-bit integer
    bitArray.extend((fill,) * intSize)
    return bitArray


# testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.
def testBit(array_name, bit_num):
    record = int(bit_num) >> 5
    offset = int(bit_num) & 31
    mask = 1 << offset
    return array_name[record] & mask


# setBit() returns an integer with the bit at 'bit_num' set to 1.
def setBit(array_name, bit_num):
    record = int(bit_num) >> 5
    offset = int(bit_num) & 31
    mask = 1 << offset
    array_name[record] |= mask
    return array_name[record]


# clearBit() returns an integer with the bit at 'bit_num' cleared.
def clearBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return array_name[record]


# toggleBit() returns an integer with the bit at 'bit_num' inverted, 0 -> 1 and 1 -> 0.
def toggleBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] ^= mask
    return array_name[record]


# --------------------- BLOOM FILTER IMPLEMENTATION ---------------------
inputList1 = []
inputList2 = []

if len(sys.argv) > 1:
    with open(sys.argv[1]) as csvFile1:
        csvReader = csv.reader(csvFile1)
        next(csvReader)
        for line in csvReader:
            inputList1.append(line)

    with open(sys.argv[2]) as csvFile2:
        csvReader = csv.reader(csvFile2)
        next(csvReader)
        for line in csvReader:
            inputList2.append(line)

    n = countEntries(sys.argv[1])
    p = 0.0000001
    m = numberOfBitsInTheFilter(n, p)
    k = numberOfHashFunctions(n, p)

    bloomFilterArray = makeBitArray(m)

    counter = 0
    while counter < len(inputList1):
        add(bloomFilterArray, inputList1[counter], k, m)
        counter += 1

    counter = 0
    while counter < len(inputList2):
        if check(bloomFilterArray, inputList2[counter], k, m):
            print(str(*inputList2[counter]) + ",Probably in the DB")
        else:
            print(str(*inputList2[counter]) + ",Not in the DB")
        counter += 1

# ----------------------------------------------------------------------
# THIS PART WAS USED FOR TESTING USING THE INPUT1.CSV & ENTRIES.CSV FILE
# with open('input1.csv') as csvFile1:
#     csvReader = csv.reader(csvFile1)
#     next(csvReader)
#     for line in csvReader:
#         inputList1.append(line)
#
# with open('entries.csv') as csvFile2:
#     csvReader = csv.reader(csvFile2)
#     next(csvReader)
#     for line in csvReader:
#         inputList2.append(line)
#
# n = countEntries('input1.csv')
# p = 0.0000001
# m = numberOfBitsInTheFilter(n, p)
# k = numberOfHashFunctions(n, p)
#
# bloomFilterArray = makeBitArray(m)
#
# counter = 0
# while counter < len(inputList1):
#     add(bloomFilterArray, inputList1[counter], k, m)
#     counter += 1
#
# counter = 0
# while counter < len(inputList2):
#     if check(bloomFilterArray, inputList2[counter], k, m):
#         print(str(inputList2[counter]) + ",Probably in the DB")
#     else:
#         print(str(inputList2[counter]) + ",Not in the DB")
#     counter += 1
