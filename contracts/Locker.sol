// SPDX-License-Identifier: MIT

//import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC20/utils/SafeERC20.sol";
import "./LockerType.sol";

pragma solidity ^0.8.2;

contract Locker is LockerTypes {
    using SafeERC20 for IERC20;

    uint256 constant MAX_VESTING_RECORDS_PER_LOCK = 250;
    LockStorageRecord[] lockerStorage;

    //map from users(investors)  to locked shares
    mapping(address => RegistryShare[])  public registry;

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
        require(IERC20(_ERC20).allowance(msg.sender, address(this)) >= _amount, "PLease approve first");
        require(_getArraySum(_unlockAmount) == _amount, "Sum vesting records must be equal lock amount");
        require(_unlockedFrom.length == _unlockAmount.length, "Length of periods and amounts arrays must be equal");
        require(_beneficiaries.length == _beneficiariesShares.length, "Length of beneficiaries and shares arrays must be equal");
        require(_getArraySum(_unlockAmount) == _amount, "Sum vesting records must be equal lock amount");

        
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
        //Copying of type struct LockerTypes.VestingRecord memory[] memory 
        //to storage not yet supported.
        //so we need this cycle
        for (uint256 i = 0; i < _unlockedFrom.length; i ++ ) {
            lock.vestings[i] = v[i];    
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

        IERC20 token = IERC20(lock.token);
        token.safeTransfer(msg.sender, availableAmount);
        //update claimed amount
        _decreaseAvailableAmount(msg.sender, _lockIndex, availableAmount);
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
        for (uint256 i = 0; i < _array.length; i ++ ) {
            res += _array[1];           
        }
        return res;
    }

    function _getAvailableAmountByLockIndex(uint256 _lockIndex) internal view returns(uint256){
        VestingRecord[] memory v = lockerStorage[_lockIndex].vestings;
        uint256 res = 0;
        for (uint256 i = 0; i < v.length; i ++ ) {
            if  (v[i].unlockTime <= block.timestamp && v[i].nftId == 0) {
                res += v[i].amountUnlock;
            }
        }
    }

    function _getUserSharePercentAndClaimedAmount(address _user, uint256 _lockIndex) 
        internal 
        view 
        returns(uint256 percent, uint256 claimed)
    {
        RegistryShare[] memory shares = registry[msg.sender];
        for (uint256 i = 0; i < shares.length; i ++ ) {
            if  (shares[i].lockIndex == _lockIndex) {
                percent += shares[i].sharePercent;
                claimed += shares[i].claimedAmount;
            }
        }
        return (percent, claimed);
    }

}