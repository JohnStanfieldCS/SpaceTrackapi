import asyncio
import json
import sys
import re 
from pprint import pprint
import spacetrack.operators as op
from spacetrack.aio import AsyncSpaceTrackClient


async def download_latest_tles():
    st = AsyncSpaceTrackClient(identity='jts0079@auburn.edu',
                               password='VMCAApassword21')

    async with st:
        data = await st.tle_latest(
            iter_lines=True, 
            ordinal=1, 
            epoch='>now-60',
            norad_cat_id = (47854,47760, 47768, 47757),
            orderby=['norad_cat_id'],
            format='tle')

        with open('tle_latest.txt', 'w') as outfile:
            async for line in data:
                outfile.write(line + ' $ ' +'\n' )

loop = asyncio.get_event_loop()
loop.run_until_complete(download_latest_tles())

with open('tleout.txt', 'w') as outfile, open('tle_latest.txt', 'r') as infile:
    for line in infile:
        outfile.write(line.replace('   ',' ').strip())
i = 0
with open('tleout.txt', 'r') as infile:
    for line in infile:
        i = i+1
        line = line.strip()
        ldata = line.split('$')

with open('tledata.txt', 'w') as outfile:
    j = 0
    for m in ldata: 
        if (j % 2 ) == 0:
            tle = ldata[j]
        elif (j % 2 ) > 0:
            tle = ldata[j]
        data = tle.replace('  ',' ')
        outfile.write(data + '\n')
        j = j+1

with open('tledata.txt', 'r') as inF:
    tlelist = []
    count = 1
    for line in inF:
        line = line.rstrip()

        if count % 2 == 0:
            tlelist.append(old_line + ' ' + line)
        else: 
            old_line = line
        count += 1

with open('TLEcomb.txt', 'w') as outF:
    satnum = 0
    for line in tlelist: 
        data = tlelist[satnum]
        outF.write(data + ' \n')
        satnum = satnum + 1

tles = []
counter =0
with open('TLEcomb.txt', 'r') as data:
    for line in data:
        counter = counter+1
        line = line.strip()
        ld = line.split(' ')
        temp_tle = {
                "Satellite Number": ld[10],
                "Element Epoch": ld[3],
                "Mean Motion Derivative": ld[4],
                "inclination": ld[11],
                "RAAN": ld[12],
                "Eccentricity": ld[13],
                "Argument of Perigee": ld[14],
                "Mean Anomaly": ld[15],
                "Mean Motion": ld[16],
                      }
        tles.append(temp_tle)

        if counter == count-1:
            break
# Opens and saves a JSON file with the current data (good for visualization)
with open('tles.json', 'w') as fp:
    print(json.dump(tles, fp, indent=4))
    sys.stdout.flush()

# Below should be in use for spawing JSON files into RESTful API
#print(json.dumps(tles))
#sys.stdout.flush()
