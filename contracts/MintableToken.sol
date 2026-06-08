// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Mintable.sol";

/**
 * @title MintableToken
 * @dev ERC20 token with minting capability for the owner
 */
contract MintableToken is ERC20, ERC20Mintable {
    uint8 private _decimals;
    uint256 private _maxSupply;

    constructor(
        string memory name_,
        string memory symbol_,
        uint8 decimals_,
        uint256 initialSupply_,
        uint256 maxSupply_
    ) ERC20(name_, symbol_) {
        require(decimals_ <= 18, "Decimals must be 18 or less");
        _decimals = decimals_;
        _maxSupply = maxSupply_ == 0 ? type(uint256).max : maxSupply_;
        _mint(msg.sender, initialSupply_);
    }

    function decimals() public view override returns (uint8) {
        return _decimals;
    }

    function maxSupply() public view returns (uint256) {
        return _maxSupply;
    }

    function mint(address to, uint256 amount) external override onlyMinter {
        require(totalSupply() + amount <= _maxSupply, "Exceeds max supply");
        _mint(to, amount);
    }
}
