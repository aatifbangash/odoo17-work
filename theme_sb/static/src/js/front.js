/** @odoo-module **/

(function () {
  $(document).ready(function() {
    // Check if the explore-cities-main-container element exists
    if ($('#explore-cities-main-container').length > 0) {
      // Execute the AJAX request only if the element exists
      $.ajax({
        url: 'https://abdul.schellbrothersheartbeat-develop.com/?engine=data-warehouse&opt=schedule-run-dev&script=logged-in-info-test.php&q=community',
        method: 'GET',
        success: function(response) {
          var html = "<div class='row'>";
          if(response.length > 0) {
            response.map(community => {
              html += `<div class="col-lg-3 mt-3 mb-3">
                          <div class="d-flex align-items-center">
                              <div class="img-container mr-3 rounded">
                                  <img class="country-image rounded"
                                       src="/theme_sb/static/src/img/city1.png"/>
                              </div>
                              <div>
                                  <h5 class="mb-0">${community.name}</h5>
                              </div>
                          </div>
                      </div>`
            })
          }
          html += "</div>";
          $('#explore-cities-main-container').html(html)
        },
        error: function(xhr, status, error) {
          console.error(error);
        }
      });
    }
  });
})();

//import { registry } from "@web/core/registry";
//
//const myService = {
//    dependencies: ["notification"],
//    start(env, { notification }) {
//        let counter = 1;
//        setInterval(() => {
////            notification.add(`Tick Tock ${counter++}`);
//        }, 1000);
//    }
//};
//
//registry.category("services").add("myService", myService);
