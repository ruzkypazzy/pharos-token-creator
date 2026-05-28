# Pharos Token Creator - Configuration Reference

## Network Configuration

**Atlantic Testnet**
- Chain ID: 688689
- Currency: PHRS
- RPC URL: https://atlantic.dplabs-internal.com
- Explorer: https://atlantic.pharosscan.xyz/

**Pacific Mainnet**
- Chain ID: 1672
- Currency: PROS
- RPC URL: https://rpc.pharos.xyz
- Explorer: https://www.pharosscan.xyz

---

## Token Configuration Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| NAME | string | Full token name | "My Token" |
| SYMBOL | string | Token ticker (3-6 chars) | "MTK" |
| DECIMALS | uint8 | Decimal places | 18 |
| INITIAL_SUPPLY | uint256 | Starting supply | 1000000000000000000000 |
| MAX_SUPPLY | uint256 | Maximum cap | 100000000000000000000000000 |
| TRANSFER_TAX | uint256 | Tax % (0-100) | 5 |

---

## Token Type Selection Guide

### 1. Standard Token
- **Best for**: Simple utility tokens
- **Features**: Basic ERC20 functionality
- **File**: `contracts/StandardToken.sol`

### 2. Burnable Token
- **Best for**: Deflationary tokenomics
- **Features**: Holders can burn tokens
- **File**: `contracts/BurnableToken.sol`

### 3. Mintable Token
- **Best for**: Rewards, inflation control
- **Features**: Owner can mint new tokens
- **File**: `contracts/MintableToken.sol`

### 4. Pausable Token
- **Best for**: Emergency stops, compliance
- **Features**: Owner can pause all transfers
- **File**: `contracts/PausableToken.sol`

### 5. Deflationary Token
- **Best for**: Automatic burning mechanism
- **Features**: Auto-burn on every transfer
- **File**: `contracts/DeflationaryToken.sol`

### 6. Reflect Token
- **Best for**: Dividend-style rewards
- **Features**: Holders earn reflections
- **File**: `contracts/ReflectToken.sol`

### 7. Blacklist Token
- **Best for**: Compliance requirements
- **Features**: Can blacklist addresses
- **File**: `contracts/BlacklistToken.sol`

---

## Deployment Configuration

### Foundry Deployment Commands

**Deploy to Testnet:**
```bash
forge script scripts/DeployStandardToken.s.sol \
  --rpc-url https://atlantic.dplabs-internal.com \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify
```

**Deploy to Mainnet:**
```bash
forge script scripts/DeployStandardToken.s.sol \
  --rpc-url https://rpc.pharos.xyz \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify
```

---

## Post-Deployment Verification

After deploying, verify on block explorer:

1. Go to https://atlantic.pharosscan.xyz/ (testnet) or https://www.pharosscan.xyz (mainnet)
2. Search for your contract address
3. Verify source code (if not auto-verified)
4. Interact with contract using block explorer

---

## Interaction Commands

### Using cast CLI

```bash
# Get token name
cast call <CONTRACT> "name()(string)" --rpc-url $PHAROS_RPC

# Get token symbol
cast call <CONTRACT> "symbol()(string)" --rpc-url $PHAROS_RPC

# Get total supply
cast call <CONTRACT> "totalSupply()(uint256)" --rpc-url $PHAROS_RPC

# Check balance
cast call <CONTRACT> "balanceOf(address)(uint256)" <WALLET> --rpc-url $PHAROS_RPC

# Transfer tokens
cast send <CONTRACT> "transfer(address,uint256)" <RECIPIENT> <AMOUNT> \
  --rpc-url $PHAROS_RPC \
  --private-key $PRIVATE_KEY

# Mint (if mintable)
cast send <CONTRACT> "mint(address,uint256)" <RECIPIENT> <AMOUNT> \
  --rpc-url $PHAROS_RPC \
  --private-key $PRIVATE_KEY

# Burn (if burnable)
cast send <CONTRACT> "burn(uint256)" <AMOUNT> \
  --rpc-url $PHAROS_RPC \
  --private-key $PRIVATE_KEY

# Pause (if pausable)
cast send <CONTRACT> "pause()" \
  --rpc-url $PHAROS_RPC \
  --private-key $PRIVATE_KEY
```

---

## Security Best Practices

1. **Never share private keys**
2. **Test on testnet first**
3. **Audit contracts before production**
4. **Enable 2FA on wallets**
5. **Use multi-sig for owner functions in production**
6. **Verify contract source code on explorer**

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Insufficient funds" | Get testnet PHRS from faucet |
| "Nonce too low" | Reset pending transactions |
| "Contract size too large" | Enable optimizer |
| "Function not found" | Check contract ABI |
| "Invalid chain ID" | Use correct RPC URL |
