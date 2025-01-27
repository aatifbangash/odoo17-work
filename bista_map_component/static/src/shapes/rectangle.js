/** @odoo-module **/

import {ShapBase} from "./base";

export class Rectangle extends ShapBase {
    setup(GoogleMap, data) {
        super.setup(GoogleMap, data)
        this.className = 'shape_rectangle'
        this.setBoundary = false

        if (this.data.bounds) {
            this.coordinates = this.model.getBoundCoordinates(this.data.bounds)
        } else {
            this.coordinates = this.model.parseCoordinates(this.data.coordinates)
        }

        this.data.shape_fill_opacity = this.data.shape_fill_opacity || 0.5
        this.data.shape_border_width = this.data.shape_border_width || 1
        this.data.shape_fill_color = this.data.shape_fill_color || "#000"
        this.data.shape_border_color = this.data.shape_border_color || "#000"
        let rectange_options = {
            bounds: this.data.bounds || this.model.getCoordinateBounds(this.coordinates),
            strokeOpacity: 1,
            strokeColor: this.data.strokeColor,
            strokeWeight: this.data.strokeWeight,
            fillColor: this.data.fillColor,
            fillOpacity: this.data.fillOpacity,
            editable: this.data.editable,
            draggable: this.data.draggable,
            clickable: true,
            visible: true,
            zIndex: this.data.sequence
        }
        this.shape = new google.maps.Rectangle(rectange_options)
        this.setPosition(this.getPosition())
        this.shape.addListener("click", this.onClick.bind(this))
    }
    setInfoWindow() {
            const container = document.createElement("div");
            container.className = "info-window";
            let $container = $(container)
            let header = this.getInfoWindowHeader()
            let content = this.getInfoWindowContent()
            let footer = this.getInfoWindowFooter()
            $container.append( content)

            if (!this.model.infowindow) {
                this.model.infowindow = new this.googleMap.maps.InfoWindow({
                    content: container,
                });
            }
            this.infoWIndowContent = container
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

   onClick(event) {

        this.setInfoWindow()
        this.showInfoWindow()
   }

    setPosition(position) {
        this.position = position
        this.shape.position = position
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


         const infoBody = $(`<div class="info-body" style="padding: 0 !important;">
                          <div class="marker_label">${content}</div>
                        </div>`);

        if (this.data.marker_content) {
            content = this.data.marker_content
        }

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
 _onMapClicked(event) {
        super._onMapClicked(event)
        this.hideInfoWindow()
    }
    showInfoWindow(event) {
        const center = this.shape.getBounds().getCenter()
        this.model.infowindow.setOptions({
            content: this.infoWIndowContent,
            anchor: this.shape,
            position: center
        })
    }
    addEventListeners() {
        super.addEventListeners()
        this.shape.addListener("bounds_changed", this.onBoundChanged.bind(this));
    }

    async onBoundChanged() {
        this.coordinates = this.model.getBoundCoordinates(this.shape.getBounds())
        this.reloadOverlay()
    }

    setSelected() {
        super.setSelected()
        if (this.google_map.isEditor) {
            this.setShapeOptions({
                editable: true,
                draggable: true,
                strokeOpacity: 1,
            });
        }
    }

    setDeselected() {
        super.setDeselected()
        this.setShapeOptions({
            editable: false,
            draggable: false,
            strokeOpacity: 0,
        })
    }
}


