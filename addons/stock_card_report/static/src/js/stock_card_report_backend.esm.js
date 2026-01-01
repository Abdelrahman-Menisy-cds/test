/** @odoo-module **/

import { Component, onWillStart, onMounted, useState, useRef, xml } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

/**
 * @cds-module
 */

class ReportWidget extends Component {
    static template = xml`<div class="o_content" t-ref="content"/>`;
    static props = ["context"];

    setup() {
        this.contentRef = useRef("content");
    }

    updateContent(html) {
        if (this.contentRef.el) {
            this.contentRef.el.innerHTML = html;
        }
    }
}

export class StockCardReportBackend extends Component {
    static template = xml`
        <div class="o_stock_card_report_page">
            <div class="o_stock_reports_page_container overflow-auto" style="height: calc(100vh - 150px);">
                <div class="o_content" t-ref="content"/>
            </div>
        </div>
    `;
    static props = ["*"];
    static components = { ReportWidget };

    setup() {
        this.actionService = useService("action");
        this.orm = useService("orm");
        this.contentRef = useRef("content");
        this.state = useState({
            html: "",
            loaded: false
        });

        this.given_context = {};
        this.odoo_context = this.props.action.context || {};
        this.controller_url = this.odoo_context.url;

        if (this.odoo_context.context) {
            this.given_context = this.odoo_context.context;
        }

        this.given_context.active_id = this.odoo_context.active_id || this.props.action.params?.active_id;
        this.given_context.model = this.odoo_context.active_model || false;
        this.given_context.ttype = this.odoo_context.ttype || false;

        onWillStart(async () => {
            await this.getHtml();
        });

        onMounted(() => {
            this.setHtml();
        });
    }

    setHtml() {
        if (this.contentRef.el && this.state.html) {
            this.contentRef.el.innerHTML = this.state.html;
            
            // Add event listeners to the existing buttons
            const printButton = this.contentRef.el.querySelector('.o_stock_card_reports_print');
            if (printButton) {
                printButton.addEventListener('click', this.print.bind(this));
            }
            
            const exportButton = this.contentRef.el.querySelector('.o_stock_card_reports_export');
            if (exportButton) {
                exportButton.addEventListener('click', this.export.bind(this));
            }
        }
    }

    async getHtml() {
        const result = await this.orm.call(
            this.given_context.model,
            "get_html",
            [this.given_context],
            { context: this.odoo_context },
        );

        this.state.html = result.html;
        this.state.loaded = true;
    }

    async print() {
        const result = await this.orm.call(
             this.given_context.model,
            "print_report",
            [this.given_context.active_id, "qweb-pdf"],
            {context: this.odoo_context},
        );

        this.actionService.doAction(result);
    }

    async export() {
        const result = await this.orm.call(
            this.given_context.model,
            "print_report",
            [this.given_context.active_id, "xlsx"],
            {context: this.odoo_context},
        );

        this.actionService.doAction(result);
    }
}

registry.category("actions").add("stock_card_report_backend", StockCardReportBackend);
