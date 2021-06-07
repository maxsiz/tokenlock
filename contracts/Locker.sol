// SPDX-License-Identifier: MIT

//import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC20/utils/SafeERC20.sol";
//import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC1155/IERC1155.sol";
import "./LockerType.sol";

pragma solidity ^0.8.2;

contract Locker is LockerTypes {
    using SafeERC20 for IERC20;

    string  constant name = "Lock & Registry v0.0.1"; 
    uint256 constant MAX_VESTING_RECORDS_PER_LOCK = 250;
    LockStorageRecord[] lockerStorage;

    //map from users(investors)  to locked shares
    mapping(address => RegistryShare[])  public registry;

    //map from lockIndex to beneficiaries list
    mapping(uint256 => address[]) beneficiariesInLock;

    event NewLock(address indexed erc20, address indexed who, uint256 lockedAmount, uint256 lockId);
    event EmitFutures(address indexed erc20, address indexed who, uint256 lockedAmount, uint256 claimDate);

    function lockTokens(
        address _ERC20, 
        uint256 _amount, 
        uint256[] memory _unlockedFrom, 
        uint256[] memory _unlockAmount,
        address[] memory _beneficiaries,
        uint256[] memory _beneficiariesShares

    )
        external 

    {
        require(_amount > 0, "Cant lock 0 amount");
        require(IERC20(_ERC20).allowance(msg.sender, address(this)) >= _amount, "Please approve first");
        require(_getArraySum(_unlockAmount) == _amount, "Sum vesting records must be equal lock amount");
        require(_unlockedFrom.length == _unlockAmount.length, "Length of periods and amounts arrays must be equal");
        require(_beneficiaries.length == _beneficiariesShares.length, "Length of beneficiaries and shares arrays must be equal");
        require(_getArraySum(_beneficiariesShares) == 100, "Sum of shares array must be equal to 100%");
        
        //Lets prepare vestings array
        VestingRecord[] memory v = new VestingRecord[](_unlockedFrom.length);
        for (uint256 i = 0; i < _unlockedFrom.length; i ++ ) {
                v[i].unlockTime = _unlockedFrom[i];
                v[i].amountUnlock = _unlockAmount[i]; 
        }
        
        //Save lock info in storage
        LockStorageRecord storage lock = lockerStorage.push();
        lock.ltype = LockType.ERC20;
        lock.token = _ERC20;
        lock.amount = _amount;

        //Save beneficaries in one map
        beneficiariesInLock[lockerStorage.length - 1];

        //Copying of type struct LockerTypes.VestingRecord memory[] memory 
        //to storage not yet supported.
        //so we need this cycle
        for (uint256 i = 0; i < _unlockedFrom.length; i ++ ) {
            lock.vestings.push(v[i]);    
        }

        //Lets save _beneficiaries for this lock
        for (uint256 i = 0; i < _beneficiaries.length; i ++ ) {
            RegistryShare[] storage shares = registry[_beneficiaries[i]];
            shares.push(RegistryShare({
                lockIndex: lockerStorage.length - 1,
                sharePercent: _beneficiariesShares[i],
                claimedAmount: 0
            }));
        }

        
        IERC20 token = IERC20(_ERC20);
        token.safeTransferFrom(msg.sender, address(this), _amount);

    }

    function claimTokens(uint256 _lockIndex, uint256 _desiredAmount) external {
        //Lets get our lockRecord by index
        require(_desiredAmount > 0, "Cant claim zero");
        LockStorageRecord memory lock = lockerStorage[_lockIndex];
        (uint256 percentShares, uint256 wasClaimed) = 
            _getUserSharePercentAndClaimedAmount(msg.sender, _lockIndex);
        uint256 availableAmount =
            //TODO check for small values 
            _getAvailableAmountByLockIndex(_lockIndex)
            * percentShares / 100
            - wasClaimed;

        if  (_desiredAmount != 0) {
            require(_desiredAmount <= availableAmount, "Insufficient for now");
            availableAmount = _desiredAmount;
        }

        //update claimed amount
        _decreaseAvailableAmount(msg.sender, _lockIndex, availableAmount);

        //send tokens
        IERC20 token = IERC20(lock.token);
        token.safeTransfer(msg.sender, availableAmount);
    }

    // function emitFutures(uint256 _lockIndex, uint256 _vestingIndex) external returns (uint256){
    //     LockStorageRecord memory lock = lockerStorage[_lockIndex];
    // }

    // function claimWithNFT(uint256 _tokenId) external {

    // }

    function getMyShares() external view returns (RegistryShare[] memory) {
        return _getUsersShares(msg.sender);
    }

    //function getMyLockedVestings() external view returns (RegistryShare[] memory)

    function getLockRecordByIndex(uint256 _index) external view returns (LockStorageRecord memory){
        return _getLockRecordByIndex(_index);
    }

    function getLockCount() external view returns (uint256) {
        return lockerStorage.length;
    }

    function getArraySum(uint256[] memory _array) external pure returns (uint256) {
        return _getArraySum(_array);
    }

    ////////////////////////////////////////////////////////////
    /////////// Internals           ////////////////////////////
    ////////////////////////////////////////////////////////////
    function _decreaseAvailableAmount(address user, uint256 _lockIndex, uint256 _amount) internal {
        RegistryShare[] storage shares = registry[msg.sender];
        for (uint256 i = 0; i < shares.length; i ++ ) {
            if  (shares[i].lockIndex == _lockIndex) {
                //It does not matter what record will update
                // with same _lockIndex. but only one!!!!
                shares[i].claimedAmount += _amount;
                break;
            }
        }

    }

    function _getArraySum(uint256[] memory _array) internal pure returns (uint256) {
        uint256 res = 0;
        for (uint256 i = 0; i < _array.length; i++) {
            res += _array[i];           
        }
        return res;
    }

    function _getAvailableAmountByLockIndex(uint256 _lockIndex) 
        internal 
        view 
        returns(uint256)
    {
        VestingRecord[] memory v = lockerStorage[_lockIndex].vestings;
        uint256 res = 0;
        for (uint256 i = 0; i < v.length; i ++ ) {
            if  (v[i].unlockTime <= block.timestamp && v[i].nftId == 0) {
                res += v[i].amountUnlock;
            }
        }
        // adding return function
        return res;
    }

    function _getUserSharePercentAndClaimedAmount(address _user, uint256 _lockIndex) 
        internal 
        view 
        returns(uint256 percent, uint256 claimed)
    {
        RegistryShare[] memory shares = registry[_user];
        for (uint256 i = 0; i < shares.length; i ++ ) {
            if  (shares[i].lockIndex == _lockIndex) {
                //We do this cycle because one adress can exist
                //more then once in one lock
                percent += shares[i].sharePercent;
                claimed += shares[i].claimedAmount;
            }
        }
        return (percent, claimed);
    }

    function _getUsersShares(address _user) internal view returns (RegistryShare[] memory) {
        return registry[_user];
    }

    function _getVestingsByLockIndex(uint256 _index) internal view returns (VestingRecord[] memory) {
        VestingRecord[] memory v = _getLockRecordByIndex(_index).vestings;
        return v;

    }

    function _getLockRecordByIndex(uint256 _index) internal view returns (LockStorageRecord memory){
        return lockerStorage[_index];
    }

}