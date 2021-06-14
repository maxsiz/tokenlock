// SPDX-License-Identifier: MIT
import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC20/utils/SafeERC20.sol";

pragma solidity ^0.8.2;

import "./LockerFutures.sol";


contract FuturesMarket is LockerFutures, FuturesMarketHolder {

    enum State {ACTIVE, CANCELED, SOLD}

   struct OrdersParam {
       uint buying;
       address owner;
       State state;
   }


    mapping(byte32 => OrdersParam) internal orders;

    event Listed(address owner, uint256  _tokenId);
    event Cancel(address owner, uint256  _tokenId);
    event Buy();



    // list to futures market
    function addOrder(FuturesMarket.Order calldata order) external {
        require(msg.sender == order.key.owner, "order could be added by token owner only");
        require(IERC1155mintable(futuresERC1155).balanceOf(msg.sender, order.key.sellAsset.tokenId) > 0, "Your future balance is zero");
        byte32 key = prepareKey(order);
        orders[key] = OrdersParam(order.buying, msg.sender, State.ACTIVE);
        uint256 tokenId = order.key.sellAsset.tokenId;
//        IERC1155mintable(futuresERC1155).safeTransferFrom(msg,sender, address(this), tokenId, IERC1155mintable(futuresERC1155).balanceOf(msg.sender, tokenId), bytes('0'));

        emit Listed(msg.sender, order.key.sellAsset.tokenId);
    }


    function cancel(FuturesMarket.Order calldata order) external {
        require(msg.sender == order.key.owner, "order could be canceled only by token owner");

        byte32 key = prepareKey(order);
        orders[key] = OrdersParam(order.buying, msg.sender, State.CANCELED);
        uint256 tokenId = order.key.sellAsset.tokenId;
//        IERC1155mintable(futuresERC1155).safeTransferFrom(address(this), msg.sender, tokenId, IERC1155mintable(futuresERC1155).balanceOf(address(this), tokenId), bytes('0'));

        emit Cancel(msg.sender, order.key.sellAsset.tokenId);
    }


    // accept ethereum
    function buyFutures(FuturesMarket.Order calldata order, uint amount) public payable returns (bool) {

        byte32 key = prepareKey(order);
        OrdersParam storage ordersParam = orders[key];
        if (order.key.buyAsset.assetType == AssetType.ETH) {
            require(msg.value == ordersParam.buying);
        }else if (order.key.buyAsset.assetType == AssetType.ERC20) {
            require(amount == ordersParam.buying);
        }

        transfer(order.key.sellAsset, amount, order.key.owner, msg.sender);
        transfer(order.key.buyAsset, amount, order.key.owner, msg.sender);
        orders[key] = OrdersParam(State.SOLD);

    }


    // internal

    function transfer(Asset memory asset, uint value, address from, address to) internal {
            if(asset.assetType == AssetType.ETH) {
                address payable toPayable = address(uint160(to));
                toPayable.transfer(value);
            } else if (asset.assetType.ERC20) {
                require(asset.tokenId == 0, "tokenId should be 0");
                IERC20 token = IERC20(asset.token);
                token.safeTransferFrom(from, to, value);
            }else {
                IERC1155mintable(futuresERC1155).safeTransferFrom(from, to, asset.tokenId, IERC1155mintable(futuresERC1155).balanceOf(from, asset.tokenId), bytes('0'));
            }

    }


     function prepareKey(FuturesMarket.Order memory order) internal pure returns (bytes32) {
        return keccak256(abi.encode(
                order.key.sellAsset.token,
                order.key.sellAsset.tokenId,
                order.key.owner,
                order.key.buyAsset.token,
                order.key.buyAsset.tokenId,
                order.key.salt
            ));
    }

}