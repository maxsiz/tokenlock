// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

import "./LockerFutures.sol";


contract FuturesMarket is LockerFutures {

    mapping(uint256 => uint256) public listing;
    mapping(uint => address) public futureOwners;

    event Listed(address indexed, uint256 indexed _tokenId);



    // list to futures market
    function addListing(uint256 _tokenId, uint256 _price) external {
        require(_price > 0, "Price should be greater than zero");
        require(IERC1155mintable(futuresERC1155).balanceOf(msg.sender, _tokenId) > 0, "Your future balance is zero");
        //transfering nft to contract
        IERC1155mintable(futuresERC1155).safeTransferFrom(msg,sender, address(this), _tokenId, IERC1155mintable(futuresERC1155).balanceOf(msg.sender, _tokenId), bytes('0'));
        Listed[_tokenId] = _price;
        futureOwners[_tokenId] = msg.sender;
    }


    // accept ethereum
    function buyFutures(uint256 _tokenId) public payable returns (bool) {
        price = listing[_tokenId];
        require(msg.value == price, "msg.value should be equal to the buy amount");

        owner = futureOwners[_tokenId];
        owner.transfer(msg.value);

        IERC1155mintable(futuresERC1155).safeTransferFrom(adress(this), msg.sender, _tokenId, IERC1155mintable(futuresERC1155).balanceOf(address(this), _tokenId), bytes('0'));




    }
    // accept stablecoin
    function buyFuturesERC20(uint256 _tokenId, uint _amount,  address _ERC20) external {

    }

}