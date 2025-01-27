/* @odoo-module */


import {Overlay} from "./overlay";
import {renderToElement} from "@web/core/utils/render";
import { jsonrpc } from "@web/core/network/rpc_service";

export class ShapBase {
    static component = {}

    setup(GoogleMap, data) {
        this.googleMap = GoogleMap
        this.map = this.googleMap.map
        this.model = GoogleMap.model
        this.data = data || {}
        this.coordinates = []
        this.model.on("onZoomChanged", (zoomLevel) => this._onZoomChanged(zoomLevel))
        this.model.on("onMapClicked", (event) => this._onMapClicked(event))
        this.model.on("onMapReady", (event) => this._onMapReady(event))
        this.model.on("onKeyEscape", (event) => this._onKeyEscape(event))
        this.overlay = false
        this.updateCoordiantes = this.model.debounce(this.onCoordinateChange.bind(this), 500)
        this.shape = false;
        this.initDefaultValues()
    }


    initDefaultValues() {
        if (!this.data.sequence) {
            this.data.sequence = 1
        }
    }

    _onZoomChanged(zoomLevel) {
        this._updateVisibility(zoomLevel)

    }

    attachMap() {
        this.shape.setMap(this.googleMap.map)
        this.overlay = new Overlay(this)
        this.linkOverlay()
        this.addEventListeners()
        let zoom = this.googleMap.getZoom()
        this._updateVisibility(zoom)
        this.initPreview();
    }

    _updateVisibility(zoomLevel) {
        if (this.data.zoomMin && zoomLevel < this.data.zoomMin) {
            this.hideShape()
        } else if (this.data.zoomMax && zoomLevel > this.data.zoomMax) {
            this.hideShape()
        } else {
            this.showShape()
        }
    }

    _onMapClicked(event) {
        // Not Implemented
    }

    _onMapReady() {
        // Not Implemented
    }

    _onKeyEscape() {

    }

    setMap(map) {
        return map
    }

    showShape() {
        if (!this.googleMap || !this.googleMap.map) {
            return
        }
        this.setMap(this.googleMap.map)
    }

    hideShape() {
        this.setMap(null)
    }


    addEventListeners() {
        if (this.shape) {
            this.shape.addListener('click', this.onClick.bind(this))
        }
    }


    onClick(isEdit) {
        if(isEdit){
            this.openEditView()

        }
        else{
            this.openPreview();

        }
    }

    openDetailView() {
    this.openPreview();
    }

    openEditView() {
     this.model.selectObject(this, true)
    }

    unlinkOverlay() {
        if (this.overlay) {
            this.overlay.setMap(null);
        }
    }

    linkOverlay() {
        if (this.overlay) {
            this.overlay.setMap(this.googleMap.map);
        }
    }

    async onCoordinateChange() {
        this.reloadOverlay()
        if (!this.data.id) {
            return
        }

        await this.model.write(this.data.id, {coordinate_ids: [(5, 0, 0)]})
        let coordinate_vals = this.model.coordinatesToJson(this.coordinates).map(function (item) {
            console.log("Map items ", item)
            return [0, 0, item]
        })

        await this.model.write(this.data.id, {coordinate_ids: coordinate_vals})
    }


    reloadOverlay() {
        if (!this.overlay) {
            return
        }
        this.overlay.setLayoutBoundary(this.coordinates)
        this.overlay.draw()
    }

    initPreview() {
        this.preview = this.googleMap.object_preview;

        if (!this.preview) {
            return
        }


        this.previewContent = this.preview.find(".preview_content")
        let close_btn = this.preview.find(".fa-close")
        close_btn.off("click")
        close_btn.on('click', this.closePreview.bind(this))
    }

   async openPreview() {
        if (!this.preview) {
            return
        }
        this.previewContent.empty()
        let content = false

        if (this.data.click_event === 'html') {
            content = this.data.content_html
        } else if (this.data.click_event === 'url') {
            content = "<iframe style='height: 100%; width: 100%' src='" + this.data.content_url + "'/>"
        } else {
            if (this.data.type === 'home') {
//                let result = []
//                let home_plans = []
//                let partner = []
//                let params = {
//                    community_slug: this.data.community_slug ?? "",
//                    partner_slug: this.data.partner_slug ?? ""
//                };
                try {
                    this.model.onLotClick(this.data)
//                    result = await jsonrpc("/get/partners/plans", params)
//                    home_plans = result.home_plans
//                    partner = result.partner
                }
                catch(error) {
                    console.error("Error Fetching Home Plans! ", error)
                }
                content = true;// renderToElement('bista_map_component.lot_preview', { data: {...this.data, home_plans, partner } })
            }
        }

        if (content) {
//            this.previewContent.empty()
//            this.previewContent.append(content)
            this.preview.show()
        }
    }


    closePreview() {
        if (this.preview) {
            this.preview.hide()
        }
    }

    setShapeOptions(options) {
        if (this.shape_type === 'marker') {
            return
        }
        this.shape.setOptions(options)
    }

}



