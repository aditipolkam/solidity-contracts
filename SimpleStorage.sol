//SPDX-Licence-Identifier:<SPDX-License>
pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 favNum; //0

    struct People {
        uint256 favNum;
        string name;
    }

    People public person = People({favNum: 87, name: "Aditi"});

    function store(uint256 _num) public {
        favNum = _num;
    }

    function retrieve() public view returns (uint256) {
        return favNum;
    }
}
