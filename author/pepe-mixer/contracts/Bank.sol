// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

contract Bank {
    address public owner;
    mapping(address => uint256) public balance ;
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    constructor() {
        owner = msg.sender;
    } 
    
    function withdraw() public onlyOwner {
        payable(owner).transfer(address(this).balance);
    }

    function done(uint256 amount) public onlyOwner {
        balance[msg.sender] -= amount;
    }
    
    receive() external payable {
        balance[msg.sender] += msg.value;
    }

}