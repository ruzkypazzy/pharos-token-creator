#!/usr/bin/env python3
"""
pharos-token-creator — Python wrapper around the Foundry deploy scripts.

This script does NOT deploy to Pharos itself (that requires a
funded signer and a real `forge` install). Instead, it:

  1. Shows the available token templates and their parameters.
  2. Renders the `forge create` command for any (template, params)
     combo, so the agent (or the user) can copy-paste it.
  3. Compiles the contracts if `forge` is installed locally.
  4. Verifies a deployed token on PharosScan if `--address` is given.

Usage:
  python scripts/deploy.py list
  python scripts/deploy.py render --template standard --name "My Token" --symbol MTK --decimals 18 --supply 1000000 --chain mainnet
  python scripts/deploy.py compile
  python scripts/deploy.py verify --address 0x... --chain mainnet
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_DIR = REPO_ROOT / "contracts"

# Token templates exposed by this skill. Each maps a friendly name
# to its constructor signature and the deploy script that drives it.
TEMPLATES = {
    "standard": {
        "label": "Standard ERC-20",
        "ctor": "(string name, string symbol, uint8 decimals, uint256 initialSupply)",
        "script": "script/DeployStandardToken.s.sol",
        "features": ["ERC-20 base", "mint", "burn"],
    },
    "mintable": {
        "label": "Mintable ERC-20 (with cap)",
        "ctor": "(string name, string symbol, uint8 decimals, uint256 initialSupply, uint256 maxSupply)",
        "script": "script/DeployMintableToken.s.sol",
        "features": ["ERC-20 base", "owner-only mint up to cap", "burn"],
    },
    "burnable": {
        "label": "Burnable ERC-20",
        "ctor": "(string name, string symbol, uint8 decimals, uint256 initialSupply)",
        "script": "script/DeployStandardToken.s.sol",
        "features": ["ERC-20 base", "public burn", "uses StandardToken (mint+burn)"],
    },
    "pausable": {
        "label": "Pausable ERC-20",
        "ctor": "(string name, string symbol, uint8 decimals, uint256 initialSupply)",
        "script": "script/DeployPausableToken.s.sol",
        "features": ["ERC-20 base", "owner pause/unpause", "burn"],
    },
    "deflationary": {
        "label": "Deflationary (fee-on-transfer) ERC-20",
        "ctor": "(string name, string symbol, uint8 decimals, uint256 initialSupply, uint256 transferTaxRate)",
        "script": "script/DeployDeflationaryToken.s.sol",
        "features": ["ERC-20 base", "transfer fee (burn)"],
    },
    "blacklist": {
        "label": "Blacklist ERC-20",
        "ctor": "(string name, string symbol, uint8 decimals, uint256 initialSupply)",
        "script": "script/DeployBlacklistToken.s.sol",
        "features": ["ERC-20 base", "owner-managed blacklist", "seize"],
    },
}

CHAINS = {
    "mainnet": {
        "label": "Pharos Pacific Mainnet",
        "chain_id": 1672,
        "rpc": "https://rpc.pharos.xyz",
        "explorer": "https://www.pharosscan.xyz",
        "symbol": "PROS",
    },
    "testnet": {
        "label": "Pharos Atlantic Testnet",
        "chain_id": 688689,
        "rpc": "https://atlantic.dplabs-internal.com",
        "explorer": "https://atlantic.pharosscan.xyz",
        "symbol": "PHRS",
    },
}


def cmd_list(_args: argparse.Namespace) -> int:
    """List all available token templates."""
    print("")
    print("=" * 72)
    print("  pharos-token-creator — available templates")
    print("=" * 72)
    for key, t in TEMPLATES.items():
        print(f"\n  [{key}] {t['label']}")
        print(f"    ctor:  {t['ctor']}")
        print(f"    script: {t['script']}")
        print(f"    features: {', '.join(t['features'])}")
    print("\nUsage:")
    print("  python scripts/deploy.py render --template standard --name MyToken --symbol MTK --supply 1000000 --chain mainnet")
    print("")
    return 0


def _wei(human_amount: float, decimals: int) -> int:
    """Convert a human-readable token amount to raw integer (with decimals).
    Uses Decimal to avoid float precision loss for large amounts like
    1_000_000 tokens with 18 decimals (= 10^24)."""
    from decimal import Decimal
    raw = Decimal(str(human_amount)) * (Decimal(10) ** decimals)
    return int(raw)


def cmd_render(args: argparse.Namespace) -> int:
    """Render the `forge create` command for a (template, params) combo."""
    tpl = TEMPLATES.get(args.template)
    if not tpl:
        print(f"❌ unknown template: {args.template}")
        print(f"   available: {', '.join(TEMPLATES)}")
        return 2
    chain = CHAINS.get(args.chain)
    if not chain:
        print(f"❌ unknown chain: {args.chain}")
        return 2

    decimals = int(args.decimals)
    if decimals < 0 or decimals > 18:
        print(f"❌ invalid decimals: {decimals} (must be 0-18)")
        return 2

    supply_wei = _wei(float(args.supply), decimals)
    if supply_wei <= 0:
        print(f"❌ supply must be > 0 (got {args.supply})")
        return 2

    fee_bps = int(args.fee_bps or 0)
    if args.template == "deflationary" and (fee_bps < 0 or fee_bps > 1000):
        print(f"❌ fee_bps out of range (0-1000, i.e. 0-10%)")
        return 2

    # Build the constructor args based on template
    if args.template in ("standard", "burnable", "pausable", "blacklist"):
        ctor_args = f'"{args.name}" "{args.symbol}" {decimals} {supply_wei}'
    elif args.template == "mintable":
        # 5th arg: maxSupply cap. Default to 10x initial supply so the deployer
        # has headroom to mint 9x more.
        max_supply = int(args.max_supply) if args.max_supply else (supply_wei * 10)
        ctor_args = f'"{args.name}" "{args.symbol}" {decimals} {supply_wei} {max_supply}'
    elif args.template == "deflationary":
        ctor_args = f'"{args.name}" "{args.symbol}" {decimals} {supply_wei} {fee_bps}'
    else:
        ctor_args = ""

    contract_file = CONTRACTS_DIR / tpl["script"].replace("Deploy", "").replace(".s.sol", ".sol")
    # For "mintable" the contract is MintableToken.sol, for "pausable" PausableToken.sol etc.
    name_to_contract = {
        "standard": "StandardToken.sol",
        "mintable": "MintableToken.sol",
        "burnable": "BurnableToken.sol",
        "pausable": "PausableToken.sol",
        "deflationary": "DeflationaryToken.sol",
        "blacklist": "BlacklistToken.sol",
    }
    contract_name = name_to_contract.get(args.template, "StandardToken.sol").replace(".sol", "")
    script_path = REPO_ROOT / tpl["script"]

    # The bash-expansion trap: if you use --private-key $PRIVATE_KEY and the shell
    # expands it, you get --private-key 0xYOURKEY (then forge wants the next arg
    # which is a positional flag, triggering the famous
    # `error: a value is required for '--private-key <RAW_PRIVATE_KEY>'`).
    #
    # The cleanest path is the keystore form: import once with cast wallet import,
    # then use --account deployer. The env-var form (FOUNDRY_PRIVATE_KEY=...) is
    # also safe but puts the key in process env while forge runs.
    cmd = (
        f"# ONE-TIME SETUP (run once, then never need it again):\n"
        f"cast wallet import --private-key 0xYOUR_PRIVATE_KEY --keystore ~/.foundry/keystore deployer\n\n"
        f"# DEPLOY (uses the imported account, no bash trap):\n"
        f"forge create "
        f"--rpc-url {chain['rpc']} "
        f"--account deployer "
        f"--broadcast "
        f"--chain-id {chain['chain_id']} "
    )
    if args.verify:
        cmd += f"--verify "
    cmd += f"--constructor-args {ctor_args} "
    cmd += f"{tpl['script']}:{Path(tpl['script']).name.replace('.s.sol', '')}"

    print("")
    print("=" * 72)
    print(f"  pharos-token-creator — render")
    print("=" * 72)
    print(f"  template:  {tpl['label']}")
    print(f"  chain:     {chain['label']} (chain {chain['chain_id']})")
    print(f"  RPC:       {chain['rpc']}")
    print(f"  explorer:  {chain['explorer']}")
    print(f"  name:      {args.name}")
    print(f"  symbol:    {args.symbol}")
    print(f"  decimals:  {decimals}")
    print(f"  supply:    {float(args.supply):,.0f} ({supply_wei:,} raw)")
    if args.template == "deflationary":
        print(f"  fee_bps:   {fee_bps} ({fee_bps/100:.2f}%)")
    print("")
    print("  Copy-paste this `forge create` command:")
    print("-" * 72)
    print(cmd)
    print("-" * 72)
    print("")
    print("  Required env vars:")
    print("    PRIVATE_KEY   — funded signer on the chosen Pharos chain")
    if args.verify:
        print("    ETHERSCAN_API_KEY  — for contract verification (Pharos uses the socialscan API)")
    print("")
    return 0


def cmd_compile(_args: argparse.Namespace) -> int:
    """Compile the contracts if `forge` is available."""
    forge = shutil.which("forge")
    if not forge:
        print("⚠️  forge (Foundry) not found on PATH.")
        print("   Install: curl -L https://foundry.paradigm.xyz | bash && foundryup")
        print("   Compile step is optional — the skill's value is the template + render workflow.")
        return 0
    print(f"  forge found at {forge}, compiling...")
    res = subprocess.run([forge, "build"], cwd=REPO_ROOT, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("❌ compile failed:")
        print(res.stderr)
        return res.returncode
    print("✅ compile succeeded")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    """Verify a deployed token contract on PharosScan by reading its on-chain state."""
    chain = CHAINS.get(args.chain)
    if not chain:
        print(f"❌ unknown chain: {args.chain}")
        return 2
    if not args.address or not args.address.startswith("0x") or len(args.address) != 42:
        print(f"❌ invalid address: {args.address}")
        return 2

    # 4-byte selectors
    SEL_NAME     = "0x06fdde03"  # name()
    SEL_SYMBOL   = "0x95d89b41"  # symbol()
    SEL_DECIMALS = "0x313ce567"  # decimals()
    SEL_TOTAL    = "0x18160ddd"  # totalSupply()

    def eth_call(data: str) -> str | None:
        payload = json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "eth_call",
            "params": [{"to": args.address, "data": data}, "latest"],
        }).encode()
        req = urllib.request.Request(chain["rpc"], data=payload, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                resp = json.loads(r.read())
        except Exception as e:
            print(f"  ! RPC error on selector {data[:10]}: {e}")
            return None
        return resp.get("result")

    def hex_to_str(h: str) -> str:
        if h is None or h == "0x" or len(h) < 66: return ""
        # ABI-encoded string: offset (32) + length (32) + data
        try:
            length = int(h[66:130], 16)
            data = bytes.fromhex(h[130:130 + 2*length])
            return data.decode("utf-8", errors="replace")
        except Exception:
            return ""

    def hex_to_int(h: str) -> int:
        if h is None: return 0
        return int(h, 16)

    name_h   = eth_call(SEL_NAME)
    sym_h    = eth_call(SEL_SYMBOL)
    dec_h    = eth_call(SEL_DECIMALS)
    tot_h    = eth_call(SEL_TOTAL)

    name   = hex_to_str(name_h) or "?"
    symbol = hex_to_str(sym_h) or "?"
    decimals = hex_to_int(dec_h)
    total  = hex_to_int(tot_h) / (10 ** decimals if decimals else 1)

    print("")
    print("=" * 72)
    print(f"  pharos-token-creator — verify deployed contract")
    print("=" * 72)
    print(f"  chain:    {chain['label']} (chain {chain['chain_id']})")
    print(f"  address:  {args.address}")
    print(f"  explorer: {chain['explorer']}/address/{args.address}")
    print(f"  name:     {name}")
    print(f"  symbol:   {symbol}")
    print(f"  decimals: {decimals}")
    print(f"  total:    {total:,.4f} {symbol}")
    print("")

    if name == "?" and symbol == "?":
        print("  ⚠️  Could not read name/symbol — address may not be a deployed ERC-20.")
        return 1
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="pharos-token-creator — Python wrapper for Foundry token deploys on Pharos",
    )
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("list", help="List all available token templates")
    sub.add_parser("compile", help="Compile the contracts (requires `forge`)")

    pr = sub.add_parser("render", help="Render the `forge create` command for a template + params")
    pr.add_argument("--template", required=True, choices=list(TEMPLATES))
    pr.add_argument("--chain", default="mainnet", choices=list(CHAINS))
    pr.add_argument("--name", required=True)
    pr.add_argument("--symbol", required=True)
    pr.add_argument("--decimals", default="18")
    pr.add_argument("--supply", required=True, help="human amount, e.g. 1000000")
    pr.add_argument("--fee-bps", default="0", help="deflationary template only (0-1000)")
    pr.add_argument("--max-supply", default="", help="mintable template only (defaults to 10x supply)")
    pr.add_argument("--verify", action="store_true", help="also verify on PharosScan after deploy")

    pv = sub.add_parser("verify", help="Verify a deployed token on PharosScan")
    pv.add_argument("--address", required=True)
    pv.add_argument("--chain", default="mainnet", choices=list(CHAINS))

    args = p.parse_args()
    if args.cmd == "list":   return cmd_list(args)
    if args.cmd == "render": return cmd_render(args)
    if args.cmd == "compile": return cmd_compile(args)
    if args.cmd == "verify": return cmd_verify(args)

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
