# ERC20 Token Standards Reference

## ERC20 Interface

```solidity
// SPDX-License-Identifier: MIT
interface IERC20 {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}
```

## Extensions

### ERC20Burnable
```solidity
function burn(uint256 amount) external;
function burnFrom(address account, uint256 amount) external;
```

### ERC20Mintable
```solidity
function mint(address to, uint256 amount) external returns (bool);
```

### ERC20Pausable
```solidity
function pause() external;
function unpause() external;
```

---

## Common Patterns

### Transfer with Tax
```solidity
function _transfer(address from, address to, uint256 amount) internal {
    uint256 tax = (amount * taxRate) / 100;
    uint256 transferAmount = amount - tax;
    super._transfer(from, taxRecipient, tax);
    super._transfer(from, to, transferAmount);
}
```

### Reflection
```solidity
function _reflect(uint256 rAmount) private {
    _rTotal -= rAmount;
    _tReflections += rAmount / _getRate();
}
```

### Blacklist Check
```solidity
function _beforeTokenTransfer(address from, address to, uint256 amount) internal {
    require(!blacklist[from] && !blacklist[to], "Address is blacklisted");
}
```

---

## Gas Optimization Tips

1. **Use events for indexing** instead of storage for search functionality
2. **Bundle state changes** to reduce SLOAD/SSTORE operations
3. **Use unchecked blocks** for arithmetic that won't overflow
4. **Enable optimizer** with 200-300 runs for production
5. **Avoid unnecessary approvals** - use permit pattern
