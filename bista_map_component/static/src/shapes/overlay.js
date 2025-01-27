/** @odoo-module **/

export function Overlay(object) {

    let MapOverlay = function (object) {
        this.object = object
        this.coordinates = object.coordinates
        this.boundary = object.model.getBoundary(object.coordinates)
        this.div = null;
        this.content = object.data.type === 'home' ? object.data.lot_number : object.content;
        this.map = object.map
        this.zoom_data = object.data.zoom_content || {}
    }


    MapOverlay.prototype = new google.maps.OverlayView();

    MapOverlay.prototype.onAdd = function () {
        this.div = document.createElement('div');
        this.div.className = object.className
        if (this.content) {
            this.div.append(this.content)
        }
        if (object.data.setBoundary !== false) {
            this.setLayoutBoundary()
        }
        const panes = this.getPanes();
        panes.overlayLayer.appendChild(this.div);
    }


    MapOverlay.prototype.setLayoutBoundary = function (new_coordinates) {
        if (new_coordinates) {
            this.coordinates = new_coordinates
            this.boundary = object.model.getBoundary(object.coordinates)
        }
        let coordinates = this.coordinates;
        const minLat = Math.min(...coordinates.map(point => point.lat()));
        const maxLat = Math.max(...coordinates.map(point => point.lat()));
        const minLng = Math.min(...coordinates.map(point => point.lng()));
        const maxLng = Math.max(...coordinates.map(point => point.lng()));

        const clipPathPoints = coordinates.map(point => {
            const normalizedX = (point.lng() - minLng) / (maxLng - minLng); // Normalize longitude
            const normalizedY = (point.lat() - minLat) / (maxLat - minLat); // Normalize latitude
            const xPercentage = (normalizedX * 100).toFixed(0);
            const yPercentage = ((1 - normalizedY) * 100).toFixed(0); // Flip y-axis for top-left origin
            return `${xPercentage}% ${yPercentage}%`;
        })
        const uniqueClipPathPoints = [...new Set(clipPathPoints)].join(", ");
        this.div.style.clipPath = `polygon(${uniqueClipPathPoints})`;
        return this.div;
    }

    MapOverlay.prototype.draw = function () {
        const southwest = new google.maps.LatLng(
            Math.min(this.boundary.bottomLeft.lat(), this.boundary.bottomRight.lat()), // Minimum latitude
            Math.min(this.boundary.bottomLeft.lng(), this.boundary.topLeft.lng()) // Minimum longitude
        );
        const northeast = new google.maps.LatLng(
            Math.max(this.boundary.topLeft.lat(), this.boundary.topRight.lat()), // Maximum latitude
            Math.max(this.boundary.topRight.lng(), this.boundary.bottomRight.lng()) // Maximum longitude
        );
        const bounds = new google.maps.LatLngBounds(southwest, northeast);

        // Get bound projection in pixel
        const overlayProjection = this.getProjection();
        const sw = overlayProjection.fromLatLngToDivPixel(
            bounds.getSouthWest(),
        );
        const ne = overlayProjection.fromLatLngToDivPixel(
            bounds.getNorthEast(),
        );


        // Reposition the layer
        if (this.div) {
            this.div.style.left = (sw.x) + "px";
            this.div.style.top = ne.y + "px";
            this.div.style.width = ne.x - sw.x + "px";
            this.div.style.height = sw.y - ne.y + "px";

            if (this.map) {
                this.setZoomContent()
            }
        }
    }

    MapOverlay.prototype.setZoomContent = function () {
        let $div = $(this.div)
        let zoom_level = this.map.getZoom()

        let zoom_to_set = false
        for (const key in this.zoom_data) {
            let zoom = parseInt(key)
            if (zoom_level >= zoom) {
                zoom_to_set = zoom
            }
        }

        let css = {}
        let options = {}

        if (this.content) {
            let $div = $(this.div)
            $div.empty()
            $div.append(this.content)
        }

        let zoom_content = this.zoom_data[zoom_to_set] || {}

        if (object.data.fill_type === 'color') {

            css = {
                'background-image': "unset",
                'background-size': "unset",
                'visibility': "unset"
            }

            if (zoom_level < 16) {
                css['visibility'] = 'hidden';
            }
        } else if (object.data.fill_type === 'image' && object.data.background_image) {
            options = {
                fillOpacity: 0,
                strokeOpacity: 0
            }
            css = {
                'background-image': "url('" + object.data.file_type + "," + object.data.background_image + "')",
                'background-size': "100% 100%",
                'display': 'block',
            }
        } else if (zoom_content && zoom_content.content) {
            $div.empty()
            css = {
                'padding': 0, 'margin': 0,
                'box-sizing': 'content-box',
                'background-image': 'unset',
                'background-size': 'unset',
            }

            if (zoom_content.type === 'image') {
                css = {
                    'background-image': "url('data:image/png;base64," + zoom_content.content + "')",
                    'background-size': "100% 100%",
                }
            } else if (zoom_content.type === 'image_url') {
                css = {
                    'background-image': 'url("' + zoom_content.content + '")',
                    'background-size': "100% 100%",
                }
            } else if (zoom_content.type === 'html') {
                $div.append(zoom_content.content)
            } else if (zoom_content.type === 'css') {
                css = JSON.parse(zoom_content.content.replace(/'/g, '"'))
            }

        }

        if (zoom_content.type === 'hide') {
            $div.hide()
        } else {
            css['z-index'] = object.data.sequence
            $div.css(css)
            $div.show()
            object.setShapeOptions(options)
        }


    }

    MapOverlay.prototype.onRemove = function () {
        if (this.div) {
            if (this.div.parentNode) {
                this.div.parentNode.removeChild(this.div);
            }
            this.div = null;
        }
    }

    return new MapOverlay(object)
}
