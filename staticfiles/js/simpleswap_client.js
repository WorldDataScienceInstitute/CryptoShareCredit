class SimpleSwapClient {
    constructor(){
        this.url = "/atm/SimpleSwapAPI/";
        this.csrfmiddlewaretoken = getCookie('csrftoken');
        this.currencyData = {};

        this.hasExtraData = false;
        this.extraPattern = "";
        this.extraData = "";
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
    };

    getEstimatedExchangeAmount(currency_from, currency_to, amount) {
        return new Promise(function(resolve,reject){
            var endpoint = "?type=ESTIMATED_EXCHANGE_AMOUNT";
            var data = {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                currency_from: currency_from,
                currency_to: currency_to,
                amount: amount    
            };
            $.ajax({
                type: "POST",
                url: "/atm/SimpleSwapAPI/" + endpoint,
                data: data,
                success: function(response){
                    resolve(response);
                },
                error: function(response){
                    reject(response);
                }
            });
        });
    };

    getMinimalExchangeAmount(currency_from, currency_to) {
        return new Promise(function(resolve,reject){
            var endpoint = "?type=MINIMAL_EXCHANGE_AMOUNT";
            var data = {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                currency_from: currency_from,
                currency_to: currency_to,
            };
            $.ajax({
                type: "POST",
                url: "/atm/SimpleSwapAPI/" + endpoint,
                data: data,
                success: function(response){
                    resolve(response);
                },
                error: function(response){
                    reject(response);
                }
            });
        });
    };








    changeGetOptions(symbol) {
        this.getExchangePairsForCurrency(symbol).then(
            function(response) {
                var element = document.getElementById("getOptions");
                var options = "";
                Object.keys(response).forEach(function(key) {
                    options += "<option value='" + key + "'>" + response[key] + "</option>";
                })
                element.innerHTML = options;
            }
        );  
    };

    changeMinimumAmount(currency_from, currency_to) {
        this.getMinimalExchangeAmount(currency_from, currency_to).then(
            function(response) {
                var element = document.getElementById("exchangeLimits");
                var inputElement = document.getElementById("sendingAmount");

                var currencyData = response.currency_data;

                simpleSwapClient.currencyData = currencyData;
                if (currencyData.has_extra_id){
                    simpleSwapClient.hasExtraData = true;
                    simpleSwapClient.extraData = currencyData.extra_id;
                    simpleSwapClient.extraPattern = currencyData.validation_extra;
                }else{
                    simpleSwapClient.hasExtraData = false;
                }
                
                

                response = response.minimal_exchange_amount;
                if (!response.max){
                    response.max = "No limit";
                }else{
                    response.max =  parseFloat(parseFloat(response.max).toFixed(5));
                   
                    inputElement.setAttribute("max", response.max);
                }
                response.min =  parseFloat(parseFloat(response.min).toFixed(5));
                var newLimits = "Min: "+ response.min + " Max: " + response.max;
                element.innerHTML = newLimits;
                inputElement.setAttribute("min", response.min);
                
                // .setAttribute("max",100);
            }
        );  
    };
    
    changeEstimatedExchangeAmount(currency_from, currency_to, amount) {
        this.getEstimatedExchangeAmount(currency_from, currency_to, amount).then(
            function(response) {
                var element = document.getElementById("approximateAmount");
                var newAmount = response;

                element.value = newAmount;
            }
        );  
    };

}


var simpleSwapClient = new SimpleSwapClient();