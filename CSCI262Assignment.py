#!/usr/bin/env python3
import hashlib
import pandas as pd
from pathlib import Path
import numpy as np
import sys
import os

class RainbowTable():
    # init method or constructor

    def __init__(self, table ,chain, pw, collisionchecklist , hashingfunction , rainbow ):
        self.table = table
        self.chain = chain
        self.pw = pw
        self.collisionchecklist = collisionchecklist
        self.hashingfunction = hashingfunction
        self.rainbow = rainbow

    def progressbar(self, it, prefix="", size=60, out=sys.stdout): # Python3.6+
        count = len(it)
        def show(j):
            x = int(size*j/count)
            print(f"{prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{count}", end='\r', file=out, flush=True)
        show(0)
        for i, item in enumerate(it):
            yield item
            show(i+1)
        print("\n", flush=True, file=out)
    #simple normal binary search
    def binary_search(self ,arr, x):
        low = 0
        high = len(arr) - 1
        mid = 0

        while low <= high:

            mid = (high + low) // 2

            # If x is greater, ignore left half
            if arr[mid] < x:
                low = mid + 1

            # If x is smaller, ignore right half
            elif arr[mid] > x:
                high = mid - 1

            # means x is present at mid
            else:
                return mid

        # If we reach here, then the element was not present
        return 'notfound'



    def transversechain(self,reduction,chainhead):
        for i in range (0,self.chain-1):
            passwords = self.pw[0][reduction]
            passwordhash = self.hashingfunction(str(passwords).encode('utf8')).hexdigest()
            reduction = int(passwordhash,16) % len(self.pw)
            self.rainbow.append([chainhead,passwordhash])
            return self.rainbow.sort(key=lambda x:int(x[1],16))

    def generate(self):
        for i in self.progressbar(range(len(self.pw)), "Computing: ", 40):
            passwords = self.pw[0][i]
            if(self.pw[0][i][-4:]!='used'):
                self.pw[0][i] = self.pw[0][i] + 'used'
            elif(self.pw[0][i][-4:]=='used'):
                passwords = self.pw[0][i][:-4]
            passwordhash = self.hashingfunction(passwords.encode('utf8')).hexdigest()
            reduction = int(passwordhash,16)  % len(self.pw)
            chaintail = self.transversechain(reduction,passwords)

    #save tables so we dont have to run the creation everytime
    def saveandsorttables(self):
        # df1 = pd.DataFrame(self.table)
        df2 = pd.DataFrame(self.rainbow)
        np.savetxt(r'Rainbow.txt', df2.values, fmt='%s')
        with open('Passwords.txt', 'w') as sortedbooks:
            for i in range(len(self.pw)):
                sortedbooks.writelines(str(self.pw[0][i])+'\n')

        # np.savetxt(r'passhash.txt', df1.values, fmt='%s')
        # df1.to_excel("output1.xlsx")
      #  df2.to_excel("output2.xlsx")

    def loopchain(self,i,readpasswordhash,password):
        for x in range (self.chain):
            passwordhash = self.hashingfunction(str(readpasswordhash.iloc[i][0]).encode('utf8')).hexdigest()
            reduction = int(passwordhash,16)  % len(self.pw)
            if(self.hashingfunction(self.pw[0][reduction].encode('utf8')).hexdigest() == password):
                print('\npre image has been found : ' + self.pw[0][reduction] + '\n')
         
                return 'found'
            else:
                return 'notfound'



    def crack(self,hash,readpasswordhash):
        password= hash
        #search the hashes of the rainbow table and chain to find the password
        index = self.binary_search([int(i,16) for i in readpasswordhash['passwordhash']],int(password,16))
        if(index!='notfound'):
            stoploop = self.loopchain(index,readpasswordhash,password)
            # print(readpasswordhash.iloc[0][index])
        else:
            for i in range (len(self.pw)):
                if(i==len(self.pw)-2):
                    print('\npassword is not found in rainbow table\n\n')
                    break
                elif(self.hashingfunction(str(readpasswordhash.iloc[i][0]).encode('utf8')).hexdigest() == password):
                    print('\npre image has been found : ' +str(readpasswordhash.iloc[i][0])+'\n')
                    break
                else:
                    pointer = self.loopchain(i,readpasswordhash,password)
                    if(pointer=='found'):
                        break




#purpose memory saving process intensive but memory cheap now so i believe this can be obselete why ....


def main():
    passwordFileArg = ''
    def createList(r1, r2):
