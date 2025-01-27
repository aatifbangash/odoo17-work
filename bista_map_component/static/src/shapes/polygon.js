/** @odoo-module **/

import {ShapBase} from "./base";

export class Polygon extends ShapBase {
    setup(GoogleMap, data) {
        super.setup(GoogleMap, data)
        this.data = data
        this.className = 'polygon_content'
        this.type = 'polygon'
        this.coordinates = this.model.parseCoordinates(this.data.coordinates) || []
        let polygon_options = {
            paths: this.coordinates,
            strokeOpacity: 1,
            strokeColor: this.data.strokeColor || '#000',
            strokeWeight: this.data.strokeWeight || 2,
            fillColor: this.data.fillColor || '#000',
            fillOpacity: this.data.fillOpacity || 0.5,
            editable: this.data.editable,
            geodesic: true,
            draggable: this.data.draggable,
            zIndex: this.data.sequence
        }
        this.shape = new google.maps.Polygon(polygon_options)
        this.setPosition(this.getPosition())
    }

    setInfoWindow() {
            const container = document.createElement("div");
            container.className = "info-window";
            let $container = $(container)
            let header = this.getInfoWindowHeader()
            let content = this.getInfoWindowContent()
            let footer = this.getInfoWindowFooter()
            $container.append(content)

            if (!this.model.infowindow) {
                this.model.infowindow = new this.googleMap.maps.InfoWindow({
                    content: container,
                });
            }
            this.infoWIndowContent = container
        }

        getInfoWindowHeader() {
        let header = `<strong>${"Lot Info"}</strong>`
        return $(`<div class="info-header"> ${header}</div>`)
    }


    getInfoWindowContent() {
        let content = `<div>
                            <div class="button-div">
                                <button id="detailsButton" class="info-window-button" >Details</button>
                            </div>
                            <div class="button-div">
                                <button id="editButton" class="info-window-button" >Edit</button>
                            </div>
                        </div>`


        setTimeout(() => {
            const detailsButton = document.getElementById("detailsButton");
            const editButton = document.getElementById("editButton");

            if (detailsButton) {
            detailsButton.classList.add("mystyle");
                detailsButton.addEventListener("click", (event) => {
                super.onClick(false)
                });
            }
            if (editButton) {
                editButton.addEventListener("click", (event) => {
                super.onClick(true)
                });
            }
        }, 100);
    const infoBody = $(`<div class="info-body" style="padding: 0 !important;">
                          <div class="marker_label">${content}</div>
                        </div>`);
        return infoBody
    }

    getInfoWindowFooter() {
        let footer = `<strong>Coordinates: </strong>
                              <span>${this.position.lat()},${this.position.lng()}</span>`

        return $(`<div class='info-footer'>
                </div>`)
    }

    hideInfoWindow() {
        if (this.model.infowindow) {
            this.model.infowindow.close();
        }
    }

    showInfoWindow(event) {
     const path = this.shape.getPath();
        let bounds = new google.maps.LatLngBounds();

        path.forEach((latLng) => {
            bounds.extend(latLng);
        });

        const center = bounds.getCenter();

        this.model.infowindow.setOptions({
            content: this.infoWIndowContent,
            anchor: this.shape,
            position: center,
        });
    }

    getPosition() {
        let position = this.data.coordinates || {}
        if (typeof (position) === "object") {
              if (Array.isArray(position)) {
                 position = new google.maps.LatLng(position[0], position[1])
            } else {
                position = new google.maps.LatLng(position.lat, position.lng)
            }
        }
        return position
    }

    setPosition(position) {
        this.position = position
        this.shape.position = position
    }

    addEventListeners() {
        super.addEventListeners()
        this.path = this.shape.getPath()
        if (this.path) {
            this.path.addListener("set_at", this.onPathChange.bind(this));
        }
    }

    onPathChange() {
        this.coordinates = this.path.getArray()
        this.updateCoordiantes()
    }

    onClick(event) {
//        super.onClick(event)
        this.setInfoWindow()
        this.showInfoWindow()
   }


}

