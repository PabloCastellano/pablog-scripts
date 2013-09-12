#!/bin/bash
# Pablo Castellano <pablo@anche.no> 2013
# sudo apt-get install libxvidcore4 libavcodec-extra-53 libav-tools
# 1440x1080 / 2.25 = 640x480 ;_)
# Don't force aspect ratio 4:3 as it will shrink some videos

echo "Convert video files to AVI (XviD + MP3) using avconv"
echo "$0 [files...]"

for file in "$@"; do
    newfile="$(echo $file | cut -d "." -f 1)_xvid.avi"
    echo "------------------------"
    echo "Converting file... $file ($newfile)"
    echo "------------------------"
    echo
    avconv -i "$file" -f avi -r 29.97 -vcodec libxvid -vtag XVID -vf scale=640:480 -maxrate 1800k -b 1500k -qmin 3 -qmax 5 -bufsize 4096 -mbd 2 -bf 2 -trellis 1 -flags +aic -cmp 2 -subcmp 2 -g 300 -acodec libmp3lame -ar 48000 -ab 128k -ac 2 -threads 0 "$newfile"
    # avconv -i "$file" -f avi -r 29.97 -vcodec libxvid -vtag XVID -vf scale=640:480 -aspect 4:3 -maxrate 1800k -b 1500k -qmin 3 -qmax 5 -bufsize 4096 -mbd 2 -bf 2 -trellis 1 -flags +aic -cmp 2 -subcmp 2 -g 300 -acodec libmp3lame -ar 48000 -ab 128k -ac 2 "$newfile"
    # -aspect 4:3 jode algunos videos. QUITAR?
    # scale se podria cambiar tb. Hacer pruebas de tamaño final de archivos
    # wish: Use multiple cores/threads
done
