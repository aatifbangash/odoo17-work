/** @odoo-module **/

// import Marker from "./shape/marker"
import {Component, useRef} from "@odoo/owl";
import {useBus} from "@web/core/utils/hooks";
import {Marker} from "../shapes/marker";


export class MapSearch extends Component {
    static template = "bista_map_component.map_search"

    setup() {
        this.input_ref = useRef("map_search_input")
        this.model = this.env.model
        this.googleMap = this.env.googleMap
        useBus(this.model, "onMapReady", (event) => {
            this._onMapReady(event.detail)
        });
    }

    async _onMapReady() {
        this.autocomplete = new this.googleMap.places.Autocomplete(this.input_ref.el, {
            componentRestrictions: {country: ["us", "ca"]},
            fields: ["address_components", "geometry"],
            types: ["address"],
        });
        this.autocomplete.addListener("place_changed", this.debounce(this.addressAutoComplete.bind(this), 500));
    }

    debounce(func, wait, immediate) {
        var timeout;
        return function () {
            var context = this, args = arguments;
            var later = function () {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }

    async addressAutoComplete() {
        const place = await this.autocomplete.getPlace();
        if (!place || !place.geometry || !place.geometry.location) {
            return
        }
        let location = {'lat': place.geometry.location.lat(), 'lng': place.geometry.location.lng()}
        let marker = new Marker()
        marker.setup(this.googleMap, {'coordinates': location})
        this.googleMap.map.fitBounds(place.geometry.viewport)
    }


}


