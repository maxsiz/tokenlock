// SPDX-License-Identifier: MIT
// Platinum Software Dev Team
// Locker  ALFA  version.Testing is in progress.


import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/access/Ownable.sol";
import "./LockerType.sol";
import "./Locker.sol";
import "../interfaces/IERC1155mintable.sol";

pragma solidity ^0.8.2;

contract LockerFutures is Locker, Ownable {
    using SafeERC20 for IERC20;

    uint256 constant DELAY_FOR_FUTURES_ISSUANCE = 1 days;
    uint256 constant LOCK_ID_SCALE = 1e18; 

    address public futuresERC1155;

    mapping(uint256 => uint256[]) indexes;

   function emitFutures(uint256 _lockIndex, uint256 _vestingIndex) 
        external 
        returns (uint256)
    {
        VestingRecord storage vr = lockerStorage[_lockIndex].vestings[_vestingIndex];
        require(vr.unlockTime > block.timestamp + DELAY_FOR_FUTURES_ISSUANCE, 
             "To late for this vesting"
        );
        require(vr.nftId == 0, "This futures already issued");
        
        //Check that tx.sender have none zero share in this lock
        //to be authorize for mint NFT 
        
        uint256 percent;
        uint256 claimed;
        (percent, claimed) = _getUserSharePercentAndClaimedAmount(msg.sender, _lockIndex);
        require(percent > 0, "Sender has no balance in this lock");
        require(claimed == 0, "Distribution was started");

        //TODO  may be need more checks

        //lets mint nft
        address[] memory bnfc = beneficiariesInLock[_lockIndex];
        uint256 amountMint; 
        for (uint256 i = 0; i < bnfc.length; i ++) {
            (percent, ) = _getUserSharePercentAndClaimedAmount(bnfc[i], _lockIndex);
            amountMint = vr.amountUnlock * percent / TOTAL_IN_PERCENT;
            IERC1155mintable(futuresERC1155).mint(
                bnfc[i],
                _getNFTtokenID(_lockIndex, _vestingIndex),
                amountMint, 
                bytes('0')
            );
        }
        //Save nftid in vesting record for exclude amount of this vesting
        //record from available for ordinar claim.
        //from this moment this amount can be claimed only for NFT owner
        vr.nftId =  _getNFTtokenID(_lockIndex, _vestingIndex);
    }

    function claimWithNFT(uint256 _tokenId) external {
        require(
            IERC1155mintable(futuresERC1155).balanceOf(msg.sender, _tokenId) > 0,
            "Your futures balance is zero"
        );

        uint256 _lockIndex = _tokenId / LOCK_ID_SCALE;
        uint256 _vestingIndex = _tokenId -  (_lockIndex * LOCK_ID_SCALE);
        VestingRecord storage vr = lockerStorage[_lockIndex].vestings[_vestingIndex];

        require(vr.unlockTime <= block.timestamp, 'Claiming NFT insufficient for now');


        //Lets get ERC20 address of lock of this futures
        IERC20 token20;
        token20 = IERC20(_getLockRecordByIndex(_lockIndex).token);

        //send tokens
        IERC20 token = IERC20(token20);
        token.safeTransfer(
            msg.sender,  
            IERC1155mintable(futuresERC1155).balanceOf(msg.sender, _tokenId)
        );

        IERC1155mintable(futuresERC1155).burn(
                msg.sender, _tokenId, IERC1155mintable(futuresERC1155).balanceOf(msg.sender, _tokenId));
    }

    ///////////////////////////////////////////////////////////
    /////   Admin functions                                 ///
    ///////////////////////////////////////////////////////////
    function setFuturesERC1155(address _erc1155) external onlyOwner {
        require(_erc1155 != address(0), "Cant set zero address");
        futuresERC1155 = _erc1155;
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