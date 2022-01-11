function SetMaxAmount(getField, setField){
    var maxAmount = document.getElementById(getField).value.split(' ')[1];
    document.getElementById(setField).max = parseFloat(maxAmount);
    document.getElementById(setField).removeAttribute("readonly");
}

function SetCollateral(getAmountField, getCollateralCurrency, setCollateralField){
    var currency = document.getElementById(getCollateralCurrency).value.split(' ')[1];
    var currencyExchangeRate = document.getElementById(currency+"_exchangeRate").innerHTML;
    var loan_amount = document.getElementById(getAmountField).value;

    var collateral = (loan_amount / parseFloat(currencyExchangeRate))*1.2;

    document.getElementById(setCollateralField).value = collateral.toFixed(4);
    
}


function test_js(){

    alert("test");
}