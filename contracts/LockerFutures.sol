// SPDX-License-Identifier: MIT

//import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/access/Ownable.sol";
//import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC1155/IERC1155.sol";
import "./LockerType.sol";
import "./Locker.sol";
import "../interfaces/IERC1155mintable.sol";

pragma solidity ^0.8.2;

contract LockerFutures is Locker {
    using SafeERC20 for IERC20;

    uint256 constant DELAY_FOR_FUTURES_ISSUANCE = 1 days;
    uint256 constant LOCK_ID_SCALE = 1e18; 

    address immutable futuresERC1155;

    constructor (address _erc1155) {
        require(_erc1155 != address(0));
        futuresERC1155 = _erc1155;
    }
    

    function emitFutures(uint256 _lockIndex, uint256 _vestingIndex) 
        external 
        returns (uint256)
    {
        VestingRecord storage vr = lockerStorage[_lockIndex].vestings[_vestingIndex];
        require(vr.unlockTime > block.timestamp + DELAY_FOR_FUTURES_ISSUANCE, 
             "To late for this vesting"
        );
        require(vr.nftId == 0, "This futures already issued");
        //TODO  may be need more checks

        //lets mint nft
        address[] memory bnfc = beneficiariesInLock[_lockIndex];
        uint256 amountMint;
        uint256 percent; 
        for (uint256 i = 0; i < bnfc.length; i ++) {
            (percent, ) = _getUserSharePercentAndClaimedAmount(bnfc[i], _lockIndex);
            amountMint = vr.amountUnlock * percent / 100;
            IERC1155mintable(futuresERC1155).mint(
                bnfc[i],
                _getNFTtokenID(_lockIndex, _lockIndex), 
                amountMint, 
                bytes('0')
            );
        }
        //Save nftid in vesting record for exclude amount of this vesting
        //record from available for ordinar claim.
        //from this moment this amount can be claimed only for NFT owner
        vr.nftId =  _getNFTtokenID(_lockIndex, _lockIndex);
    }

    function claimWithNFT(uint256 _tokenId) external {
        require(
            IERC1155mintable(futuresERC1155).balanceOf(msg.sender, _tokenId) > 0,
            "Your futures balance is zero"
        );
        //Lets get ERC20 address of lock of this futures
        IERC20 token20;
        token20 = IERC20(_getLockRecordByIndex(_tokenId / LOCK_ID_SCALE).token);

        //send tokens
        IERC20 token = IERC20(token20);
        token.safeTransfer(
            msg.sender,  
            IERC1155mintable(futuresERC1155).balanceOf(msg.sender, _tokenId)
        );
    }

    ////////////////////////////////////////////////////////////
    /////////// Internals           ////////////////////////////
    ////////////////////////////////////////////////////////////
    function _getNFTtokenID(uint256 _lockIndex, uint256 _vestingIndex) 
        internal 
        returns (uint256)
    {
        return _lockIndex * LOCK_ID_SCALE +_vestingIndex;
    }
}