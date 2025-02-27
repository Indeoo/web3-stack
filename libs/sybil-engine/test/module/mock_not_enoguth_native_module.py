from sybil_engine.domain.balance.balance import NotEnoughNativeBalance
from sybil_engine.module.module import Module


class MockNotEnoughNativeModule(Module):

    def execute(self, account):
        raise NotEnoughNativeBalance("test exception")

    def log(self):
        return "TEST FAIL MODULE"
