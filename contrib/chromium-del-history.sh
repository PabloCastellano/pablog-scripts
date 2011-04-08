#!/bin/bash

DATABASE=~/.config/chromium/Default/History
URL=""

print_usage()
{
    printf "usage: `basename $0` URL\n"
    exit 1;
}

which sqlite3 >/dev/null
if [ $? -ne 0 ]; then
    printf "sqlite3 must be installed before running this script.\n"
    exit 1
fi

if [ $# -lt 1 ]; then
    print_usage
fi
URL=$1

cat << _EOF_ | sqlite3 $DATABASE
SELECT * FROM urls WHERE url LIKE '%$URL%'; 
_EOF_
if [ $? -ne 0 ]; then
    printf "google-chrome must be terminated before running this script.\n"
    exit 1
fi

printf "\nDo you want to delete the above urls? [y/n] "
read foo
if [ $foo != "y" ] && [ $foo != "Y" ]; then
    exit 0
fi

printf "deleting..\n"
cat << _EOF_ | sqlite3 $DATABASE
DELETE FROM urls WHERE url LIKE '%$URL%';
_EOF_

exit 0
