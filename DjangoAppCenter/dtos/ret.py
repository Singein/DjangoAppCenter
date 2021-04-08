class BaseRet:
    ret: int
    message: str
    error_code: str
    data: dict

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def success(message: str = None) -> dict:
        base_ret = BaseRet()
        base_ret.ret = 1
        base_ret.message = message
        return base_ret.to_dict()

    @staticmethod
    def fail(message: str = "System error", error_code: str = "10000") -> dict:
        base_ret = BaseRet()
        base_ret.ret = 0
        base_ret.message = message
        base_ret.error_code = error_code
        return base_ret.to_dict()
