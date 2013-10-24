#!/bin/bash
if [ ! -d "./animations" ]; then
	mkdir tmp
fi
for ARG in $*
do
	filename=$(basename "$ARG")
	filename="${filename%.*}"
	giffile="${filename}.gif"
	#ffmpeg -ss 00:00:00.000 -i $1 -pix_fmt rgb24 -r 10 -s 1024x768 -t 00:00:20.000 $filename.temp.gif
	ffmpeg -ss 00:00:00.000 -i $ARG -pix_fmt rgb24 -r 10 -s 1024x768 $filename.temp.gif
	convert -layers Optimize $filename.temp.gif $giffile 
	mv $giffile "./animations/${giffile}"
	rm $filename.temp.gif
done
