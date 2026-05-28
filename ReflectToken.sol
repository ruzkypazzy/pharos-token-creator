// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title ReflectToken
 * @dev ERC20 token with reflection rewards for holders
 * @notice Each holder receives a share of each transfer as rewards
 */
contract ReflectToken is ERC20, Ownable {
    uint8 private _decimals;
    uint256 private _reflectionRate;
    uint256 private _burnRate;
    uint256 private _marketingRate;
    address private _marketingWallet;

    uint256 private _tTotal;
    uint256 private _rTotal;
    uint256 private _tReflections;
    mapping(address => uint256) private _rBalances;
    mapping(address => uint256) private _tBalances;
    mapping(address => uint256) private _lastTxTime;

    event TransferTaxCollected(address indexed from, uint256 burnAmount, uint256 marketingAmount);

    constructor(
        string memory name_,
        string memory symbol_,
        uint8 decimals_,
        uint256 initialSupply_,
        uint256 reflectionRate_,
        uint256 burnRate_,
        uint256 marketingRate_,
        address marketingWallet_
    ) ERC20(name_, symbol_) Ownable(msg.sender) {
        require(decimals_ <= 18, "Decimals must be 18 or less");
        require(reflectionRate_ + burnRate_ + marketingRate_ <= 100, "Total tax exceeds 100%");

        _decimals = decimals_;
        _reflectionRate = reflectionRate_;
        _burnRate = burnRate_;
        _marketingRate = marketingRate_;
        _marketingWallet = marketingWallet_;

        _tTotal = initialSupply_ * 10 ** decimals_;
        _rTotal = type(uint256).max - (type(uint256).max % _tTotal);
        _tReflections = 0;

        _rBalances[msg.sender] = _rTotal;
        _tBalances[msg.sender] = _tTotal;

        emit Transfer(address(0), msg.sender, _tTotal);
    }

    function decimals() public view override returns (uint8) {
        return _decimals;
    }

    function reflectionRate() public view returns (uint256) {
        return _reflectionRate;
    }

    function totalSupply() public view override returns (uint256) {
        return _tTotal - _tReflections;
    }

    function _getRate() private view returns (uint256) {
        if (_tTotal == 0) return 0;
        return _rTotal / _tTotal;
    }

    function _updateRevenueTotals(uint256 rAmount) private {
        _rTotal -= rAmount;
        _tReflections += rAmount / _getRate();
    }

    function balanceOf(address account) public view override returns (uint256) {
        return _tBalances[account];
    }

    function _transfer(address from, address to, uint256 amount) internal override {
        require(from != address(0), "Transfer from zero address");
        require(to != address(0), "Transfer to zero address");
        require(amount <= _tBalances[from], "Insufficient balance");

        uint256 taxAmount = ((_burnRate + _marketingRate) * amount) / 100;
        uint256 reflectionAmount = (_reflectionRate * amount) / 100;
        uint256 transferAmount = amount - taxAmount;

        _tBalances[from] -= amount;

        if (taxAmount > 0) {
            uint256 burnAmount = (_burnRate * amount) / 100;
            uint256 marketingAmount = (_marketingRate * amount) / 100;

            // Burn portion
            _tBalances[address(0)] += burnAmount;
            _tTotal -= burnAmount;

            // Marketing portion
            if (_marketingWallet != address(0)) {
                _tBalances[_marketingWallet] += marketingAmount;
            }

            emit Transfer(from, address(0), burnAmount);
            if (_marketingWallet != address(0)) {
                emit Transfer(from, _marketingWallet, marketingAmount);
            }
            emit TransferTaxCollected(from, burnAmount, marketingAmount);
        }

        uint256 currentRate = _getRate();
        uint256 rAmount = transferAmount * currentRate;
        _rBalances[from] -= rAmount;
        _rBalances[to] += rAmount;
        _tBalances[to] += transferAmount;

        emit Transfer(from, to, transferAmount);
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
}
