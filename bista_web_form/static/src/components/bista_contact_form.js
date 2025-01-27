/** @odoo-module */

import publicWidget from '@web/legacy/js/public/public_widget';
import {renderToElement} from "@web/core/utils/render";
import {jsonrpc} from "@web/core/network/rpc_service";

publicWidget.registry.bista_contact_form = publicWidget.Widget.extend({
    selector: '.bista_contact_form',
    init() {
        this._super(...arguments);
        this.rpc = this.bindService("rpc");
        this.orm = this.bindService("orm");


        this.config_options = {
            config_email: {
                id: 'config_email',
                title: 'Send Me Email updates',
                icon: 'fa-paper-plane',
                description: 'I want to stay in the loop about all things Schell Brothers.'
            },
            config_help: {
                id: 'config_help',
                title: 'I Need Help Choosing',
                description: 'I like your homes and communities. I need help narrowing down choices.',
                icon: 'fa-map-marker',
            },
            config_contact: {
                id: 'config_contact',
                title: "I'am Ready to Talk!",
                description: 'I have my eye on a specific community and I am ready to talk about it.',
                icon: 'fa-comments'
            }
        }

        this.communities = {
            richmond_virginia: {
                id: 'richmond_virginia',
                title: 'Richmond, Virginia',
                icon: 'TN',
                count: 6,
            },
            boise_idaho: {
                id: 'boise_idaho',
                title: 'Boise, Idaho',
                count: 0,
                icon: 'ID'
            },
            delaware_beaches: {
                id: 'delaware_beaches',
                title: 'Delaware Beaches',
                count: 16,
                icon: "DE"
            },
            nashville_tennessee: {
                id: 'nashville_tennessee',
                title: 'Nashville, Tennessee',
                count: 8,
                icon: "TN"
            },
        }
    },


    async willStart() {
        let communities = await jsonrpc("/get/partners")
        if (communities) {
            this.communities = communities
        }

        this.el = $(this.el)
        this.contact_form = renderToElement('bista_web_form.contact_form_template', {form: this})
        this.root = $(".contact_form")
        this.root.append(this.contact_form)
        this.selected_config = false;
        this.selected_community = false;

        this.triggerBistaWebForm();
    },

    triggerBistaWebForm: function () {
            const BistaWebForm = publicWidget.registry.bista_web_form;
            const bistaWebFormInstance = new BistaWebForm();
            bistaWebFormInstance.attachTo($('.bista_web_form'));
        },
    async start() {
        await this._super(...arguments);
        let self = this;
        const callback = function (mutationsList, observer) {
            if ($('.option').length) {
                observer.disconnect();
                self.ready()
            }
        };
        const targetNode = document.body;
        const observer = new MutationObserver(callback);
        observer.observe(targetNode, {childList: true, subtree: true});
    },


    ready() {
        this.config_success = $("#config_success")
        this.config_container = $("#config_options")
        this.config_description = $("#config_description")
        this.community_section = $("#section_communities")
        this.community_success = $("#section_community_success")
        this.community_description = $("#community_description")
        this.bista_web_form = $("#bista_web_form")
        this.company_input = $('.form_content input[name="company_id"]')
        this.params = this.getUrlParams()
        this.contactBtn()
        this.cancelBtn()
    },


    toggleConfig(config_id) {
        if (typeof config_id === 'string') {
            let config = this.config_options[config_id]
            if (config) {
                this.config_description.html(config.title)
                this.selected_config = config_id
            }
        }

        if (this.config_container.hasClass('d-none')) {
            this.config_container.removeClass('d-none')
            this.config_success.addClass('d-none')
            this.community_section.addClass('d-none')
            this.bista_web_form.addClass('d-none')
        } else {
            this.config_container.addClass('d-none')
            this.config_success.removeClass('d-none')
            if (this.params['community_id'] || this.params['company_id']) {
                this.bista_web_form.removeClass('d-none')
            } else {
                this.community_section.removeClass('d-none')
            }
        }

    },

    toggleCommunities(community_id) {
        if (typeof community_id === 'string') {
            let community = this.communities[community_id]
            if (community) {
                this.selected_community = community_id;
                this.community_description.html(community.title)
                this.company_input.val(community_id)
            }
        }

        if (this.community_section.hasClass('d-none')) {
            this.community_section.removeClass('d-none')
            this.community_success.addClass('d-none')
            this.bista_web_form.addClass('d-none')
        } else {
            this.community_section.addClass('d-none')
            this.community_success.removeClass('d-none')
            this.bista_web_form.removeClass('d-none')
        }

    },


    getUrlParams() {
        let params = {};
        let searchParams = new URLSearchParams(window.location.search);

        searchParams.forEach(function (value, key) {
            params[key] = value;
        });

        this.constructTitle(params)

        return params;
    },


    constructTitle(params) {
    if (Object.keys(params).length > 0) {
        let entityType = null;
        let entityId = null;

        if ('community_id' in params) {
            entityType = 'community';
            entityId = params['community_id'];
        } else if ('company_id' in params) {
            entityType = 'company';
            entityId = params['company_id'];
        }

        if (entityType && entityId) {
            jsonrpc(`/get/${entityType}`, {[`${entityType}_id`]: entityId})
            .then((entity) => {
                const entityName = entity.name;
                this.config_container.find('.content strong:first').text((_, currentText) => {
                    return currentText + ` about ${entityName}`;
                });

                this.config_options['config_email']['title'] = `${this.config_options['config_email']['title']} about ${entityName}`;
            })
            .catch((error) => {
                console.log(error);
            });
        }
    }
},

    contactBtn() {
        let header = $("header")
        let self = this;
        header.find('a[href="/contactus"], a.im_interested').on('click', function (event) {
            event.preventDefault();
            if (self.root.hasClass("form_invisible")) {
                self.root.removeClass("form_invisible")
            } else {
                self.root.addClass("form_invisible")
            }

        });
    },

    cancelBtn() {
    const cancelButton = document.querySelector('.close-badge')
    const webForm = document.querySelector('.contact_form.bista_contact_form')
        cancelButton.addEventListener('click', function (event) {
            event.preventDefault();
            webForm.classList.add("form_invisible")

        });
    },


});
