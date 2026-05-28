// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "../contracts/MintableToken.sol";

/**
 * @title DeployMintableToken
 * @dev Script to deploy a Mintable ERC20 token
 */
contract DeployMintableToken is Script {
    // Configuration
    string constant TOKEN_NAME = "Mintable Token";
    string constant TOKEN_SYMBOL = "MNTT";
    uint8 constant DECIMALS = 18;
    uint256 constant INITIAL_SUPPLY = 1000000 * 10**18; // 1 million
    uint256 constant MAX_SUPPLY = 10000000 * 10**18; // 10 million max

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        string memory rpcUrl = vm.envString("PHAROS_RPC");

        vm.startBroadcast(deployerPrivateKey);

        MintableToken token = new MintableToken(
            TOKEN_NAME,
            TOKEN_SYMBOL,
            DECIMALS,
            INITIAL_SUPPLY,
            MAX_SUPPLY
        );

        vm.stopBroadcast();

        console.log("Mintable Token deployed!");
        console.log("Name:", token.name());
        console.log("Symbol:", token.symbol());
        console.log("Initial Supply:", INITIAL_SUPPLY);
        console.log("Max Supply:", token.maxSupply());
        console.log("Contract Address:", address(token));
    }
}
