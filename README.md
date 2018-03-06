# TDTSpain2VLC

Script Python para descargar el listado de canales TDT por streaming de TV-Online-TDT-Spain y convertirlo a una playlist XSPF para VLC.

El listado de canales se obtiene del repositorio TV-Online-TDT-Spain: https://github.com/ruvelro/TV-Online-TDT-Spain

Al ejecutar este script se descargará automáticamente la [playlist json](https://github.com/ruvelro/TV-Online-TDT-Spain/blob/master/tv-spain.json) y se convertirá a XSPF, el formato de playlists que utiliza VLC.

Así mismo, se pueden seleccionar qué canales obtener mediante whitelist o blacklist, en los archivos Whitelist.txt o Blacklist.txt respectivamente. Se deben especificar los nombres de canales deseados, tal cual aparecen en el repositorio original, escribiendo uno por línea. El funcionamiento de los archivos es el siguiente:

* Whitelist: sólo se descargarán los canales especificados aquí. Blacklist se ignorará si hay algún canal especificado en Whitelist.
* Blacklist: se descargarán todos los canales excepto los especificados aquí.

_En ambos archivos se ignorarán líneas en blanco y que empiecen por **#**_
