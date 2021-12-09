## Locker smart contracts

### Tests
We use Brownie framework for developing and unit test. For run tests
first please [install it](https://eth-brownie.readthedocs.io/en/stable/install.html)

```bash
brownie pm install OpenZeppelin/openzeppelin-contracts@4.1.0
brownie test
```

Don't forget [ganache-cli](https://www.npmjs.com/package/ganache-cli)


## Main contract method  
**LockerFutures**  
`getUserShares(address _user)` - returns array of structures:  
```solidity
//Investor's share record
    struct RegistryShare {
        uint256 lockIndex;     //Array index of lock record
        uint256 sharePercent;  //Investors share in this lock
        uint256 claimedAmount; //Already claimed amount
    }
```    
` getUserBalances(address _user, uint256 _lockIndex)` - returns tuple of two int:  
- totalBalance - total balance in Lock (minus already claimed);  
- available - available for claim in **this** moment;  

`getLockRecordByIndex(uint256 _index)` - returns structure with common lock Info

## Deployments Info

### Rinkeby TestNet ALFA (DEMO, NFT claim checks OFF)  20210619
**Simple Locker**
https://rinkeby.etherscan.io/address/0xff658a290a12936ba94fdc306647d48246974758#code

**Locker with Futures**
https://rinkeby.etherscan.io/address/0x53395d118ec15f505f2fac14c6a7a6eac9a5a4c9#code

**Futures 1155**
https://rinkeby.etherscan.io/address/0x28ca4994327bdecdd77bcbb0d9838324ee882941#code
