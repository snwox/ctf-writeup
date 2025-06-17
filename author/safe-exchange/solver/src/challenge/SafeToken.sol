pragma solidity 0.8.25;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract SafeToken is ERC20, Ownable {
    constructor() ERC20("SafeToken", "SAFE") Ownable(msg.sender) {
        _mint(msg.sender, 4_000_000 * 10 ** 18);
    }

    // function burn(uint256 amount) external {
    //     _burn(msg.sender, amount);
    // }

    // function mint(address to, uint256 amount) external {
    //     _mint(to, amount);
    // }
}