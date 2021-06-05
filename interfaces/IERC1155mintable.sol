// SPDX-License-Identifier: MIT

import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC1155/IERC1155.sol";

pragma solidity ^0.8.2;

interface  IERC1155mintable is IERC1155 {
    function mint(address account, uint256 id, uint256 amount, bytes memory data) external;

    function burn(address account, uint256 id, uint256 amount) external;
}