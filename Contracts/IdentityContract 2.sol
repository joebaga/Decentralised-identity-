// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract IdentityContract is Ownable, AccessControl {
    
    struct Person {
        address adr;
        int256 count;  // Tracks incidents or attempts
    }

    // Mapping to record users with flagged behavior
    mapping(address => Person) public illegalBehavior;

    // Define access roles and events for tracking actions
    bytes32 public constant SPECIAL_ROLE = keccak256("SPECIAL_ROLE");

    event SuccessfulAccess(address indexed account);
    event FailedAccess(address indexed account);
    event AccessDenied(address indexed account);

    // Constructor to set the admin role to the contract deployer
    constructor() public {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    // Function to check a user’s role and handle behavior tracking
    function checkUser(bytes32 role, address account) public {
        require(account != address(0), "Invalid account address");

        if (hasRole(role, msg.sender)) {
            emit SuccessfulAccess(account);
        } else {
            emit FailedAccess(account);
            illegalBehavior[account].adr = account;
            illegalBehavior[account].count += 1;

            // Deny access if the user exceeds 5 failed attempts
            if (illegalBehavior[account].count > 5) {
                emit AccessDenied(account);
            }
        }
    }

    // Additional functionality for role assignment 
    function grantSpecialRole(address account) public onlyOwner {
        grantRole(SPECIAL_ROLE, account);
    }

    function revokeSpecialRole(address account) public onlyOwner {
        revokeRole(SPECIAL_ROLE, account);
    }
}
