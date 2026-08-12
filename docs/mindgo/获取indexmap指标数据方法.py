import pandas as pd

def 通用取数函数(apiid, BASE_TIME):
    """
    获取异动股票列表
    
    参数:
        apiid: API ID，如 '985' 表示异动股票
        BASE_TIME: 交易日期，格式 'YYYYMMDD'
    
    返回:
        DataFrame，包含股票代码等信息
    """
    api = get_arsenal_api('cbas-babel-frondend-pod')
    r = api.post('/babel/api/query_index',
                files={'queryId': (None, apiid), "baseDay": (None, BASE_TIME)})
    data = r.json()
    print(data)
    # 解析返回数据
    key_to_label = {item['key']: item['label'] for item in data['titles']}
    processed_data = []
    
    df = pd.DataFrame(processed_data)
    df["trade_date"] = BASE_TIME
    return df