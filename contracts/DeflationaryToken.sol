// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";

/**
 * @title DeflationaryToken
 * @dev ERC20 token with automatic burn on each transfer
 */
contract DeflationaryToken is ERC20, ERC20Burnable {
    uint8 private _decimals;
    uint256 private _transferTaxRate;
    address private _burnWallet;

    constructor(
        string memory name_,
        string memory symbol_,
        uint8 decimals_,
        uint256 initialSupply_,
        uint256 transferTaxRate_
    ) ERC20(name_, symbol_) {
        require(decimals_ <= 18, "Decimals must be 18 or less");
        require(transferTaxRate_ <= 100, "Tax rate cannot exceed 100%");
        _decimals = decimals_;
        _transferTaxRate = transferTaxRate_;
        _burnWallet = address(0x000000000000000000000000000000000000dEaD);
        _mint(msg.sender, initialSupply_);
    }

    function decimals() public view override returns (uint8) {
        return _decimals;
    }

    function transferTaxRate() public view returns (uint256) {
        return _transferTaxRate;
    }

    function _transfer(address from, address to, uint256 amount) internal override {
        if (_transferTaxRate > 0) {
            uint256 tax = (amount * _transferTaxRate) / 100;
            uint256 afterTax = amount - tax;
            super._transfer(from, _burnWallet, tax);
            super._transfer(from, to, afterTax);
        } else {
            super._transfer(from, to, amount);
        }
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    modifier onlyOwner() {
        require(msg.sender == owner(), "Caller is not the owner");
        _;
    }

    function owner() public view returns (address) {
        return _msgSender();
    }
}
