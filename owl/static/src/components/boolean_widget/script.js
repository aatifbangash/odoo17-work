/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, useState } from "@odoo/owl";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { useRecordObserver } from "@web/model/relational_model/utils";

export class BooleanWidget extends Component {
    static template = "owl.BooleanWidget";
    static components = { CheckBox };
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.state = useState({});
        useRecordObserver((record) => {
            this.state.value = record.data[this.props.name];
        });
    }

    onChange(ev) {
        const newValue = ev.target.checked;
        this.state.value = newValue;
        this.props.record.update({ [this.props.name]: newValue });
    }
}

export const booleanWidget = {
    component: BooleanWidget,
    displayName: _t("Checkbox"),
    supportedTypes: ["boolean"],
    isEmpty: () => false,
};

registry.category("fields").add("boolean_widget", booleanWidget);
