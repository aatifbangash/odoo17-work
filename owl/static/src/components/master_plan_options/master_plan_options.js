/** @odoo-module **/
import { registry } from '@web/core/registry';
const { Component, useState, onWillStart, useRef, onWillDestroy, } = owl;
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser"
import { routeToUrl } from "@web/core/browser/router_service"
import { loadJS } from "@web/core/assets"
function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}
export class MasterPlanOptions extends Component {
    setup(){
        this.state = useState({
            task: {
                name:"",
                color:"#FF0000",
                completed:false
            },
            optionSet:[],
            inherited_name: "",
            selectedOption: 0,
            price_type: "fixed",
            option_value_image: '',
            unit_type: "",
            is_override: false,
            quantity: 0,
            FILETYPE_BASE64_MAGICWORD: {
                '/': 'jpeg',
                'i': 'png',
                'R': 'gif',
                'U': 'webp',
                'Q': 'svg+xml'
            },
            editOptionName: {
            isAttribute: true,
                option_id: 0,
                homeplan_id: 0,
                name: '',
                price: 0,
                master_plan_option_id: 0
            },
            editOptionValue: {
                master_plan_option_id: 0,
                name: '',
                description: '',
                price: 0,
                image: null
            },
            createOptions: [],
            homeplan_name: this.props.action.params.homeplan_name,
            isMasterPlan: false,
            isHomePlan: false,
            isCommunity: false,
            option_type: '',
            homeplan_id: this.props.action.context.active_id,
            community_homeplan_id: this.props.action.context.homeplan_id,
            menu_id: this.props.action.params.menu_id,
            createOptionValues: [],
            isEdit: false,
            activeId: false,
            selectedParentOption: -1,
            currentPage: 1,
            itemsPerPage: 5,
            totalRecords: 1,
            totalPages: 1,
            selectedParentOption: -1,
            classes: [{id: -1, name: 'All Classes'}],
            locations: [{id:-1, name: 'All Locations'}],
            categories: [{id: -1, name: 'All Categories'}],
            selectedClass: -1,
            selectedCategory: -1,
            selectedLocation: -1,
            timeoutId: null,
            enabled: 'all',
            enabledOptions: [
            {id: 'all', name: 'All Options'},
            {id: 'active', name: 'Enabled'},
            {id: 'inactive', name: 'Disabled'}
            ],
            view_type:this.props.action.params.view_type,
        }),
        this.action = useService("action");
        this.exportToExcel = this.exportToExcel.bind(this);
        this.addOptionValue = this.addOptionValue.bind(this);
        this.saveOptionSet = this.saveOptionSet.bind(this);
        this.addTask = this.addTask.bind(this);
        this.getAllOptionValues = this.getAllOptionValues.bind(this);
        this.changeOptionNameHandler = this.changeOptionNameHandler.bind(this);
        this.changeOptionPriceHandler = this.changeOptionPriceHandler.bind(this);
        this.overrideOptionName = this.overrideOptionName.bind(this);
        this.setAsBase = this.setAsBase.bind(this);
        this.imageDataUri = this.imageDataUri.bind(this);
        this.setPriceType = this.setPriceType.bind(this);
        this.getOptionValueParams = this.getOptionValueParams.bind(this);
        this.editOptionValues = this.editOptionValues.bind(this);
        this.getAllOptions = this.getAllOptions.bind(this);
        this.goBack = this.goBack.bind(this);
        this.settingPaginationStates = this.settingPaginationStates.bind(this);
        this.getPages = this.getPages.bind(this);
        this.nextPage = this.nextPage.bind(this);
        this.prevPage = this.prevPage.bind(this);
        this.getAllOptionsForModal = this.getAllOptionsForModal.bind(this);
        this.onSearchTextChange = debounce(this.onSearchTextChange.bind(this), 1000);
        this.orm = useService("orm")
        this.model = "owl.todo.list"
        this.searchInput = useRef("search-input")

        onWillStart(async ()=>{
//            await this.getAllTasks()

            const params = this.props.action
            const router = this.env.services.router
            let { search, hash } = router.current
            if (this.props.action.params.panel || this.props.action.params.homeplan_name || this.props.action.params.community_name) {
                search.panel = this.props.action.params.panel
                search.homeplan_name = this.props.action.params.homeplan_name
                search.homeplan_id = this.props.action.context.homeplan_id
                search.menu_id = hash.menu_id
                search.community_name = this.props.action.params.community_name
                search.prev_view_type = this.props.action.params.view_type
            }
            this.state.view_type = search.prev_view_type
            this.state.isMasterPlan =  search.panel === "Master Plans"
            this.state.isHomePlan= search.panel === "Home plans"
            this.state.isCommunity= search.panel === "Communities"
            this.state.homeplan_name= search.homeplan_name
            this.state.community_homeplan_id = search.homeplan_id
            this.state.menu_id = search.menu_id
            this.state.community_name = search.community_name
            const state = JSON.parse(JSON.stringify(this.state))
//        browser.location.href = browser.location.origin //+ routeToUrl(router.current)
            const menuName =await this.getMenuDetails(this.props.action.params.menu_id)

            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js")
            let optionSet ={}
            let selectedOptions = []
            // Filter dropdowns
            let res = await fetch('/option_classes', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });
            let res_data = await res.json();
            if (res_data.data) {
                console.log('No Locations found...')
            }
            else{
                this.state.classes = [...this.state.classes,...res_data]
            }
            res = await fetch('/option_locations', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });

            res_data = await res.json();
            if (res_data.data) {
                console.log('No Locations found...')
            }
            else {
                this.state.locations = [...this.state.locations,...res_data]
            }
            res = await fetch('/option_categories', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });

