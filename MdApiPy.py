#-*- coding=utf-8 -*-

import time
from TickController import TickController
from FinalLogger import logger

from ctpwrapper.MdApi import MdApiWrapper
from ctpwrapper import ApiStructure

class MdApiPy(MdApiWrapper):
    def __init__(self, instruments, broker_id, investor_id, passwd, *args,**kwargs):
        self.requestid=0
        self.instruments = instruments
        self.broker_id =broker_id
        self.investor_id = investor_id
        self.passwd = passwd

    def isErrorRspInfo(self, info):
        if info.ErrorID !=0:
            logger.info('ErrorID=%d, ErrorMsg=%s' % info.ErrorID % info.ErrorMsg.decode('gbk'))
        return info.ErrorID !=0

    def Create(self, pszFlowPath="", bIsUsingUdp=False, bIsMulticast=False):
        """创建MdApi
        @param pszFlowPath 存贮订阅信息文件的目录，默认为当前目录
        @return 创建出的UserApi
        modify for udp marketdata
        """
        super(MdApiPy, self).Create(pszFlowPath.encode(), bIsUsingUdp, bIsMulticast)

    def Init(self):
        """
        初始化运行环境,只有调用后,接口才开始工作
        """
        super(MdApiPy, self).Init()
        time.sleep(0.1)  # wait for c++ init

    def Join(self) -> int:
        """
        等待接口线程结束运行
        @return 线程退出代码
        :return:
        """
        return super(MdApiPy, self).Join()

    def ReqUserLogin(self, pReqUserLoginField, nRequestID) -> int:
        """
        用户登录请求
        :return:
        """
        return super(MdApiPy, self).ReqUserLogin(pReqUserLoginField, nRequestID)

    def ReqUserLogout(self, pUserLogout, nRequestID) -> int:
        """
         登出请求
        :return:
        """
        return super(MdApiPy, self).ReqUserLogout(pUserLogout, nRequestID)

    def GetTradingDay(self) -> str:
        """
        获取当前交易日
        @retrun 获取到的交易日
        @remark 只有登录成功后,才能得到正确的交易日
        :return:
        """
        day = super(MdApiPy, self).GetTradingDay()
        return day.decode()

    def RegisterFront(self, pszFrontAddress: str):
        """
        注册前置机网络地址
        @param pszFrontAddress：前置机网络地址。
        @remark 网络地址的格式为：“protocol:# ipaddress:port”，如：”tcp:# 127.0.0.1:17001”。
        @remark “tcp”代表传输协议，“127.0.0.1”代表服务器地址。”17001”代表服务器端口号。
        """
        super(MdApiPy, self).RegisterFront(pszFrontAddress.encode())

    def RegisterNameServer(self, pszNsAddress: str):
        """
        注册名字服务器网络地址
        @param pszNsAddress：名字服务器网络地址。
        @remark 网络地址的格式为：“protocol:# ipaddress:port”，如：”tcp:# 127.0.0.1:12001”。
        @remark “tcp”代表传输协议，“127.0.0.1”代表服务器地址。”12001”代表服务器端口号。
        @remark RegisterNameServer优先于RegisterFront
        """
        super(MdApiPy, self).RegisterNameServer(pszNsAddress.encode())

    def RegisterFensUserInfo(self, pFensUserInfo):
        """
        注册名字服务器用户信息
        @param pFensUserInfo：用户信息。
        """
        super(MdApiPy, self).RegisterFensUserInfo(pFensUserInfo)

    def SubscribeMarketData(self, pInstrumentID: list) -> int:
        """
         订阅行情。
        @param ppInstrumentID 合约ID
        :return: int
        """
        ids = [bytes(item, encoding="utf-8") for item in pInstrumentID]
        return super(MdApiPy, self).SubscribeMarketData(ids)

    def UnSubscribeMarketData(self, pInstrumentID: list) -> int:
        """
        退订行情。
        @param ppInstrumentID 合约ID
        :return: int
        """
        ids = [bytes(item, encoding="utf-8") for item in pInstrumentID]

        return super(MdApiPy, self).UnSubscribeMarketData(ids)

    def SubscribeForQuoteRsp(self, pInstrumentID: list) -> int:
        """
        订阅询价。
        :param pInstrumentID: 合约ID list
        :return: int
        """
        ids = [bytes(item, encoding="utf-8") for item in pInstrumentID]

        return super(MdApiPy, self).SubscribeForQuoteRsp(ids)

    def UnSubscribeForQuoteRsp(self, pInstrumentID: list) -> int:
        """
        退订询价。
        :param pInstrumentID: 合约ID list
        :return: int
        """
        ids = [bytes(item, encoding="utf-8") for item in pInstrumentID]

        return super(MdApiPy, self).UnSubscribeForQuoteRsp(ids)

    # for receive message

    def OnFrontConnected(self):
        """
        当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。
        :return:
        """
        logger.info('OnFrontConnected')
        req = ApiStructure.ReqUserLoginField(BrokerID=self.broker_id, UserID=self.investor_id, Password=self.passwd)
        self.requestid += 1
        r = self.ReqUserLogin(req, self.requestid)

    def OnFrontDisconnected(self, nReason):
        """
        当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。
        @param nReason 错误原因
            4097 0x1001 网络读失败
            4098 0x1002 网络写失败
            8193 0x2001 读心跳超时
            8194 0x2002 发送心跳超时
            8195 0x2003 收到不能识别的错误消息
        客户端与服务端的连接断开有两种情况：
            网络原因导致连接断开
            服务端主动断开连接
        服务器主动断开连接有两种可能：
            客户端长时间没有从服务端接收报文，时间超时
            客户端建立的连接数超过限制
        :param nReason:
        """
        logger.info('onFrontDisConnected, nReason = %d' % nReason)

    def OnHeartBeatWarning(self, nTimeLapse):
        """
        心跳超时警告。当长时间未收到报文时，该方法被调用。

        :param nTimeLapse: 距离上次接收报文的时间
        :return:
        """
        logger.info('OnHeartBeatWarning, nTimeLapse = %s' % nTimeLapse)

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        """
        登录请求响应
        :param pRspUserLogin:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        if bIsLast and not self.isErrorRspInfo(pRspInfo):
            self.SubscribeMarketData(self.instruments)

    def OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast):
        """
        登出请求响应
        :param pUserLogout:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        pass

    def OnRspError(self, pRspInfo, nRequestID, bIsLast):
        """
        错误应答
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        self.isErrorRspInfo(pRspInfo)

    def OnRspSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        """
        订阅行情应答
        :param pSpecificInstrument:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        pass

    def OnRspUnSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        """
        取消订阅行情应答
        :param pSpecificInstrument:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        pass

    def OnRspSubForQuoteRsp(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        """
        订阅询价应答
        :param pSpecificInstrument:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        pass

    def OnRspUnSubForQuoteRsp(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        """
        取消订阅询价应答
        :param pSpecificInstrument:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        pass

    def OnRtnDepthMarketData(self, pDepthMarketData):
        """
        深度行情通知
        :param pDepthMarketData:
        :return:
        """
        TickController.processTick(pDepthMarketData.to_dict())

    def OnRtnForQuoteRsp(self, pForQuoteRsp):
        """
        询价通知
        :param pForQuoteRsp:
        :return:
        """
        pass
