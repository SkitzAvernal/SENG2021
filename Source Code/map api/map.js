import 'ol/ol.css';
import {Map, View, Tile} from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import XYZ from 'ol/source/XYZ';
import LayerGroup from 'ol/layer/Group';

window.onload = init;

function init(){
    var map = new Map({
        view: new View({
            center: [16832505.12095191, -4011613.961964385],
            zoom: 12,
            maxZoom: 18,
            minZoom:4
        }),

        target: 'js-map'
    })

    //BaseMap Layers
    const openStreetMapStandard = new TileLayer({
        source : new OSM(),
        visible:false,
        title: 'OSMStandard'
    })

    const opStreetMapHumanitarian = new TileLayer({
        source: new OSM({
            url: 'http://{a-c}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png'
        }),
        visible: false,
        title: 'OSMHumanitarian'
    })


    const stamenTerrain = new TileLayer({
        source: new XYZ({
            url:  "http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg",
            attributions: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'
        }),
        visible: true,
        title: 'StamenTerrain'
    })

    // layer group
    const baseLayerGroup = new LayerGroup({
        layers: [
            openStreetMapStandard, opStreetMapHumanitarian, stamenTerrain
        ]
    })
    map.addLayer(baseLayerGroup);
}

jQuery(document).ready(function($) {
    var bsDefaults = {
          offset: false,
          overlay: true,
          width: '330px'
       },
       bsMain = $('.bs-offset-main'),
       bsOverlay = $('.bs-canvas-overlay');

    $('[data-toggle="canvas"][aria-expanded="false"]').on('click', function() {
       var canvas = $(this).data('target'),
          opts = $.extend({}, bsDefaults, $(canvas).data()),
          prop = $(canvas).hasClass('bs-canvas-right') ? 'margin-right' : 'margin-left';

       if (opts.width === '100%')
          opts.offset = false;

       $(canvas).css('width', opts.width);
       if (opts.offset && bsMain.length)
          bsMain.css(prop, opts.width);

       $(canvas + ' .bs-canvas-close').attr('aria-expanded', "true");
       $('[data-toggle="canvas"][data-target="' + canvas + '"]').attr('aria-expanded', "true");
       if (opts.overlay && bsOverlay.length)
          bsOverlay.addClass('show');
       return false;
    });

    $('.bs-canvas-close, .bs-canvas-overlay').on('click', function() {
       var canvas, aria;
       if ($(this).hasClass('bs-canvas-close')) {
          canvas = $(this).closest('.bs-canvas');
          aria = $(this).add($('[data-toggle="canvas"][data-target="#' + canvas.attr('id') + '"]'));
          if (bsMain.length)
             bsMain.css(($(canvas).hasClass('bs-canvas-right') ? 'margin-right' : 'margin-left'), '');
       } else {
          canvas = $('.bs-canvas');
          aria = $('.bs-canvas-close, [data-toggle="canvas"]');
          if (bsMain.length)
             bsMain.css({
                'margin-left': '',
                'margin-right': ''
             });
       }
       canvas.css('width', '');
       aria.attr('aria-expanded', "false");
       if (bsOverlay.length)
          bsOverlay.removeClass('show');
       return false;
    });
});

var search_btn = document.getElementById("search_btn");
search_btn.addEventListener("click", function() {
    location.replace('./landmark.html')
});

var fetchData = {
    method: 'GET',
    headers: {

      'Accept': 'application/json',
    }
  }



  fetch('https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?apiKey=4ZRwHTCnCEe1HV3smhin6xJBjTP9r8zwWyZz-8rM3a4&mode=retrieveLandmarks&prox=37.7442,-119.5931,1000', fetchData)
  .then(response => response.json())
  .then(data => console.log(data.Response.View))