// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

abstract contract LockerTypes {

    enum LockType {ERC20, LP}
    
    //Lock storage record
    struct  LockStorageRecord {
        LockType ltype;
        address token;
        uint256 amount;
        VestingRecord[] vestings;
    }

    struct VestingRecord {
        uint256 unlockTime;
        uint256 amountUnlock;
        uint256 nftId;
    }

    struct RegistryShare {
        uint256 lockIndex;
        uint256 sharePercent;
        uint256 claimedAmount;
    }


}