/** @odoo-module */

import { registry } from "@web/core/registry"
import { KpiCards } from "./kpi_cards/kpi_cards"
import { Charts } from "./charts/charts"
import { loadJS } from "@web/core/assets"
import { session } from "@web/session";
//Get user group
import { useService } from "@web/core/utils/hooks";

const { Component, useRef, onWillStart, onMounted, useState } = owl

export class OwlSbDashboard extends Component {
    setup(){
        this.state = useState({
            is_franchisor: session.is_franchisor,
            companies:{
                value: 0
            },
            masterPlanes:{
                value: 0
            },
            enabledPlans:{
                value: 0
            },
            communities:{
                value: 0
            },
            orders:{
                value: 0
            },
            period: 90

        });

        this.orm = useService("orm");
        this.actionService = useService("action");

        onWillStart(async ()=>{
            this.getDate();
            await this.getPartners();
            await this.getMasterPlanes();
            await this.getEnabledPlanes();
            await this.getCmmunities();
        })

            // get user group
            //       this.userService = useService("user");
            //       this.checkUserGroup();
    }

    async getPartners(){
        if(!this.state.is_franchisor)
            return;

        let domain = [];
        if(this.state.period > 0){
            domain = [["create_date", ">", this.state.date]]
        }

        const data = await this.orm.searchCount("res.company",domain);
        this.state.companies.value = data;
    }

    viewPartners(){
        let domain = [];
        if(this.state.period > 0){
            domain = [["create_date", ">", this.state.date]]
        }

        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Partners",
            res_model: "res.company",
            domain: domain,
            views: [
                [false, "list"],
                [false, "form"],
            ]
        });
    }

    async getMasterPlanes(){
        if(!this.state.is_franchisor)
            return;

        let domain = [];
        if(this.state.period > 0){
            domain = [["create_date", ">", this.state.date]]
        }

        const data = await this.orm.searchCount("product.template",domain);
        this.state.masterPlanes.value = data;
    }

    async getEnabledPlanes() {
        if(this.state.is_franchisor)
            return;
        let domain = [
            ["company_id", "=", session.user_companies.current_company],
        ];
        if(this.state.period > 0){
            domain.push(["create_date", ">", this.state.date])
        }

        const data = await this.orm.searchCount("module_sb.franchise_homeplans",domain);
        this.state.enabledPlans.value = data;
    }
    viewMasterPlanes(){
        this.actionService.doAction({
            type: "ir.actions.client",
            tag:"owl.plans",
            params: {
            }

        });
    }

    async getCmmunities(){
        let domain = [];
        if(this.state.period > 0){
            domain = [["create_date", ">", this.state.date]]
        }

        const data = await this.orm.searchCount("community_module.community",domain);
        this.state.communities.value = data;
    }
    viewCmmunities(){
         let domain = [];
        if(this.state.period > 0){
            domain = [["create_date", ">", this.state.date]]
        }

        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Cumminities",
            res_model: "community_module.community",
            domain: domain,
            views: [
                [false, "kanban"],
                [false, "form"],
            ]
        });
    }



    async getOrders(){
        //const data = await this.orm.searchCount("res.company",[]);
        this.state.orders.value = 0;
    }
    viewOrders(){
        console.log("viewOrders");
    }

    async onChangePeriod(){
        this.getDate();
        await this.getPartners();
        await this.getMasterPlanes();
        await this.getEnabledPlanes();
        await this.getCmmunities();
    }

    getDate(){
        this.state.date = luxon.DateTime.now().minus({ days: this.state.period }).toFormat('MM/dd/yyyy');
    }

    viewCompanies(){
    }


//     async checkUserGroup() {
//        // Replace 'module_name.group_name' with the actual group XML ID
//        const hasGroup = await this.userService.hasGroup("base.group_allow_export");
//        console.log("User has group:", hasGroup);
//
//        // You can then use this boolean to control the UI or logic
//        if (hasGroup) {
//            // User has the specified group
//        } else {
//            // User does not have the specified group
//        }
//    }
}

OwlSbDashboard.template = "owl.OwlSBDashboard"
OwlSbDashboard.components = { KpiCards, Charts }
//OwlSalesDashboard.components = { KpiCard, ChartRenderer }

registry.category("actions").add("owl.sb_dashboard", OwlSbDashboard)