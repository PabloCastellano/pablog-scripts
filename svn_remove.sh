#!/bin/sh
#Removes all svn signs from a SVN repository

find . -name '.svn' -type d -exec rm -rv '{}' +
