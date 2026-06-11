# Pharos Token Creator

Create and deploy custom ERC20 tokens on Pharos blockchain with configurable tokenomics.

## Overview

`pharos-token-creator` is an AI agent skill that enables developers and users to create custom ERC20 tokens on Pharos blockchain without writing Solidity code from scratch. Simply configure your token parameters, deploy with Foundry, and your token is live on-chain.

## Features

- **Multiple Token Types**: Standard, Burnable, Mintable, Pausable, Deflationary, Reflect, Blacklist
- **Custom Tokenomics**: Configurable name, symbol, decimals, supply, and tax
- **Foundry Powered**: Fast, reliable deployments using industry-standard tools
- **OpenZeppelin Secured**: Battle-tested smart contract patterns
- **Fully Documented**: Comprehensive guides and reference materials

## Supported Token Types

| Type | Description | File |
|------|-------------|------|
| **Standard** | Basic ERC20 | `contracts/StandardToken.sol` |
| **Burnable** | Token holders can burn tokens | `contracts/BurnableToken.sol` |
| **Mintable** | Owner can mint new tokens | `contracts/MintableToken.sol` |
| **Pausable** | Owner can pause transfers | `contracts/PausableToken.sol` |
| **Deflationary** | Auto-burn on transfers | `contracts/DeflationaryToken.sol` |
| **Reflect** | Reflection rewards for holders | `contracts/ReflectToken.sol` |
| **Blacklist** | Address blacklisting | `contracts/BlacklistToken.sol` |

## Quick Start

### Prerequisites

