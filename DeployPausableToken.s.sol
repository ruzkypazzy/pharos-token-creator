// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "./PausableToken.sol";

/**
 * @title DeployPausableToken
 * @dev Script to deploy a Pausable ERC20 token
 * @notice Owner can pause all transfers in emergencies
 */
contract DeployPausableToken is Script {
    // Configuration
    string constant TOKEN_NAME = "Pausable Token";
    string constant TOKEN_SYMBOL = "PAUS";
    uint8 constant DECIMALS = 18;
    uint256 constant INITIAL_SUPPLY = 1000000 * 10**18;

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        string memory rpcUrl = vm.envString("PHAROS_RPC");

        vm.startBroadcast(deployerPrivateKey);

        PausableToken token = new PausableToken(
            TOKEN_NAME,
            TOKEN_SYMBOL,
            DECIMALS,
            INITIAL_SUPPLY
        );

        vm.stopBroadcast();

        console.log("Pausable Token deployed!");
        console.log("Name:", token.name());
        console.log("Symbol:", token.symbol());
        console.log("Contract Address:", address(token));
        console.log("Owner:", token.owner());
    }
}
