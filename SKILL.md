---
name: pharos-token-creator
description: Create and deploy ERC20 tokens on Pharos blockchain with custom tokenomics. Supports standard, burnable, mintable, pausable, and deflationary token types.
invocation_triggers:
  - create token on pharos
  - deploy erc20 pharos
  - make a new token
  - launch token
  - pharos token factory
  - create my own crypto token
  - deploy token contract
skill_type: token_creator
version: 1.0.0
author: ruzkypazzy
networks:
  atlantic-testnet:
    chainId: 688689
    rpcUrl: https://atlantic.dplabs-internal.com
    explorerUrl: https://atlantic.pharosscan.xyz/
  pacific-mainnet:
    chainId: 1672
    rpcUrl: https://rpc.pharos.xyz
    explorerUrl: https://www.pharosscan.xyz
supported_token_types:
  - standard
  - burnable
  - mintable
  - pausable
  - deflationary
  - reflecct
  - blacklist
prerequisites:
  - Foundry (forge, cast)
  - Source code editor
  - PHRS (testnet) or PROS (mainnet) for gas
dependencies:
  - forge
  - cast
  - OpenZeppelin contracts (via remappings)
warnings:
  - Always test on testnet first
  - Verify contract source code on block explorer
  - Keep private keys secure
  - Audit contracts before mainnet deployment
---

# Pharos Token Creator

Create and deploy custom ERC20 tokens on Pharos blockchain with configurable tokenomics. This skill enables AI agents to generate Solidity smart contracts and deploy them directly to Pharos testnet or mainnet using Foundry.

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/ruzkypazzy/pharos-token-creator
cd pharos-token-creator

# 2. Create your configuration
cp .env.example .env
# Edit .env with your private key and token settings

# 3. Install dependencies
forge install OpenZeppelin/openzeppelin-contracts@v5.0.0

# 4. Deploy to testnet
forge script scripts/DeployToken.s.sol --rpc-url https://atlantic.dplabs-internal.com --private-key $PRIVATE_KEY --broadcast

# 5. Verify on block explorer
cast verify-contract --rpc-url https://atlantic.dplabs-internal.com <CONTRACT_ADDRESS>
```

## Token Types Available

| Type | Description | Use Case |
|------|-------------|----------|
| **Standard** | Basic ERC20 with no extra features | Simple utility tokens |
| **Burnable** | Token holders can burn their tokens | Deflationary mechanics |
| **Mintable** | Owner can mint new tokens | Rewards, inflation control |
| **Pausable** | Owner can pause all transfers | Emergency stops |
| **Deflationary** | Auto-burn on every transfer | Automatic burn mechanism |
| **Reflect** | Holders earn reflections from each transfer | Dividend-style rewards |
| **Blacklist** | Owner can blacklist addresses | Compliance, fraud prevention |

## Configuration Options

| Parameter | Description | Example |
|-----------|-------------|---------|
| `NAME` | Token name | "My Token" |
| `SYMBOL` | Token symbol (3-6 chars) | "MTK" |
| `DECIMALS` | Token decimals | 18 |
| `INITIAL_SUPPLY` | Total supply (with decimals) | 1000000000000000000000 (1000 tokens) |
| `OWNER` | Contract owner address | Your wallet address |
| `MAX_SUPPLY` | Optional maximum supply | 1000000000000000000000000 |
| `TRANSFER_TAX` | Tax percentage (0-100) | 5 |

## Usage Examples

### Standard Token

```bash
export NAME="MyToken"
export SYMBOL="MTK"
export DECIMALS=18
export INITIAL_SUPPLY=1000000000000000000000

forge script scripts/DeployStandardToken.s.sol \
  --rpc-url https://atlantic.dplabs-internal.com \
  --private-key $PRIVATE_KEY \
  --broadcast
```

### Deflationary Token

```bash
export NAME="DeflationaryCoin"
export SYMBOL="DFC"
export DECIMALS=18
export INITIAL_SUPPLY=1000000000000000000000
export TRANSFER_TAX=5

forge script scripts/DeployDeflationaryToken.s.sol \
  --rpc-url https://atlantic.dplabs-internal.com \
  --private-key $PRIVATE_KEY \
  --broadcast
```

### Mintable Token

```bash
forge script scripts/DeployMintableToken.s.sol \
  --rpc-url https://atlantic.dplabs-internal.com \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify
```

## Post-Deployment Commands

```bash
# Check token name
cast call <CONTRACT> "name()(string)" --rpc-url https://atlantic.dplabs-internal.com

# Check total supply
cast call <CONTRACT> "totalSupply()(uint256)" --rpc-url https://atlantic.dplabs-internal.com

# Check balance
cast call <CONTRACT> "balanceOf(address)(uint256)" <WALLET_ADDRESS> --rpc-url https://atlantic.dplabs-internal.com

# Transfer tokens
cast send <CONTRACT> "transfer(address,uint256)" <RECIPIENT> <AMOUNT> --rpc-url https://atlantic.dplabs-internal.com --private-key $PRIVATE_KEY

# Mint new tokens (if mintable)
cast send <CONTRACT> "mint(address,uint256)" <RECIPIENT> <AMOUNT> --rpc-url https://atlantic.dplabs-internal.com --private-key $PRIVATE_KEY

# Burn tokens (if burnable)
cast send <CONTRACT> "burn(uint256)" <AMOUNT> --rpc-url https://atlantic.dplabs-internal.com --private-key $PRIVATE_KEY
```

## Network Configuration

**Atlantic Testnet (Recommended for Testing):**
- Chain ID: 688689
- RPC URL: https://atlantic.dplabs-internal.com
- Explorer: https://atlantic.pharosscan.xyz/
- Currency: PHRS (Test tokens, no real value)

**Pacific Mainnet (Production):**
- Chain ID: 1672
- RPC URL: https://rpc.pharos.xyz
- Explorer: https://www.pharosscan.xyz
- Currency: PROS (Real value)

## Best Practices

1. **Always test on testnet first** - Deploy to Atlantic testnet before mainnet
2. **Audit your contracts** - Have your code reviewed before production use
3. **Start with small supplies** - Test with minimal initial supply
4. **Keep private keys secure** - Never commit private keys to version control
5. **Verify source code** - Use block explorer verification for transparency
6. **Document tokenomics** - Clearly explain token utility and economics

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Insufficient funds" error | Get testnet PHRS from faucet |
| "Nonce too low" error | Check pending transactions or increase gas |
| "Contract size too large" | Enable optimizer or split into multiple contracts |
| "Function not found" | Ensure correct contract ABI is being used |
| "Invalid chain ID" | Verify you are using the correct network RPC |

## Security Considerations

- **Never share private keys** - Use environment variables
- **Enable 2FA** - Secure wallets used in production
- **Limit minting权限** - Consider multi-sig for minting functions
- **Test thoroughly** - Cover edge cases before deployment
- **Consider proxy pattern** - For upgradeable tokens (advanced)

## Supported Frameworks

- **Foundry** - Primary deployment tool (recommended)
- **Hardhat** - Alternative (requires additional setup)
- **Remix IDE** - Browser-based development

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please submit issues and pull requests to the repository.
