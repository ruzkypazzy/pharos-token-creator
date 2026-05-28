# ERC20 Token Templates

## Template 1: Basic Token

```
Name: _______
Symbol: _______
Decimals: 18
Initial Supply: _______
Max Supply: _______
```

## Template 2: Simple Token with Burnable

```
Name: _______
Symbol: _______
Decimals: 18
Initial Supply: _______
Features: Burnable by holders
```

## Template 3: Token with Owner Minting

```
Name: _______
Symbol: _______
Decimals: 18
Initial Supply: _______
Max Supply: _______
Features: Owner can mint new tokens
```

## Template 4: Deflationary Token

```
Name: _______
Symbol: _______
Decimals: 18
Initial Supply: _______
Transfer Tax: ____% (burned automatically)
```

## Template 5: Compliant Token

```
Name: _______
Symbol: _______
Decimals: 18
Initial Supply: _______
Features: Blacklist capability for compliance
```

## Template 6: Reflect Token

```
Name: _______
Symbol: _______
Decimals: 18
Initial Supply: _______
Reflection Rate: ____%
Burn Rate: ____%
Marketing Rate: ____%
Marketing Wallet: _______
```

---

## Quick Fill Templates

### Meme Coin
- Name: _______
- Symbol: _______
- Initial Supply: 1,000,000,000 (1 billion)
- Decimals: 18
- Features: Standard or Burnable

### Governance Token
- Name: _______
- Symbol: _______
- Initial Supply: _______
- Max Supply: 1,000,000,000
- Decimals: 18
- Features: Mintable (for future emissions)

### Stablecoin
- Name: _______
- Symbol: _______
- Initial Supply: _______
- Decimals: 18
- Features: Mintable, Pausable

### Utility Token
- Name: _______
- Symbol: _______
- Initial Supply: _______
- Decimals: 18
- Features: Standard

---

## Formula Reference

### Supply Calculations
```
totalSupply = INITIAL_SUPPLY * 10^DECIMALS
```

### Example
```
1000000 * 10^18 = 1000000000000000000000

In .env format:
INITIAL_SUPPLY=1000000000000000000000
```

### Gas Estimation
```
Deployment cost: ~1,500,000 - 2,000,000 gas
Transfer cost: ~50,000 - 100,000 gas
Mint cost: ~60,000 - 120,000 gas
```
