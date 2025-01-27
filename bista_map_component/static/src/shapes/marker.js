/* @odoo-module */

import {ShapBase} from "./base";

export class Marker extends ShapBase {
    setup(GoogleMap, data) {
        super.setup(GoogleMap, data);
        this.shape_type = 'marker'
        this.shape = new this.googleMap.maps.marker.AdvancedMarkerElement();
        this.map = this.googleMap.map;
        this.setPosition(this.getPosition())
        this.shape.addListener("click", this.onClick.bind(this))
        this.model.on("onKeyEscape", this.onKeyEscape.bind(this))
        this.model.on("onMapClicked", this._onMapClicked.bind(this))
    }

    getPosition() {
        let position = this.data.coordinates || {}
        if (this.data.marker_lat && this.data.marker_lng) {
            position = [this.data.marker_lat, this.data.marker_lng]
        }
        if (typeof (position) === "object") {
            if (Array.isArray(position)) {
                position = new google.maps.LatLng(position[0], position[1])
            } else {
                position = new google.maps.LatLng(position.lat, position.lng)
            }
        }

        return position
    }

    _onZoomChanged(zoomLevel) {
        super._onZoomChanged(zoomLevel)

    }

    _onMapClicked(event) {
        super._onMapClicked(event)
        this.hideInfoWindow()
    }


    setPosition(position) {
        this.position = position
        this.shape.position = position
    }

    setMap(map) {
        this.shape.setMap(map)
    }

    async getAddress() {
        if (!this.position) {
            return
        }

        let response = await this.googleMap.geocoder.geocode({location: this.position})

        let address1 = "";
        let postcode = "";
        let state = "";
        let country = "";
        let locality = ""

        if (response.results) {
            let place = response.results[0]
            if (!place || !place.address_components) {
                return
            }

            for (const component of place.address_components) {
                // @ts-ignore remove once typings fixed
                const componentType = component.types[0];

                switch (componentType) {
                    case "street_number": {
                        address1 = `${component.long_name} ${address1}`;
                        break;
                    }

                    case "route": {
                        address1 += component.short_name;
                        break;
                    }

                    case "postal_code": {
                        postcode = `${component.long_name}${postcode}`;
                        break;
                    }

                    case "postal_code_suffix": {
                        postcode = `${postcode}-${component.long_name}`;
                        break;
                    }
                    case "locality":
                        locality = component.long_name;
                        break;
                    case "administrative_area_level_1": {
                        state = component.long_name;
                        break;
                    }
                    case "country" :
                        country = component.long_name;
                        break;
                }
            }


        }

        this.data = {
            ...this.data,
            'street': address1,
            'zip': postcode,
            'city': locality,
            'state': state,
            'country': country
        }


    }

    async onClick(event) {
        await this.getAddress()
        this.setInfoWindow()
        this.showInfoWindow()
    }

    setInfoWindow() {
        const container = document.createElement("div");
        container.className = "info-window";
        let $container = $(container)
        let header = this.getInfoWindowHeader()
        let content = this.getInfoWindowContent()
        let footer = this.getInfoWindowFooter()
        $container.append(header, content, footer)

        if (!this.model.infowindow) {
            this.model.infowindow = new this.googleMap.maps.InfoWindow({
                content: container,
            });
        }
        this.infoWIndowContent = container
    }

    getInfoWindowHeader() {
        let header = `<strong>${this.data.name || "Description"}</strong>`
        if (this.data.marker_header) {
            header = this.data.marker_header
        }
        return $(`<div class="info-header"> ${header}</div>`)
    }


    getInfoWindowContent() {
        let content = `<p>${this.data.street}</p>
                        <div class="address_group">
                            <span>${this.data.city || this.data.state}</span>,
                            <span>${this.data.zip}</span>,
                            <span>${this.data.state}</span>
                        </div>
                        <p>${this.data.country}</p>`
        if (this.data.marker_content) {
            content = this.data.marker_content
        }
        return $(`<div class="info-body">
                        <div class="marker_label">${content}</div>
                    </div>`)
    }

    getInfoWindowFooter() {
        let footer = `<strong>Coordinates: </strong>
                              <span>${this.position.lat()},${this.position.lng()}</span>`
        if (this.data.marker_footer) {
            footer = this.data.marker_footer
        }
        return $(`<div class='info-footer'>
                    ${footer}
                </div>`)
    }

    hideInfoWindow() {
        if (this.model.infowindow) {
            this.model.infowindow.close();
        }
    }

    showInfoWindow(event) {
        this.model.infowindow.setOptions({
            content: this.infoWIndowContent,
            anchor: this.shape
        })
    }


    onKeyEscape() {
        this.hideInfoWindow()
    }


}