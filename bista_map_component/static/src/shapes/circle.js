/** @odoo-module **/

import {ShapBase} from "./base";

export class Circle extends ShapBase {
    u

    setup(GoogleMap, data) {
        super.setup(GoogleMap, data)
        this.className = 'shape_rectangle'
        this.type = 'circle'
        this.setBoundary = false
        this.center = data.center

        if (this.data.coordinates) {
            this.coordinates = this.model.parseCoordinates(this.data.coordinates)
            this.coordinate = this.coordinates[0]
            this.center = this.coordinate
        }

        this.radius = this.data.radius
        this.shape = new google.maps.Circle({
            strokeColor: this.data.strokeColor || '#000',
            strokeWeight: this.data.strokeWeight || 2,
            fillColor: this.data.fillColor || '#000',
            fillOpacity: this.data.fillOpacity || 0.5,
            strokeOpacity: 0.8,
            center: this.center,
            radius: this.radius,
            editable: this.data.editable,
            draggable: this.data.draggable,
            clickable: true,
            visible: true,
            zIndex: this.data.sequence
        })

        // Assign circle points as coordinates
        this.getClipPath()

    }

    getClipPath() {
        // Function to calculate points on the circle's circumference

        if (!this.center || !this.radius) {
            return
        }
        let centerLat = this.center.lat()
        let centerLng = this.center.lng()

        let self = this;
        const calculateCirclePoints = (centerLat, centerLng, radius) => {
            const points = [];
            const numSegments = 360; // Number of segments to approximate the circle
            for (let i = 0; i < numSegments; i++) {
                const angle = (i * Math.PI * 2) / numSegments;
                const pointLat = centerLat + (radius / 111320) * Math.cos(angle); // 111320 meters per degree latitude
                const pointLng = centerLng + (radius / (111320 * Math.cos(centerLat * (Math.PI / 180)))) * Math.sin(angle);
                points.push(self.model.getPosition(pointLat, pointLng));
            }
            return points;
        };
        this.coordinates = calculateCirclePoints(centerLat, centerLng, this.radius);
    }

    addEventListeners() {
        super.addEventListeners()
        this.shape.addListener("center_changed", this.onCenterChanged.bind(this));
        this.shape.addListener("radius_changed", this.onRadiusChanged.bind(this));
    }

    async onRadiusChanged() {
        this.center = this.shape.getCenter()
        this.radius = this.shape.getRadius()
        this.getClipPath()
        this.reloadOverlay()
        await this.model.write(this.data.id, {radius: this.radius})
    }

    getRadius() {
        return this.shape.getRadius()
    }

    getCenter() {
        this.coordinate = this.shape.getCenter()
        this.coordinates = [{lat: this.coordinate.lat(), lng: this.coordinate.lng()}]
        return this.coordinate
    }

    onCenterChanged() {
        this.onCoordinateChange()
    }


    async onCoordinateChange() {
        this.center = this.getCenter()
        this.getClipPath()
        await this.model.write(this.data.id, {coordinate_ids: [(5, 0, 0)]})
        let coordinate_vals = this.model.coordinatesToJson([this.coordinate]).map(function (item) {
            return [0, 0, item]
        })

        await this.model.write(this.data.id, {coordinate_ids: coordinate_vals})
    }

}

export default Circle;

