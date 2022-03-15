import os
import sys

#fname = input("Subtitle File Name")
fname = 'subs0226.txt'
subfile = open(fname, "r")
data = open('output.csv', "w")

lc = 0
process = -1
prevdata = False
data.write("item,time,fs,iso,ev,gps0,gps1,gps2,distance,height,hs,vs\n")
for line in subfile.readlines():
    lc = lc + 1
    if (lc-1) % 5 == 0 or (lc-1) == 0:
        prevdata = True
        # Number Line
        datanum = int(line)
        process = 0
        data.write((str(datanum) + ','))
        continue

    if process == 0:
        # Time Line
        start = line.split(' ')[0]
        data.write(str(lc) + ',')
        process = 1
        continue

    if process == 1:
        print('------')
        print("DATALINE")
        # Dataline
        dataline = line.split(',')
        print(dataline)
        fs = dataline[0][2:5]
        iso = dataline[2][5:8]
        ev = dataline[3][4]
        gps0 = dataline[5][6:len(dataline[5])]
        gps1 = dataline[6][1:len(dataline[6])]
        gps2 = dataline[7][1:len(dataline[7])-1]
        distance = dataline[8][3:len(dataline[8])-1]
        height = dataline[9][3:len(dataline[9])-1]
        hs = dataline[10][4:len(dataline[10])-3]
        vs = dataline[11][4:len(dataline[11])-5]

        dataprint = (str(fs) + ',' + str(iso) + ',' + str(ev) + ',' + str(gps0) + ',' + str(gps1) + ',' + str(gps2) +
                     ',' + str(distance) + ',' + str(height) + ',' + str(hs) + ',' + str(vs))
        data.write(dataprint)
        data.write('\n')
        print('------')
        process = -1
        continue




