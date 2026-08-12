# iFinD数据接口

- ID: 419
- 分类: iFinD数据接口
- URL: https://quant.10jqka.com.cn/view/dataplatform/detail/419
- 简介: iFinD金融数据终端提供Python数据接口

## 使用说明

<p align="center">

  <img src="http://u.thsi.cn/imgsrc/pefile/f51dabdb7a7fd12b67e3163d80a832bc.png" align="middle"  width="500" />
</p>

## 介绍?️

iFinD金融数据终端提供Python数据接口，目前已可在SuperMind上使用，使用方法如下：

```python
#引入iFinDPy库
from iFinDPy import *
#使用测试账号登录（有效期至2017年7月10日）
THS_iFinDLogin('SuperMind002','929789')
```

* iFinD数据接口申请试用链接：[同花顺私募之家-iFinD数据接口](https://www.forfunds.cn/platform/pcweb/?formApplyShow=true "同花顺私募之家-iFinD数据接口")

> 注意：点击链接后会跳转至同花顺私募之家，你需要进入产品中心，并在投研服务中找到“iFinD数据接口”这款产品，点击“申请试用”，填写信息并提交，我们的运营人员会当日联系您，请保持电话畅通

* iFinD数据接口说明文档查看：[《iFinD Python 数据接口操作说明》](http://ft.10jqka.com.cn/thsft/iFindService/docCenter?ID=S201501231127 "《同花顺 Python 接口操作说明》")

## 使用说明?️

### 超级命令

- 在iFinD终端中输入'sc'，就可以打开超级命令界面
- 在超级命令界面中，选择想要获取的数据，即可自动生成代码

### 常用数据

- 获取高频序列数据

  ```python
  from iFinDPy import *
  THS_iFinDLogin('SuperMind002','929789')
  #获取平安银行2023年3月1日下午2点15分至3点15分的分钟开高低收数据
  THS_HighFrequenceSequence(
      '000001.SZ',
      'open;high;low;close',
      'CPS:0,MaxPoints:50000,Fill:Previous,Interval:1',
      '2017-06-27 14:15:00',
      '2017-06-27 15:15:00'
  )
  ```
  <br />
- 获取实时行情数据

  ```python
  from iFinDPy import *
  THS_iFinDLogin('SuperMind002','929789')
  #获取平安银行当前买一价和买一量数据
  THS_RealtimeQuotes('000001.SZ','mrj1;mrl1','pricetype:1')
  ```
  <br />
- 获取历史行情数据

  ```python
  from iFinDPy import *
  THS_iFinDLogin('SuperMind002','929789')
  #获取平安银行当前3月1日至4月1日的日级开高低收数据
  THS_HistoryQuotes(
      '000001.SZ',
      'open,high,low,close',
      'period:D,pricetype:1,rptcategory:0,fqdate:1900-01-01,hb:YSHB,fill:Previous',
      '2023-03-01',
      '2023-04-01'
  )
  ```
  <br />
- 获取日期序列数据

  ```python
  from iFinDPy import *
  THS_iFinDLogin('SuperMind002','929789')
  #获取平安银行3月1日至4月1日的总股本数据
  THS_DateSequence(
      '000001.SZ',
      'capitalization',
      'CPS:0,Days:Tradedays,Fill:Previous,Interval:D,Currency:ORIGINAL',
      '2023-03-01',
      '2023-04-01'
  )
  ```
  <br />
- 获取数据池数据

  ```python
  from iFinDPy import *
  THS_iFinDLogin('SuperMind002','929789')
  #获取上证50成分股数据
  THS_DataPool('block','2023-03-01;001005260','date:Y,security_name:Y,thscode:Y')
  ```
  <br />
- 获取经济数据库数据

  ```python
  from iFinDPy import *
  THS_iFinDLogin('SuperMind002','929789')
  #获取2021年1月1日以来的GDP季度数据
  THS_EDBQuery('M001620326','2021-01-01','2023-04-01')
  ```

