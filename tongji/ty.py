#!/usr/bin/python
import os
import xlwt

os.system('sh 1 >data.txt')
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Sheet1')
header = ['vteam','image','label','ns']
for i in range(len(header)):
    sheet.write(0, i, header[i])
with open('data.txt', 'r') as f:
    lines = f.readlines()
row = 1
for line in lines:
    data = line.strip().split(',')
    for i in range(len(data)):
        sheet.write(row, i, data[i])
    row += 1

os.system('sh 2')
with open('f3', 'r') as f:
    llines = f.readlines()

for line in llines:
    data = line.strip().split(',')
    for i in range(len(data)):
        sheet.write(row, i, data[i])
    row += 1


os.system('sh 4>f4')
with open('f4', 'r') as f:
    llines = f.readlines()
for line in llines:
    data = line.strip().split(',')
    for i in range(len(data)):
        sheet.write(row, i, data[i])
    row += 1
workbook.save('output.xls')


os.system('sh 3')
