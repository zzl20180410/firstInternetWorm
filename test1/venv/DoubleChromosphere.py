class DoubleChromosphere:
    # 主键
    ID = 0
    def setID(self, ID):
            self.__ID = ID
    def getID(self):
        return self.__ID
    # 第一个号码
    first = 0
    def setFirst(self, first):
            self.__first = first
    def getFirst(self):
        return self.__first
    # 第二个号码
    second = 0
    # 第三个号码
    third = 0
    # 第四个号码
    fourth = 0
    # 第五个号码
    fifth = 0
    # 第六个号码
    sixth = 0
    # 第七个号码
    seventh = 0
    # 创建时间
    createTime = None
    # 期号
    issueNumber = ''
    # 本期销量
    currentSalesVolume = 0
    # 奖金滚存
    poolRolling = 0
    # 开奖日期
    lotteryDate = None
    # 兑奖截止日期
    expiryDate = None
    # 开奖日期
    outOrder = None

    # def __init__(self):
    #
    # @property
    # def age(self):
    #     return self.__age
    #
    # @age.setter
    # def setAge(self, age):
    #         self._age = age
    # @age.getter
    # def age(self):
    #     return self._age
