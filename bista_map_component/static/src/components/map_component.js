/* @odoo-module */

import {MapModel} from "../model/map_model";
import {Component, onMounted, onWillStart, useRef, useState, useSubEnv} from "@odoo/owl";
import {registry} from "@web/core/registry"
import {jsonrpc} from "@web/core/network/rpc_service";
import {useBus, useService} from "@web/core/utils/hooks";
import {MapSearch} from "./map_search";
import {MapEditor} from "./map_editor";
import {Marker} from "../shapes/marker";
import {Rectangle} from "../shapes/rectangle";
import Circle from "../shapes/circle";
import {Polygon} from "../shapes/polygon";


export class GoogleMap extends Component {
    static template = "bista_map_component.map_template";
    test(num) {
        console.log('testing function')
        return [1,2,3,4].concat(num);
    }
    setup() {
        this.orm = useService("orm");
        this.model = new MapModel(this)
        this.state = useState({'zoomLevel': 15})
        this.community_ids = useState([])
        this.core_community_ids = useState([])
        this.status_ids = useState([])
        this.ui = useService("ui");
        onWillStart(this._onWIllStart.bind(this))
        onMounted(this._onMounted.bind(this))
        this.getCommunity = this.getCommunity.bind(this)
        useSubEnv({
            model: this.model,
            googleMap: this,
        });

        this.map_container_ref = useRef("google_map_container")
        this.map_legends_ref = useRef("map_legends")
        this.community_list_ref = useRef("community_list")
        this.map_zoom_level_ref = useRef("map_zoom_level")
        this.object_preview = useRef("object_preview")
        this.google = false;
        useBus(this.model, "onMapClicked", (event) => {
            this.onMapClicked(event.detail)
        });
        useBus(this.model, "onZoomChanged", (event) => {
            this.onZoomChanged(event.detail)
        });
        this.coordinates = []

    }

    async _onWIllStart() {

    }

    async _onMounted() {
        this.map_legends = $(this.map_legends_ref.el)
        this.community_list = $(this.community_list_ref.el)
        this.map_zoom_level = $(this.map_zoom_level_ref.el)
        this.object_preview = $(this.object_preview.el)
        await this.initMap()

    }

    onChange() {

    }

    getCommunity(community){
    if (!this.map) {
        console.error("Map is not initialized yet.");
        return;
    }
    const coordinatesArray = JSON.parse(community.coordinates);
    if(coordinatesArray.length > 0){
    const [lat, lng] = coordinatesArray[0]?.map(coord => parseFloat(coord));
    console.log("lat lng: ", lat, lng, coordinatesArray.length)

     if (this.map) {
        this.map.setCenter({ lat: lat, lng: lng });
        this.map.setZoom(16);

        new google.maps.Marker({
            position: { lat: lat, lng: lng },
            map: this.map,
            title: community.name,
        });
    } else {
        console.error("Google Map instance is not initialized!");
        }
    }else{
    console.log("Coordinates not found for Community")
    }
    }


    async initMap() {
        let google_api_key = await jsonrpc("/map/api_key")
        if (google_api_key) {
            this.isEditor = await jsonrpc("/website_editor_right")
            this.maps = google.maps
            let loader = await new this.maps.plugins.loader.Loader({
                apiKey: google_api_key,
                libraries: ["places", "drawing", "geometry", 'marker']
            });

            this.google = await loader.load()
            this.places = this.maps.places

            await this.loadMap()
            this.model.onMapReady()
        }
    }


    async loadMap() {
        this.map_div = $(this.map_container_ref.el)
        this.bounds = new this.maps.LatLngBounds();
        this.drawingMode = false;

        let options = this.props.map
        let center = {lat: options.center_lat, lng: options.center_lng}
        let mapOptions = {
            center: center,
            zoom: options.init_zoom || 15,
            mapTypeId: this.maps.MapTypeId.MAP,
            streetViewControl: true,
            panControl: false,
            zoomControl: true,
            scrollWheel: true,
            navigationControl: false,
            mapTypeControl: true,
            scaleControl: true,
            heading: 0,
            gestureHandling: 'cooperative',
            rotateControl: false,
            mapId: options.map_id || this.generateUniqueId(),
        }

        this.map = await new this.maps.Map(this.map_container_ref.el, mapOptions)

        this.geocoder = new this.maps.Geocoder();
        this.attachCompass()
        this.attachLegends()
        if (this.isEditor) {
            this.attachZoomLevel()
            this.attachCoordinatesView()
            this.drawing_manager()
        }
        this.renderShapes()
        this.eventListeners()
        this.getCommunities()
        this.getItemStatus()
        this.getCoreCommunities()

    }

    async getCoreCommunities() {
        let self = this;
        let core_community_ids = await jsonrpc("/get_core_communities")
        core_community_ids.forEach(function (community) {
            self.core_community_ids.push(community)
        })
    }

    async getCommunities() {
        let self = this;
        let community_ids = await jsonrpc("/get_communities")
        community_ids.forEach(function (community) {
            self.community_ids.push(community)
        })
    }

