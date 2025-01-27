/** @odoo-module */

import publicWidget from '@web/legacy/js/public/public_widget';
import {renderToElement} from "@web/core/utils/render";
import {jsonrpc} from "@web/core/network/rpc_service";


publicWidget.registry.bista_web_form = publicWidget.Widget.extend({
    selector: '.bista_web_form',
    init() {
        this._super(...arguments);
        this.rpc = this.bindService("rpc");
        this.orm = this.bindService("orm");
        this.numSection = 0;
        this.record = {}
    },


    willStart: async function () {
        this.el = $(this.el)
        this.root = this.el.find(".contact_form")
        this.footer = this.el.find('.form_footer')
        this.form_ref = this.el.attr('form_id')
        this.form_data = await jsonrpc('/web/get_form_data', {'ref': this.form_ref})
        this.params = this.getUrlParams()
        this.render()
    },


    render() {
        this.renderHeader()
        this.renderContent()
        this.renderConfirmationMessage()
    },

    renderConfirmationMessage() {
        if (this.form_data.post_action === 'confirmation' && this.form_data.confirmation_message) {
            this.confirmation_message = this.el.find(".confirmation_message")
            this.confirmation_message.html(this.form_data.confirmation_message)
        } else if (this.form_data.redirect_url) {
            window.location = this.form_data.redirect_url
        }
    },

    getUrlParams() {
        let params = {};
        let searchParams = new URLSearchParams(window.location.search);

        searchParams.forEach(function (value, key) {
            params[key] = value;
        });

        return params;
    },

    renderContent() {
        this.content = this.el.find('.form_content')
        this.section_list = {}
        let self = this;


        for (let section in this.form_data.sections) {
            this.numSection += 1
            let fields = this.form_data.sections[section].fields
            fields = Object.keys(fields)
                .map(key => fields[key])  // Convert the fields object to an array
                .sort((a, b) => a.sequence - b.sequence)

            let section_el = renderToElement('bista_web_form.section', {'section': section, 'index': this.numSection})
            section_el = $(section_el)
            section_el.attr("id", this.numSection)

            let section_content = section_el.find(".section_content")
            this.content.append(section_el)
            for (let field in fields) {
                field = fields[field]

                let value = this.params[field.field_description]
                if (field.value_source === 'param' && value) {
                    this.record[field.field_description] = value
                }

                let ttype = field.field_type
                let field_el = false
                let field_ref = false
                if (["many2one", "selection"].includes(ttype)) {
                    field_ref = 'bista_web_form.field_selection'
                } else if (['char', 'integer', 'float'].includes(ttype)) {
                    field_ref = 'bista_web_form.field_basic'
                } else if (['text', 'html'].includes(ttype)) {
                    field_ref = 'bista_web_form.field_text'
                }

                field_el = renderToElement(field_ref, {field: field, record: this.record})
                if (field_el) {
                    section_content.append(field_el)
                }

            }

            section_el.on('submit', function (e) {
                e.preventDefault();
                e.stopPropagation();
                section_el.hide();
                let formData = $(this).serializeArray()
                formData.forEach(function (field) {
                    self.record[field.name] = field.value
                })
                let form_id = section_el.attr("id")
                self.updateFormState(form_id)
                if (parseInt(form_id) === self.numSection) {
                    self.saveRecord()
                }


            })

            section_el.find(".back_btn").on('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                section_el.hide();
                self.goBack(section_el.attr('id'))
            })
        }
        this.updateFormState('0')


    },

    async saveRecord() {
        let result = false;
        try {
            result = await jsonrpc('/web/set_form_data', {
                'ref': this.form_ref,
                'data': this.record
            })
            this.confirmation_message.html(this.form_data.confirmation_message)
        } catch (error) {
            this.confirmation_message.removeClass('d-none')
            this.confirmation_message.html(error)
        }
        console.log("Result ", result)
        if (result) {
            this.confirmation_message.removeClass('d-none')
        }
    },

    getSectionId(section_id) {
        try {
            return (parseInt(section_id))
        } catch (e) {
            alert("Invalid section id " + section_id)
        }
    },

    goBack(section) {
        let section_id = this.getSectionId(section)
        let prev_section_id = section_id - 1
        this.el.find("#" + prev_section_id).show()
    },

    updateFormState(section_id) {
        let next_section_id = this.getSectionId(section_id) + 1
        let next_section = this.el.find("#" + next_section_id)
        if (next_section) {
            next_section.show()
        }

        let action_btn_string = 'Submit'
        if (this.numSection > next_section_id) {
            action_btn_string = 'Next'
        }
        next_section.find(".submit_btn").html(action_btn_string)
        if (next_section_id > 1) {
            next_section.find(".back_btn").removeClass('d-none')
        }
    },

    renderHeader() {
        this.header = this.el.find('.form_header')
        this.title = this.header.find("h1")
        if (this.title) {
            this.title.html(this.form_data.name)
        }
    }

});
