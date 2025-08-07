// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

/// @notice Caller does not have the CONTROLLER role.
error NotController(address caller);

/// @notice Caller does not have the ADMIN role.
error NotAdmin(address caller);

/// @notice Wrong inputed address.
error AddressZero();

/// @notice AvailableERC721Ids does not match with lotAmount .
error MismatchERC721PrizeAmount(uint256 lotAmount, uint256 erc721PrizeAmount);

/// @notice Prize is not a contract.
error InvalidPrize(address prizeAddress);

/// @notice Prize amount exceeds token balance of contract.
error PrizeAmountExceedsBalance(address prizeAddress, uint256 prizeAmount, uint256 contractBalance);

/// @notice ERC721 with tokenId is not owned by this contract.
error TokenNotOwnedByContract(address prizeAddress, uint256 tokenId);

/// @notice Message signer is not allowed.
error SignerNotAllowed(address signer);

/// @notice Nonce was already used.
error NonceAlreadyUsed(uint256 nonce);

/// @notice Signature has expired.
error SignatureExpired(uint256 expirationTimestamp, uint256 currentTimestamp);

/// @notice Used request ID is invalid.
error InvalidRequestId(uint256 requestId);

/// @notice User has not won that prize Id.
error PrizeNotWonByUser(uint32 prizeId, address user);

/// @notice Vrf request has not expired yet.
error VrfRequestHasNotExpired(uint256 expirationTimestamp);

/// @notice ERC20 prize should not have ERC721 related parameter.
error ERC20PrizeWrongParam();

/// @notice Sum of prizes probabilities exceeded max probability.
error MaxProbabilityExceeded(uint256 totalProbabilities);

/// @notice Transfer of native token prize failed.
error NativeTokenTransferFailed();

/// @notice Invalid lot amount for a prize.
error InvalidLotAmount();

/// @title SpinGame
/// @dev Interface for a prize-based spin game.
interface ISpinGame {
    /// @notice Structure representing a prize.
    struct Prize {
        uint32 lotAmount; // Amount of lots of this prize.
        uint64 probability; // Probability of winning this reward.
        address tokenAddress; // ERC721 or ERC20 contract address.
        uint256 amount; // Amount of tokens to send (ERC20).
        uint256[] availableERC721Ids; // List of available ERC721 IDs.
    }

    /// @notice Structure representing an ECDSA signature.
    struct Signature {
        bytes32 r;
        bytes32 s;
        uint8 v;
    }

    /// @notice Structure defining data signed on a participation.
    struct ParticipationRequest {
        address user;
        uint256 expirationTimestamp;
        uint64 nonce;
        uint64 boost;
    }

    /// @notice Emitted when a new batch of prizes is updated.
    /// @param newPrizeIds The ids of the new prizes.
    /// @param prizes The prizes that got updated.
    event PrizesUpdated(uint32[] newPrizeIds, Prize[] prizes);

    /// @notice Emitted when a user wins a prize.
    event PrizeWon(address indexed user, uint32 indexed prizeId);

    /// @notice Emitted when a user does not win any prize.
    event NoPrizeWon(address indexed user);

    /// @notice Emitted when a new signer is set.
    event SignerUpdated(address signer);

    /// @notice Emitted when a new vrfOperator is set.
    event vrfOperatorUpdated(address vrfOperator);

    /// @notice Emitted when a new participation is registered.
    event Participation(address indexed user, uint256 requestId, uint64 nonce, uint256 expirationTimestamp, uint64 boost);

    /// @notice Emitted when a participation is cancelled.
    event ParticipationCancelled(address user, uint256 requestId);

    /// @notice Emitted when a prize is claimed.
    event PrizeClaimed(address indexed user, uint32 prizeId);

}