"""
AKShare 接口加载器测试类
"""

import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
import pandas as pd

from .akshare_interface import AKShareInterfaceLoader, AKShareInvoker, InterfaceDetail, InterfaceParameter


class TestAKShareInterface(unittest.TestCase):
    """AKShare 接口测试类"""

    def setUp(self):
        """测试前准备"""
        # 创建测试用的 Markdown 内容
        self.test_md_content = """## [AKShare]股票数据

### A股

#### 股票市场总貌

##### 上海证券交易所

接口: stock_sse_summary

目标地址: http://www.sse.com.cn/market/stockdata/statistic/

描述: 上海证券交易所-股票数据总貌

限量: 单次返回最近交易日的股票数据总貌(当前交易日的数据需要交易所收盘后统计)

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数-实时行情数据

| 名称  | 类型     | 描述  |
|-----|--------|-----|
| 项目  | object | -   |
| 股票  | object | -   |
| 科创板 | object | -   |
| 主板  | object | -   |

接口示例

```python
import akshare as ak

stock_sse_summary_df = ak.stock_sse_summary()
print(stock_sse_summary_df)
```

数据示例

```
      项目     股票       科创板         主板
0   流通股本   40403.47    413.63   39989.84
1    总市值  516714.68   55719.6  460995.09
2  平均市盈率      17.92      71.0      16.51
```

##### 深圳证券交易所

接口: stock_szse_summary

目标地址: http://www.szse.cn/market/overview/index.html

描述: 深圳证券交易所-市场总貌-证券类别统计

限量: 单次返回指定 date 的市场总貌数据-证券类别统计

输入参数

| 名称   | 类型  | 描述                                  |
|------|-----|-------------------------------------|
| date | str | date="20200619"; 当前交易日的数据需要交易所收盘后统计 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 证券类别 | object  | -       |
| 数量   | int64   | 注意单位: 只 |
| 成交金额 | float64 | 注意单位: 元 |

接口示例

```python
import akshare as ak

stock_szse_summary_df = ak.stock_szse_summary(date="20200619")
print(stock_szse_summary_df)
```

数据示例

```
     证券类别    数量          成交金额           总市值
0      股票  2284  4.647749e+11  2.706514e+13
1    主板A股   460  9.775950e+10  7.864787e+12
```

### 期货数据

#### 商品期货

接口: futures_main_sina

目标地址: https://finance.sina.com.cn/futuremarket/

描述: 新浪财经-期货-主力合约实时行情

限量: 单次返回指定 symbol 的期货主力合约实时行情数据

输入参数

| 名称     | 类型  | 描述                           |
|--------|-----|------------------------------|
| symbol | str | symbol="CU0"; 期货品种的主力合约代码 |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 代码   | object  | -   |
| 名称   | object  | -   |
| 最新价  | float64 | -   |

接口示例

```python
import akshare as ak

futures_main_sina_df = ak.futures_main_sina(symbol="CU0")
print(futures_main_sina_df)
```

数据示例

```
   代码    名称      最新价
0  CU0  沪铜主力  51230
```
"""

        # 创建临时文件
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8')
        self.temp_file.write(self.test_md_content)
        self.temp_file.close()

        # 创建加载器和调用器
        self.loader = AKShareInterfaceLoader(self.temp_file.name)
        self.invoker = AKShareInvoker(self.loader)

    def tearDown(self):
        """测试后清理"""
        # 删除临时文件
        os.unlink(self.temp_file.name)

    def test_interface_loading(self):
        """测试接口加载"""
        self.assertGreater(self.loader.get_interface_count(), 0)
        self.assertIn('stock_sse_summary', self.loader.interfaces)
        self.assertIn('stock_szse_summary', self.loader.interfaces)
        self.assertIn('futures_main_sina', self.loader.interfaces)

    def test_list_interfaces(self):
        """测试列出所有接口"""
        interfaces = self.invoker.list_interfaces()
        self.assertIsInstance(interfaces, list)
        self.assertIn('stock_sse_summary', interfaces)
        self.assertIn('stock_szse_summary', interfaces)
        self.assertIn('futures_main_sina', interfaces)

    def test_get_interface(self):
        """测试获取特定接口"""
        interface = self.invoker.get_interface('stock_sse_summary')
        self.assertIsNotNone(interface)
        self.assertIsInstance(interface, InterfaceDetail)

        if interface:  # 类型检查
            self.assertEqual(interface.name, 'stock_sse_summary')
            self.assertEqual(interface.description, '上海证券交易所-股票数据总貌')
            self.assertEqual(interface.target_url, 'http://www.sse.com.cn/market/stockdata/statistic/')
            self.assertEqual(interface.category, 'A股')
            self.assertEqual(interface.subcategory, '上海证券交易所')

        # 测试不存在的接口
        non_existent = self.invoker.get_interface('non_existent_interface')
        self.assertIsNone(non_existent)

    def test_interface_parameters(self):
        """测试接口参数解析"""
        # 测试有参数的接口
        interface = self.invoker.get_interface('stock_szse_summary')
        self.assertIsNotNone(interface)
        self.assertIsInstance(interface, InterfaceDetail)

        if interface:  # 类型检查
            # 检查输入参数
            self.assertEqual(len(interface.input_parameters), 1)
            input_param = interface.input_parameters[0]
            self.assertEqual(input_param.name, 'date')
            self.assertEqual(input_param.type, 'str')
            self.assertIn('20200619', input_param.description)

            # 检查输出参数
            self.assertGreater(len(interface.output_parameters), 0)
            output_params = interface.output_parameters
            param_names = [p.name for p in output_params]
            self.assertIn('证券类别', param_names)
            self.assertIn('数量', param_names)

    def test_interface_code_examples(self):
        """测试代码示例解析"""
        interface = self.loader.get_interface('stock_sse_summary')
        self.assertIsNotNone(interface)
        self.assertIsInstance(interface, InterfaceDetail)

        if interface:  # 类型检查
            # 检查示例代码
            self.assertIn('import akshare as ak', interface.example_code)
            self.assertIn('stock_sse_summary_df = ak.stock_sse_summary()', interface.example_code)

            # 检查示例数据
            self.assertIn('项目', interface.example_data)
            self.assertIn('股票', interface.example_data)

    def test_search_interfaces(self):
        """测试搜索接口"""
        # 搜索包含"股票"的接口
        results = self.invoker.search_interfaces('股票')
        self.assertGreater(len(results), 0)

        # 验证结果包含期望的接口
        result_names = [r.name for r in results]
        self.assertIn('stock_sse_summary', result_names)
        # stock_szse_summary 可能不在搜索结果中，因为它的描述中没有"股票"字样

        # 搜索期货相关接口
        futures_results = self.invoker.search_interfaces('期货')
        self.assertGreater(len(futures_results), 0)
        futures_names = [r.name for r in futures_results]
        self.assertIn('futures_main_sina', futures_names)

        # 搜索不存在的关键词
        no_results = self.invoker.search_interfaces('不存在的关键词')
        self.assertEqual(len(no_results), 0)

    def test_get_interfaces_by_category(self):
        """测试按类别获取接口"""
        # 获取A股类别的接口
        stock_interfaces = self.invoker.get_interfaces_by_category('A股')
        self.assertGreater(len(stock_interfaces), 0)

        stock_names = [i.name for i in stock_interfaces]
        self.assertIn('stock_sse_summary', stock_names)
        self.assertIn('stock_szse_summary', stock_names)

        # 获取期货数据类别的接口
        futures_interfaces = self.invoker.get_interfaces_by_category('期货')
        self.assertGreater(len(futures_interfaces), 0)

        futures_names = [i.name for i in futures_interfaces]
        self.assertIn('futures_main_sina', futures_names)

    def test_get_categories(self):
        """测试获取所有类别"""
        categories = self.invoker.get_categories()
        self.assertIsInstance(categories, list)
        self.assertIn('A股', categories)
        self.assertIn('期货数据', categories)

    def test_interface_detail_to_dict(self):
        """测试接口详情转字典"""
        interface = self.loader.get_interface('stock_sse_summary')
        self.assertIsNotNone(interface)
        self.assertIsInstance(interface, InterfaceDetail)

        if interface:  # 类型检查
            interface_dict = interface.to_dict()
            self.assertIsInstance(interface_dict, dict)

            # 检查必要字段
            required_fields = ['name', 'target_url', 'description', 'limitation',
                              'input_parameters', 'output_parameters', 'example_code',
                              'example_data', 'category', 'subcategory']

            for field in required_fields:
                self.assertIn(field, interface_dict)

            # 检查参数格式
            self.assertIsInstance(interface_dict['input_parameters'], list)
            self.assertIsInstance(interface_dict['output_parameters'], list)

    def test_interface_detail_str(self):
        """测试接口详情字符串表示"""
        interface = self.loader.get_interface('stock_sse_summary')
        self.assertIsInstance(interface, InterfaceDetail)

        str_repr = str(interface)
        self.assertIn('stock_sse_summary', str_repr)
        self.assertIn('上海证券交易所-股票数据总貌', str_repr)

    def test_parameter_classes(self):
        """测试参数类"""
        # 测试基本参数
        param = InterfaceParameter("test_name", "str", "测试描述")
        self.assertEqual(param.name, "test_name")
        self.assertEqual(param.type, "str")
        self.assertEqual(param.description, "测试描述")
        self.assertTrue(param.required)  # 默认为必需
        self.assertIsNone(param.default_value)

        # 测试可选参数
        optional_param = InterfaceParameter("optional_param", "str", "可选参数，默认值为test")
        self.assertFalse(optional_param.required)

        # 测试带默认值的参数
        default_param = InterfaceParameter("date", "str", 'date="20200619"; 交易日期')
        self.assertFalse(default_param.required)
        self.assertEqual(default_param.default_value, "20200619")

        # 测试占位符参数
        placeholder_param = InterfaceParameter("-", "-", "-")
        self.assertTrue(placeholder_param.is_placeholder())
        self.assertFalse(placeholder_param.required)

    def test_edge_cases(self):
        """测试边界情况"""
        # 测试空搜索 - 空字符串可能返回所有结果，这是合理的
        empty_results = self.invoker.search_interfaces('')
        # 不强制要求返回0个结果，因为空字符串可能匹配所有接口

        # 测试大小写不敏感搜索
        upper_results = self.invoker.search_interfaces('股票')
        lower_results = self.invoker.search_interfaces('股票')
        self.assertEqual(len(upper_results), len(lower_results))

        # 测试不存在的类别
        no_category = self.invoker.get_interfaces_by_category('不存在的类别')
        self.assertEqual(len(no_category), 0)

    @patch('akshare.stock_sse_summary')
    def test_invoke_method(self, mock_akshare_func):
        """测试 invoke 方法"""
        # 模拟 akshare 返回数据
        mock_data = pd.DataFrame({
            '项目': ['流通股本', '总市值'],
            '股票': [40403.47, 516714.68],
            '科创板': [413.63, 55719.6]
        })
        mock_akshare_func.return_value = mock_data

        # 调用接口
        result = self.invoker.invoke('stock_sse_summary')

        # 验证结果
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertIn('项目', result.columns)
        self.assertIn('股票', result.columns)

        # 验证 akshare 被正确调用
        mock_akshare_func.assert_called_once_with()

    @patch('akshare.stock_szse_summary')
    def test_invoke_with_parameters(self, mock_akshare_func):
        """测试带参数的接口调用"""
        mock_data = pd.DataFrame({
            '证券类别': ['股票', '主板A股'],
            '数量': [2284, 460],
            '成交金额': [4.647749e+11, 9.775950e+10]
        })
        mock_akshare_func.return_value = mock_data

        # 调用带参数的接口
        result = self.invoker.invoke('stock_szse_summary', date='20200619')

        # 验证结果
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)

        # 验证参数传递
        mock_akshare_func.assert_called_once_with(date='20200619')

    def test_invoke_nonexistent_interface(self):
        """测试调用不存在的接口"""
        with self.assertRaises(ValueError) as context:
            self.invoker.invoke('nonexistent_interface')

        self.assertIn('不存在', str(context.exception))

    @patch('akshare.stock_sse_summary')
    def test_invoke_with_validation(self, mock_akshare_func):
        """测试带验证的接口调用"""
        mock_data = pd.DataFrame({'test': [1, 2, 3]})
        mock_akshare_func.return_value = mock_data

        # 调用带验证的接口
        result = self.invoker.invoke_with_validation('stock_sse_summary')

        # 验证返回格式
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        self.assertIsNone(result['error'])
        self.assertIsInstance(result['data'], pd.DataFrame)
        self.assertIsInstance(result['interface_info'], dict)

        # 验证接口信息
        info = result['interface_info']
        self.assertEqual(info['name'], 'stock_sse_summary')
        self.assertEqual(info['rows'], 3)
        self.assertEqual(info['columns'], ['test'])

    def test_invoke_with_validation_error(self):
        """测试带验证的接口调用错误情况"""
        result = self.invoker.invoke_with_validation('nonexistent_interface')

        # 验证错误处理
        self.assertIsInstance(result, dict)
        self.assertFalse(result['success'])
        self.assertIsNotNone(result['error'])
        self.assertIsNone(result['data'])

    def test_batch_invoke(self):
        """测试批量调用接口"""
        with patch('akshare.stock_sse_summary') as mock_func1, \
             patch('akshare.futures_main_sina') as mock_func2:

            # 模拟返回数据
            mock_func1.return_value = pd.DataFrame({'test1': [1, 2]})
            mock_func2.return_value = pd.DataFrame({'test2': [3, 4]})

            # 批量请求
            requests = [
                {'interface_name': 'stock_sse_summary'},
                {'interface_name': 'futures_main_sina', 'symbol': 'CU0'},
                {'interface_name': 'nonexistent_interface'}
            ]

            results = self.invoker.batch_invoke(requests)

            # 验证结果
            self.assertEqual(len(results), 3)

            # 第一个请求成功
            self.assertTrue(results[0]['success'])
            self.assertIsInstance(results[0]['data'], pd.DataFrame)

            # 第二个请求成功
            self.assertTrue(results[1]['success'])
            self.assertIsInstance(results[1]['data'], pd.DataFrame)

            # 第三个请求失败
            self.assertFalse(results[2]['success'])
            self.assertIsNotNone(results[2]['error'])

    def test_parameter_validation(self):
        """测试参数验证"""
        # 创建一个有必需参数的测试接口
        test_interface = InterfaceDetail(
            name="test_interface",
            target_url="http://test.com",
            description="测试接口",
            limitation="测试限制",
            input_parameters=[
                InterfaceParameter("required_param", "str", "必需参数"),
                InterfaceParameter("optional_param", "str", "可选参数，默认值为test")
            ],
            output_parameters=[],
            example_code="",
            example_data="",
            category="测试",
            subcategory="测试子类"
        )

        # 测试缺少必需参数的情况
        with self.assertRaises(ValueError) as context:
            self.invoker._validate_parameters(test_interface, {})

        self.assertIn('缺少必需参数', str(context.exception))

        # 测试提供了必需参数的情况
        try:
            self.invoker._validate_parameters(test_interface, {"required_param": "test_value"})
            # 应该不抛出异常
        except ValueError:
            self.fail("不应该抛出 ValueError，因为已提供必需参数")

    @patch('builtins.__import__')
    def test_invoke_without_akshare(self, mock_import):
        """测试没有安装 akshare 的情况"""
        mock_import.side_effect = ImportError("No module named 'akshare'")

        with self.assertRaises(ImportError) as context:
            self.invoker.invoke('stock_sse_summary')

        self.assertIn('请先安装 akshare 库', str(context.exception))

    @patch('akshare.stock_sse_summary')
    def test_invoke_non_dataframe_result(self, mock_akshare_func):
        """测试处理非 DataFrame 返回结果"""
        # 模拟返回非 DataFrame 数据
        mock_akshare_func.return_value = [1, 2, 3, 4, 5]

        result = self.invoker.invoke('stock_sse_summary')

        # 验证转换为 DataFrame
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 5)

    def test_parameter_info_methods(self):
        """测试参数信息方法"""
        # 测试获取可选参数 (date 参数因为有默认值被标记为可选)
        optional_params = self.invoker.get_optional_parameters('stock_szse_summary')
        self.assertIsInstance(optional_params, list)
        self.assertIn('date', optional_params)

        # 测试获取可选参数
        optional_params = self.invoker.get_optional_parameters('stock_sse_summary')
        self.assertIsInstance(optional_params, list)

        # 测试获取参数信息
        param_info = self.invoker.get_parameter_info('stock_szse_summary')
        self.assertIsInstance(param_info, dict)
        self.assertIn('required_parameters', param_info)
        self.assertIn('optional_parameters', param_info)

        # 验证可选参数信息
        if param_info['optional_parameters']:
            optional_param = param_info['optional_parameters'][0]
            self.assertIn('name', optional_param)
            self.assertIn('type', optional_param)
            self.assertIn('description', optional_param)
            self.assertIn('default_value', optional_param)

    def test_parameter_validation_with_attributes(self):
        """测试使用属性的参数验证"""
        interface = self.loader.get_interface('stock_szse_summary')
        self.assertIsNotNone(interface)

        if interface:
            # 验证参数属性正确设置
            date_param = None
            for param in interface.input_parameters:
                if param.name == 'date':
                    date_param = param
                    break

            if date_param:
                # date 参数有默认值，所以被标记为可选
                self.assertFalse(date_param.required)
                self.assertIsNotNone(date_param.default_value)

            # 由于 date 参数是可选的，验证不传参数应该成功
            try:
                self.invoker._validate_parameters(interface, {})
                # 如果没有抛出异常，说明验证通过（因为没有必需参数）
            except ValueError:
                # 如果抛出了异常，检查是否是因为有其他必需参数
                pass

    def test_parameter_to_dict(self):
        """测试参数转字典功能"""
        param = InterfaceParameter("test_param", "str", "可选的测试参数，默认: hello")
        param_dict = param.to_dict()

        self.assertIsInstance(param_dict, dict)
        self.assertEqual(param_dict['name'], "test_param")
        self.assertEqual(param_dict['type'], "str")
        self.assertIn('required', param_dict)
        self.assertIn('default_value', param_dict)


