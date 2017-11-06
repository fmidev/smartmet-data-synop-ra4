#!/bin/sh
#
# Finnish Meteorological Institute / Mikko Rauhala (2015-2016)
#
# SmartMet Data Ingestion Module for SYNOP Observations for RA IV
#

URL=https://ra4-gifs.weather.gov/data/RMTN/SURFACE/

if [ -d /smartmet ]; then
    BASE=/smartmet
else
    BASE=$HOME
fi

IN=$BASE/data/incoming/synop
OUT=$BASE/data/gts
EDITOR=$BASE/editor/in
TMP=$BASE/tmp/data/synop
TIMESTAMP=`date +%Y%m%d%H%M`

SYNOPFILE=$TMP/${TIMESTAMP}_gts_world_synop.sqd
SHIPFILE=$TMP/${TIMESTAMP}_gts_world_ship.sqd
BUOYFILE=$TMP/${TIMESTAMP}_gts_world_buoy.sqd
TMPFILE=$TMP/synop-$$.txt

mkdir -p $TMP
mkdir -p $OUT/{synop,ship,buoy}/world/querydata

echo "URL: $URL"
echo "IN:  $IN" 
echo "OUT: $OUT" 
echo "TMP: $TMP" 
echo "SYNOP File: $SYNOPFILE"
echo "SHIP  File: $SHIPFILE"
echo "BUOY  File: $BUOYFILE"
echo "TMP File: $TMPFILE"

echo "Fetching file list..."

FILES=$(wget -nv -O - $URL | grep -oP 'href="\KS[IMN][^"]+(?=")')
echo "done";

for file in $FILES
do
    echo -n $file
    if [ -s $IN/$file ]; then
      	echo " cached"
    else
	echo "$download$URL/$file" >> $TMPFILE;
	echo " download"
    fi
done 

echo "Downloading files...";
cat $TMPFILE | xargs -n 1 -P 50 wget -nv -N --no-check-certificate -P $IN
echo "done"

rm -f $TMPFILE

# Do SYNOP stations
synop2qd -t "$IN/*" > $SYNOPFILE

# Do SHIP SYNOP stations
synop2qd -S -t -p 1002,SHIP "$IN/*" > $SHIPFILE

# Do SHIP SYNOP stations
synop2qd -B -t -p 1017,BUOY "$IN/*" > $BUOYFILE


if [ -s $SYNOPFILE ]; then
    lbzip2 -k $SYNOPFILE
    mv -f $SYNOPFILE $OUT/synop/world/querydata/
    mv -f ${SYNOPFILE}.bz2 $EDITOR
fi

if [ -s $SHIPFILE ]; then
    lbzip2 -k $SHIPFILE
    mv -f $SHIPFILE $OUT/ship/world/querydata/
    mv -f ${SHIPFILE}.bz2 $EDITOR
fi

if [ -s $BUOYFILE ]; then
    lbzip2 -k $BUOYFILE
    mv -f $BUOYFILE $OUT/buoy/world/querydata/
    mv -f ${BUOYFILE}.bz2 $EDITOR
fi

rm -f $TMP/*.sqd*
