####################################################
# Script to manage the openlayers map using Brython
####################################################
from javascript import JSObject, JSConstructor
from browser import document, window, alert

######################
## Openlayers stuff ##
######################
# Create the map and an OpenStreetMap layer
ol = window.ol
layer = JSConstructor(ol.layer.Tile)({
    "source" : JSConstructor(ol.source.XYZ) ({
        "url" : "http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg",
        "attributions" : "Map tiles by <a href='http://stamen.com'>Stamen Design</a>, under <a href='http://creativecommons.org/licenses/by/3.0'>CC BY 3.0</a>. Data by <a href='http://openstreetmap.org'>OpenStreetMap</a>, under <a href='http://www.openstreetmap.org/copyright'>ODbL</a>."
    })
})
# Initial map settings with location zoom and an initial markers layer
# with a marker in the center of the map

view = JSConstructor(ol.View) ({
    "center": [{{lon}}, {{lat}}],
    "zoom" : {{ zoom }}
})

map = JSConstructor(ol.Map)({
    "target": "mapdiv",
    "layers": [layer],
    "view": view
})



#############################
## End of Openlayers stuff ##
#############################