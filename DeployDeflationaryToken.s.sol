// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "./DeflationaryToken.sol";

/**
 * @title DeployDeflationaryToken
 * @dev Script to deploy a Deflationary ERC20 token
 * @notice Configures automatic burn on each transfer
 */
contract DeployDeflationaryToken is Script {
    // Configuration - Change these values
    string constant TOKEN_NAME = "Deflationary Token";
    string constant TOKEN_SYMBOL = "DFLCT";
    uint8 constant DECIMALS = 18;
    uint256 constant INITIAL_SUPPLY = 1000000 * 10**18; // 1 million tokens
    uint256 constant TRANSFER_TAX_RATE = 5; // 5% burn on each transfer

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        string memory rpcUrl = vm.envString("PHAROS_RPC");

        vm.startBroadcast(deployerPrivateKey);

        DeflationaryToken token = new DeflationaryToken(
            TOKEN_NAME,
            TOKEN_SYMBOL,
            DECIMALS,
            INITIAL_SUPPLY,
            TRANSFER_TAX_RATE
        );

        vm.stopBroadcast();

        console.log("Deflationary Token deployed!");
        console.log("Name:", token.name());
        console.log("Symbol:", token.symbol());
        console.log("Transfer Tax Rate:", token.transferTaxRate(), "%");
        console.log("Contract Address:", address(token));
    }
}
