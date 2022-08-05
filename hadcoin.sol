// ICO hadcoins

//versao
pragma solidity ^0.4.11;

contract hadcoin_ico {
    // numero maximo de coins disponiveis no ICO
    uint public max_hadcoins = 1000000;

    // cotacao do coin pro dólar
    // com 1 dolár, da pra comprar 1000 hadcoins
    uint public usd_to_hadcoin = 1000;

    //total de coins que foram compradas por investidores
    uint public total_hadcoins_bought = 0;

    //funcoes de equivalencia
    mapping(address => uint) equity_hadcoins;
    mapping(address => uint) equity_usd; // valor dos hadcoins em dolar

    //verificando se o investidor pode comprar hadcoins
    modifier can_buy_hadcoins(uint usd_invested){
        require (usd_invested * usd_to_hadcoin + total_hadcoins_bought <= max_hadcoins);
        _;
    }

    //retorna o valor do investimento em hacoins
    function equity_in_hadcoins(address investor) external constant returns(uint){
        return equity_hadcoins[investor];
    }

    // retorna o valor do investimento em dolares
    function equity_in_usd(address investor) external constant returns(uint){
        return equity_usd[investor];
    }

    //compra de hadcoins
    function buy_hadcoins(address investor, uint usd_invested) external
    can_buy_hadcoins(usd_invested) {
        uint hadcoins_bought = usd_invested * usd_to_hadcoin;
        equity_hadcoins[investor] += hadcoins_bought;
        equity_usd[investor] = equity_hadcoins[investor] / 1000;
        total_hadcoins_bought += hadcoins_bought;
    }

    //venda de hadcoins
    function sell_hadcoins(address investor, uint hadcoins_sold) external {
        equity_hadcoins[investor] -= hadcoins_sold;
        equity_usd[investor] = equity_hadcoins[investor] / 1000;
        total_hadcoins_bought -= hadcoins_sold;
    }
}
