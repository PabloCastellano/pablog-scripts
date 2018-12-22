#!/bin/bash
DIR="$HOME/Imágenes/movil/backup_$(date +%y-%m-%d)"
DELETE="yes"  # yes / no

function retrieve {
    adb pull $1 $2
}

# Delete recursive!!!
function deleteall {
    adb shell rm -fr $1
}

function spaceused {
    echo "Space used in: $1"
    adb shell du -h $1
}

mkdir -p $DIR/Camara
mkdir -p $DIR/Download
mkdir -p $DIR/Pictures
mkdir -p $DIR/SoundRecorder
mkdir -p $DIR/WhatsApp/Media
mkdir -p $DIR/FaceApp

retrieve "/sdcard/DCIM/Camera" $DIR/Camara
retrieve "/sdcard/Download" $DIR/Download
retrieve "/sdcard/Pictures" $DIR/Pictures
retrieve "/sdcard/SoundRecorder" $DIR/SoundRecorder
retrieve "/sdcard/WhatsApp/Media" $DIR/WhatsApp/Media
retrieve "/sdcard/FaceApp" $DIR/FaceApp

spaceused "/sdcard/DCIM/.thumbnails"
spaceused "/sdcard/DCIM/Camera"
spaceused "/sdcard/Download"
spaceused "/sdcard/Pictures"
spaceused "/sdcard/SoundRecorder"
spaceused "/sdcard/WhatsApp/Media"
spaceused "/sdcard/FaceApp"

if [ "$DELETE" = "yes" ]; then
  deleteall "/sdcard/DCIM/.thumbnails"
  deleteall "/sdcard/DCIM/Camera"
  deleteall "/sdcard/Download"
  deleteall "/sdcard/Pictures"
  deleteall "/sdcard/SoundRecorder"
  deleteall "/sdcard/WhatsApp/Media"
  deleteall "/sdcard/FaceApp"

  spaceused "/sdcard/DCIM/.thumbnails"
  spaceused "/sdcard/DCIM/Camera"
  spaceused "/sdcard/Download"
  spaceused "/sdcard/Pictures"
  spaceused "/sdcard/SoundRecorder"
  spaceused "/sdcard/WhatsApp/Media"
  spaceused "/sdcard/FaceApp"
fi


# Convertir los SoundRecorder a MP3.
# Normalmente MP3 96Kbps 44100Hz se escucha igual para conversaciones
# y ocupa un poco más de la mitad
# mkdir converted && for f in *.mp4; do avconv -i "$f" -vn -c:a libmp3lame -ar 44100 -ac 2 -ab 96k "converted/${f/%mp4/mp3}"; done

# /DCIM/.thumbnails/.thumbdata3--1967290299 no lo borra porque es oculto (1,5GB)