# Testing if range r1 and r2
# are equal
        if (r1 == r2):
            return r1
        else:
            # Create empty list
            res = []
            # loop to append successors to
            # list until r2 is reached.
            while(r1 < r2+1 ):
                res.append(r1)
                r1 += 1
            return res
    if(len(sys.argv)>1):
        passwordFileArg = str(sys.argv[1])
        if(passwordFileArg[-4:]!='.txt'):
            passwordFileArg = passwordFileArg + '.txt'
        while True:
            if(passwordFileArg[-4:]!='.txt'):
                passwordFileArg = passwordFileArg + '.txt'
            file=Path(str(passwordFileArg))
            if(file.exists()):
                print("\n\nPassword file has been found !\n\n")
                break
            else:
                passwordFileArg = input("password reference file(ARGUMENT) not found please input another file name\n")
    else:            
        while True:
            if(len(passwordFileArg)==0):
                passwordFileArg = input("Please input a reference password file name\n")
                if(passwordFileArg[-4:]!='.txt'):
                    passwordFileArg = passwordFileArg + '.txt'
                    file=Path(str(passwordFileArg))
                    if(file.exists()):
                        print("\n\nPassword file has been found !\n\n")
                        break
                    else:
                        passwordFileArg = input("file not found please input another file name\n")
            else:
                if(passwordFileArg[-4:]!='.txt'):
                    passwordFileArg = passwordFileArg + '.txt'
                file=Path(str(passwordFileArg))
                if(file.exists()):
                    print("\n\nPassword file has been found !\n\n")
                    break
                else:
                    passwordFileArg = input("file not found please input another file name\n")

    print("Rainbow Table functions what would you like to do? Please select options")
    print("//Please note files associated such as password files and generated rainbow table files will be in the same directory//")
    print("1 . generate rainbow table")
    print("2 . Crack password hash")
    print("3 . Refresh reference file(remove all used tag on the passwords in the reference file)")
    print("4 . Exit the Program")
    while True:
        try:
            chioce = float(input())
            if chioce < 1 or chioce > 4:
                raise ValueError
            elif(chioce==1):
                while True:
                    file=Path(str(passwordFileArg))
                    if file.exists():
                        df = pd.read_csv( passwordFileArg, header=None)
                        df = df.replace(np.nan, 'null', regex=True)
                        instance = RainbowTable( [], 5, df ,createList(0,len(df)-1), hashlib.md5,[])
                        print("Reading")
                        print(len(df))
                        print("rows of password")
                        instance.generate()
                        instance.saveandsorttables()
                        print('Rainbow table Rainbow.txt created in current directory')
                        print("1 . generate rainbow table")
                        print("2 . Crack password hash")
                        print("3 . Refresh reference file(remove all used tag on the passwords in the reference file)")
                        print("4 . Exit the Program")
                        break
                    else:
                        print("filename does not exist, please enter another file")
                        pass
                        

            elif(chioce==2):
                filename = 'Rainbow.txt'
                if(Path(str(filename)).exists()):
                    readpasswordhash= pd.read_csv(filename,sep=' ',names=['password','passwordhash'] )
                    unused = []
                    df = pd.read_csv( passwordFileArg, header=None)
                    df = df.replace(np.nan, 'null', regex=True)
                    while True:
                        hash = input("Please input a valid hash to crack \n")
                        if(len(hash)==32):
                            print("----------------------------------------------------------------------------------------------------------------------")
                            print("Currently rehashing and appending of rainbow table is not supported")
                            print("\nPlease note the following passwords has not been hashed(error) or has been untaged in your reference file :  ")
                            df2= df
                            df = [x[:-4] if x[-4:]=='used' else x for x in df[0]]
                            dfreport = [x[:-4] if x[-4:]=='used' else unused.append(x) for x in df2[0]]
                            if(len(unused)!=0 and len(unused) != len(df)):
                                for i in range(len(unused)):
                                    print(unused[i])
                            elif(len(unused) == len(df)):
                                print("THE REFERENCE FILE PASSWORDS HAS ALL BEEN UNTAGGED. PLEASE CONSIDER REHASHING THE PASSWORDS")
                            else:
                                print('ALL PASSWORD IN REFERNCE FILE HASH BEEN TAGGES USED')
                            print("----------------------------------------------------------------------------------------------------------------------")
                            instance = RainbowTable( [], 5, pd.DataFrame(df) ,createList(0,len(df)-1), hashlib.md5,[])
                            instance.crack(hash,readpasswordhash)
                            print("1 . generate rainbow table")
                            print("2 . Crack password hash")
                            print("3 . Refresh reference file(remove all used tag on the passwords in the reference file)")
                            print("4 . Exit the Program")
                            break
                        else:
                            print("WARNING: you input hash is not 32 chars")
                            pass
                else:
                    print("***************Rainbow table does not exist please generate the rainbow table")
                    print("1 . generate rainbow table")
                    print("2 . Crack password hash")
                    print("3 . Refresh reference file(remove all used tag on the passwords in the reference file)")
                    print("4 . Exit the Program")
                    pass
            elif(chioce ==3):
                while True:
                    if(Path(str(passwordFileArg)).exists()):
                        df = pd.read_csv(passwordFileArg, header=None)
                        df = df.replace(np.nan,'null', regex=True)
                        df = [str(x[:-4]) if str(x[-4:])=='used' else str(x) for x in df[0]]
                        df = pd.DataFrame(df)
                        instance = RainbowTable( [], 5, df ,createList(0,len(df)-1), hashlib.md5,[])
                        with open(passwordFileArg, 'w') as sortedbooks:
                            for i in instance.progressbar(range(len(df)), "Computing: ", 40):
                                sortedbooks.writelines(str(df[0][i])+'\n')
                        print("1 . generate rainbow table")
                        print("2 . Crack password hash")
                        print("3 . Refresh reference file(remove all used tag on the passwords in the reference file)")
                        print("4 . Exit the Program")
                            
                        break
                    else:
                        print("password reference file is not found")
                        passwordFileArg = input("Please input password file name again")
                        pass
                    # except Exception as e:
                    #     print('file not found')
            else:
                break

        except ValueError:
            print('Please enter a valid chioce.')


if __name__ == "__main__":
        main()
                











