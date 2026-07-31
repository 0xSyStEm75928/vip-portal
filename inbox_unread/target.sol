// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SATAN_v.old - Mobile Optimized Core Target Contract
 * @dev ガス代（Gas Cost）を最小化したモバイルフレンドリー設計
 */
contract TargetSatan {
    address public owner;
    bool public isLocked;
    uint32 public lastUpdatedBlock;

    event SyncVerified(address indexed operator, uint32 indexed blockNum);

    modifier onlyOwner() {
        require(msg.sender == owner, "SATAN: Caller is not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function verifyAndLock(bytes32 signature) external {
        require(!isLocked, "SATAN: Already locked");
        require(signature != bytes32(0), "SATAN: Invalid signature");

        isLocked = true;
        lastUpdatedBlock = uint32(block.number);

        emit SyncVerified(msg.sender, uint32(block.number));
    }

    function unlock() external onlyOwner {
        isLocked = false;
    }
}
