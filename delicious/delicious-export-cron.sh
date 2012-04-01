#!/bin/bash
# delicious-export-cron.sh - Export bookmarks & commit - 1/April/2012
# Copyright (C) 2012 Pablo Castellano <pablo@anche.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#!!!!!!!!!!!!!!!!!!!!!!!!!! Setup FIRST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Variables: $SCRIPTSDIR, $LOGSDIR, $GITDIR
#
# Copy this file to $SCRIPTSDIR/delicious-export-cron.sh
# chmod 755 $SCRIPTSDIR/delicious-export-cron.sh
#
# Add the following line to /etc/crontab:
# 05 23   * * *   root    $SCRIPTSDIR/delicious-export-cron.sh
# Or (save output as log):
# 05 23   * * *   root    $SCRIPTSDIR/delicious-export-cron.sh >> $LOGSDIR/delicious.log
#
# mkdir -p $GITDIR
# cd $GITDIR
# cp $SOMEWHERE/delicious-export.py .
# chmod 755 delicious-export.py
# git init 
# touch delicious.html
# git add delicious.html
# git commit delicious.html -m init

### Configure
GITDIR='CHANGE_ME'
###

if [ ! -d $GITDIR ]; then
    echo "Directory $GITDIR doesn't exist"
    exit
fi

cd $GITDIR
./delicious-export.py
git commit delicious.html -m "Update"