    async getItemStatus() {
        let self = this;
        let status_ids = await jsonrpc("/get_item_status")
        status_ids.forEach(function (status) {
            self.status_ids.push(status)
        })
    }

    setCenter(position) {
        this.map.fitBounds(position)
    }

    generateUniqueId() {
        return 'id-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    }

    attachZoomLevel() {
        this.map.controls[this.maps.ControlPosition.BOTTOM_RIGHT].push(this.map_zoom_level_ref.el)
    }

    attachCompass() {
        let compass = document.createElement('div');
        compass.className = "map_compass"
        this.map.controls[this.maps.ControlPosition.BOTTOM_RIGHT].push(compass)
    }


    attachLegends() {
        this.map.controls[this.maps.ControlPosition.BOTTOM_LEFT].push(this.map_legends_ref.el)
    }


    attachCoordinatesView() {
        this.coordinateInfo = document.createElement('div');
        this.coordinateInfo.className = "map_coordinates"
        this.map.controls[this.maps.ControlPosition.BOTTOM_LEFT].push(this.coordinateInfo)
    }

    eventListeners() {
        let self = this;
        this.map.addListener('click', (event) => {
            self.model.onMapClicked(event)
        })

        this.map.addListener('zoom_changed', () => {
            self.model.onZoomChanged(self.map.getZoom())
        })

        if (this.drawingManager) {
            this.drawingManager.addListener('overlaycomplete', this.createObject.bind(this));
        }

        this.map.addListener("tilesloaded", () => {
            const loader = document.getElementById('map-loader');
            if (loader) {
                loader.style.display = 'none';
            }
        });
    }


    getZoom() {
        return this.map.getZoom()
    }

    onMapClicked(event) {
        if (!this.coordinateInfo) {
            return
        }

        var lat = event.latLng.lat();
        var lng = event.latLng.lng();
        this.coordinateInfo.innerHTML = lat + "," + lng
    }

    onZoomChanged(zoomLevel) {
        this.state.zoomLevel = zoomLevel
    }

    drawing_manager() {
        this.drawingManager = new google.maps.drawing.DrawingManager({
            drawingModes: [
                this.maps.drawing.OverlayType.CIRCLE,
                this.maps.drawing.OverlayType.POLYGON,
                this.maps.drawing.OverlayType.RECTANGLE,
            ],
            drawingControl: true,
            drawingControlOptions: {
                position: this.maps.ControlPosition.TOP_LEFT,
            },
        });
        this.drawingManager.setMap(this.map);

    }


    async createObject(event) {
        let object = false;
        let self = this;
        if (event.type === this.maps.drawing.OverlayType.RECTANGLE) {
            object = await this.renderRectangle({
                name: "Rectangle",
                shape_type: 'rectangle',
                bounds: event.overlay.getBounds(),
            })
        } else if (event.type === this.maps.drawing.OverlayType.POLYGON) {
            object = await this.renderPolygon({
                name: "polygon",
                shape_type: 'polygon',
                coordinates: event.overlay.getPath().getArray(),
            })

        } else if (event.type === this.maps.drawing.OverlayType.CIRCLE) {
            var c = event.overlay;
            let center = c.getCenter()
            let radius = c.getRadius()
            object = await this.renderCircle({
                radius: radius,
                center: center,
                shape_type: 'circle'
            })
        }

        // event.overlay.setMap(null)
        this.drawingManager.setOptions({
            drawingMode: null,
        })
        event.overlay.setMap(null)
        if (object) {
            this.model.selectObject(object)
        }
    }


    renderShapes() {
        let data = this.props.item_data
        let self = this;

        for (var index in data) {
            let object = {...data[index], partner_slug: this.props.partner_slug, community_slug:this.props.community_slug }
            let shape = false
            if (object.shape_type === 'marker') {
                shape = this.renderMarker(object)
            } else if (object.shape_type === 'rectangle') {
                shape = this.renderRectangle(object)
            } else if (object.shape_type === 'circle') {
                shape = this.renderCircle(object)
            } else if (object.shape_type === 'polygon') {
                shape = this.renderPolygon(object)
            }
            shape.coordinates.forEach(function (point) {
                self.coordinates.push(point)
            })
        }

        this.focusCenter()


    }


    renderMarker(data) {
        let m = new Marker()
        m.setup(this, data)
        this.coordinates.push(m.getPosition())
        m.attachMap()
        return m

    }

    renderRectangle(data) {
        let r = new Rectangle()
        r.setup(this, data)
        r.attachMap()
        return r

    }

    renderCircle(data) {
        let c = new Circle()
        c.setup(this, data)
        c.attachMap()
        return c
    }


    renderPolygon(data) {
        let p = new Polygon()
        p.setup(this, data)
        p.attachMap()
        return p

    }

    focusCenter() {
        let center = this.model.getCenter(this.coordinates)
        this.setCenter(center)
    }


}

GoogleMap.components = {
    MapSearch, MapEditor
}


registry.category("public_components").add("GoogleMap", GoogleMap);
