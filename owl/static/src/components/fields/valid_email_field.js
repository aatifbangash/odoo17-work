/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { useInputField } from "@web/views/fields/input_field_hook";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { browser } from "@web/core/browser/browser";
import { Component, useRef, useEffect, useState, onWillStart, EventBus, useSubEnv } from "@odoo/owl";

export class ValidEmailField extends Component {
    static template = "owl.ValidEmailField";
    static props = {
        ...standardFieldProps,
        placeholder: { type: String, optional: true },
    };

    setup() {
        console.log(this.env.model)
        this.state = useState({
            name: "Name from State"
        });

        this.textareaRef = useRef("textarea");
        useSubEnv({
            overviewBus: new EventBus(),
        });
        onWillStart(async () => {
//            console.log(this.props.action.context)
//            await this.getWarehouses();
//            await this.initBomData();
        });
        useEffect(
            () => {
                console.log('changed')
//                if (inputEl) {
//                    inputEl.addEventListener("input", this.onInput.bind(this));
//                    return () => {
//                        inputEl.removeEventListener("input", this.onInput.bind(this));
//                    };
//                }
            },
            () => [this.textareaRef.el.value]
        );
//        console.log(this.props.record.data[this.props.name].records[0])
//        console.log(this.props.record)
//        console.log(this.props.name)
//        console.log(this.props.record.data['community_homeplans_ids'].records[0].data['homeplan_id'][1])
//        console.log(this.props.record.data['community_homeplans_ids'])
//        console.log(this.props.record.fields['community_homeplans_ids'].type)
//        console.log(this.props.record.fields['community_homeplans_ids'].viewMode)
//        console.log(this.props.record.fields['community_homeplans_ids'].relation)
//        console.log(this.props.record.fields['community_homeplans_ids'])
//        console.log(this.props.record.data[this.props.name])
//        console.log(this.props.record.data)
//        useInputField({ getValue: () => this.props.record.data[this.props.name] || "From Owl" });
        useInputField({
            getValue: () => this.props.record.data[this.props.name] || "",
            refName: "textarea",
//            preventLineBreaks: !this.props.lineBreaks,
        });
    }

    update_textarea(){
        console.log('hsaaaa')
        this.textareaRef.el.value = 'here'
        browser.localStorage.setItem('l_storage', 'l_storage_value_from_owl');
    }
    onChange(newValue) {
        console.log(newValue)
    }
}

export const ValidEmailFieldObject = {
    component: ValidEmailField,
    displayName: "Custom Field",

    supportedTypes: ["text"],
    extractProps: ({ attrs, options }) => ({
        placeholder: attrs.placeholder,
        myCustomData: options.any_custom_data
    }),
};

registry.category("fields").add("valid_email", ValidEmailFieldObject);
