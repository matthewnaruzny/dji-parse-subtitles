import sys
import os
import argparse

import subprocess
import simplekml

ffmpeg = "/usr/local/bin/ffmpeg"


def extract_subtitle(filename):
    # Extract Subtitle Track from MP4
    titlename = filename.split('.')[0]
    mstatus = subprocess.run("ffmpeg -i " + filename + " -map 0:s:0 " + titlename + ".srt").returncode
    if mstatus != 0:
        print("Failed to extract subtitles. Check filename and ffmpeg installation.")
        sys.exit()


def write_csv(filename):
    titlename = filename.split('.')[0]
    subfile = open((titlename + '.srt'), "r")
    csvdata = open((titlename + '.csv'), "w")
    csvdata.write("item,time,fs,iso,ev,gps0,gps1,gps2,distance,height,hs,vs\n")
    lc = 0
    process = -1
    prevdata = False

    for line in subfile.readlines():
        lc = lc + 1
        if (lc - 1) % 5 == 0 or (lc - 1) == 0:
            prevdata = True
            # Number Line
            datanum = int(line)
            process = 0
            csvdata.write((str(datanum) + ','))
            continue

        if process == 0:
            # Time Line
            start = line.split(' ')[0]
            csvdata.write(str(lc) + ',')
            process = 1
            continue

        if process == 1:
            # Dataline
            dataline = line.split(',')
            fs = dataline[0][2:len(dataline[0])]
            iso = dataline[2][5:len(dataline[2])]
            ev = dataline[3][4:len(dataline[3])]
            gps0 = dataline[5][6:len(dataline[5])]
            gps1 = dataline[6][1:len(dataline[6])]
            gps2 = dataline[7][1:len(dataline[7]) - 1]
            distance = dataline[8][3:len(dataline[8]) - 1]
            height = dataline[9][3:len(dataline[9]) - 1]
            hs = dataline[10][4:len(dataline[10]) - 3]
            vs = dataline[11][4:len(dataline[11]) - 5]

            dataprint = (
                    str(fs) + ',' + str(iso) + ',' + str(ev) + ',' + str(gps0) + ',' + str(gps1) + ',' + str(gps2) +
                    ',' + str(distance) + ',' + str(height) + ',' + str(hs) + ',' + str(vs))
            csvdata.write(dataprint)
            csvdata.write('\n')

            process = -1
            continue

    csvdata.close()
    subfile.close()


def write_kml(filename):
    titlename = filename.split('.')[0]
    csvdata = open((titlename + '.csv'), "r")
    kml = simplekml.Kml()
    lc = 0
    for line in csvdata.readlines():
        lc = lc + 1
        data = line.split(',')
        gps0 = data[5]
        gps1 = data[6]
        gps2 = data[7]
        kml.newpoint(description=lc,
                     coords=[(gps0, gps1, gps2)])

    kml.save(titlename + '.kml')


def clean(filename):
    # Clean up extra files
    titlename = filename.split('.')[0]
    os.remove(titlename + '.srt')


# Generate CSV by default.

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Drone video filename")
parser.add_argument("-s", help="Keep Subtitle File", action="store_true")
parser.add_argument("-k", help="Generate KML", action="store_true")
args = parser.parse_args()

input_filename = args.filename

extract_subtitle(input_filename)
write_csv(input_filename)
if args.k:
    write_kml(input_filename)
if not args.s:
    clean(input_filename)

print("\n\n--Done--")
