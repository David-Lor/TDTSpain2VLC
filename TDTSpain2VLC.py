
import requests
from xml.etree.ElementTree import Element, SubElement, Comment, tostring # https://pymotw.com/2/xml/etree/ElementTree/create.html
from xml.dom import minidom # https://stackoverflow.com/questions/28813876/how-do-i-get-pythons-elementtree-to-pretty-print-to-an-xml-file

PLAYLIST_NOMBRE = "Canales TDT"
PLAYLIST_ARCHIVO = "TDT.xspf"
JSON_URL = "https://raw.githubusercontent.com/ruvelro/TV-Online-TDT-Spain/master/tv-spain.json"

class Canal(object):
    def __init__(self, js):
        #Inicializar con parte JSON (dict) perteneciente al canal
        self.id = js["id"]
        self.enabled = js["enabled"]
        self.nombre = js["name"]
        self.streaming = js["link_m3u8"]
    def printInfoCanal(self):
        print("Canal #{} - {}".format(
            self.id,
            "Activo" if self.enabled else "Inactivo"
        ))
        print("Nombre:", self.nombre)
        print("URL:", self.streaming)

def obtener_canales(soloActivos=True):
    #Devuelve listado de objetos Canal tras parsear el JSON del repositorio
    print("Obteniendo canales...")
    jsList = requests.get(JSON_URL).json() #Return: list of dicts
    canalesEncontrados = [Canal(js) for js in jsList]
    canalesActivos = [canal for canal in canalesEncontrados if canal.enabled]
    print("Se han encontrado {} canales activos de {} canales listados:".format(len(canalesEncontrados), len(canalesActivos)))
    for canal in canalesEncontrados:
        print()
        canal.printInfoCanal()
    if soloActivos:
        return canalesActivos
    else:
        return canalesEncontrados

def cargar_lista(archivo):
    #Devuelve listado de nombres definidos en los archivos whitelist y blacklist
    l = []
    try:
        file = open(archivo, "r")
        filelines = file.readlines()
        for line in filelines:
            if line.replace(" ","")[0] == "#": #Ignorar líneas comentadas (empiezan por #)
                continue
            if line == "\n": #Ignorar líneas en blanco
                continue
            l.append(line.replace("\n", ""))
        file.close()
    except FileNotFoundError:
        pass
    return l

def generar_xspf(canales):
    """
    SINTAXIS ARCHIVO XSPF:
        <?xml version="1.0" encoding="UTF-8"?>
        <playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">
            <title>Lista de reproducción</title>
            <trackList>
                <track>
                    <location>http://a3live-lh.akamaihd.net/i/antena3_1@35248/master.m3u8</location>
                    <title>Antena 3</title>
                    <extension application="http://www.videolan.org/vlc/playlist/0">
                        <vlc:id>0</vlc:id>
                        <vlc:option>network-caching=1000</vlc:option>
                    </extension>
                </track>
                <track>
                    <location>http://a3live-lh.akamaihd.net/i/lasexta_1@35272/master.m3u8</location>
                    <title>La Sexta</title>
                    <extension application="http://www.videolan.org/vlc/playlist/0">
                        <vlc:id>1</vlc:id>
                        <vlc:option>network-caching=1000</vlc:option>
                    </extension>
                </track>
            </trackList>
            <extension application="http://www.videolan.org/vlc/playlist/0">
                    <vlc:item tid="0"/>
                    <vlc:item tid="1"/>
            </extension>
        </playlist>
    """
    
    xml = Element("playlist", {
        "xmlns" : "http://xspf.org/ns/0/",
        "xmlns:vlc" : "http://www.videolan.org/vlc/playlist/ns/0/",
        "version" : "1"
    })
    xml.append(Comment("Playlist generada con los canales de https://github.com/ruvelro/TV-Online-TDT-Spain y el script TDTSpain2VLC"))
    SubElement(xml, "title").text = PLAYLIST_NOMBRE
    
    xml_tracklist = SubElement(xml, "trackList")

    for canal in canales:
        xml_tracklist_track = SubElement(xml_tracklist, "track")
        SubElement(xml_tracklist_track, "title").text = canal.nombre
        SubElement(xml_tracklist_track, "location").text = canal.streaming
        xml_tracklist_track_extension = SubElement(xml_tracklist_track, "extension", {
            "application" : "http://www.videolan.org/vlc/playlist/0"
        })
        SubElement(xml_tracklist_track_extension, "vlc:id").text = str(canal.id)
        SubElement(xml_tracklist_track_extension, "vlc:option").text = "network-caching=1000" #¿?

    xml_extension = SubElement( xml, "extension", {
        "application":"http://www.videolan.org/vlc/playlist/0"
    })

    for canal in canales:
        SubElement( xml_extension, "vlc:item", {
            "tid" : str(canal.id)
        })

    return minidom.parseString(tostring(xml)).toprettyxml(indent="    ")

def guardar_xspf(xml):
    file = open(PLAYLIST_ARCHIVO, "w")
    file.write(xml)
    file.close()


if __name__ == "__main__":
	
    whitelist, blacklist = False, False
    
    #Cargar lista de whitelist
    whitelist = cargar_lista("Whitelist.txt")
    
    #Cargar lista de blacklist
    if not whitelist:
        blacklist = cargar_lista("Blacklist.txt")

    canales_obtenidos = obtener_canales()

    #Quitar canales no deseados según blacklist/whitelist
    if whitelist:
        canales = [canal for canal in canales_obtenidos if canal.nombre in whitelist]
    elif blacklist:
        canales = [canal for canal in canales_obtenidos if canal.nombre not in blacklist]
    else:
        canales = canales_obtenidos

    #Generar XSPF final
    guardar_xspf(generar_xspf(canales))
    print()
    print("{} canales guardados en {}".format(len(canales), PLAYLIST_ARCHIVO))

