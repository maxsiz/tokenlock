// SPDX-License-Identifier: MIT
// https://eips.ethereum.org/EIPS/eip-1155
pragma solidity 0.8.9;

import "OpenZeppelin/openzeppelin-contracts@4.3.2/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
import "OpenZeppelin/openzeppelin-contracts@4.3.2/contracts/utils/Strings.sol";



contract Futures1155 is ERC1155Supply {

    using Strings for uint256;
    using Strings for uint160;
    
    address public locker;
    string  public name = 'Platinum Locker Collection';
    mapping(uint256 => bool) public tansferrable;
    
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

    function setTansferrableCondition(uint256 id, bool _is) external {
        require(msg.sender == locker, "Only locker can set");
        tansferrable[id] = _is;
    }



    /**
     * @dev Override standart OpenZeppelin hook
     * due to check Transfer false tokens  never be transfered
     *
     */

    function safeTransferFrom(
        address from,
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) public override  {
        require(tansferrable[id], "token is not tansferrable");

        super.safeTransferFrom(from, to, id, amount, data);
    }

    /**
     * @dev Override standart OpenZeppelin hook
     * due to check Transfer false tokens  never be transfered
     *
     */
    function safeBatchTransferFrom(
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) public override {

        require(ids.length == amounts.length, "ERC1155: ids and amounts length mismatch");

        for (uint256 i = 0; i < ids.length; ++i) {
            safeTransferFrom(from, to, ids[i], amounts[i], data);
        }
    }

    function uri(uint256 _tokenID) public view virtual override 
        returns (string memory) 
    {
        return string(abi.encodePacked(
            ERC1155.uri(0),
            uint160(address(this)).toHexString(),
            "/", _tokenID.toString())
        );
    }

}