            res_data = await res.json();
            if (res_data.data) {
                console.log('No Categories found...')
            }
            else {
                this.state.categories = [...this.state.categories,...res_data]
            }

            // Data queries
            let filterParams = ''
            const class_id = -1
            const location_id = -1
            const category_id = -1
            if (this.state.selectedClass> 0){
                filterParams = filterParams + '&class_id=' + this.state.selectedClass
            }
            if (this.state.selectedLocation > 0){
                filterParams = filterParams + '&location_id=' +  this.state.selectedLocation
            }
            if (this.state.selectedCategory > 0) {
                filterParams = filterParams + '&category_id=' +  this.state.selectedCategory
            }
            if (this.state.isHomePlan) {
                const res = await fetch('/master_plan_active/'+this.state.homeplan_id+'/options?page_no='+this.state.currentPage+filterParams, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' },
                });
                const response = await fetch('/home_plan/'+this.state.homeplan_id+'/options',  {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' },
                })
                selectedOptions =  await response.json()
                optionSet = await res.json()
            }
            else if (this.state.isMasterPlan) {
                const res = await fetch('/master_plan/'+this.state.homeplan_id+'/options?page_no='+this.state.currentPage+filterParams, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' },
                });
                optionSet = await res.json()
            }
            else if (this.state.isCommunity){
                const res = await fetch('/home_plan_active/'+this.state.community_homeplan_id+'/options/'+ this.state.homeplan_id+'?page_no='+this.state.currentPage+filterParams, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' },
                });
                const response = await fetch('/community/home_plan/'+this.state.homeplan_id+'/options',  {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' },
                })
                selectedOptions =  await response.json()
                optionSet = await res.json()
            }
            if(optionSet.data === 'Not found'){
                this.state.optionSet = []
            } else {
                this.state.itemsPerPage = optionSet?.pagination?.page_size;
                this.state.totalRecords = optionSet?.pagination?.total_records;
                this.state.totalPages = optionSet?.pagination?.total_pages;
                this.state.optionSet = optionSet?.data?.map((option)=> {
                    const children = option.option_values?.map((child)=> {
                        let selectedOpt = false
                        if (selectedOptions?.data !== 'Not found'){
                            selectedOpt = selectedOptions?.data?.find((ov)=> {
                                if(state.isHomePlan){
                                    return  ov?.master_plan_option_id === child?.master_plan_option_id
                                }
                                else if (state.isCommunity) {
                                    return  ov?.homeplan_option_id === child?.home_plan_option_id
                                }
                            })
                        }
                        return {
                            id: child.option_value_id,
                            name: child.name,
                            is_base: ((this.state.isMasterPlan || this.state.isHomePlan || this.state.isCommunity) || !selectedOpt) ? child.is_base : selectedOpt?.is_base,
                            option_set_id: !child.option_set_id ? '' : child.option_set_id,
                            option_classes_id: child.option_classes_id,
                            option_categories_id: child.option_categories_id,
                            master_plan_option_id: child.master_plan_option_id,
                            homeplan_option_id: child.home_plan_option_id,
                            description: child.description === 'null' ? '' : child.description,
                            inherited_name: child.inherited_name,
                            is_override: child.is_override,
                            price: child.price,
                            image: child.image,
                            quantity: !child.quantity ? '-' : child.quantity,
                            is_active: this.state.isMasterPlan || !selectedOpt ? child?.is_active : selectedOpt?.is_active
                        }
                    })
                    return {
                        id: option.option_id,
                        recordId: option.id, //this is used to enable disable option name 3 dots buttons on create/edit mode.
                        is_override: option.is_override,
                        homeplan_id: option.homeplan_id,
                        primaryId: option.id,
                        name: option.name,
                        inherited_name: option.inherited_name,
                        option_categories_id: option.option_categories_id,
                        option_type: option.option_type,
                        price: option.price > 0 ? option.price : undefined,
                        price_type: option.price_type,
                        unit_type: !option.units ? '-' : option.units,
                        option_classes_id: option.option_classes_id,
                        is_active: children?.some((child)=> child.is_active),
                        children
                    }
                })
            }

        })
        onWillDestroy(() => {
            // remove listener
            const router = this.env.services.router
            let { search } = router.current
            delete search.panel
            delete search.homeplan_name
            delete search.community_name
            delete search.homeplan_id
            delete search.menu_id
            delete search.prev_view_type
        });
    }
     onSearchTextChange(searchText) {
        console.log({ searchText });
        this.getAllOptions(1, searchText);
    }
    async onScroll(e) {
        const container = e.target;
        const nearBottom = container.scrollHeight - container.scrollTop <= container.clientHeight + 100;
        if (nearBottom && this.state.currentPage < this.state.totalPages) {
            this.state.currentPage = this.state.currentPage + 1;
            const prevOptions = this.state.optionSet
            await this.getAllOptions(this.state.currentPage);
            this.state.optionSet = [...prevOptions, ...this.state.optionSet]
        }
    }
    imageDataUri(base64Source) {
    const mimeType = this.state.FILETYPE_BASE64_MAGICWORD[base64Source?.charAt(0)] || 'png';
    return `data:image/${mimeType};base64,${base64Source}`;
    }

    exportToExcel(){
        const optionsData = JSON.parse(JSON.stringify(this.state.optionSet));
        const headerStyle = {
            font: {
                name: "Arial",
                sz: 16,
                bold: true,
                color: { rgb: "FFFFFF" },
            },
            fill: {
                fgColor: { rgb: "4F81BD" },
            },
            alignment: {
                horizontal: "center",
                vertical: "center",
            },
        };

        const cellStyle = {
            font: {
                name: "Calibri",
                sz: 12,
                color: { rgb: "000000" },
            },
            alignment: {
                horizontal: "left",
                vertical: "center",
            },
        };

        const dataToExport = []
        optionsData.forEach((option)=>{
            option.children.forEach((optionValue)=> {
                dataToExport.push({
                    "Option": option.name,
                    "Category": option.option_categories_id[1],
                    "Class": option.option_classes_id[1],
                    "Option Value": optionValue.name,
                    "Quantity": optionValue.quantity,
                    ...(this.state.isHomePlan ? {
                            "Price": optionValue.price,
                            "Extended Price": optionValue.quantity === '-' ? optionValue.price : optionValue.quantity * optionValue.price
                        }:
                        this.state.isCommunity ? {
                            "Price": optionValue.price,
                            "Extended Price": optionValue.quantity === '-' ? optionValue.price : optionValue.quantity * optionValue.price
                            }: {})

                })
            })
        })
        // Convert data to worksheet
        const worksheet = XLSX.utils.json_to_sheet(dataToExport);
        // Create a new workbook
        const headers = Object.keys(dataToExport[0]);
            headers.forEach((header, index) => {
                const cellAddress = XLSX.utils.encode_cell({ c: index, r: 0 });
                if (!worksheet[cellAddress]) {
                    worksheet[cellAddress] = { t: 's', v: header };
                }
                worksheet[cellAddress].s = headerStyle;
            });

            // Apply cell style
            for (let R = 1; R <= dataToExport.length; ++R) {
                for (let C = 0; C < headers.length; ++C) {
                    const cellAddress = XLSX.utils.encode_cell({ c: C, r: R });
                    if (worksheet[cellAddress]) {
                        worksheet[cellAddress].s = cellStyle;
                    }
                }
            }
        const workbook = XLSX.utils.book_new();
        // Append worksheet to workbook
        XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");
        // Generate Excel file and trigger download
        XLSX.writeFile(workbook, "data.xlsx");

    }

    settingPaginationStates(pagination){
            this.state.currentPage = pagination?.page_no;
            this.state.itemsPerPage = pagination?.page_size;
            this.state.totalRecords = pagination?.total_records;
            this.state.totalPages = pagination?.total_pages;
    }


    async getAllOptions(page, searchText){
        this.state.currentPage = page
        let optionSet ={}
        let selectedOptions = []
        const state = JSON.parse(JSON.stringify(this.state))
        let filterParams = ''
        const class_id = -1
        const location_id = -1
        const category_id = -1
        if (this.state.selectedClass> 0){
            filterParams = filterParams + '&class_id=' + this.state.selectedClass
        } if(this.state.selectedLocation > 0){
            filterParams = filterParams + '&location_id=' +  this.state.selectedLocation
        } if(this.state.selectedCategory > 0) {
            filterParams = filterParams + '&category_id=' +  this.state.selectedCategory
        } if(searchText){
            filterParams = filterParams + '&search_term=' +  searchText
        } if(this.state.enabled !== 'all'){
            filterParams = filterParams + '&status=' +  this.state.enabled
        }
        if (this.state.isHomePlan) {
            const res = await fetch('/master_plan_active/'+this.state.homeplan_id+'/options?page_no='+this.state.currentPage+filterParams, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });
            const response = await fetch('/home_plan/'+this.state.homeplan_id+'/options',  {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            })
            selectedOptions =  await response.json()
            optionSet = await res.json()
        }
        else if (this.state.isMasterPlan) {
            const res = await fetch('/master_plan/'+this.state.homeplan_id+'/options?page_no='+this.state.currentPage+filterParams, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });
            optionSet = await res.json()
        }
        else if (this.state.isCommunity){
            const res = await fetch('/home_plan_active/'+this.state.community_homeplan_id+'/options/'+ this.state.homeplan_id+'?page_no='+this.state.currentPage+filterParams, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });
            const response = await fetch('/community/home_plan/'+this.state.homeplan_id+'/options',  {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            })
            selectedOptions =  await response.json()
            optionSet = await res.json()
        }
        if(optionSet.data === 'Not found'){
            this.state.optionSet = []
        } else {
            this.settingPaginationStates(optionSet?.pagination)
            this.state.optionSet = optionSet?.data?.map((option)=> {
                const children = option.option_values?.map((child)=> {
                    let selectedOpt = false
                    if (selectedOptions?.data !== 'Not found'){
                        selectedOpt = selectedOptions?.data?.find((ov)=> {
                            if(state.isHomePlan){
                                return  ov?.master_plan_option_id === child?.master_plan_option_id
                            }
                            else if (state.isCommunity) {
                                return  ov?.homeplan_option_id === child?.home_plan_option_id
                            }
                        })
                    }
                    return {
                        id: child.option_value_id,
                        name: child.name,
                        is_base: ((this.state.isMasterPlan || this.state.isHomePlan || this.state.isCommunity) || !selectedOpt) ? child.is_base : selectedOpt?.is_base,
                        option_set_id: !child.option_set_id ? '' : child.option_set_id,
                        option_classes_id: child.option_classes_id,
                        option_categories_id: child.option_categories_id,
                        master_plan_option_id: child.master_plan_option_id,
                        homeplan_option_id: child.home_plan_option_id,
                        description: child.description === 'null' ? '' : child.description,
                        price: child.price,
                        image: child.image,
                        quantity: !child.quantity ? '-' : child.quantity,
                        inherited_name: child.inherited_name,
                        is_override: child.is_override,
                        is_active: this.state.isMasterPlan || !selectedOpt ? child?.is_active : selectedOpt?.is_active
                    }
                })
                return {
                    id: option.option_id,
                    recordId: option.id, //this is used to enable disable option name 3 dots buttons on create/edit mode.
                    is_override: option.is_override,
                    homeplan_id: option.homeplan_id,
                    primaryId: option.id,
                    name: option.name,
                    inherited_name: option.inherited_name,
                    option_type: option.option_type,
                    price: option.price > 0 ? option.price : undefined,
                    price_type: option.price_type,
                    unit_type: !option.units ? '-' : option.units,
                    option_categories_id: option.option_categories_id,
                    option_classes_id: option.option_classes_id,
                    is_active: children?.some((child)=> child.is_active),
                    children
                }
            })
        }
    }

    nextPage(){
        this.state.currentPage = this.state.currentPage + 1;
        this.getAllOptions(this.state.currentPage)
    }

    prevPage(){
        this.state.currentPage = this.state.currentPage - 1;
        this.getAllOptions(this.state.currentPage)
    }

    async goBack(){

        if (this.state.view_type !== 'form') {
            this.action.doAction({
                type: 'ir.actions.client',
                tag: 'owl.plans',  // The tag defined for your OWL component
                'target': 'main',
                name: this.state.isMasterPlan ?  "Master Plans": "Plans",
                context: {},
                params: {
                    menu_id: this.state.menu_id, // Ensure this value is defined
                },// Optional context
            });
        } else {
            this.action.doAction({
                type: "ir.actions.act_window",
                target: 'current',
                context: {},
                name:  this.state.isMasterPlan ? "Master Plans" : "Plans",
                res_model: "product.template",
                'target': 'main',
                views: [[false, "form"]],
                res_id: this.state.homeplan_id,
            });
        }
    }
    async getOptionValueParams(child, option){
    this.state.inherited_name = child.inherited_name;
    this.state.price_type = option.price_type;
        this.state.editOptionValue = {
            name: child.is_override ? child.name : '',
            description: child.description || null,
            type: 'option_value'
        }
        if (this.state.isCommunity){
            this.state.editOptionValue = {
                ...this.state.editOptionValue,
                name: child.is_override ? child.name : '',
                price: child.price,
                homeplan_option_id: child.homeplan_option_id,
                community_homeplan_id: this.state.homeplan_id
            }
        }
        else if (this.state.isHomePlan){
            this.state.editOptionValue = {
                ...this.state.editOptionValue,
                name: child.is_override ? child.name : '',
                price: child.price,
                master_plan_option_id: child.master_plan_option_id
            }
        }
        else {
        this.state.quantity = child.quantity;
            this.state.editOptionValue = {
                ...this.state.editOptionValue,
                name: child.is_override ? child.name : '',
                master_plan_option_id: child.master_plan_option_id
            }
        }
    }


    async editOptionValues(){
        this.state.inherited_name = '';
        let notification = this.env.services.notification
        const state = JSON.parse(JSON.stringify(this.state))
        const form_data = new FormData();
        if (state.isHomePlan) {
            form_data.append("name", this.state.editOptionValue.name);
            form_data.append("description", this.state.editOptionValue.description);
            form_data.append("type", "option_value");
            form_data.append("master_plan_option_id", this.state.editOptionValue.master_plan_option_id);
            form_data.append("price", Number(this.state.editOptionValue.price));
            form_data.append("image", this.state.editOptionValue.image);
            if(this.state.option_type === 'quantity'){
            form_data.append("quantity", this.state.quantity === '-' ? 0 : this.state.quantity);
            }
        }
        else {
            form_data.append("name", this.state.editOptionValue.name);
            form_data.append("description", this.state.editOptionValue.description);
            if (state.isMasterPlan) {
                form_data.append("master_plan_option_id", this.state.editOptionValue.master_plan_option_id);
                form_data.append("quantity", Number(this.state.quantity));
            } else {
                form_data.append("homeplan_option_id", this.state.editOptionValue.homeplan_option_id);
                form_data.append("price", Number(this.state.editOptionValue.price));
                form_data.append('community_homeplan_id', this.state.editOptionValue.community_homeplan_id)
                if(this.state.option_type === 'quantity'){
                    form_data.append("quantity", this.state.quantity === '-' ? 0 : this.state.quantity);
                }
            }
            form_data.append("type", "option_value");
//            if (this.state.editOptionValue.quantity && state.isMasterPlan) {
//            }
            form_data.append("image", this.state.editOptionValue.image);
        }

        const options = {
            method: 'POST',
            headers: {
//            cookie: 'frontend_lang=en_US',
            mimeType: "multipart/form-data",
//            Accept: 'application/json'
            },
            body: form_data
        };
        const response = state.isHomePlan ? await fetch('/home_plan/option_override', options)
                            : state.isCommunity ? await fetch('/community/home_plan/option_override', options)
                            : await fetch('/master_plan/option_value_override', options)
        const data = await response.json()
        if(data.data === 'Record saved'){
            let close = notification.add("Record saved.", {
                title: "Success",
                type: "info", //info, warning, danger, success
                sticky: true,
                className: "p-4"
            })
            setTimeout(close, 1000);
            this.state.quantity = 0;
            this.getAllOptions(1)
        }
    }
    async getMenuDetails(menuId) {
          try {
            const menu = await this.orm.searchRead(
                "ir.ui.menu",
                [
                    ["id", "=", menuId]
                ],
                ['name']
            );
            if (menu.length > 0)
                return menu[0].name

            return false
          } catch (error) {
            console.error("Error fetching menu details:", error);
            return false
          }
      }

    async getAllOptionValues(option_categories_id, option_classes_id, optionId){
        const categoryId =JSON.parse(JSON.stringify(option_categories_id))
        const classId = option_classes_id ? JSON.parse(JSON.stringify(option_classes_id)) : undefined
        this.state.selectedParentOption = optionId
        const response = await fetch('/option_values/categories/'+ categoryId?.[0] + '/classes/' + classId?.[0], {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        });
        const data = await response.json()
        const optionSet = JSON.parse(JSON.stringify(this.state.optionSet))
        this.state.createOptionValues = [{id: 0, name: 'Select option value'},
        ...(data?.data === 'not found' || data?.data === 'Not found' ? []
            : data?.map(d=> {
               const optionValue = (optionSet.find(op=> {
                    return op?.id === optionId
                }))
                let isOptionValueSelected = null
                if(optionValue.children){
                   isOptionValueSelected = optionValue.children.find(child=>{
                        return child?.id === d?.id
                    })
                }
                if(!isOptionValueSelected){
                    return { ...d, is_active: true}
                }
            }).filter((option)=> option)
        )];
    }
     async getAllOptionsForModal(){
        const response = await fetch('/options'+'?homeplan_id='+this.state.homeplan_id, {
                method: 'GET',
                    headers: { 'Content-Type': 'application/json' },
            });
            const data = await response.json();
            this.state.createOptions = [{id: 0, name: 'Select option'},...(data?.data === 'Not found' ? []
            : data?.map(d=> {
                    return { ...d,is_active: true }
               }))];
    }
    addTask(){
        this.resetForm()
        const state =  JSON.parse(JSON.stringify(this.state))
        if (this.state.selectedOption > 0) {
            this.state.optionSet.unshift(state.createOptions.find((op)=>op.id === parseInt(state.selectedOption)))
        }
        this.state.selectedOption = 0
    }
    addOptionValue(){
        this.resetForm()
        const state =  JSON.parse(JSON.stringify(this.state))
        this.state.optionSet = state.optionSet.map((option)=> {
            if(state.selectedOption>0){
                const optionValue = state.createOptionValues.find((ov)=> ov.id ===parseInt(state.selectedOption))
                if(this.state.selectedParentOption === option.id && (option.option_categories_id[0] === optionValue.option_categories_id[0] || option.option_classes_id[0] === optionValue.option_classes_id[0])){
                    if(option.children  && option.children.length){
                        option.children.unshift({...optionValue, quantity: this.state.quantity, unit_type: this.state.unit_type})
                    } else {
                        option.children = [{...optionValue, quantity: this.state.quantity, unit_type: this.state.unit_type}]
                    }
                }
            }
            return option
        })
        this.state.selectedOption = 0
        this.state.quantity = 0
        this.state.unit_type = 0
    }
    editTask(task){
        this.state.activeId = task.id
        this.state.isEdit = true
        this.state.task = {...task}
    }

    getPages(){
    let pageStart = 1;
    let pageEnd = Math.min(this.state.currentPage * this.state.itemsPerPage, this.state.totalRecords)
    return `${pageStart}-${pageEnd} / ${this.state.totalRecords}`
    }

    async saveOptionSet(){
        const state = JSON.parse(JSON.stringify(this.state))
        let requestBody = []
        let notification = this.env.services.notification
        if (this.state.isMasterPlan){
            let undefinedExists = state.optionSet.filter(option=> {
            if(option.option_type !== 'binary'){
            return option.children === undefined
            }
            })
            if(undefinedExists.length > 0){
                   let close = notification.add("Option must contain atleast one option value.", {
                        title: "Error",
                        type: "danger", //info, warning, danger, success
                        sticky: false,
                        className: "p-4"
                    })
                    setTimeout(close, 1000);
            } else {

//                requestBody = state.optionSet.filter(option => option.children !== undefined).map((option)=> {
                requestBody = state.optionSet.map((option)=> {
                    return {
                        option_id: option.id,
                        name: option.name,
                        id: option.primaryId,
                        is_active: option.is_active,
                        homeplan_id: this.props.action.context.active_id,
                        option_values: option.children ? option.children.map((child)=> ({
                            option_value_id: child.id,
                            name: child.name,
                            quantity: child.quantity,
                            is_active: child.is_active,
                            master_plan_option_id: child.master_plan_option_id
                        })) : []
                    }
                })
                    if(requestBody.length > 0){
                    let filterParams = ''
                    const class_id = -1
                    const location_id = -1
                    const category_id = -1
                    if (this.state.selectedClass> 0){
                        filterParams = filterParams + '&class_id=' + this.state.selectedClass
                    } if(this.state.selectedLocation > 0){
                        filterParams = filterParams + '&location_id=' +  this.state.selectedLocation
                    } if(this.state.selectedCategory > 0) {
                        filterParams = filterParams + '&category_id=' +  this.state.selectedCategory
                    }
                    const response = await fetch('/master_plan/options', {
                        method: 'POST',
                        body: JSON.stringify(requestBody),
                        headers: { 'Content-Type': 'application/json' },
                    });
                    const data = await response.json()
                    if (data.data === 'Record created'){
                            let close = notification.add("Record saved.", {
                                title: "Success",
                                type: "info", //info, warning, danger, success
                                sticky: false,
                                className: "p-4"
                            })
                            setTimeout(close, 1000);

                            const res = await fetch('/master_plan/'+this.state.homeplan_id+'/options?page_no='+this.state.currentPage+filterParams, {
                                method: 'GET',
                                headers: { 'Content-Type': 'application/json' },
                            });
                            let optionSet = await res.json()
                            let selectedOptions = []
                            if(optionSet.data === 'Not found'){
                                this.state.optionSet = []
                            } else {
                                this.settingPaginationStates(optionSet?.pagination)
                                this.state.optionSet = optionSet?.data?.map((option)=> {
                                const children = option.option_values?.map((child)=> {
                                    let selectedOpt = false
                                    if (selectedOptions?.data !== 'Not found'){
                                     selectedOpt = selectedOptions?.data?.find((ov)=> ov?.master_plan_option_id === child?.master_plan_option_id)
                                     }
                                    return {
                                        id: child.option_value_id,
                                        name: child.name,
                                        is_base: child.is_base,
                                        option_set_id: !child.option_set_id ? '' : child.option_set_id,
                                        option_classes_id: child.option_classes_id,
                                        option_categories_id: child.option_categories_id,
                                        master_plan_option_id: child.master_plan_option_id,
                                        price: child.price,
                                        image: child.image,
                                        quantity: !child.quantity ? '-' : child.quantity,
                                        inherited_name: child.inherited_name,
                                        homeplan_option_id: child.homeplan_option_id,
                                        is_override: child.is_override,
                                        is_active: this.state.isMasterPlan || !selectedOpt ? child?.is_active : selectedOpt?.is_active
                                    }
                                })
                                return {
                                    id: option.option_id,
                                    recordId: option.id,
                                    homeplan_id: option.homeplan_id,
                                    is_override: option.is_override,
                                    primaryId: option.id,
                                    name: option.name,
                                    inherited_name: option.inherited_name,
                                    option_type: option.option_type,
                                    price: option.price > 0 ? option.price : undefined,
                                    price_type: option.price_type,
                                    unit_type: !option.units ? '-' : option.units,
                                    option_categories_id: option.option_categories_id,
                                    option_classes_id: option.option_classes_id,
                                    is_active: children?.some((child)=> child.is_active),
                                    children
                                }})
                            }
                        }
                }
            }
        }
        else if(this.state.isHomePlan) {
            state.optionSet.map((option)=> option.children.map((child)=> {
                    requestBody.push({
                        master_plan_option_id: child.master_plan_option_id,
                        homeplan_id: this.props.action.context.active_id,
                        is_active: child.is_active,
                        is_base: child?.is_base,
                    })
                })
            )
            if(requestBody.length > 0){
                const options = {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                    Accept: 'application/json'
                  },
                  body:  JSON.stringify(requestBody), //'[{"homeplan_id":15,"master_plan_option_id":155,"is_active":true}]'
                };
                const response = await fetch('/home_plan/options', options)

                const data = await response.json()
                if(data.data === 'Success'){
                    let close = notification.add("Record saved.", {
                        title: "Success",
                        type: "info", //info, warning, danger, success
                        sticky: true,
                        className: "p-4"
                    })
                    setTimeout(close, 1000);

                    this.getAllOptions(1);
                }
            }
        }
        else if(this.state.isCommunity) {
            state.optionSet.map((option)=> option.children.map((child)=> {
                    requestBody.push({
                        homeplan_option_id: child.homeplan_option_id,
                        community_homeplan_id: this.props.action.context.active_id,
                        is_active: child.is_active,
                    })
                })
            )
            if(requestBody.length > 0){
                const options = {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                    Accept: 'application/json'
                  },
                  body:  JSON.stringify(requestBody),
                };
                const response = await fetch('/community/home_plan/options', options)

                const data = await response.json()
                if(data.data === 'Success'){
                    let close = notification.add("Record saved.", {
                        title: "Success",
                        type: "info", //info, warning, danger, success
                        sticky: true,
                        className: "p-4"
                    })
                    setTimeout(close, 1000);
                    this.getAllOptions(1);
                }
            }
        }
    }

    resetForm(){
        this.state.task = {name:"", color:"#FF0000", completed:false}
    }

    toggleParentAndChildren(parentTask) {
        parentTask.is_active = !parentTask.is_active;
       parentTask.children?.length && parentTask.children.forEach(child => {
            child.is_active = parentTask.is_active;
        });
    }

    toggleChildAndParent(childTask, parentTask) {
        childTask.is_active = !childTask.is_active;
        const allChildrenChecked = parentTask.children.every(child => child.is_active);
        const anyChildChecked = parentTask.children.some(child => child.is_active);
        parentTask.is_active = anyChildChecked || allChildrenChecked;
    }

    changeOptionNameHandler(e) {
        this.state.editOptionName.name = e.target.value
    }

    changeOptionPriceHandler(e) {
        this.state.editOptionName.price = e.target.value
    }

    async overrideOptionName() {
        this.state.inherited_name = "";
        const { option_id, homeplan_id, name, master_plan_option_id, price } = this.state.editOptionName
        const requestBody = this.state.isMasterPlan ?
        { option_id, name, homeplan_id: this.state.homeplan_id }
        : this.state.isCommunity ?
        {
          homeplan_option_id:master_plan_option_id,
          community_homeplan_id: this.state.homeplan_id,
          price: Number(price),
          name,
          type:"option"
         }
        : { master_plan_option_id, name, type: 'option', price: Number(price)};
        let notification = this.env.services.notification
        if(requestBody){
            const response = await fetch(
            this.state.isMasterPlan ? '/master_plan/option_override'
            : this.state.isCommunity ?'/community/home_plan/option_override'
            : this.state.isHomePlan ? '/home_plan/option_override' : '/', {
                method: 'POST',
                body: JSON.stringify(requestBody),
                headers: { 'Content-Type': 'application/json' },
            });
            const data = await response.json()
            if (data.data === 'Record saved'){
                let close = notification.add("Record saved.", {
                    title: "Success",
                    type: "info", //info, warning, danger, success
                    sticky: false,
                    className: "p-4"
                })
                setTimeout(close, 1000);
                this.getAllOptions(1)
            }
        }
    }
    async setAsBase(id, home_plan_option_id){
        const requestBody = this.state.isCommunity ? {community_homeplan_id: this.state.homeplan_id, homeplan_option_id: home_plan_option_id}
        : {master_plan_option_id: id, is_base: true, ...(this.state.isHomePlan && {
        homeplan_id: this.state.homeplan_id
        })};
                let notification = this.env.services.notification
                if(requestBody){
                    const response = await fetch(this.state.isMasterPlan ?
                    '/master_plan/option_value_set_base': this.state.isHomePlan ? '/home_plan/option_value_set_base' : '/community/home_plan/option_value_set_base' , {
                        method: 'POST',
                        body: JSON.stringify(requestBody),
                        headers: { 'Content-Type': 'application/json' },
                    });
                    const data = await response.json()
                    if (data.data === 'Record updated'){
                            let close = notification.add("Record saved.", {
                                title: "Success",
                                type: "info", //info, warning, danger, success
                                sticky: false,
                                className: "p-4"
                            })
                            setTimeout(close, 1000);
                            this.getAllOptions(1)
                        }
                }
    }
    setPriceType(id) {
        const optionValues = JSON.parse(JSON.stringify(this.state.createOptionValues))
        const selectedOptionValue = optionValues.find((optionValue, index) => Number(optionValue.id) === Number(id));
        this.state.quantity = 0;
        this.state.unit_type = !selectedOptionValue.units ? '-' : selectedOptionValue.units;
        this.state.price_type = selectedOptionValue?.price_type;
    }

}

MasterPlanOptions.template = 'owl.MasterPlanOptions'
registry.category('actions').add('owl.master_plan_options', MasterPlanOptions);