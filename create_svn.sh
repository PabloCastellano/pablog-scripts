#!/bin/bash
# Pablo Castellano <pablo@anche.no> 2011

SVNDIR="/var/svn"

# Opcional. Da por hecho que tienes configurado libapache2-svn
SVNURL="http://svn.mydomain.net"

#----------------------------------
#Check root
if [[ $EUID -ne 0 ]]; then
	echo "Solo root puede llevar a cabo esta acción"
	exit
fi

#Check arguments
if [ -z $1 ]; then
	echo "Necesitas especificar el nombre del repositorio"
	exit
fi

if [ ! -d $SVNDIR ]; then
	echo "El directorio $SVNDIR no existe"
	exit
fi

cd $SVNDIR

if [ -d $1 ]; then
	echo "El repositorio $1 ya existe"
	exit
fi

svnadmin create $1
chown www-data:www-data $1/ -R

echo "Se ha creado el directorio $SVNDIR/$1"
echo "Clona el repositorio con el siguiente comando:"
echo "    svn co $SVNURL/$1"
