class SimpleSwapClient {
    constructor(){
        this.url = "/atm/SimpleSwapAPI/";
        this.csrfmiddlewaretoken = getCookie('csrftoken')
    }

    getExchangePairsForCurrency(symbol){
        return new Promise(function(resolve,reject){
            var endpoint = "?type=CURRENCY_EXCHANGE_PAIRS";
            var data = {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                symbol: symbol
    
            };
            $.ajax({
                type: "POST",
                url: "/atm/SimpleSwapAPI/" + endpoint,
                data: data,
                success: function(response){
                   resolve(response);
                    // changeGetOptions(document.getElementById("getOptions"), response);
                    // console.log(response);
                },
                error: function(response){
                    reject(response);
                }
            });
        });
    }

    changeGetOptions(symbol) {
        this.getExchangePairsForCurrency(symbol).then(
            function(json) {
                var element = document.getElementById("getOptions");
                var options = "";
                Object.keys(json).forEach(function(key) {
                    options += "<option value='" + key + "'>" + json[key] + "</option>";
                })
                element.innerHTML = options;
            }
        );
        // json = await simpleSwapClient.getExchangePairsForCurrency(symbol);
    
    }
}


var simpleSwapClient = new SimpleSwapClient();