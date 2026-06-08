// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../src/StandardToken.sol";

/**
 * @title DeployStandardToken
 * @dev Script to deploy a Standard ERC20 token to Pharos blockchain
 */
contract DeployStandardToken is Script {
    // Configuration - Change these values
    string constant TOKEN_NAME = "My Pharos Token";
    string constant TOKEN_SYMBOL = "MPT";
    uint8 constant DECIMALS = 18;
    uint256 constant INITIAL_SUPPLY = 1000000 * 10**18; // 1 million tokens

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        string memory rpcUrl = vm.envString("PHAROS_RPC");

        vm.startBroadcast(deployerPrivateKey);

        StandardToken token = new StandardToken(
            TOKEN_NAME,
            TOKEN_SYMBOL,
            DECIMALS,
            INITIAL_SUPPLY
        );

        vm.stopBroadcast();

        console.log("Token deployed!");
        console.log("Name:", token.name());
        console.log("Symbol:", token.symbol());
        console.log("Decimals:", token.decimals());
        console.log("Total Supply:", token.totalSupply());
        console.log("Contract Address:", address(token));
    }
}
