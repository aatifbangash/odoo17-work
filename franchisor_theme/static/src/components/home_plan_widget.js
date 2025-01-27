/* @odoo-module */

import {Component, onMounted, onWillStart, useRef, useState, useSubEnv} from "@odoo/owl";
import {registry} from "@web/core/registry"
import {useBus} from "@web/core/utils/hooks";
import {jsonrpc} from "@web/core/network/rpc_service";
import {GoogleMap} from "@bista_map_component/components/map_component"
import {MapModel} from "@bista_map_component/model/map_model"
import { patch } from "@web/core/utils/patch";

export class HomePlans extends Component {
    static template = "franchisor_theme.home_plan_template";

    setup() {
        console.log("HomePlans initialized!");
        onWillStart(this._onWIllStart.bind(this))
        this.imageDataUri = this.imageDataUri.bind(this);
        console.log(this.props, 'jkjk')
//        this.state.isDrawer = this.props.isDrawer ?? false
        this.state = useState({'partner_slug': this.props.partner_slug, 'community': this.props.community, FILETYPE_BASE64_MAGICWORD: {
                '/': 'jpeg',
                'i': 'png',
                'R': 'gif',
                'U': 'webp',
                'Q': 'svg+xml'
            }})
    }

    imageDataUri(base64Source) {
        const mimeType = this.state.FILETYPE_BASE64_MAGICWORD[base64Source?.charAt(0)] || 'png';

        return `data:image/${mimeType};base64,${base64Source}`;
    }

    async _onWIllStart() {
        console.log(this.state)
        let params = {
            community_slug: this.state.community ?? "",
            partner_slug: this.state.partner_slug
        };


        try {
            let communities = await jsonrpc("/get/partners/plans", params)
            this.state.home_plans = communities.home_plans
            this.state.partner = communities.partner
            this.state.isDrawer = this.props.isDrawer
        }catch(error){
            console.error("Error Fetching Home Plans! ", error)
        }

    }



    async _onMounted() {
    }


}

// inherit the GoogleMap OWL Component and modified/add the onLotClick event
patch(GoogleMap.prototype, {
    setup() {
        super.setup(...arguments);
        useBus(this.model, "onLotClick", (event) => {
            this._onLotClick(event.detail)
        });
    },
    _onLotClick(data) {
        this.state.record_id = data.id
        this.state.partner_slug = data.partner_slug
        this.state.community = data.community_slug
        this.state.status_name = data.status_name
    }
});

// inherit the MapModel OWL Component and modified/add the onLotClick event
patch(MapModel.prototype, {
    onLotClick(data) {
        this.trigger("onLotClick", data)
    }
});

GoogleMap.components = { ...GoogleMap.components, HomePlans }

registry.category("public_components").add("HomePlans", HomePlans);
