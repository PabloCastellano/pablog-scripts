#!/bin/bash

## XKCD's webcomic retrieving tool

# xkcd_retriever
# (c)2008 GNU GPL, Javi Moreno "vierito5" (vierito5{AT}gmail{DOT}com)
#
# xkcd_retriever is a tool to retrieve the webcomic updates from xkcd.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation;
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY
# RIGHTS.  IN NO EVENT SHALL THE COPYRIGHT HOLDER(S) AND AUTHOR(S) BE LIABLE
# FOR ANY CLAIM, OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
# AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# ALL LIABILITY, INCLUDING LIABILITY FOR INFRINGEMENT OF ANY PATENTS,
# COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS, RELATING TO USE OF THIS SOFTWARE
# IS DISCLAIMED.

VERSION=0.1

## Vars ##

BASE_URL="http://xkcd.com"
IMG_URL="http://imgs.xkcd.com/comics/"
TMP_DIR="/tmp"

NUMBER=0
ALL=0
SINGLE=0
LAST=0

## Functions ##

usage()
{
cat << EOF
usage: $0 $version [OPTION]
(c)2008 GNU GPL, Javi Moreno "vierito5" (vierito5{AT}gmail{DOT}com)

Retrieve easily XKCD updates

OPTIONS:
   -h  		show this message
   -a 		download ALL xkcd webcomics
   -s N		download update number N
   -l N		download last N updates
EOF
}

download()
{
echo ""
echo "Downloading update number $NUMBER"
echo ""
# First, get the name of the image
curl ${BASE_URL}/${NUMBER}/index.html > ${TMP_DIR}/index
NAME=`grep "Image URL" ${TMP_DIR}/index | awk -F"/comics/" '{ print $2}' | awk 'sub(".........$", "")'`
# Now, download it
wget ${IMG_URL}/${NAME}.png
# Use a nicer filename
mv ${NAME}.png ${NUMBER}_${NAME}.png
}

get_last()
{
curl ${BASE_URL}/index.html > ${TMP_DIR}/index
NUMBER=`grep "Permanent link to this comic" ${TMP_DIR}/index | awk -F"xkcd.com/" '{ print $2}' | awk 'sub("......$", "")'`
}

## Main ##

if [[ $# -eq 0  ]]
then
	usage
	exit 0
fi

while getopts “h:as:l:” OPTION
do
	case $OPTION in
        h)
             	usage
             	exit 0
             	;;
        a)
		ALL=1
		echo "Downloading all updates"
             	;;
        s)
		SINGLE=1
		NUMBER=$OPTARG
		echo "Downloading update number $NUMBER"
             	;;
        l)
          	LAST=1
		GROUP=$OPTARG
		echo "Downloading last $GROUP updates"
             	;;
        ?)
        	usage
             	exit 0
             	;;
	esac
done

if [[ $SINGLE -eq 1 ]]
then
	download
	rm ${TMP_DIR}/index
	echo ""
	echo "Done!!"
	echo ""
	exit 0
fi

if [[ $ALL -eq 1 ]]
then
	# First we need to get the number of the last updates
	get_last
	# Download all of them
	while [ $NUMBER -gt 0 ]
	do
		# Download each
		download
		NUMBER=$[$NUMBER-1]
	done
	rm ${TMP_DIR}/index
	echo ""
	echo "Done!!"
	echo ""
	exit 0
fi

if [[ $LAST -eq 1 ]]
then
	get_last
	UNTIL=`expr $NUMBER - $GROUP`
	echo "Downloading from the ` expr $UNTIL + 1` to the $NUMBER update"
	while [ $NUMBER -gt $UNTIL ]
	do
		# Download each
		download
		NUMBER=$[$NUMBER-1]
	done
	rm ${TMP_DIR}/index
	echo ""
	echo "Done!!"
	echo ""
	exit 0
fi