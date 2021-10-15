// NFT contract
// TokenURI can be one of 3 different dogs
// Random selected

// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    bytes32 public keyhash;
    uint256 public fee;
    uint256 public tokenCounter;
    // set those three kinds as three status
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Dogie", "DOG")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        // verCoordinator call the fullfillRandomness function, so msg.sender will be vrfCoordinator
        // we need find the orginal sender
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        // each tokenId has a specific breed based on mapping
        tokenIdToBreed[newTokenId] = breed;
        address owner = requestIdToSender[requestId];
        emit breedAssigned(newTokenId, breed);
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
        // _setTokenURI(newTokenId, tokenURI);
    }

    function setTokenURI(uint256 newTokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), newTokenId),
            "ERC721: caller is not owner or approved"
        );
        _setTokenURI(newTokenId, _tokenURI);
    }
}
