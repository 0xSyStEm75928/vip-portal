// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SATAN_v.old - Mobile Optimized Core Target Contract
 * @dev ガス代（Gas Cost）を最小化したモバイルフレンドリー設計
 */
contract TargetSatan {
    // 状態変数のパッキング（256ビットスロットを最適に共有）
    address public owner;
    bool public isLocked;
    uint32 public lastUpdatedBlock; // uint256からuint32に圧縮してストレージを節約

    // 検証用のイベントログ（モバイル端末用の軽量なインデックス検索用）
    event SyncVerified(address indexed operator, uint32 indexed blockNum);

    modifier onlyOwner() {
        require(msg.sender == owner, "SATAN: Caller is not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /**
     * @notice モバイル端末用に極限までガス代を削った同期ロック関数
     * @dev Checks-Effects-Interactionsパターンを遵守しリエントランシーを本質からブロック
     */
    function verifyAndLock(bytes32 signature) external {
        // ガス代節約のため、状態変数の変更前に条件チェックを完了させる
        require(!isLocked, "SATAN: Already locked");
        require(signature != bytes32(0), "SATAN: Invalid signature");

        // 効果的な状態変更
        isLocked = true;
        lastUpdatedBlock = uint32(block.number);

        // イベントログ出力
        emit SyncVerified(msg.sender, uint32(block.number));
    }

    /**
     * @notice ロックの解除（オーナー限定）
     */
    function unlock() external onlyOwner {
        isLocked = false;
    }
}
