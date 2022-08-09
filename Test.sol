// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// Read/write number, accept ether
contract Test {
    receive() external payable {}

    uint256 public number = 0;

    function setNumber(uint256 value) public {
        number = number + value;
    }
}
