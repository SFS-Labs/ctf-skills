// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// Absichtlich verwundbar — dient nur dem Nachweis, dass die Skill-Kette greift.
contract Vault {
    mapping(address => uint256) public balances;
    uint256 public totalDeposits;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;
    }

    // Bug 1: state update nach externem Call -> Reentrancy
    function withdraw() public {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "empty");
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");
        balances[msg.sender] = 0;
        totalDeposits -= amount;
    }

    // Bug 2: tx.origin-Autorisierung
    function sweep(address payable to) public {
        require(tx.origin == owner, "not owner");
        to.transfer(address(this).balance);
    }

    // Bug 3: ungepruefter Low-Level-Call, Folgefehler ignoriert
    function forceSend(address target, bytes memory data) public {
        target.call(data);
    }

    // Invariante fuer den Fuzzer: Vertragsguthaben deckt alle Einlagen
    function echidna_solvent() public view returns (bool) {
        return address(this).balance >= totalDeposits;
    }

    // Assertion-Variante fuer Medusa (revertet statt bool zurueckzugeben)
    function assert_solvent() public view {
        require(address(this).balance >= totalDeposits, "insolvent");
    }
}
