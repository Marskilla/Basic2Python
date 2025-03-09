# Converted from ProgramsToConvert\FirstProgram\01-SourceProgram.bas using Basic2Python.py V0.0.1

# Required for CLS equivalent
import os

# 5 CLS
os.system('cls' if os.name == 'nt' else 'clear')
# 10 a$="Welcome to this first program"
aS="Welcome to this first program"
# 20 PRINT a$
print(aS)
# 30 PRINT"to convert in Python"
print("to convert in Python")
# 40 PRINT""
print()
# 50 PRINT"What is your name"
print("What is your name")
# 60 INPUT name$
nameS = input()
# 70 INPUT"What is your age : ",age%
ageN = int(input("What is your age : "))
# 80 CLS
os.system('cls' if os.name == 'nt' else 'clear')
# 80 PRINT "Next year, ";name$;" you will be";age%+1;"."
print("Next year, ", nameS, " you will be", ageN+1, ".", end='')