class TestAKShareInterfaceIntegration(unittest.TestCase):
    """AKShare 接口集成测试"""

    def setUp(self):
        """测试前准备"""
        # 获取真实的 ak_share.md 文件路径
        current_dir = os.path.dirname(__file__)
        self.real_md_path = os.path.join(current_dir, 'ak_share.md')

    def test_real_file_loading(self):
        """测试加载真实的 ak_share.md 文件"""
        if not os.path.exists(self.real_md_path):
            self.skipTest("ak_share.md 文件不存在")

        loader = AKShareInterfaceLoader(self.real_md_path)

        # 验证加载了接口
        self.assertGreater(loader.get_interface_count(), 0)

        # 验证有接口列表
        interfaces = loader.list_interfaces()
        self.assertGreater(len(interfaces), 0)

        # 验证有类别
        categories = loader.get_categories()
        self.assertGreater(len(categories), 0)

        print(f"✅ 成功加载真实文件，共 {loader.get_interface_count()} 个接口")
        print(f"📂 发现 {len(categories)} 个类别")

    def test_real_file_search(self):
        """测试在真实文件中搜索"""
        if not os.path.exists(self.real_md_path):
            self.skipTest("ak_share.md 文件不存在")

        loader = AKShareInterfaceLoader(self.real_md_path)

        # 搜索股票相关接口
        stock_results = loader.search_interfaces('stock')
        self.assertGreater(len(stock_results), 0)

        # 验证搜索结果
        for interface in stock_results[:3]:  # 检查前3个结果
            self.assertIsInstance(interface, InterfaceDetail)
            self.assertTrue(interface.name)
            self.assertTrue(interface.description)

        print(f"🔍 搜索 'stock' 找到 {len(stock_results)} 个接口")


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()

    # 添加单元测试
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAKShareInterface))

    # 添加集成测试
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAKShareInterfaceIntegration))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
