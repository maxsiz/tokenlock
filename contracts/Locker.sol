// SPDX-License-Identifier: MIT

import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC20/utils/SafeERC20.sol";

pragma solidity ^0.8.2;

contract Locker {
    using SafeERC20 for IERC20;

    function lock(address _ERC20, uint256 _amount) external {
        require(IERC20(_ERC20).allowance(msg.sender, address(this)) >= _amount, "PLease approve first");
        IERC20 token = IERC20(_ERC20);
        token.safeTransferFrom(msg.sender, address(this), _amount);


    }

}