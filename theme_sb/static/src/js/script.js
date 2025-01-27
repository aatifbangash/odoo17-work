/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';
import { session } from "@web/session";

publicWidget.registry.YhCities = publicWidget.Widget.extend({
    selector: '.explore-cities',
    init(parent, options) {
        this._super(parent, options);
//        this._rpc = this.bindService("rpc");
//        this.notification = this.bindService("notification");
//        this.orm = this.bindService("orm");
    },
//    willStart: async function () {
//            this.preFillValues = {};
//            if (session.user_id) {
//                this.preFillValues = (await this.orm.read(
//                    "res.users",
//                    [session.user_id],
////                    ['name', 'phone', 'email', 'commercial_company_name']
//                ))[0] || {};
//            }
//        },
    start() {
        let citiesRow = this.el.querySelector('#yh-cities-row')

        if (citiesRow){
//        console.log(session)
//        console.log(this.preFillValues)


            citiesRow.innerHTML = "<ul>"
            fetch('https://abdul.schellbrothersheartbeat-develop.com/?engine=data-warehouse&opt=schedule-run-dev&script=logged-in-info-test.php&q=community')
              .then(response => response.json())
              .then(communities => {
                    communities.map(community => {
                        let li = document.createElement('li');
                        li.textContent = community.name;
                        citiesRow.appendChild(li);
                    })
              })
              .catch(error => console.error('Error fetching data:', error));
            citiesRow.innerHTML += "</ul>"
//              this.notification.add(
//                            'herrr',
//                            { type: 'warning', sticky: true }
//                        )
//            this._rpc({
//                route: '/cities/',
//                params:{}
//            }).then(data=>{
//                let html = ``
//                data.forEach(city=>{
//                    html += `<div class="col-lg-3 mb-5">
//                        <div class="d-flex align-items-center">
//                            <div class="img-container mr-3 rounded">
//                                <img class="country-image rounded" src="data:image/png;base64,${city.image}"/>
//                            </div>
//                            <div>
//                                <h5 class="mb-0">${city.state_id ? city.state_id[1] : ''}</h5>
//                                <div>${city.country_id ? city.country_id[1] : ''}</div>
//                            </div>
//                        </div>
//                    </div>`
//                })
//                citiesRow.innerHTML = html
//            })
        }
    },
});

export default publicWidget.registry.YhCities;