/** @odoo-module */

import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
const { Component, useRef, onWillStart, onMounted } = owl

export class Charts extends Component {
    setup(){
        this.chartRef = useRef("chartCanvas");

        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")
        })

        onMounted(()=> this.renderChart())
    }
    renderChart(){

            const data = [
                { year: 2010, count: 10 },
                { year: 2011, count: 20 },
                { year: 2012, count: 15 },
                { year: 2013, count: 25 },
                { year: 2014, count: 22 },
                { year: 2015, count: 30 },
                { year: 2016, count: 28 },
              ];

            new Chart(this.chartRef.el,
                {
                  type: this.props.type,
                  data: {
                    labels: data.map(row => row.year),
                    datasets: [
                      {
                        label: this.props.title,
                        data: data.map(row => row.count)
                      }
                    ]
                  },
                  options: {
                    responsive:true,
                    plugins:{
                        legend: {
                            display: true,
                            position: "bottom"
                        },
                        title: {
                            display: true,
                            text:"test chart",
                            position:"bottom"
                        }
                    }
                  }
                }
              );
        }


}

Charts.template = "owl.Charts"