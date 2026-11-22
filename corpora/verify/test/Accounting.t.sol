// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Solvency.t.sol";

/// Orakel fuer die Eigenschaft, die die Aggregat-Invariante strukturell nicht sieht.
///
/// `echidna_solvent()` vergleicht `address(this).balance` mit `totalDeposits`. Beim
/// Reentrancy-Drain sinkt `totalDeposits` im Gleichschritt mit dem Guthaben, deshalb
/// bleibt die Invariante wahr. Verletzt ist die Deckung der individuellen
/// Einlageforderung: `balances[depositor] > address(vault).balance`.
contract AccountingTest {
    Vault vault;

    function setUp() public {
        vault = new Vault();
    }

    function test_aggregate_invariant_blind_to_reentrancy() public payable {
        vault.deposit{value: 2 ether}();
        uint256 before = address(vault).balance; // 2 ETH ehrliche Einlage

        Attacker atk = new Attacker(vault);
        atk.attack{value: 1 ether}();

        // Gemessene Auszahlung: Vault-Delta, kein angenommener Absolutwert.
        uint256 paidOut = before + 1 ether - address(vault).balance;

        // 1. Aggregat-Invariante haelt weiterhin — sie ist fuer den Diebstahl blind.
        require(vault.echidna_solvent(), "Aggregat-Invariante muss scheinbar halten");
        require(vault.totalDeposits() == 0, "Zaehler sinkt im Gleichschritt");

        // 2. Der Vault hat mehr ausbezahlt, als der Angreifer eingezahlt hat.
        require(paidOut == 3 ether, "drei Auszahlungen zu je 1 ETH");
        require(paidOut > 1 ether, "Auszahlung groesser als Einlage");

        // 3. Die Einlageforderung des ehrlichen Nutzers ist nicht mehr gedeckt.
        require(vault.balances(address(this)) == 2 ether, "Forderung unveraendert");
        require(address(vault).balance == 0, "Vault-Guthaben nach Drain");
        require(
            vault.balances(address(this)) > address(vault).balance,
            "Deckungsluecke muss messbar sein"
        );
        require(atk.calls() == 2, "Reentrancy muss zweimal auszahlen");
    }

    receive() external payable {}
}
