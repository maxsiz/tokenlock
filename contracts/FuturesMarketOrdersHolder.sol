// SPDX-License-Identifier: MIT


pragma solidity ^0.8.2;


contract FuturesMarketHolder {

    enum AssetType {ETH, ERC20, ERC1155}

    struct Asset {
        address token;
        uint tokenId;
        AssetType assetType;
    }
    struct OrderKey {
        address owner;
        uint salt;
        Asset sellAsset;
        Asset buyAsset;
    }

    struct Order {
        OrderKey key;
        uint buying;
    }
}