#!/usr/bin/env python3

# Homework Number: 6
# Name: Steven Rutledge
# ECN Login: rutleds
# Due Date: 2/28/22

from email import message
import sys
from turtle import left
from BitVector import *
from PrimeGenerator import PrimeGenerator

def keyGen(pOut, qOut):
    pGenerator = PrimeGenerator(bits = 128)
    p = pGenerator.findPrime()
    qGenerator = PrimeGenerator(bits = 128)
    q = qGenerator.findPrime()
    # print(q)
    # print(p)
    # Write to File after Encrpytion
    f = open(pOut, 'w')
    f.write(str(p))
    f.close()
    fq = open(qOut, 'w')
    fq.write(str(q))
    fq.close()

def encryption(messageFile, pFile, qFile, outFile):
    print("Encryption")
    FILEINP = open(pFile)
    p = int(FILEINP.read())
    print(p)
    FILEINP.close()
    FILEINQ = open(qFile)
    q = int(FILEINQ.read())
    print(q)
    FILEINQ.close()
    bv = BitVector(filename = messageFile)
    fOut = open(outFile, 'w')

    n = BitVector (intVal = (p*q))
    e = BitVector(intVal = 65537)
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
    
def decryption(encryptionFile, pFile, qFile, outFile):
    print("decryption")
    FILEINP = open(pFile)
    p = int(FILEINP.read())
    # print(p)
    FILEINP.close()
    FILEINQ = open(qFile)
    q = int(FILEINQ.read())
    # print(q)
    FILEINQ.close()
    n = BitVector (intVal = (p*q))
    totN = BitVector (intVal = ((p-1)*(q-1)))
    e = BitVector(intVal = 65537)
    d = e.multiplicative_inverse(totN)
    # print(d)
    FILEIN = open(encryptionFile)                                                  #(J)
    bv = BitVector( hexstring = FILEIN.read() )
    FILEIN.close
    fOUT = open(outFile, 'w')
    mult = 1
    leftover = bv._getsize() % 256
    
    while(mult * 256 - 1 < bv._getsize()):
        
        bitvec = bv[256*(mult-1): 256*mult]
        block = int(bitvec)
        dInt = int(d)
        Vp = pow(block,dInt, p)
        Vq = pow(block,dInt, q)


        bQ = BitVector(intVal = q)
        bP = BitVector(intVal = p)
        Xp = q * (int(bQ.multiplicative_inverse(bP)))
        Xq = p * (int(bP.multiplicative_inverse(bQ)))
        preChop = BitVector(intVal = ((Vp*Xp + Vq*Xq) % int(n)))
        # print(preChop)
        while(preChop._getsize() < 256):
            preChop.pad_from_left(1)
        print(preChop.get_bitvector_in_ascii())
        postChop = preChop[128:]
        # print(postChop.get_bitvector_in_ascii())
        fOUT.write(postChop.get_bitvector_in_ascii().rstrip('\0'))
        mult+=1
 
    fOUT.close()



if __name__ == "__main__":
    args = sys.argv[1:]
    print(args)
    if(args[0]) == '-g':
        keyGen(args[1], args[2])

    if(args[0]) == '-e':
        encryption(args[1], args[2], args[3], args[4])
    
    elif(args[0] == '-d'):
        decryption(args[1], args[2], args[3], args[4])
