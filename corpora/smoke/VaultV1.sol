// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/// v1 der corpora/verify-Vorlage: Verwundbar (state update nach externem Call).
contract Vault {
    mapping(address => uint256) public balances;
    uint256 public totalDeposits;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;
    }

    function withdraw() public {
        uint256 amount = balances[msg.sender];
        require(amount > 0);
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok);
        balances[msg.sender] = 0;
        totalDeposits -= amount;
    }
}
