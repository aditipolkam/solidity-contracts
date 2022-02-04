pragma solidity ^0.6.0;

contract Bank {
    struct Account {
        uint256 accountNumber;
        string accountHolder;
        uint256 accountBalance;
    }

    Account[] private accounts;
    mapping(uint256 => uint256) public accountNoToBalance;

    function addAccount(
        uint256 _accountNumber,
        string memory _accountHolder,
        uint256 _accountBalance
    ) public {
        accounts.push(Account(_accountNumber, _accountHolder, _accountBalance));
        accountNoToBalance[_accountNumber] = _accountBalance;
    }

    function withdraw(uint256 _accountNumber, uint256 amount) public {
        accountNoToBalance[_accountNumber] =
            accountNoToBalance[_accountNumber] -
            amount;
    }

    function deposit(uint256 _accountNumber, uint256 amount) public {
        accountNoToBalance[_accountNumber] =
            accountNoToBalance[_accountNumber] +
            amount;
    }
}
