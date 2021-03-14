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
            norad_cat_id = (25544, 44238, 44252, 44289, 44713, 44717),
            orderby=['norad_cat_id'],
            format='tle')

        with open('tle_latest.txt', 'w') as outfile:
            async for line in data:
                outfile.write(line + ' $ ' +'\n' )

loop = asyncio.get_event_loop()
loop.run_until_complete(download_latest_tles())


with open('tleout.txt', 'w') as outfile, open('tle_latest.txt', 'r') as infile:
    for line in infile:
        #outfile.write(line.splitlines())
        outfile.write(line.replace('   ',' ').strip())
i = 0
with open('tle.txt', 'w') as outfile, open('tleout.txt', 'r') as infile:
    for line in infile:
        i = i+1
        line = line.strip()
        ldata = line.split('$')
        #outfile.write(ldata + '\n')

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


tles = []
i =0
with open('tledata.txt', 'r') as data:
    for line in data:
        i = i+1
        line = line.strip()
        ld = line.split(' ')
        #print(line[1])
        temp_tle = {}
        linval = (i % 2)
        if linval > 0:
            temp_tle = {
                "element set": ld[0],
                "Satellite Number": ld[1],
                "Element Epoch": ld[3],
                "Mean Motion Deriv": ld[4]
                        }
        if linval == 0:
            temp_tle = {
                "element set": ld[0],
                "Satellite Number": ld[1],
                "inclination": ld[2],
                "RAAN": ld[3],
                "Eccentricity": ld[4],
                "Argument of Perigee": ld[5],
                "Mean Anomaly": ld[6],
                "Mean Motion": ld[7],
                      }
        tles.append(temp_tle)

        target = i
        if target== 10:
            break
# Opens and saves a JSON file with the current data (good for visualization)
with open('tles.json', 'w') as fp:
    print(json.dump(tles, fp, indent=4))
    sys.stdout.flush()

# Below should be in use for spawing JSON files into RESTful API
#print(json.dumps(tles))
#sys.stdout.flush()
