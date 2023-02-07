#!/usr/bin/env python3

# Homework Number: 6
# Name: Steven Rutledge
# ECN Login: rutleds
# Due Date: 2/28/22

from email import message
from math import floor
import sys
from BitVector import *
from PrimeGenerator import PrimeGenerator
import solve_pRoot_BST
import numpy

def keyGen():
    primeGenerator = PrimeGenerator(bits = 128)
    prime = primeGenerator.findPrime()
    return(prime)
    

def encryptHelp(messageFile, p, q, outFile):
    bv = BitVector(filename = messageFile)
    fOut = open(outFile, 'w')

    n = BitVector (intVal = (p*q))
    e = BitVector(intVal = 3)
    while (bv.more_to_read):
        bvBlock = bv.read_bits_from_file( 128 )
        while(bvBlock._getsize() < 128):
            bvBlock += BitVector(bitstring = '0')   
        while(bvBlock._getsize() < 256):
            bvBlock.pad_from_left(1)
        encrypt = int(bvBlock) ** int(e)
        newEncypt = BitVector(intVal = (encrypt % int(n)))
        while(len(newEncypt) % 256 != 0):
            newEncypt.pad_from_left(1)
        fOut.write(newEncypt.get_bitvector_in_hex())
    fOut.close()
    
def encryption(messageFile, file1, file2, file3, nfile):
    fOut = open(nfile, 'w')
    p1 = keyGen()
    q1 = keyGen()
    n1 = p1 * q1
    fOut.write(str(n1)+ '\n')
    encryptHelp(messageFile, p1, q1, file1)

    p2 = keyGen()
    q2 = keyGen()
    n2 = p2 * q2
    fOut.write(str(n2)+'\n')
    encryptHelp(messageFile, p2, q2, file2)

    p3 = keyGen()
    q3 = keyGen()
    n3 = p3 * q3
    fOut.write(str(n3)+'\n')
    encryptHelp(messageFile, p3, q3, file3)
    
    fOut.close()

def crack(encFile1, encFile2, encFile3, nFile, outFile):
    # print(solve_pRoot_BST.solve_pRoot(3, 27))
    fNFile = open(nFile)
    n1 = int(fNFile.readline().rstrip('\n'))
    n2 = int(fNFile.readline().rstrip('\n'))
    # print(n2)
    # print(n2+1)
    n3 = int(fNFile.readline().rstrip('\n'))
    bigN = n1 * n2 * n3
    # print(bigN)
    fNFile.close()
    enc1File = open(encFile1)  
    enc1 = (BitVector( hexstring = enc1File.read() ))
    enc1File.close()
    enc2File = open(encFile2)  
    enc2 = (BitVector( hexstring = enc2File.read() ))
    enc2File.close()
    enc3File = open(encFile3)  
    enc3 = (BitVector( hexstring = enc3File.read() ))
    enc3File.close()

    fOUT = open(outFile, 'w')
    mult = 1

    m1 = BitVector(intVal = n1)
    m2 = BitVector(intVal = n2)
    m3 = BitVector(intVal = n3)
    M = BitVector(intVal = bigN)
    M1 = bigN//n1
    M2 = bigN//n2
    M3 = bigN//n3

    
    c1 = M1 * pow(M1, -1, n1)
    c2 = M2 * pow(M2, -1, n2)
    c3 = M3 * pow(M3, -1, n3)
    bottom = min(len(enc1), len(enc2), len(enc3))
    

    while(mult * 256 - 1 < bottom):
        # print(mult)
        bitvec1 = int(enc1[256*(mult-1): 256*mult])
        bitvec2 = int(enc2[256*(mult-1): 256*mult])
        bitvec3 = int(enc3[256*(mult-1): 256*mult])
        one = bitvec1 * c1
        two = bitvec2 * c2
        three = bitvec3 * c3
        Sum = one + two + three
        
        M3 = Sum % bigN

        intM = solve_pRoot_BST.solve_pRoot(3,M3)
        outM = BitVector(intVal = intM)
        # print(outM)
        while(outM._getsize() < 256):
            outM.pad_from_left(1)
            
        MFinal = outM[128:]
        fOUT.write(MFinal.get_bitvector_in_ascii().rstrip('\0'))
        mult+=1

    fOUT.close()

if __name__ == "__main__":
    args = sys.argv[1:]
    print(args)

    if(args[0]) == '-e':
        encryption(args[1], args[2], args[3], args[4], args[5])
    
    elif(args[0] == '-c'):
        crack(args[1], args[2], args[3], args[4], args[5])
