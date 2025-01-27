/** @odoo-module **/
import { registry } from '@web/core/registry';
const { Component, useState, onWillStart, useRef, onWillDestroy, } = owl;
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser"
import { routeToUrl } from "@web/core/browser/router_service"
import { session } from "@web/session";

export class MasterPlanOptions extends Component {
    setup(){
        this.orm = useService("orm")
        this.action = useService("action");
        this.state = useState({
            header: 'Master Plans',
            activePlans: [],
            inActivePlans: [],
            activeMasterPlans: [],
            inActiveMasterPlans: [],
            activePartnerPlans: [],
            inActivePartnerPlans: [],
            is_franchisor: session.is_franchisor,
            menu_id: this.props.action.params.menu_id,
            panel: '',
            confirmId: -1,
            community_name: ''
        });
        this.activatePlan = this.activatePlan.bind(this);
        this.deActivatePlan = this.deActivatePlan.bind(this);
        this.setMasterPlanAvailable = this.setMasterPlanAvailable.bind(this);
        this.setPlanToggle = this.setPlanToggle.bind(this);
        this.disablePlan = this.disablePlan.bind(this);
        this.toggleModal = this.toggleModal.bind(this);
        this.goBack = this.goBack.bind(this);

        onWillStart(async ()=>{
            console.log(this.props.action.params.panelName)
            console.log(this.props.action.context.active_id)
            console.log(session.is_franchisor)
            const fields = [
                        'id',
                        'type',
                        'default_code',
                        'active',
                        'name',
                        'slug',
                        'kova_model_rid',
                        'legal_name',
                        'is_published',
                        'base_price',
                        'incentive_price',
                        'price',
                        'min_bedrooms',
                        'max_bedrooms',
                        'min_bathrooms',
                        'max_bathrooms',
                        'base_heated_square_feet',
                        'max_heated_square_feet',
                        'base_total_square_feet',
                        'max_total_square_feet'
                    ]

            const router = this.env.services.router
            let { search, hash } = router.current
            if (this.props.action.params.panel || this.props.action.params.homeplan_name) {
                search.panelName = this.props.action.params.panel
                search.community_name = this.props.action.params.community_name
                search.menu_id = hash.menu_id
            }
            this.state.menu_id = search.menu_id
            this.state.panelName = search.panelName
            this.state.community_name = search.community_name
            const activeMasterPlans = await this.orm.searchRead('product.template', [['is_published', '=', true]], fields)
            const inActiveMasterPlans = await this.orm.searchRead('product.template', [['is_published', '=', false]], fields)
            const partnerEnabledPlans = await this.orm.searchRead('module_sb.franchise_homeplans', [['company_id', '=', session.user_companies.current_company]], [])
            const enabledPlans = partnerEnabledPlans.map((obj) => obj['homeplan_id'][0])
            const activePartnerPlans = [];
            const inActivePartnerPlans = [];
            const activeCommunityPlans = [];
            const inActiveCommunityPlans = [];

            for (const plan of activeMasterPlans) {
                if (enabledPlans.includes(plan.id)) {
                    activePartnerPlans.push({ ...plan, enable: true });
                } else {
                    inActivePartnerPlans.push({ ...plan, enable: false });
                }
            }

            this.state.activeMasterPlans = activeMasterPlans
            this.state.inActiveMasterPlans = inActiveMasterPlans
            this.state.activePartnerPlans = activePartnerPlans
            this.state.inActivePartnerPlans = inActivePartnerPlans
            if (this.state.panelName == 'Community') {
                const community_id = this.props.action.context.active_id;
                const communityPlans = await this.orm.searchRead('community_module.community_homeplans', [['community_id', '=', community_id]], ["homeplan_id" ,"base_price"]);
                const communityEnabledPlans = communityPlans.map((obj) => ({ homeplan_id: obj['homeplan_id'][0], id: obj['id'], base_price: obj['base_price'] }));

                for (const plan of activePartnerPlans) {
                    const match = communityEnabledPlans.find((enabledPlan) => enabledPlan.homeplan_id === plan.id);
                    if (match) {
                        activeCommunityPlans.push({ ...plan, price: match.base_price, community_plan_id: match.id, enable: true });
                    } else {
                        inActiveCommunityPlans.push({ ...plan, enable: false });
                    }
                }
                console.log('Active Community Plans:', activeCommunityPlans);
                console.log('Inactive Community Plans:', inActiveCommunityPlans);
                this.state.activePlans = activeCommunityPlans
                this.state.inActivePlans = inActiveCommunityPlans
            }
            if (this.state.is_franchisor) {
                this.state.activePlans = activeMasterPlans
                this.state.inActivePlans = inActiveMasterPlans
            } else {
            if (this.state.panelName == 'Community') {
                    this.state.activePlans = activeCommunityPlans
                    this.state.inActivePlans = inActiveCommunityPlans
                    this.state.header = 'Community Plans'
                }
                 else {
                    this.state.activePlans = activePartnerPlans
                    this.state.inActivePlans = inActivePartnerPlans
                    this.state.header = 'Plans'
                }
            }
//            this.state.activePartnerPlans = activePartnerPlans
//            this.state.inActivePartnerPlans = inActivePartnerPlans
//            console.log('Active Master Plans:', activeMasterPlans);
//            console.log('Inactive Master Plans:', inActiveMasterPlans);
//            console.log('Active Partner Plans:', activePartnerPlans);
//            console.log('Inactive Partner Plans:', inActivePartnerPlans);
        })
         onWillDestroy(() => {
            // remove listener
            const router = this.env.services.router
            let { search } = router.current
            delete search.panelName
        });
    }
    async goBack(){
        const kanbanViewURL =  "web#model=community_module.community&view_type=kanban&menu_id="+this.state.menu_id;
        window.location.hash = kanbanViewURL;
    }
    activatePlan = async (plan_id)=> {
        const activeCommunityPlans = [];
        const inActiveCommunityPlans = [];
        const community_id = this.props.action.context.active_id;
        let newRecordId = await this.orm.create('community_module.community_homeplans',[ {
            'community_id': community_id,
            'homeplan_id': plan_id
        }]);
        const communityPlans = await this.orm.searchRead('community_module.community_homeplans', [['community_id', '=', community_id]], []);
        const communityEnabledPlans = communityPlans.map((obj) => ({ homeplan_id: obj['homeplan_id'][0], id: obj['id'] }));

        for (const plan of this.state.activePartnerPlans) {
            const match = communityEnabledPlans.find((enabledPlan) => enabledPlan.homeplan_id === plan.id);
            console.log(communityEnabledPlans)
            if (match) {
                activeCommunityPlans.push({ ...plan, community_plan_id: match.id, enable: true });
            } else {
                inActiveCommunityPlans.push({ ...plan, enable: false });
            }
        }
        this.state.activePlans = activeCommunityPlans
        this.state.inActivePlans = inActiveCommunityPlans
    }
    deActivatePlan = async (plan_id)=> {
        const activeCommunityPlans = [];
        const inActiveCommunityPlans = [];
        const community_id = this.props.action.context.active_id;
        let domain = [
            ['community_id', '=', community_id],
            ['homeplan_id', '=', plan_id]
        ];
        let recordsToDelete = await this.orm.searchRead('community_module.community_homeplans', domain, []);

        for (let record of recordsToDelete) {
            await this.orm.unlink('community_module.community_homeplans', [record.id]);
        }
        const communityPlans = await this.orm.searchRead('community_module.community_homeplans', [['community_id', '=', community_id]]);
        const communityEnabledPlans = communityPlans.map((obj) => ({ homeplan_id: obj['homeplan_id'][0], id: obj['id'] }));

        for (const plan of this.state.activePartnerPlans) {
            const match = communityEnabledPlans.find((enabledPlan) => enabledPlan.homeplan_id === plan.id);
            console.log(communityEnabledPlans)
            if (match) {
                activeCommunityPlans.push({ ...plan, community_plan_id: match.id, enable: true });
            } else {
                inActiveCommunityPlans.push({ ...plan, enable: false });
            }
        }
        this.state.activePlans = activeCommunityPlans
        this.state.inActivePlans = inActiveCommunityPlans
    }
    setMasterPlanAvailable = async (id, e) => {
        const plan = await this.orm.searchRead('product.template', [['id', '=', id]])
        console.log('!',{ plan })
        if (plan.length > 0) {
            await this.orm.write("product.template", [id], {
                is_published: !plan[0].is_published
            });
        }
        const activeMasterPlans = await this.orm.searchRead('product.template', [['is_published', '=', true]], [])
        const inActiveMasterPlans = await this.orm.searchRead('product.template', [['is_published', '=', false]], [])
        this.state.activePlans = activeMasterPlans
        this.state.inActivePlans = inActiveMasterPlans
    }
    setPlanToggle = async (id) => {
        let domain = [
            ['company_id', '=', session.user_companies.current_company],
            ['homeplan_id', '=', id]
        ]
        let records = await this.orm.searchRead('module_sb.franchise_homeplans', domain, []);
        if (records.length > 0) {
            for (let record of records) {
                await this.orm.unlink('module_sb.franchise_homeplans', [record.id]);
            }
        } else {
            await this.orm.create('module_sb.franchise_homeplans',[ {
                'company_id': session.user_companies.current_company,
                'homeplan_id': id
            }])
        }
        const partnerEnabledPlans = await this.orm.searchRead('module_sb.franchise_homeplans', [['company_id', '=', session.user_companies.current_company]], [])
        const enabledPlans = partnerEnabledPlans.map((obj) => obj['homeplan_id'][0])
        const activePartnerPlans = []
        const inActivePartnerPlans = []
        for (const plan of this.state.activeMasterPlans) {
            if (enabledPlans.includes(plan.id)) {
               activePartnerPlans.push({ ...plan, enable: true });
            } else {
                inActivePartnerPlans.push({ ...plan, enable: false });
            }
        }
        this.state.activePlans = activePartnerPlans
        this.state.inActivePlans = inActivePartnerPlans
    }
    disablePlan = async () => {
        console.log({di: this.state.confirmId})
        if(this.state.is_franchisor) {
            this.setMasterPlanAvailable(this.state.confirmId)
        } else {
            if (this.state.panelName == 'Community') {
                this.deActivatePlan(this.state.confirmId)
            } else {
                   this.setPlanToggle(this.state.confirmId)
            }
        }
        this.toggleModal(-1)
    }
    toggleModal(id) {
    console.log({id})
        this.state.confirmId = id
    }
    newPlan = async () => {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "product.template",
            views: [[false, "form"]]
        });
    }

    editPlan = async (id) => {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "product.template",
            views: [[false, "form"]],
            res_id: id
        });
    }

    editCommunityPlan = async (id) => {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "community_module.community_homeplans",
            views: [[false, "form"]],
            res_id: id,
            context: {
                    default_active_id: id,
                    default_res_model: "community_module.community_homeplans",
                    default_res_id: id,
                    community_name: this.state.community_name
                },
        });
    }

    setMasterPlanOption = async (id, name,activeMasterPlan) => {
        console.log({activeMasterPlan})
        this.action.doAction({
            type: "ir.actions.client",
            tag: "owl.master_plan_options",
            context: {
                homeplan_id: id,
                active_id:this.state.panelName =='Community' ? activeMasterPlan.community_plan_id : id
            },
            params: {
                homeplan_id: id,
                homeplan_name: name,
                panel: this.state.is_franchisor ? 'Master Plans' : this.state.panelName =='Community' ? 'Communities' : 'Home plans',
                    community_name: this.state.community_name
            },
        });
    }

    formattedPrice = (price) => {
    const decimalPrice = Number(price).toFixed(2);
        return parseFloat(decimalPrice).toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

}

MasterPlanOptions.template = 'owl.Plans'
registry.category('actions').add('owl.plans', MasterPlanOptions);