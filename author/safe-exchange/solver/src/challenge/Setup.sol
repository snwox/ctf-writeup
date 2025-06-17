pragma solidity ^0.8.25;

import {SafeExchanger} from "./SafeExchanger.sol";
import {SafeToken} from "./SafeToken.sol";

contract Setup {
    address public bot;
    SafeToken public safe_token;
    SafeExchanger public safe_exchanger;
    bool public solved;
    constructor(bytes memory bytecode) payable {

        safe_token = new SafeToken();
        safe_exchanger = new SafeExchanger(safe_token, 46060);
        safe_token.approve(address(safe_exchanger), type(uint256).max);

        safe_exchanger.addLiquidity{value: address(this).balance}(46030, 46100, 10_000 ether);
        safe_exchanger.addLiquidity{value: address(this).balance}(46040, 46090, 5_000 ether);
        safe_exchanger.addLiquidity{value: address(this).balance}(46050, 46080, 2_500 ether);
        safe_exchanger.addLiquidity{value: address(this).balance}(46060, 46070, 1_250 ether);

        bytecode = abi.encodePacked(bytecode, address(safe_token), address(safe_exchanger));
        assembly {
            let addr := create(0, add(bytecode, 0x20), mload(bytecode))
            sstore(bot.slot, addr)
        }

        safe_token.transfer(bot, 100_000 ether);
        payable(bot).transfer(100_000 ether);
    }

    function faucet() public payable {
        require(msg.value > 0, "no value");
        safe_token.transfer(msg.sender, msg.value);
    }

    function check() public {
        require(!solved, "already solved");
        require(address(msg.sender).balance > 80_000 ether, "not solved");
        solved = true;
    }

    function isSolved() public view returns (bool) {
        return solved;
    }

    receive() external payable {}
}
