/** @odoo-module **/

import {EventBus,useState} from "@odoo/owl";

export class MapModel extends EventBus {
    constructor(GoogleMap) {
        super();
        this.googleMap = GoogleMap
        this.orm = this.googleMap.orm
        this.params = this.googleMap.props;
        this.record = new Set();
        this.arch = {}
        this.fields = {}
        this.events = {};
        this.resModel = 'google.map.item'
        this.communities = useState([])
        this.resId = false
        this.selectedObject = false;
        this.editor = false;
    }


    notify() {
        this.triggerState("update")
    }


    onMapReady() {
        this.triggerState("onMapReady")
        document.addEventListener("keydown", this.onKeyDown.bind(this));
        this.getCommunities()
    }

    onDocumentClicked() {
        this.triggerState("onDocumentClicked")
    }

    onMapClicked(event) {
        this.triggerState("onMapClicked", event)
    }

    onZoomChanged(zoomLevel) {
        this.triggerState("onZoomChanged", zoomLevel)
    }

    on(event, listener) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(listener);
    }

    off(event, listener) {
        if (!this.events[event]) return;
        this.events[event] = this.events[event].filter(l => l !== listener);
    }

    triggerState(event, ...args) {
        this.trigger(event, ...args)
        if (!this.events[event]) return;
        this.events[event].forEach(listener => listener(...args));
    }


    onKeyDown(event) {
        if (event.key === "Escape") {
            this.triggerState("onKeyEscape")
        }
        if (event.key === "Delete") {
            this.triggerState("onKeyEnter")
        }
    }

    async getSections(community_id) {
         let res = await this.orm.call(
                    'community_module.section', // Model name
                    'get_sections_by_community', // Python method name
                    [community_id])
                    return res
    }
    async getCommunities() {
        let res = await this.orm.call(
                    'community_module.community', // Model name
                    'get_all_communities') // Python method name)
        this.communities = res
    }
    async get_map_item_by_core_id(id, type='home'){
        let res = await this.orm.call(
                    type === 'home' ? 'community_module.lot' : 'community_module.community', // Model name
                    type === 'home' ?'get_lot_by_id' : 'get_community_by_id',[id])
        console.log(res)
        return res
    }
    async create(data, type='home') {
        if (!data) {
            return "Missing Data to create"
        }
        this.showProgress()
        let res = await this.orm.create(type === 'home' ? 'community_module.lot' : 'community_module.community', [data])
        this.hideProgress()
        return res
    }

    async write(resId, data) {
        if (!resId || !data) {
            return "Missing Record ID or Data"
        }

        this.showProgress()
        let res = false;
        try {
            res = await this.orm.write(this.resModel, [resId], data)
        } catch (e) {
            console.log("Write Error: ", e)
        }
        this.hideProgress()
        return res
    }


    async unlink(ids) {
        if (!ids) {
            return
        }
        this.showProgress()
        let res = await this.orm.unlink(this.resModel, ids)
        this.hideProgress()
        return res
    }


    showProgress() {
        this.googleMap.ui.block()
    }

    hideProgress() {
        this.googleMap.ui.unblock()
    }


    parseCoordinates(coordinates) {
        if (!coordinates) {
            return []
        }
        if (typeof coordinates === "object") {
            let point = coordinates[0]
            let latlng = point instanceof google.maps.LatLng
            if (latlng) {
                return coordinates
            }
            if (point && typeof point[0] !== 'object') {
                return coordinates.map((point) => {
                    return this.getPosition(point[0], point[1])
                })
            }
            return coordinates
        }

        let cordObject = JSON.parse(coordinates)
        return cordObject.map(coord => new google.maps.LatLng(coord[0], coord[1]));
    }

    getBoundary(coordinates) {
        const bounds = this.getCoordinateBounds(coordinates)
        const northEast = bounds.getNorthEast();
        const southWest = bounds.getSouthWest();
        const northWest = this.getPosition(northEast.lat(), southWest.lng());
        const southEast = this.getPosition(southWest.lat(), northEast.lng());
        return {
            topLeft: northWest, topRight: northEast, bottomLeft: southWest, bottomRight: southEast,
        };
    }

    getCoordinateBounds(coordinates) {
        coordinates = coordinates || []
        const bounds = new google.maps.LatLngBounds();
        coordinates.forEach((point) => {
            bounds.extend(point);
        });
        return bounds
    }

    getBoundCoordinates(bounds) {
        const ne = bounds.getNorthEast();
        const sw = bounds.getSouthWest();
        const nw = this.getPosition(ne.lat(), sw.lng());
        const se = this.getPosition(sw.lat(), ne.lng());
        return [ne, nw, sw, se]
    }

    getCenter(coordinates) {
        let bounds = this.getCoordinateBounds(coordinates || this.coordinates)
        return bounds
    }

    getPosition(lat, lng) {
        return new google.maps.LatLng(lat, lng)
    }

    debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => {
                func.apply(this, args);
            }, delay);
        }
    }

    coordinatesToJson(coordinates) {
        let self = this;
        return coordinates.map(function (latlng) {
            return self.coordinateToJson(latlng)
        })
    }

    coordinateToJson(latlng) {
        return {'lat': latlng.lat(), 'lng': latlng.lng()}
    }

    selectObject(object, alternateEdit = false) {
        if (!this.editor) {
            console.log("NO editor, something went wrong")
            return
        }
        if (this.editor.editing && !alternateEdit) {
            console.log("Currently editing another object ignoring click event")
            return
        }
        this.selectedObject = object
        this.editor.showEditor()
    }


}
