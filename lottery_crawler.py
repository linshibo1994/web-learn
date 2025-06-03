import time
import requests
import pandas as pd

def fetch_lottery_data(page_no=1, page_size=30):
    url = "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice"
    params = {
        'name': 'ssq',
        'pageNo': page_no,
        'pageSize': page_size,
        'systemType': 'PC'
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'www.cwl.gov.cn',
        'Referer': 'https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url=url, params=params, headers=headers)
        if response.status_code == 200:
            result = response.json()['result']
            if not result:
                return None
            data = [[int(a['code'])] + [int(k) for k in a['red'].split(',')] + [int(a['blue'])] for a in result]
            return pd.DataFrame(data, columns=['期号', '红球1', '红球2', '红球3', '红球4', '红球5', '红球6', '蓝球'])
        else:
            print(f'请求错误：{response.status_code}')
            return None
    except Exception as e:
        print(f'发生异常：{e}')
        return None

def main():
    data_frames = []
    page = 1
    total_pages = 4  # 获取最近100期数据（每页30期，需要4页）
    
    print("开始爬取双色球开奖数据...")
    
    while page <= total_pages:
        print(f"正在爬取第{page}页数据....")
        new_data = fetch_lottery_data(page)
        
        if new_data is not None:
            print(f"第{page}页数据爬取成功")
            data_frames.append(new_data)
            page += 1
            time.sleep(1)  # 添加延时，避免请求过于频繁
        else:
            print("数据爬取失败，程序退出")
            break
    
    if data_frames:
        # 合并所有数据
        final_data = pd.concat(data_frames, ignore_index=True)
        # 保存到CSV文件
        output_file = 'ssq_latest_100.csv'
        final_data.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"数据已保存到文件：{output_file}")
        print(f"共获取{len(final_data)}期开奖数据")

if __name__ == '__main__':
    main()