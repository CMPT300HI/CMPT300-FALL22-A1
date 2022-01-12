import subprocess as sp
import re
import os
def checkMakefile():
    '''
    this function will check if make file is working or not by running it 
    function will return true if make file works properly
    '''
    p = sp.run(['make'])
    if p.returncode !=0:
        return False
    else:
        return True

def checkProb1():
    '''
    This function will check if output file exists or is empty. if not, it will check if the file contains digit only. If yes, it will return true.
    '''
    fileExist = os.path.exists('output1.txt')
    myinteger = False
    if fileExist == False or os.stat('output1.txt').st_size == 0:
        return False
    else:
        fh = open('output1.txt','r')
        for i in fh:
            i = i.strip()
            if i.isdecimal():
                myinteger = True
            else:
                myinteger = False
                break
    if myinteger:
        return True
    else:
        return False

def checkProb2():
    '''
    This function reads a file containing memory details and calculates memory utilization
    '''
    f = open("meminfo.txt")
    for i in f:
        i = i.strip()
        if re.search('memtotal',i,re.IGNORECASE):
          x = re.search('memtotal:.*?([0-9]+)',i,re.IGNORECASE)
          memtotal= int(x.group(1))
        elif re.search('memfree',i,re.IGNORECASE):
          x = re.search('memfree:.*?([0-9]+)',i,re.IGNORECASE)
          memfree= int(x.group(1))
        elif re.search('^buffers',i,re.IGNORECASE):
          x = re.search('buffers:.*?([0-9]+)',i,re.IGNORECASE)
          buffers= int(x.group(1))
        elif re.search('^cached',i,re.IGNORECASE):
          x = re.search('cached:.*?([0-9]+)',i,re.IGNORECASE)
          cache= int(x.group(1))
        elif re.search('^slab',i,re.IGNORECASE):
          x = re.search('slab:.*?([0-9]+)',i,re.IGNORECASE)
          slab= int(x.group(1))
    memutil =((memtotal-memfree-buffers-cache-slab)/memtotal)*100
    return memutil

def checkProb3():
    '''
    this function will run 2 linux commands to check OS name and version details and capture the output
    function will return a list containing OS and version details
    '''
    osRelease = sp.run(['cat','/etc/os-release'],capture_output=True,text=True)
    version = sp.run(['cat','/proc/version'],capture_output=True,text=True)
    osR = (osRelease.stdout).split('\n')[0:3]
    ver =(version.stdout).split('\n')[0:1]
    result = osR + ver
    return result

def main():
    '''
    This is our main function where we check against each assignment and assign grades to student.
    '''
    totalPoint = 0
    x = checkMakefile()
    if x:
        totalPoint = totalPoint + 10
    else:
        if sp.run(['test','-f','meninfo.txt']).returncode == 0:
           totalPoint = totalPoint + 5
    prob1Point = 0
    prob2Point = 0
    prob3Point = 0
    prob1Result = checkProb1()
    prob2Result = round(checkProb2(),2)
    prob3Result = checkProb3()
    fh3 = open('output3.txt','r')
    cmpList3 = fh3.readlines()
    cmpList3 = [x.strip() for x in cmpList3]
    found = False
    if prob1Result:
        prob1Point =prob1Point +10
        totalPoint =totalPoint + prob1Point
    for i in prob3Result:
         if i in cmpList3:
             found = True
         else:
             found = False
    if (found):
         prob3Point = prob3Point + 10
         totalPoint = totalPoint + prob3Point
    fh2 = open('output2.txt','r')
    memUtilResult = float((fh2.read().strip('\n')))
    if abs(prob2Result - memUtilResult) < 6:
         prob2Point = prob2Point + 10
         totalPoint = totalPoint + prob2Point 
    return totalPoint,prob3Point,prob2Point,prob1Point

x = main()
print(x)