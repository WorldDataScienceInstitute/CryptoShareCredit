function SetMaxAmount(getField, setField){
    var currency = document.getElementById(getField).value.split(' ')[0];
    var rate = document.getElementById(currency+"_exchangeRate").innerHTML;
    var maxAmount = 1*1000/rate
    var minAmount = 1*150/rate

    document.getElementById(setField).value = "";

    document.getElementById(setField).max = parseFloat(maxAmount).toFixed(4);
    document.getElementById(setField).min = parseFloat(minAmount).toFixed(4);
    document.getElementById(setField).placeholder = "Enter the amount you want to borrow || Min: " + minAmount.toFixed(4) +" Max: " + maxAmount.toFixed(4);
    document.getElementById(setField).removeAttribute("readonly");
}

function ActivateAmountField(setField){
    document.getElementById(setField).removeAttribute("readonly");
}

function SetCollateral(getAmountField, getPaymentCurrency, getCollateralCurrency, setCollateralField){
    var currency = document.getElementById(getPaymentCurrency).value.split(' ')[0];
    var currencyCollateral = document.getElementById(getCollateralCurrency).value.split(' ')[0];

    if(currency != "NotSelected"){
        var currencyRate = 1;
        // var currencyRate = document.getElementById(currency+"_exchangeRate").innerHTML;
        var currencyCollateralRate = document.getElementById(currencyCollateral+"_exchangeRate").innerHTML;

        var loan_amount = document.getElementById(getAmountField).value;

        var currencyLoanExchange = loan_amount * currencyRate;

        var collateral = currencyLoanExchange / currencyCollateralRate * 1.2;
    
        document.getElementById(setCollateralField).value = parseFloat(collateral).toFixed(4);
    }

    
}


function test_js(){

    alert("test");
}