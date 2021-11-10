// SPDX-License-Identifier: MIT
// Degen Farm. Collectible NFT game
pragma solidity 0.8.9;

import "OpenZeppelin/openzeppelin-contracts@4.3.2/contracts/token/ERC20/ERC20.sol";

contract TokenMock is ERC20 {
    constructor(string memory name_,
        string memory symbol_) ERC20(name_, symbol_)  {
        _mint(msg.sender, 500000000e18);

    }
}
