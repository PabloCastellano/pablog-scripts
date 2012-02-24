#!/bin/sh
#
# https://lapaginademarcos.wordpress.com/2012/02/20/linux-como-redimensionar-imagenes-desde-la-consola/

#Este comando convertirá todas las imágenes jpg del directorio actual a un ancho de 72 píxeles.
find . -maxdepth 1 -name "*.jpg" -exec convert -resize 72x {} {} \;

# En este caso convertirá la imagen a un máximo de 72 y le anexará al nombre el valor .72.jpg.
find . -maxdepth 1 -name "*.jpg" -exec convert -resize 72x {} {}.72.jpg \;
