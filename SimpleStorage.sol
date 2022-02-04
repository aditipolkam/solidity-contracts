//SPDX-Licence-Identifier:<SPDX-License>
pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 favNum; //0

    function storeNum(uint256 num) public {
        favNum = num;
    }
}
