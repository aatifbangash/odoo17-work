/* @odoo-module */

import {Component, onMounted, onWillStart, useRef, useState} from "@odoo/owl";
import {useBus} from "@web/core/utils/hooks";


export class MapEditor extends Component {
    static template = "bista_map_component.map_editor";

    setup() {
        this.editor = useRef("editor")
        this.model = this.env.model
        this.googleMap = this.env.googleMap
        useBus(this.model, "onMapReady", (event) => {
            this._onMapReady(event.detail)
        });
        this.community_ids = this.model.communities
        this.core_community_ids = this.googleMap.core_community_ids
        this.status_ids = this.googleMap.status_ids
        this.state = useState({
            sequence: 1,
            type: ''
        })
        this.section_ids = []
        onWillStart(this._onWIllStart.bind(this))
        onMounted(this._onMounted.bind(this))
        this.params = this.getUrlParams()
    }
    getUrlParams() {
            let params = {};
            let searchParams = new URLSearchParams(window.location.search);

            searchParams.forEach(function (value, key) {
                params[key] = value;
            });

            return params;
        }
    _onMounted() {
        this.initUI()
        this.model.editor = this
        this.eventListeners()
    }

    _onWIllStart() {

    }

    _onMapReady() {
    }

    initUI() {
        this.editor = $(this.editor.el)
        if (!this.editor) {
            return
        }
        this.image = this.editor.find("#image")
        this.imageB64 = false

    }

    eventListeners() {
        let input = this.editor.find("input")
        let select = this.editor.find("select")
        select.on('change', this.onChange.bind(this))
        input.on('change', this.onChange.bind(this))
    }


    onFillTypeChanged(event) {
        this.onChange(event)
        this.object.data.fill_type = this.state.fill_type
        this.object.overlay.draw()
    }


    onBlur(event) {
        this.onChange(event)
        this.object.overlay.content = this.state.lot_number
        this.object.overlay.draw()
    }

    onChange(event) {
        let field = $(event.target)
        let name = field.attr('name')
        let type = field.attr('type')
        if (type === 'checkbox') {
            this.state[name] = field.is(':checked')
        } else if (type === 'file') {
            this.state[name] = this.getImage(event)
        } else {
            this.state[name] = field.val()
            if (name =="community_id") {
                this.getSections(field.val())
            }
        }

        this.setOptions()
    }

    async getSections(community_id) {
        this.section_ids = await this.model.getSections(parseInt(community_id))
        console.log(this.section_ids)
    }
    getImage(event) {
        let image = event.target
        if (!image || !image.files || !image.files[0]) {
            return
        }
        var reader = new FileReader();
        reader.onload = (e) => {
            this.readFile(e.target.result) // Pass the base64 image data
        }
        reader.readAsDataURL(image.files[0])
        return this.imageB64
    }

    readFile(imageBase64) {
        let image_data = imageBase64.split(",")
        this.state.file_type = image_data[0]
        this.state.background_image = image_data[1]
        this.object.fill_type = 'image'
        this.object.data.file_type = image_data[0]
        this.object.data.background_image = image_data[1]
        this.object.data.fill_type = 'image'
        this.object.overlay.draw()
    }

    setOptions() {
        if (this.object) {
            let options = this.getOptions()
            this.object.setShapeOptions(options)
        }
    }

    getOptions() {
        let status = {}
        let self = this;
        if (this.state.status_id) {
            status = this.status_ids.filter(function (item) {
                return item.id.toString() === self.state.status_id.toString()
            })[0]
        }
        return {
            strokeColor: status.strokeColor || '#000',
            strokeWeight: status.strokeWeight || 2,
            fillColor: status.fillColor || '#000',
            fillOpacity: status.fillOpacity || 0.5,
            strokeOpacity: status.strokeOpacity,
            draggable: this.state.draggable,
            editable: this.state.editable,
            zIndex: this.state.sequence,
        }
    }

    setOrderForward() {
        let seq = parseInt(this.state.sequence) || 0
        this.state.sequence = seq + 1
        this.setOptions()
    }

    setOrderBackward() {
        let seq = parseInt(this.state.sequence) || 0
        this.state.sequence = seq - 1
        this.setOptions()
    }

    createObject(event) {
        let self = this;
        if (event.overlay) {
            event.overlay.setMap(null)
            self.googleMap.drawingManager.setOptions({
                drawingMode: null,
            })
        }

    }

    showEditor() {
        if (!this.googleMap.isEditor) {
            return
        }
        this.community_ids = this.model.communities
        this.getSections(this.community_ids[0].id)
        this.toggleDrawing(false)
        this.object = this.model.selectedObject
        this.data = this.object.data
        this.shape = this.object.shape
        this.setData(this.data)
        this.editor.show()
        this.editing = true;

    }

    toggleDrawing(option) {
        this.googleMap.drawingManager.setOptions({drawingControl: option});
    }


    hideEditor() {
        this.editor.hide()
        this.editing = false
        this.model.selectedObject = false;
        this.toggleDrawing(true)

    }

    async save() {
        let core_lot_data = {}
        let data = {
            status_id: parseInt(this.state.status_id || 0),
            background_image: this.state.background_image,
            sequence: this.state.sequence,
            fill_type: this.state.fill_type,
            file_type: this.state.file_type,
            radius: this.object.radius
        }
         if (this.state.type ==='community'){
            core_lot_data = {
                is_active: 1,
                display_name :this.state.name,
                legal_name : this.state.name,
                company_id: parseInt(this.params.company_id || 0)
            }

        } else {
            core_lot_data = {
                is_active: 1,
                name: this.state.name,
                lot_number: this.state.lot_number,
                section_id: parseInt(this.state.section_id || 0)
            }
        }
        let res = false;
        if (!this.object.data.id) {
            res = await this.model.create(core_lot_data,this.state.type )
            let map_lot = await this.model.get_map_item_by_core_id(res[0], this.state.type)
            if (map_lot) {
                data.id = map_lot[0].google_map_item_id[0]
            }

            data['google_map_id'] = this.googleMap.props.map.id
            data['shape_type'] = this.object.data.shape_type
            res = await this.model.write(data.id, data)
            this.object.data.id = data.id
            this.object.onCoordinateChange()
        } else {
            res = await this.model.write(this.data.id, data)
        }
        this.hideEditor();
    }

    discard() {
        this.hideEditor()
        if (!this.object.data.id && this.object.shape) {
            this.object.shape.setMap(null)
        }
    }

    setData(data) {

        this.data = data
        if (!this.data) {
            return
        }

        let self = this;
        self.state['core_community_id'] = false
        Object.keys(data).forEach(function (key) {
            self.state[key] = data[key]
        })
    }


    getData() {
        let data = this.state
        return data
    }


    onKeyDown(event) {
        if (!this.editing) {
            return
        }
        if (event.key === "Escape" || event.key === "Enter" || event.key === "Delete") {
            this.discard()
        }
        if (event.key === "Enter") {
            this.save()
        }
    }

}



