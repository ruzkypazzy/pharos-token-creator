// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "./BlacklistToken.sol";

/**
 * @title DeployBlacklistToken
 * @dev Script to deploy a Blacklist ERC20 token
 * @notice Owner can blacklist addresses for compliance
 */
contract DeployBlacklistToken is Script {
    // Configuration
    string constant TOKEN_NAME = "Compliant Token";
    string constant TOKEN_SYMBOL = "CPLT";
    uint8 constant DECIMALS = 18;
    uint256 constant INITIAL_SUPPLY = 1000000 * 10**18;

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        string memory rpcUrl = vm.envString("PHAROS_RPC");

        vm.startBroadcast(deployerPrivateKey);

        BlacklistToken token = new BlacklistToken(
            TOKEN_NAME,
            TOKEN_SYMBOL,
            DECIMALS,
            INITIAL_SUPPLY
        );

        vm.stopBroadcast();

        console.log("Blacklist Token deployed!");
        console.log("Name:", token.name());
        console.log("Symbol:", token.symbol());
        console.log("Contract Address:", address(token));
    }
}
