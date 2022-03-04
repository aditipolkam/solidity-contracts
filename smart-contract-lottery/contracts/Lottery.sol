// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    address payable[] public players;
    unit256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;

    constructor(address _pricefeed) public {
        usdEntryFee = 5 * (10**18); //wei
        ethUsdPriceFeed = AggregatorV3Interface(_pricefeed);
    }

    function enter() public payable {
        //5$ minimum
        require();
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {}

    function startLottery() public {}

    function endLottery() public {}
}
