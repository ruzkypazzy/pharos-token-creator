// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title BlacklistToken
 * @dev ERC20 token with blacklist functionality for compliance
 */
contract BlacklistToken is ERC20, Ownable {
    uint8 private _decimals;

    mapping(address => bool) private _blacklist;

    event BlacklistUpdated(address indexed account, bool isBlacklisted);

    constructor(
        string memory name_,
        string memory symbol_,
        uint8 decimals_,
        uint256 initialSupply_
    ) ERC20(name_, symbol_) Ownable(msg.sender) {
        require(decimals_ <= 18, "Decimals must be 18 or less");
        _decimals = decimals_;
        _mint(msg.sender, initialSupply_);
    }

    function decimals() public view override returns (uint8) {
        return _decimals;
    }

    function isBlacklisted(address account) public view returns (bool) {
        return _blacklist[account];
    }

    function addToBlacklist(address account) external onlyOwner {
        require(account != address(0), "Cannot blacklist zero address");
        _blacklist[account] = true;
        emit BlacklistUpdated(account, true);
    }

    function removeFromBlacklist(address account) external onlyOwner {
        _blacklist[account] = false;
        emit BlacklistUpdated(account, false);
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override {
        require(!_blacklist[from] && !_blacklist[to], "Blacklisted address");
        super._beforeTokenTransfer(from, to, amount);
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
}
