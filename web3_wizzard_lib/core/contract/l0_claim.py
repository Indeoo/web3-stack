from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction

abi = [{'inputs': [{'internalType': 'address', 'name': '_zroToken', 'type': 'address'},
                   {'internalType': 'address', 'name': '_endpoint', 'type': 'address'},
                   {'internalType': 'bytes32', 'name': '_merkleRoot', 'type': 'bytes32'},
                   {'internalType': 'address', 'name': '_donateContract', 'type': 'address'},
                   {'internalType': 'address', 'name': '_stargateUsdc', 'type': 'address'},
                   {'internalType': 'address', 'name': '_stargateUsdt', 'type': 'address'},
                   {'internalType': 'address', 'name': '_stargateNative', 'type': 'address'},
                   {'internalType': 'uint256', 'name': '_nativePrice', 'type': 'uint256'},
                   {'internalType': 'address', 'name': '_owner', 'type': 'address'}], 'stateMutability': 'nonpayable',
        'type': 'constructor'},
       {'inputs': [{'internalType': 'address', 'name': 'target', 'type': 'address'}], 'name': 'AddressEmptyCode',
        'type': 'error'}, {'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}],
                           'name': 'AddressInsufficientBalance', 'type': 'error'},
       {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'AlreadyClaimed',
        'type': 'error'}, {'inputs': [], 'name': 'DonateAndClaimAlreadySet', 'type': 'error'},
       {'inputs': [], 'name': 'FailedInnerCall', 'type': 'error'}, {
           'inputs': [{'internalType': 'enum Currency', 'name': 'currency', 'type': 'uint8'},
                      {'internalType': 'uint256', 'name': 'expectedAmount', 'type': 'uint256'},
                      {'internalType': 'uint256', 'name': 'actualAmount', 'type': 'uint256'}],
           'name': 'InsufficientDonation', 'type': 'error'}, {'inputs': [], 'name': 'InvalidDelegate', 'type': 'error'},
       {'inputs': [], 'name': 'InvalidEndpointCall', 'type': 'error'},
       {'inputs': [], 'name': 'InvalidNativeStargate', 'type': 'error'},
       {'inputs': [], 'name': 'InvalidProof', 'type': 'error'},
       {'inputs': [{'internalType': 'uint32', 'name': 'eid', 'type': 'uint32'}], 'name': 'NoPeer', 'type': 'error'},
       {'inputs': [], 'name': 'OnlyDonateAndClaim', 'type': 'error'},
       {'inputs': [{'internalType': 'address', 'name': 'addr', 'type': 'address'}], 'name': 'OnlyEndpoint',
        'type': 'error'}, {'inputs': [{'internalType': 'uint32', 'name': 'eid', 'type': 'uint32'},
                                      {'internalType': 'bytes32', 'name': 'sender', 'type': 'bytes32'}],
                           'name': 'OnlyPeer', 'type': 'error'},
       {'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}], 'name': 'OwnableInvalidOwner',
        'type': 'error'}, {'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}],
                           'name': 'OwnableUnauthorizedAccount', 'type': 'error'},
       {'inputs': [{'internalType': 'address', 'name': 'token', 'type': 'address'}], 'name': 'SafeERC20FailedOperation',
        'type': 'error'}, {'inputs': [{'internalType': 'enum Currency', 'name': 'currency', 'type': 'uint8'}],
                           'name': 'UnsupportedCurrency', 'type': 'error'},
       {'inputs': [], 'name': 'DENOMINATOR', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
        'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'components': [
        {'internalType': 'uint32', 'name': 'srcEid', 'type': 'uint32'},
        {'internalType': 'bytes32', 'name': 'sender', 'type': 'bytes32'},
        {'internalType': 'uint64', 'name': 'nonce', 'type': 'uint64'}], 'internalType': 'struct Origin',
        'name': 'origin', 'type': 'tuple'}],
           'name': 'allowInitializePath', 'outputs': [
            {'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {
           'inputs': [{'internalType': 'enum Currency', 'name': '_currency', 'type': 'uint8'},
                      {'internalType': 'address', 'name': '_user', 'type': 'address'},
                      {'internalType': 'uint256', 'name': '_zroAmount', 'type': 'uint256'}], 'name': 'assertDonation',
           'outputs': [], 'stateMutability': 'view', 'type': 'function'}, {
           'inputs': [{'internalType': 'address', 'name': '_user', 'type': 'address'},
                      {'internalType': 'enum Currency', 'name': '_currency', 'type': 'uint8'},
                      {'internalType': 'uint256', 'name': '_zroAmount', 'type': 'uint256'},
                      {'internalType': 'bytes32[]', 'name': '_proof', 'type': 'bytes32[]'},
                      {'internalType': 'address', 'name': '_to', 'type': 'address'},
                      {'internalType': 'bytes', 'name': '', 'type': 'bytes'}], 'name': 'claim', 'outputs': [{
            'components': [
                {
                    'internalType': 'bytes32',
                    'name': 'guid',
                    'type': 'bytes32'},
                {
                    'internalType': 'uint64',
                    'name': 'nonce',
                    'type': 'uint64'},
                {
                    'components': [
                        {
                            'internalType': 'uint256',
                            'name': 'nativeFee',
                            'type': 'uint256'},
                        {
                            'internalType': 'uint256',
                            'name': 'lzTokenFee',
                            'type': 'uint256'}],
                    'internalType': 'struct MessagingFee',
                    'name': 'fee',
                    'type': 'tuple'}],
            'internalType': 'struct MessagingReceipt',
            'name': 'receipt',
            'type': 'tuple'}],
           'stateMutability': 'payable', 'type': 'function'}, {
           'inputs': [{'internalType': 'enum Currency', 'name': '_currency', 'type': 'uint8'},
                      {'internalType': 'uint256', 'name': '_zroAmount', 'type': 'uint256'},
                      {'internalType': 'bytes32[]', 'name': '_proof', 'type': 'bytes32[]'},
                      {'internalType': 'address', 'name': '_to', 'type': 'address'},
                      {'internalType': 'bytes', 'name': '', 'type': 'bytes'}], 'name': 'claim', 'outputs': [{
            'components': [
                {
                    'internalType': 'bytes32',
                    'name': 'guid',
                    'type': 'bytes32'},
                {
                    'internalType': 'uint64',
                    'name': 'nonce',
                    'type': 'uint64'},
                {
                    'components': [
                        {
                            'internalType': 'uint256',
                            'name': 'nativeFee',
                            'type': 'uint256'},
                        {
                            'internalType': 'uint256',
                            'name': 'lzTokenFee',
                            'type': 'uint256'}],
                    'internalType': 'struct MessagingFee',
                    'name': 'fee',
                    'type': 'tuple'}],
            'internalType': 'struct MessagingReceipt',
            'name': 'receipt',
            'type': 'tuple'}],
           'stateMutability': 'payable', 'type': 'function'}, {
           'inputs': [{'internalType': 'enum Currency', 'name': 'currency', 'type': 'uint8'},
                      {'internalType': 'uint256', 'name': 'amountToDonate', 'type': 'uint256'},
                      {'internalType': 'uint256', 'name': '_zroAmount', 'type': 'uint256'},
                      {'internalType': 'bytes32[]', 'name': '_proof', 'type': 'bytes32[]'},
                      {'internalType': 'address', 'name': '_to', 'type': 'address'},
                      {'internalType': 'bytes', 'name': '_extraBytes', 'type': 'bytes'}], 'name': 'donateAndClaim',
           'outputs': [{'components': [{'internalType': 'bytes32', 'name': 'guid', 'type': 'bytes32'},
                                       {'internalType': 'uint64', 'name': 'nonce', 'type': 'uint64'}, {'components': [
                   {'internalType': 'uint256', 'name': 'nativeFee', 'type': 'uint256'},
                   {'internalType': 'uint256', 'name': 'lzTokenFee', 'type': 'uint256'}],
                                           'internalType': 'struct MessagingFee',
                                           'name': 'fee',
                                           'type': 'tuple'}],
                        'internalType': 'struct MessagingReceipt', 'name': 'receipt', 'type': 'tuple'}],
           'stateMutability': 'payable', 'type': 'function'}, {'inputs': [], 'name': 'donateContract', 'outputs': [
        {'internalType': 'contract IDonate', 'name': '', 'type': 'address'}], 'stateMutability': 'view',
                                                               'type': 'function'}, {'inputs': [], 'name': 'endpoint',
                                                                                     'outputs': [{
                                                                                         'internalType': 'contract ILayerZeroEndpointV2',
                                                                                         'name': '',
                                                                                         'type': 'address'}],
                                                                                     'stateMutability': 'view',
                                                                                     'type': 'function'}, {'inputs': [{
        'components': [
            {
                'internalType': 'uint32',
                'name': 'srcEid',
                'type': 'uint32'},
            {
                'internalType': 'bytes32',
                'name': 'sender',
                'type': 'bytes32'},
            {
                'internalType': 'uint64',
                'name': 'nonce',
                'type': 'uint64'}],
        'internalType': 'struct Origin',
        'name': '',
        'type': 'tuple'},
        {
            'internalType': 'bytes',
            'name': '',
            'type': 'bytes'},
        {
            'internalType': 'address',
            'name': '_sender',
            'type': 'address'}],
           'name': 'isComposeMsgSender',
           'outputs': [{
               'internalType': 'bool',
               'name': '',
               'type': 'bool'}],
           'stateMutability': 'view',
           'type': 'function'},
       {'inputs': [{'components': [{'internalType': 'uint32', 'name': 'srcEid', 'type': 'uint32'},
                                   {'internalType': 'bytes32', 'name': 'sender', 'type': 'bytes32'},
                                   {'internalType': 'uint64', 'name': 'nonce', 'type': 'uint64'}],
                    'internalType': 'struct Origin', 'name': '_origin', 'type': 'tuple'},
                   {'internalType': 'bytes32', 'name': '_guid', 'type': 'bytes32'},
                   {'internalType': 'bytes', 'name': '_message', 'type': 'bytes'},
                   {'internalType': 'address', 'name': '_executor', 'type': 'address'},
                   {'internalType': 'bytes', 'name': '_extraData', 'type': 'bytes'}], 'name': 'lzReceive',
        'outputs': [], 'stateMutability': 'payable', 'type': 'function'},
       {'inputs': [], 'name': 'merkleRoot', 'outputs': [{'internalType': 'bytes32', 'name': '', 'type': 'bytes32'}],
        'stateMutability': 'view', 'type': 'function'}, {
           'inputs': [{'internalType': 'uint32', 'name': '', 'type': 'uint32'},
                      {'internalType': 'bytes32', 'name': '', 'type': 'bytes32'}], 'name': 'nextNonce',
           'outputs': [{'internalType': 'uint64', 'name': 'nonce', 'type': 'uint64'}], 'stateMutability': 'view',
           'type': 'function'}, {'inputs': [], 'name': 'numeratorNative',
                                 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
                                 'stateMutability': 'view', 'type': 'function'},
       {'inputs': [], 'name': 'numeratorUsdc', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
        'stateMutability': 'view', 'type': 'function'},
       {'inputs': [], 'name': 'numeratorUsdt', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
        'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'oAppVersion', 'outputs': [
        {'internalType': 'uint64', 'name': 'senderVersion', 'type': 'uint64'},
        {'internalType': 'uint64', 'name': 'receiverVersion', 'type': 'uint64'}], 'stateMutability': 'view',
                                                         'type': 'function'},
       {'inputs': [], 'name': 'owner', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}],
        'stateMutability': 'view', 'type': 'function'},
       {'inputs': [{'internalType': 'uint32', 'name': 'eid', 'type': 'uint32'}], 'name': 'peers',
        'outputs': [{'internalType': 'bytes32', 'name': 'peer', 'type': 'bytes32'}], 'stateMutability': 'view',
        'type': 'function'}, {'inputs': [{'internalType': 'uint32', 'name': '_dstEid', 'type': 'uint32'},
                                         {'internalType': 'uint256', 'name': '_zroAmount', 'type': 'uint256'}],
                              'name': 'quoteClaimCallback', 'outputs': [{'components': [
            {'internalType': 'uint256', 'name': 'nativeFee', 'type': 'uint256'},
            {'internalType': 'uint256', 'name': 'lzTokenFee', 'type': 'uint256'}],
            'internalType': 'struct MessagingFee',
            'name': 'msgFee', 'type': 'tuple'}],
                              'stateMutability': 'view', 'type': 'function'},
       {'inputs': [], 'name': 'renounceOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'},
       {'inputs': [{'internalType': 'uint256', 'name': '_zroAmount', 'type': 'uint256'}], 'name': 'requiredDonation',
        'outputs': [{'components': [{'internalType': 'uint256', 'name': 'usdc', 'type': 'uint256'},
                                    {'internalType': 'uint256', 'name': 'usdt', 'type': 'uint256'},
                                    {'internalType': 'uint256', 'name': 'native', 'type': 'uint256'}],
                     'internalType': 'struct Donation', 'name': '', 'type': 'tuple'}], 'stateMutability': 'view',
        'type': 'function'},
       {'inputs': [{'internalType': 'address', 'name': '_delegate', 'type': 'address'}], 'name': 'setDelegate',
        'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'},
       {'inputs': [{'internalType': 'address', 'name': '_donateAndClaim', 'type': 'address'}],
        'name': 'setDonateAndClaim', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'},
       {'inputs': [{'internalType': 'bytes32', 'name': '_merkleRoot', 'type': 'bytes32'}], 'name': 'setMerkleRoot',
        'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {
           'inputs': [{'internalType': 'uint32', 'name': '_eid', 'type': 'uint32'},
                      {'internalType': 'bytes32', 'name': '_peer', 'type': 'bytes32'}], 'name': 'setPeer',
           'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'},
       {'inputs': [{'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'transferOwnership',
        'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {
           'inputs': [{'internalType': 'address', 'name': '_to', 'type': 'address'},
                      {'internalType': 'uint256', 'name': '_amount', 'type': 'uint256'}], 'name': 'withdrawZro',
           'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'},
       {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'zroClaimed',
        'outputs': [{'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'stateMutability': 'view',
        'type': 'function'},
       {'inputs': [], 'name': 'zroToken', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}],
        'stateMutability': 'view', 'type': 'function'}]


class L0Claim(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def donateAndClaim(self, account, donate_amount, amount_to_claim, merkle_proof):
        txn_params = self.build_generic_data(account.address, False)
        txn_params['value'] = donate_amount

        return self.contract.functions.donateAndClaim(
            2,
            donate_amount,
            #5520000000000000
            #5520000000000000
            amount_to_claim,
            #183461138113000003000
            #183461138113000003000
            merkle_proof,
            #['0x1fce26056b7cc81752ae974a8baa89d78123fd539f5fb47f0e5cb1f2c603b3c8', '0x63e5fe91dbafe187829bc84f8e6ddb6c6f4d62e5ef1ff4796913101fc0ea916e', '0x9a734b2f26f5334741ee26eda57cef6c4f84430e1d91be1b65cb4e7be577d0e9', '0xcc8bc1df42652bfd0aa8032a1cf50a31e31ecbe78d52411491076bfc59b70e7d', '0x8edc7e63ae09f38a3e00b6ee33fb102eee1771ce73b8a6b089cfcc3c2b4b7b8f', '0x8870668769d7dfa64e8695bf51741c73358923b7ad7e07dd6055c088760063cc', '0x75321dbf87f550059a302d401fd3aae9b13204316e202b3d0bd459447d611739', '0x5d48d0538089ccbfade4265ff10efae09691a0204dcef8db5b20064d3c6103bb', '0xa6d7408758dc62d68fc1d768714f4f9422bb1ad8f222a687c0e1c4d88e7ddfcf', '0xfa0a2c7465fccd5838f147abad0b3f928b716eabfbbae622de7cfdb0c0fcbce1', '0x30369b62a912a4555e898133ad536bbc8b58af456cdb1001e38a8e0e4d01c034', '0xea79cef9445e78b7c5695d0bb5e5d676bfa5b7ced66df915ec13fb6fd6b3e131', '0xc4abfec16adca47f0c0d5d22dcb87586b66cba0048a684e440be04175dbc5c58', '0xecffcc8af84ed13272ad00aeee065c02e4778b6cfd0d124222f23264b0679076', '0x767c848c0da4bee189851e644bb437e9ef426d6e418f14fd3e9337e5ffe3596f', '0x55ab35e3f06e43b8af688169490819fdcb4180258210acb11db1976379754b1c', '0x950b026464be9f6fd40516d45236a70f07ff78b3dc1b9d258c9ddbf7fd0a003f', '0x6b71fb967b62b9e1f399a856517a1da9c22a0993fdb84b1b998b14849c2d7e9e', '0x9ae69f117d127a35e00c470d6bff380bfabbca78d86668984e867861853ee8fc', '0xa042d488b6a933c88ec4b41ba407ff13521c2e67e842697017bc19ed9f9a8e5d', '0x65b28f8ec7c9c9fc471c6a5000a1906b04e8da896a739ffddf6d3b71e47fd60d']
            #['0x1fce26056b7cc81752ae974a8baa89d78123fd539f5fb47f0e5cb1f2c603b3c8', '0x63e5fe91dbafe187829bc84f8e6ddb6c6f4d62e5ef1ff4796913101fc0ea916e', '0x9a734b2f26f5334741ee26eda57cef6c4f84430e1d91be1b65cb4e7be577d0e9', '0xcc8bc1df42652bfd0aa8032a1cf50a31e31ecbe78d52411491076bfc59b70e7d', '0x8edc7e63ae09f38a3e00b6ee33fb102eee1771ce73b8a6b089cfcc3c2b4b7b8f', '0x8870668769d7dfa64e8695bf51741c73358923b7ad7e07dd6055c088760063cc', '0x75321dbf87f550059a302d401fd3aae9b13204316e202b3d0bd459447d611739', '0x5d48d0538089ccbfade4265ff10efae09691a0204dcef8db5b20064d3c6103bb', '0xa6d7408758dc62d68fc1d768714f4f9422bb1ad8f222a687c0e1c4d88e7ddfcf', '0xfa0a2c7465fccd5838f147abad0b3f928b716eabfbbae622de7cfdb0c0fcbce1', '0x30369b62a912a4555e898133ad536bbc8b58af456cdb1001e38a8e0e4d01c034', '0xea79cef9445e78b7c5695d0bb5e5d676bfa5b7ced66df915ec13fb6fd6b3e131', '0xc4abfec16adca47f0c0d5d22dcb87586b66cba0048a684e440be04175dbc5c58', '0xecffcc8af84ed13272ad00aeee065c02e4778b6cfd0d124222f23264b0679076', '0x767c848c0da4bee189851e644bb437e9ef426d6e418f14fd3e9337e5ffe3596f', '0x55ab35e3f06e43b8af688169490819fdcb4180258210acb11db1976379754b1c', '0x950b026464be9f6fd40516d45236a70f07ff78b3dc1b9d258c9ddbf7fd0a003f', '0x6b71fb967b62b9e1f399a856517a1da9c22a0993fdb84b1b998b14849c2d7e9e', '0x9ae69f117d127a35e00c470d6bff380bfabbca78d86668984e867861853ee8fc', '0xa042d488b6a933c88ec4b41ba407ff13521c2e67e842697017bc19ed9f9a8e5d', '0x65b28f8ec7c9c9fc471c6a5000a1906b04e8da896a739ffddf6d3b71e47fd60d']
            account.address,
            '0x'
        ).build_transaction(txn_params)
