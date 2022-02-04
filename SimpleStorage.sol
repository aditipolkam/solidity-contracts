//SPDX-Licence-Identifier:<SPDX-License>
pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 public favNum; //0

    function store(uint256 _num) public {
        favNum = _num;
    }
}
