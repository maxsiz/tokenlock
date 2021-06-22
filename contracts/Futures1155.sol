// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC1155/ERC1155.sol";



contract Futures1155 is ERC1155 {
    
    address public locker;

    
    /**
     * @dev we use uri_ here for Compatibility with
     * https://eips.ethereum.org/EIPS/eip-1155#metadata
     * 
     */
    constructor (string memory uri_, address _locker) ERC1155(uri_) {
        locker = _locker;
               
    }

    function mint(address account, uint256 id, uint256 amount, bytes memory data) external {
        require(msg.sender == locker, "Only locker can mint" );
        _mint(account, id, amount, data);
    }

    function burn(address account, uint256 id, uint256 amount) external {
        require(msg.sender == locker, "Only locker can burn" );
        _burn(account, id, amount);

    }



}


