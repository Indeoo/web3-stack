// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {IERC721} from "@openzeppelin/contracts/interfaces/IERC721.sol";
import {IERC20} from "@openzeppelin/contracts/interfaces/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {AccessControlUpgradeable} from "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import {EIP712Upgradeable} from "@openzeppelin/contracts-upgradeable/utils/cryptography/EIP712Upgradeable.sol";
import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import {ERC2771ContextUpgradeable, ContextUpgradeable} from "@openzeppelin/contracts-upgradeable/metatx/ERC2771ContextUpgradeable.sol";
import {GelatoVRFConsumerBase} from "@gelato/contracts/GelatoVRFConsumerBase.sol";

import "./interfaces/ISpin.sol";

/// @title SpinGame
/// @dev A contract for a prize-based spin game.
contract SpinGame is
    ISpinGame,
    ERC2771ContextUpgradeable,
    AccessControlUpgradeable,
    EIP712Upgradeable,
    GelatoVRFConsumerBase
{
    using SafeERC20 for IERC20;

    bytes32 public constant CONTROLLER_ROLE =
        0x7b765e0e932d348852a6f810bfa1ab891e259123f02db8cdcde614c570223357; //keccak256("CONTROLLER_ROLE");

    uint256 public constant BASE_POINT = 1e8;
    string private constant _SIGNING_DOMAIN = "SpinGame";
    string private constant _SIGNATURE_VERSION = "1";

    /// @dev This gap exists at this location to cater for Gelato changes based on an audit finding.
    uint256[50] private __gelatoBuffer;

    /// @notice Next available prize ID to be assigned.
    uint32 public nextPrizeId;

    /// @notice Sum of all prizes probabilities.
    uint64 public totalProbabilities;

    /// @notice Signer address that is signing payloads.
    address public signer;

    /// @notice VRF operator address.
    address public vrfOperator;

    /// @notice Maps VRF request ID to the user who initiated the spin.
    mapping(uint256 requestId => address user) public requestIdToUser;

    /// @notice Maps VRF request ID to their emission timestamp.
    mapping(uint256 requestId => uint256 timestamp) public requestIdTimestamp;

    /// @notice Maps user to his latest boost to be reused in VRF call.
    mapping(address user => uint64 boost) public userToBoost;

    /// @notice Maps user nonce to whether they have been used.
    mapping(address user => mapping(uint64 nonce => bool used)) public nonces;

    /// @notice List of prize Ids.
    uint32[] public prizeIds;

    /// @notice Maps user to his won prizes. (userAddress => prizeId => amountOfPrizeIdWon).
    mapping(address user => mapping(uint256 prizeId => uint256 numberOfPrizes))
        private userToPrizesWon;

    /// @notice Mapping of prize IDs to Prize details.
    mapping(uint32 prizeId => Prize prize) private prizes;

    /// @custom:oz-upgrades-unsafe-allow constructor
    /// @dev This is required for the upgradeable contract to work with the ERC2771ContextUpgradeable contract.
    constructor(address _trustedForwarderAddress) ERC2771ContextUpgradeable(_trustedForwarderAddress) {
        _disableInitializers();
    }

    /// @param _signer Admin address that is signing payloads.
    /// @param _admin Contract administrator.
    /// @param _controller Gelato controller address that can update prizes.
    /// @param _vrfOperator VRF operator address that will be used to provide randomness.
    function initialize(
        address _signer,
        address _admin,
        address _controller,
        address _vrfOperator
    ) public initializer {
        if(_signer == address(0)) {
            revert AddressZero();
        }

        if(_admin == address(0)) {
            revert AddressZero();
        }

        if(_controller == address(0)) {
            revert AddressZero();
        }

        if(_vrfOperator == address(0)) {
            revert AddressZero();
        }

        __EIP712_init(_SIGNING_DOMAIN, _SIGNATURE_VERSION);
        __AccessControl_init();

        signer = _signer;
        vrfOperator = _vrfOperator;

        _grantRole(DEFAULT_ADMIN_ROLE, _admin);
        _grantRole(CONTROLLER_ROLE, _controller);
    }

    /// @notice Ensures only those with the CONTROLLER_ROLE can call certain functions.
    modifier onlyController() {
        if (!hasRole(CONTROLLER_ROLE, _msgSender())) {
            revert NotController(_msgSender());
        }
        _;
    }

    /// @notice Ensures only those with the DEFAULT_ADMIN_ROLE can call certain functions.
    modifier onlyAdmin() {
        if (!hasRole(DEFAULT_ADMIN_ROLE, _msgSender())) {
            revert NotAdmin(_msgSender());
        }
        _;
    }

    /// @notice Returns a prize with specific Id from the contract.
    /// @param _prizeId Id of the prize to retrieve information for.
    /// @return Prize The selected prize.
    function getPrize(uint32 _prizeId) external view returns (Prize memory) {
        return prizes[_prizeId];
    }

    /// @notice Returns amounts of prize won for a list of prizeId.
    /// @param _user Address of the user to check.
    /// @param _prizeIds List of prize Ids to check.
    /// @return Number of times each prize was won by the user.
    function getUserPrizesWon(
        address _user,
        uint32[] calldata _prizeIds
    ) external view returns (uint256[] memory) {
        uint256[] memory amounts = new uint256[](_prizeIds.length);
        uint256 len = _prizeIds.length;
        for (uint256 i; i < len; i++) {
            amounts[i] = userToPrizesWon[_user][_prizeIds[i]];
        }
        return amounts;
    }

    /// @notice Returns whether a user has won at least one prize with specific prizeId.
    /// @param _user Address of the user to check.
    /// @param _prizeId Id of the prize to check.
    /// @return If user has won prizeId.
    function hasWonPrize(
        address _user,
        uint32 _prizeId
    ) external view returns (bool) {
        return userToPrizesWon[_user][_prizeId] != 0;
    }

    /// @notice Returns the number of different prizes available.
    /// @return PrizesAmount The amount of prizes available.
    function getPrizesAmount() external view returns (uint256) {
        return prizeIds.length;
    }

    /// @notice Setter for vrf Operator.
    /// @param _vrfOperator Address to set.
    function setVrfOperator(address _vrfOperator) external onlyAdmin {
        if (_vrfOperator == address(0)) {
            revert AddressZero();
        }
        vrfOperator = _vrfOperator;
        emit vrfOperatorUpdated(_vrfOperator);
    }

    /// @notice Setter for signer.
    /// @param _signer Address to set.
    function setSigner(address _signer) external onlyAdmin {
        if (_signer == address(0)) {
            revert AddressZero();
        }
        signer = _signer;
        emit SignerUpdated(_signer);
    }

    /// @notice Sets the current prize list. Can only be called by a controller.
    /// @dev Stores the current prize details in contract state. Prizes can be ERC20 or ERC721.
    /// @param _prizes Prizes to set.
    function setPrizes(Prize[] calldata _prizes) external onlyController {
        totalProbabilities = 0;
        _addPrizes(_prizes);
    }

    /// @notice Allows a user to participate in the game.
    /// @dev This function will trigger a random draw mechanism.
    /// @param _nonce A unique identifier for the user's spin.
    /// @param _expirationTimestamp Timestamp indicating when the request expires.
    /// @param _boost Probabilities boost for user.
    /// @param _signature A signature verifying the request.
    function participate(
        uint64 _nonce,
        uint256 _expirationTimestamp,
        uint64 _boost,
        Signature calldata _signature
    ) external returns (uint256) {
        address user = _msgSender();
        if (nonces[user][_nonce]) {
            revert NonceAlreadyUsed(_nonce);
        }
        if (block.timestamp >= _expirationTimestamp) {
            revert SignatureExpired(_expirationTimestamp, block.timestamp);
        }

        nonces[user][_nonce] = true;

        address recoveredSigner = ECDSA.recover(
            _hashParticipation(user, _expirationTimestamp, _nonce, _boost),
            _signature.v,
            _signature.r,
            _signature.s
        );
        address signer_ = signer;
        if (recoveredSigner != signer_ || signer_ == address(0)) {
            revert SignerNotAllowed(recoveredSigner);
        }

        userToBoost[user] = _boost;

        uint256 requestId = _requestRandomness("");

        requestIdToUser[requestId] = user;
        requestIdTimestamp[requestId] = block.timestamp;

        emit Participation(
            user,
            requestId,
            _nonce,
            _expirationTimestamp,
            _boost
        );
        return requestId;
    }

    /// @notice Allows a user to claim a prize after it has been picked.
    /// @dev Has to be called after VRF callback.
    /// @param _prizeId Id of the prize to claim.
    function claimPrize(
        uint32 _prizeId
    ) external {
        address user = _msgSender();

        if (userToPrizesWon[user][_prizeId] == 0) {
            revert PrizeNotWonByUser(_prizeId, user);
        }

        unchecked {
            // Previous condition checks for > 0.
            userToPrizesWon[user][_prizeId] -= 1;
        }

        _transferPrize(user, _prizeId);
        emit PrizeClaimed(user, _prizeId);
    }

    /// @dev Admin function to withdraw ERC20 tokens from the contract.
    /// @param _tokenAddress The address of the ERC20 token to withdraw.
    /// @param _amount Amount of tokens to withdraw.
    function adminWithdrawERC20(
        address _tokenAddress,
        uint256 _amount
    ) external onlyAdmin {
        IERC20(_tokenAddress).safeTransfer(_msgSender(), _amount);
    }

    /// @dev Admin function to withdraw Native token from the contract.
    /// @param _amount Amount of tokens to withdraw.
    function adminWithdrawNative(uint256 _amount) external onlyAdmin {
        (bool success, ) = _msgSender().call{value: _amount}("");
        if (!success) {
            revert NativeTokenTransferFailed();
        }
    }

    /// @dev Admin function to withdraw ERC721 tokens from the contract.
    /// @param _tokenAddress The address of the ERC721 token to withdraw.
    /// @param _tokenIds Token IDs to withdraw.
    function adminWithdrawERC721(
        address _tokenAddress,
        uint256[] calldata _tokenIds
    ) external onlyAdmin {
        address sender = _msgSender();
        uint256 len = _tokenIds.length;
        for (uint256 i; i < len; i++) {
            IERC721(_tokenAddress).safeTransferFrom(
                address(this),
                sender,
                _tokenIds[i]
            );
        }
    }

    /// @notice To be called if a vrf request has failed.
    /// @dev Will cancel users current participation request.
    /// @param _requestId The failing vrf requestId.
    function cancelParticipation(uint256 _requestId) external onlyAdmin {
        address user = requestIdToUser[_requestId];
        if (user == address(0)) {
            revert InvalidRequestId(_requestId);
        }
        if (block.timestamp - requestIdTimestamp[_requestId] < 1 hours) {
            revert VrfRequestHasNotExpired(
                requestIdTimestamp[_requestId] + 1 hours
            );
        }
        delete requestIdToUser[_requestId];
        delete userToBoost[user];
        delete requestIdTimestamp[_requestId];

        emit ParticipationCancelled(user, _requestId);
    }

    /// @notice Receives ETH to facilitate ETH-based prizes.
    receive() external payable {}

    /// @notice Transfers a prize to the winning user.
    /// @dev Can transfer either an ERC20 or ERC721 token.
    /// @param _winner The address of the prize recipient.
    /// @param _prizeId The ID of the prize being transferred.
    function _transferPrize(address _winner, uint32 _prizeId) internal {
        Prize storage prize = prizes[_prizeId];
        address tokenAddress = prize.tokenAddress;
        uint256 prizeAmount = prize.amount;

        if (prizeAmount > 0) {
            // Native token
            if (prize.tokenAddress == address(0)) {
                uint256 contractBalance = address(this).balance;
                if (contractBalance < prizeAmount) {
                    revert PrizeAmountExceedsBalance(
                        tokenAddress,
                        prizeAmount,
                        contractBalance
                    );
                }
                (bool success, ) = _winner.call{value: prizeAmount}("");
                if (!success) {
                    revert NativeTokenTransferFailed();
                }
            } else {
                uint256 contractBalance = IERC20(tokenAddress).balanceOf(
                    address(this)
                );
                if (contractBalance < prizeAmount) {
                    revert PrizeAmountExceedsBalance(
                        tokenAddress,
                        prizeAmount,
                        contractBalance
                    );
                }
                IERC20(tokenAddress).safeTransfer(_winner, prizeAmount);
            }
        } else {
            uint256 tokenId = prize.availableERC721Ids[
                prize.availableERC721Ids.length - 1
            ];
            if (IERC721(tokenAddress).ownerOf(tokenId) != address(this)) {
                revert TokenNotOwnedByContract(tokenAddress, tokenId);
            }

            prize.availableERC721Ids.pop();
            IERC721(tokenAddress).safeTransferFrom(
                address(this),
                _winner,
                tokenId
            );
        }
    }

    /// @notice Generates the EIP-712 hash for a participation request.
    /// @param _user The user participating.
    /// @param _expirationTimestamp Timestamp indicating when the request expires.
    /// @param _nonce A unique identifier for the user's spin.
    /// @param _boost Probabilities boost for user.
    /// @return participationHash EIP-712 participation hash.
    function _hashParticipation(
        address _user,
        uint256 _expirationTimestamp,
        uint64 _nonce,
        uint64 _boost
    ) internal view returns (bytes32 participationHash) {
        assembly ("memory-safe") {
            let mPtr := mload(0x40)
            mstore(
                mPtr,
                0x76a8e8adf20e8e3846fb3b3a191f9794668970776c24d0fd46a10c745e485bfe // keccak256("ParticipationRequest(address user,uint256 expirationTimestamp,uint64 nonce,uint64 boost)")
            )
            mstore(add(mPtr, 0x20), _user)
            mstore(add(mPtr, 0x40), _expirationTimestamp)
            mstore(add(mPtr, 0x60), _nonce)
            mstore(add(mPtr, 0x80), _boost)
            participationHash := keccak256(mPtr, 0xa0)
        }

        participationHash = _hashTypedDataV4(participationHash);
    }

    /// @notice Returns the address of the VRF operator authorized to fulfill randomness requests.
    /// @dev The operator can be found on the Gelato dashboard after a VRF is deployed.
    /// @return Address of the operator.
    function _operator() internal view override returns (address) {
        return vrfOperator;
    }

    /// @notice Internal function to add prizes.
    /// @dev Replacing prizes does not affect claimed or unclaimed prizes by users who won them.
    /// @param _prizes Prizes to replace all existing prizes with.
    function _addPrizes(Prize[] calldata _prizes) internal {
        uint256 len = _prizes.length;
        uint32 currentPrizeId = nextPrizeId;
        uint64 totalProbIncrease;

        uint32[] memory newPrizeIds = new uint32[](len);

        for (uint256 i; i < len; i++) {
            address tokenAddress = _prizes[i].tokenAddress;

            if (
                _prizes[i].tokenAddress.code.length == 0 &&
                _prizes[i].tokenAddress != address(0)
            ) {
                revert InvalidPrize(_prizes[i].tokenAddress);
            }

            uint256 erc721IdsLen = _prizes[i].availableERC721Ids.length;
            uint256 prizeAmount = _prizes[i].amount;
            uint32 lotAmount = _prizes[i].lotAmount;

            if (lotAmount == 0) {
                revert InvalidLotAmount();
            }

            if (prizeAmount == 0) {
                if (erc721IdsLen != _prizes[i].lotAmount) {
                    revert MismatchERC721PrizeAmount(erc721IdsLen, lotAmount);
                }
            } else {
                if (erc721IdsLen != 0) {
                    revert ERC20PrizeWrongParam();
                }
            }

            uint64 probability = _prizes[i].probability;

            prizes[currentPrizeId] = Prize({
                tokenAddress: tokenAddress,
                amount: prizeAmount,
                lotAmount: lotAmount,
                probability: probability,
                availableERC721Ids: _prizes[i].availableERC721Ids
            });
            unchecked {
                newPrizeIds[i] = currentPrizeId;
                currentPrizeId += 1;
            }

            totalProbIncrease += probability;
        }

        totalProbabilities += totalProbIncrease;

        if (totalProbabilities > BASE_POINT) {
            revert MaxProbabilityExceeded(totalProbabilities);
        }
        nextPrizeId = currentPrizeId;

        prizeIds = newPrizeIds;
        emit PrizesUpdated(newPrizeIds, _prizes);
    }

    /// @notice Assigns a random number to a user (via an external randomness provider).
    /// @dev Will be called back by the random number provider and finalize the draw mechanism by picking a prize for user.
    /// @param _randomness The generated random number.
    /// @param _requestId The ID of the random number request.
    function _fulfillRandomness(
        uint256 _randomness,
        uint256 _requestId,
        bytes memory
    ) internal override {
        address user = requestIdToUser[_requestId];
        if (user == address(0)) {
            revert InvalidRequestId(_requestId);
        }

        delete requestIdToUser[_requestId];
        delete requestIdTimestamp[_requestId];

        uint256 cumulativeProbability;
        uint256 winningThreshold = _randomness % BASE_POINT;
        uint32 selectedPrizeId;
        uint64 userBoost = userToBoost[user];

        // Apply boost on the sum of totalProbabilities.
        uint256 boostedTotalProbabilities = (totalProbabilities * userBoost) /
            BASE_POINT;

        // If boostedTotalProbabilities exceeds 100% we have to increase the winning threshold so it stays in bound.
        //
        // Example:
        //   PrizeA probability: 50%
        //   PrizeB probability: 30%
        //   User boost: 1.5x
        //   boostedPrizeAProbability: 75%
        //   boostedPrizeBProbability: 45%
        //
        //   We now have a total of 120% totalBoostedProbability so we need to increase winning threshold by boostedTotalProbabilities to BASE_POINT ratio.
        //
        //   winningThreshold = winningThreshold * 12_000 / 10_000
        if (boostedTotalProbabilities > BASE_POINT) {
            winningThreshold = _randomness % boostedTotalProbabilities;
        }

        uint32[] memory localPrizeIds = prizeIds;
        uint256 prizeLen = localPrizeIds.length;

        for (uint256 i; i < prizeLen; i++) {
            Prize storage prize = prizes[localPrizeIds[i]];

            uint64 prizeProbability = prize.probability;
            if (prizeProbability == 0) {
                continue;
            }

            // Apply boost on a single prize probability.
            uint256 boostedPrizeProbability = (prizeProbability * userBoost) /
                BASE_POINT;

            unchecked {
                cumulativeProbability += boostedPrizeProbability;
            }

            // 2nd condition avoids rounding error in boosted probability edge case
            if (
                winningThreshold < cumulativeProbability ||
                (boostedTotalProbabilities >= BASE_POINT && i == prizeLen - 1)
            ) {
                selectedPrizeId = localPrizeIds[i];

                /// Should never underflow due to earlier check.
                unchecked {
                    prize.lotAmount -= 1;
                }

                if (prize.lotAmount == 0) {
                    totalProbabilities -= prizeProbability;
                    prize.probability = 0;
                }
                userToPrizesWon[user][selectedPrizeId] += 1;
                emit PrizeWon(user, selectedPrizeId);

                return;
            }
        }
        emit NoPrizeWon(user);
    }

    // Overrides needed due to multiple inheritance of Context
    function _msgSender()
        internal
        view
        override(ContextUpgradeable, ERC2771ContextUpgradeable)
        returns (address)
    {
        return ERC2771ContextUpgradeable._msgSender();
    }

    function _msgData()
        internal
        view
        override(ContextUpgradeable, ERC2771ContextUpgradeable)
        returns (bytes calldata)
    {
        return ERC2771ContextUpgradeable._msgData();
    }

    function _contextSuffixLength()
        internal
        view
        override(ContextUpgradeable, ERC2771ContextUpgradeable)
        returns (uint256)
    {
        return ERC2771ContextUpgradeable._contextSuffixLength();
    }
}