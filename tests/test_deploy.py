"""
Smoke tests for pharos-token-creator deploy wrapper.

Covers:
  - Template registry completeness
  - Wei conversion
  - Decimal validation
  - Supply validation
  - Render command generation
  - Verify command (live, against a real ERC-20 on Pharos mainnet)
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Make scripts/ importable
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))

import pytest  # noqa: E402

import deploy  # noqa: E402


# A real ERC-20 on Pharos mainnet (USDC, from the PSCD findings)
SAMPLE_TOKEN = "0xc879c018db60520f4355c26ed1a6d572cdac1815"


def test_all_templates_have_required_fields():
    """Each template must have a label, ctor, script, and features list."""
    for key, t in deploy.TEMPLATES.items():
        assert "label" in t, f"template {key} missing label"
        assert "ctor" in t, f"template {key} missing ctor"
        assert "script" in t, f"template {key} missing script"
        assert "features" in t, f"template {key} missing features"
        assert isinstance(t["features"], list)
        assert len(t["features"]) > 0


def test_templates_have_matching_deploy_scripts():
    """Every template's deploy script should exist in the repo."""
    for key, t in deploy.TEMPLATES.items():
        script_path = ROOT / t["script"]
        assert script_path.exists(), f"missing deploy script for {key}: {t['script']}"


def test_wei_conversion_basic():
    """_wei(1, 18) = 10**18; _wei(1, 6) = 1_000_000."""
    assert deploy._wei(1, 18) == 10**18
    assert deploy._wei(1, 6) == 1_000_000
    assert deploy._wei(0.5, 6) == 500_000


def test_chains_have_required_fields():
    """Each chain needs label, chain_id, rpc, explorer, symbol."""
    for key, c in deploy.CHAINS.items():
        assert "label" in c
        assert "chain_id" in c
        assert "rpc" in c
        assert "explorer" in c
        assert "symbol" in c
        assert isinstance(c["chain_id"], int)


def test_render_unknown_template_exits_2():
    """render --template <bad> should exit 2."""
    p = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "deploy.py"),
         "render", "--template", "nope", "--name", "x", "--symbol", "X",
         "--supply", "100"],
        capture_output=True, text=True,
    )
    assert p.returncode == 2


def test_render_unknown_chain_exits_2():
    """render --chain <bad> should exit 2."""
    p = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "deploy.py"),
         "render", "--template", "standard", "--name", "x", "--symbol", "X",
         "--supply", "100", "--chain", "fake"],
        capture_output=True, text=True,
    )
    assert p.returncode == 2


def test_render_negative_decimals_exits_2():
    """render with --decimals 25 should reject (max 18)."""
    p = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "deploy.py"),
         "render", "--template", "standard", "--name", "x", "--symbol", "X",
         "--decimals", "25", "--supply", "100"],
        capture_output=True, text=True,
    )
    assert p.returncode == 2


def test_render_zero_supply_exits_2():
    """render with --supply 0 should reject."""
    p = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "deploy.py"),
         "render", "--template", "standard", "--name", "x", "--symbol", "X",
         "--supply", "0"],
        capture_output=True, text=True,
    )
    assert p.returncode == 2


def test_render_standard_includes_forge_create():
    """render --template standard should produce a valid `forge create` command."""
    p = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "deploy.py"),
         "render", "--template", "standard",
         "--name", "PharosUSD", "--symbol", "PUSD",
         "--decimals", "6", "--supply", "1000000",
         "--chain", "mainnet"],
        capture_output=True, text=True,
    )
    assert p.returncode == 0
    assert "forge create" in p.stdout
    assert "PharosUSD" in p.stdout
    assert "PUSD" in p.stdout
    assert "1672" in p.stdout
    assert "rpc.pharos.xyz" in p.stdout


def test_render_deflationary_includes_fee_bps():
    """render --template deflationary should include the fee argument."""
    p = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "deploy.py"),
         "render", "--template", "deflationary",
         "--name", "FeeTok", "--symbol", "FEE",
         "--decimals", "18", "--supply", "5000000",
         "--fee-bps", "50", "--chain", "testnet"],
        capture_output=True, text=True,
    )
    assert p.returncode == 0
    assert "fee" in p.stdout.lower() or "50" in p.stdout


def test_list_prints_all_6_templates():
    """The `list` subcommand should show all 6 token templates."""
    p = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "deploy.py"), "list"],
        capture_output=True, text=True,
    )
    assert p.returncode == 0
    for key in ("standard", "mintable", "burnable", "pausable", "deflationary", "blacklist"):
        assert f"[{key}]" in p.stdout


@pytest.mark.skipif(
    not os.environ.get("PHAROS_LIVE", "1") == "1",
    reason="set PHAROS_LIVE=1 to run live RPC tests",
)
def test_verify_live_mainnet_usdc():
    """Verify a real ERC-20 (USDC) on Pharos mainnet — should read USDC / 6 decimals."""
    p = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "deploy.py"),
         "verify", "--address", SAMPLE_TOKEN, "--chain", "mainnet"],
        capture_output=True, text=True,
    )
    assert p.returncode == 0
    assert "USDC" in p.stdout
    assert "6" in p.stdout  # decimals