- [Foundry](https://book.getfoundry.sh/getting-started/installation)
- PHRS (testnet) or PROS (mainnet) for gas fees

## Install

### 1. Install Foundry (the engine the skill is built on)

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

Verify with `cast --version`. This gives you `cast`, `forge`, `anvil`, and `chisel` on your `$PATH`.

### 2. Install jq (used to parse JSON)

```bash
# macOS
brew install jq
# Debian/Ubuntu/Termux
apt install -y jq
# Alpine
apk add jq
```

Verify with `jq --version`.

### 3. Get the skill

```bash
git clone https://github.com/ruzkypazzy/pharos-token-creator
cd pharos-token-creator
chmod +x scripts/*.sh
```

That's it. No `pip install`, no `npm install`, no `forge build`, no compile. The skill is one or more bash scripts that use `cast` (from Foundry) for every RPC read. The `assets/networks.json` file already knows the Pharos Pacific Mainnet and Atlantic Testnet endpoints.
### 1. Install Foundry (the engine the skill is built on)

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

Verify with `cast --version`. This gives you `cast`, `forge`, `anvil`, and `chisel` on your `$PATH`.

### 2. Install jq (used to parse JSON)

```bash
# macOS
brew install jq
# Debian/Ubuntu/Termux
apt install -y jq
# Alpine
apk add jq
```

Verify with `jq --version`.

### 3. Get the skill

```bash
git clone https://github.com/ruzkypazzy/pharos-token-creator
cd pharos-token-creator
chmod +x scripts/*.sh
```

That's it. No `pip install`, no `npm install`, no `forge build`, no compile. The skill is one or more bash scripts that use `cast` (from Foundry) for every RPC read. The `assets/networks.json` file already knows the Pharos Pacific Mainnet and Atlantic Testnet endpoints.
### 1. Install Foundry (the engine the skill is built on)

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

Verify with `cast --version`. This gives you `cast`, `forge`, `anvil`, and `chisel` on your `$PATH`.

### 2. Install jq (used to parse JSON)

```bash
# macOS
brew install jq
# Debian/Ubuntu/Termux
apt install -y jq
# Alpine
apk add jq
```

Verify with `jq --version`.

### 3. Get the skill

```bash
git clone https://github.com/ruzkypazzy/pharos-token-creator
cd pharos-token-creator
chmod +x scripts/*.sh
```

That's it. No `pip install`, no `npm install`, no `forge build`, no compile. The skill is one or more bash scripts that use `cast` (from Foundry) for every RPC read. The `assets/networks.json` file already knows the Pharos Pacific Mainnet and Atlantic Testnet endpoints.
### Configuration

Edit `.env` file:

```env
PRIVATE_KEY=your_private_key_here
Atlantic_RPC=https://atlantic.dplabs-internal.com
Pacific_RPC=https://rpc.pharos.xyz
```

### Deployment

**To Atlantic Testnet:**

```bash
# Deploy your token
forge script scripts/DeployToken.s.sol \
  --rpc-url $Atlantic_RPC \
  --private-key $PRIVATE_KEY \
  --broadcast
```

**To Pacific Mainnet:**

```bash
forge script scripts/DeployToken.s.sol \
  --rpc-url $Pacific_RPC \
  --private-key $PRIVATE_KEY \
  --broadcast
```

## Usage Examples

### Create a Standard Token

```bash
# Configure in .env
TOKEN_NAME="My First Token"
TOKEN_SYMBOL="MFT"
TOKEN_DECIMALS=18
INITIAL_SUPPLY=1000000000000000000000  # 1000 tokens
```

Run deployment:
```bash
forge script scripts/DeployStandardToken.s.sol \
  --rpc-url $Atlantic_RPC \
  --private-key $PRIVATE_KEY \
  --broadcast
```

### Create a Deflationary Token

Deflationary tokens automatically burn a percentage of each transfer.

```bash
# Configure tax rate (e.g., 5%)
TRANSFER_TAX=5
```

### Create a Mintable Token

Mintable tokens allow the owner to create new tokens after deployment.

```bash
forge script scripts/DeployMintableToken.s.sol \
  --rpc-url $Atlantic_RPC \
  --private-key $PRIVATE_KEY \
  --broadcast
```

## Post-Deployment

### Verify Deployment

```bash
# Check token contract
cast call <CONTRACT_ADDRESS> "name()(string)" --rpc-url $Atlantic_RPC
cast call <CONTRACT_ADDRESS> "symbol()(string)" --rpc-url $Atlantic_RPC
cast call <CONTRACT_ADDRESS> "totalSupply()(uint256)" --rpc-url $Atlantic_RPC
```

### Interact with Your Token

```bash
# Transfer tokens
cast send <CONTRACT> "transfer(address,uint256)" <RECIPIENT> <AMOUNT> \
  --rpc-url $Atlantic_RPC \
  --private-key $PRIVATE_KEY

# Check balance
cast call <CONTRACT> "balanceOf(address)(uint256)" <WALLET> \
  --rpc-url $Atlantic_RPC
```

### Explore on Block Explorer

- **Testnet**: https://atlantic.pharosscan.xyz/
- **Mainnet**: https://www.pharosscan.xyz

## Token Options Reference

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Full token name |
| `symbol` | string | Token ticker (3-6 chars recommended) |
| `decimals` | uint8 | Decimal places (18 standard) |
| `totalSupply` | uint256 | Initial total supply |
| `transferTax` | uint256 | Tax % on each transfer (optional) |
| `maxSupply` | uint256 | Maximum supply cap (optional) |

## Security Best Practices

1. **Test First**: Always deploy to testnet before mainnet
2. **Audit Code**: Have contracts reviewed before production
3. **Secure Keys**: Never commit private keys to version control
4. **Verify Contracts**: Verify source code on block explorer
5. **Limit Permissions**: Use multi-sig for owner functions in production

## Network Information

**Atlantic Testnet:**
- Chain ID: 688689
- Currency: PHRS
- RPC: https://atlantic.dplabs-internal.com
- Explorer: https://atlantic.pharosscan.xyz/

**Pacific Mainnet:**
- Chain ID: 1672
- Currency: PROS
- RPC: https://rpc.pharos.xyz
- Explorer: https://www.pharosscan.xyz

## Testing

```bash
# Run all tests
forge test

# Run specific test
forge test --match-test testTokenName

# Coverage report
forge coverage
```

## License

MIT License

## Contributing

Pull requests welcome! Please follow the existing code style and include tests.

## Resources

- [Pharos Documentation](https://docs.pharos.xyz)
- [Foundry Book](https://book.getfoundry.sh)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts)
- [ERC20 Standard](https://eips.ethereum.org/EIPS/eip-20)
