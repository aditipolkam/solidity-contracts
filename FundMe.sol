//SPDX-Licence-Identifier: MIT

pragma solidity >0.6.6 <0.9.0;

interface AggregatorV3Interface {
    function decimals() external view returns (uint8);

    function description() external view returns (string memory);

    function version() external view returns (uint256);

    function getRoundData(
        uint80 _roundId
    )
        external
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );

    function latestRoundData()
        external
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );
}

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;
    address public owner;
    address[] public funders;

    constructor() {
        owner = msg.sender;
    }

    function fund() public payable {
        uint256 minimumUSD = 5 * (10 ** 18);
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more eth."
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x9326BFA02ADD2366b30bacB125260Af641031331
        );
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x9326BFA02ADD2366b30bacB125260Af641031331 //contract address of aggregator - eth->USD
        );
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        //314373126523 price of eth returned by answer having 8 decimal places
        return uint256(answer * 10000000000); //18 decimal places
    }

    //1000000000
    function getConversionRate(
        uint256 ethAmount
    ) public view returns (uint256) {
        uint256 ethPrice = getPrice(); //18 decimal places
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000; //current price of eth * amount of eth sent
        return ethAmountInUsd; //amount of eth sent in USD
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
