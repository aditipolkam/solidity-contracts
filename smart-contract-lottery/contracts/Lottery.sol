// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6 <0.8.8;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is Ownable, VRFConsumerBase {
    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyHash;

    constructor(
        address _pricefeed,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18); //wei
        ethUsdPriceFeed = AggregatorV3Interface(_pricefeed);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }

    function enter() public payable {
        require(LOTTERY_STATE.OPEN == lottery_state);
        require(
            msg.value >= getEntranceFee(),
            "You must pay at least 50$ worth ETH"
        );
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10;
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            LOTTERY_STATE.CLOSED == lottery_state,
            "Lottery is already open"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            LOTTERY_STATE.CALCULATING_WINNER == lottery_state,
            "Lottery is not open"
        );
        require(_randomness > 0, "Randomness must be positive");
        uint256 winnerIndex = _randomness % players.length;
        address payable recentWinner = players[winnerIndex];
        recentWinner.transfer(address(this).balance);
        lottery_state = LOTTERY_STATE.CLOSED;
        players = new address payable[](0);
        //send(winner, msg.value);
    }
}
