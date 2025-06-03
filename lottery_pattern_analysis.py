import pandas as pd
import numpy as np

# 读取CSV文件
df = pd.read_csv('ssq_latest_100.csv')

# 将期号转换为整数以便排序
df['期号'] = df['期号'].astype(int)
df = df.sort_values('期号')

def analyze_consecutive_periods(start_period):
    # 找到起始期的索引
    start_idx = df[df['期号'] == start_period].index[0]
    current_data = df.iloc[start_idx:]
    
    print(f'\n从{start_period}期开始分析：')
    
    # 逐期分析
    for i in range(len(current_data)-1):
        current = current_data.iloc[i]
        next_period = current_data.iloc[i+1]
        
        current_reds = set([current[f'红球{j}'] for j in range(1, 7)])
        next_reds = set([next_period[f'红球{j}'] for j in range(1, 7)])
        
        # 计算重复号码
        repeats = current_reds.intersection(next_reds)
        
        print(f"\n{current['期号']}期号码：红球{[current[f'红球{j}'] for j in range(1, 7)]}，蓝球{current['蓝球']}")
        print(f"与下期重复号码：{list(repeats) if repeats else '无'}")
        
        # 每10期进行小结
        if (i + 1) % 10 == 0:
            period_data = current_data.iloc[i-9:i+1]
            analyze_period_summary(period_data, 10)
        
        # 每20期进行小结
        if (i + 1) % 20 == 0:
            period_data = current_data.iloc[i-19:i+1]
            analyze_period_summary(period_data, 20)
        
        # 每50期进行小结
        if (i + 1) % 50 == 0:
            period_data = current_data.iloc[i-49:i+1]
            analyze_period_summary(period_data, 50)

def analyze_period_summary(data, period_count):
    print(f"\n===== 最近{period_count}期分析 =====")
    
    # 红球出现频率
    red_numbers = pd.Series([])
    for i in range(1, 7):
        red_numbers = pd.concat([red_numbers, data[f'红球{i}']])
    red_freq = red_numbers.value_counts().nlargest(5)
    
    # 蓝球出现频率
    blue_freq = data['蓝球'].value_counts().nlargest(3)
    
    print(f"\n红球出现TOP5：{dict(red_freq)}")
    print(f"蓝球出现TOP3：{dict(blue_freq)}")
    
    # 计算平均重号数
    repeat_count = 0
    for i in range(len(data)-1):
        current_nums = set([data.iloc[i][f'红球{j}'] for j in range(1, 7)])
        next_nums = set([data.iloc[i+1][f'红球{j}'] for j in range(1, 7)])
        repeat_count += len(current_nums.intersection(next_nums))
    
    avg_repeats = repeat_count / (len(data)-1) if len(data) > 1 else 0
    print(f"平均每期重号数：{avg_repeats:.2f}个")

def predict_next_numbers(last_period_data):
    # 基于最近的开奖结果预测下一期可能出现的号码
    recent_reds = []
    for i in range(1, 7):
        recent_reds.extend(last_period_data[f'红球{i}'].tolist())
    
    red_freq = pd.Series(recent_reds).value_counts()
    
    # 选择出现频率较高的红球
    potential_reds = red_freq.nlargest(10).index.tolist()
    
    # 选择出现频率较高的蓝球
    blue_freq = last_period_data['蓝球'].value_counts()
    potential_blues = blue_freq.nlargest(5).index.tolist()
    
    print("\n=== 下期号码预测分析 ===")
    print(f"红球热号（出现频率由高到低）：{potential_reds}")
    print(f"蓝球热号（出现频率由高到低）：{potential_blues}")

def format_numbers(numbers):
    """格式化号码列表，确保输出整数"""
    return [int(x) for x in numbers]

# 修改主程序部分
if __name__ == '__main__':
    start_period = 2024091
    
    # 确保数据按期号降序排列，以便从最早期开始分析
    df['期号'] = df['期号'].astype(str).astype(int)  # 确保期号为整数
    df = df.sort_values('期号', ascending=False)  # 降序排列
    
    # 获取起始期及之后的数据
    analysis_data = df[df['期号'] >= start_period].copy()
    analysis_data = analysis_data.sort_values('期号')
    
    if len(analysis_data) == 0:
        print(f"未找到{start_period}期及之后的数据")
        exit()
    
    print(f'\n从{start_period}期开始分析：')
    
    # 逐期分析
    for i in range(len(analysis_data)-1):
        current = analysis_data.iloc[i]
        next_period = analysis_data.iloc[i+1]
        
        current_reds = format_numbers([current[f'红球{j}'] for j in range(1, 7)])
        next_reds = format_numbers([next_period[f'红球{j}'] for j in range(1, 7)])
        
        # 计算重复号码
        repeats = set(current_reds).intersection(set(next_reds))
        
        print(f"\n{current['期号']}期号码：红球{sorted(current_reds)}，蓝球{int(current['蓝球'])}")
        print(f"下期号码：红球{sorted(next_reds)}，蓝球{int(next_period['蓝球'])}")
        print(f"重复号码：{sorted(list(repeats)) if repeats else '无'}")
        
        # 每10期进行小结
        if (i + 1) % 10 == 0:
            period_data = analysis_data.iloc[max(0, i-9):i+1]
            print(f"\n===== 最近10期分析（{period_data.iloc[0]['期号']}-{period_data.iloc[-1]['期号']}） =====")
            analyze_period_summary(period_data, 10)
        
        # 每20期进行小结
        if (i + 1) % 20 == 0:
            period_data = analysis_data.iloc[max(0, i-19):i+1]
            print(f"\n===== 最近20期分析（{period_data.iloc[0]['期号']}-{period_data.iloc[-1]['期号']}） =====")
            analyze_period_summary(period_data, 20)
        
        # 每50期进行小结
        if (i + 1) % 50 == 0:
            period_data = analysis_data.iloc[max(0, i-49):i+1]
            print(f"\n===== 最近50期分析（{period_data.iloc[0]['期号']}-{period_data.iloc[-1]['期号']}） =====")
            analyze_period_summary(period_data, 50)
    
    # 预测下一期号码
    print("\n=== 下期号码预测分析 ===")
    last_10_periods = analysis_data.tail(10)
    predict_next_numbers(last_10_periods)
    
    print(f"\n最新一期（{df.iloc[0]['期号']}）的号码：")
    latest = df.iloc[0]
    latest_reds = format_numbers([latest[f'红球{j}'] for j in range(1, 7)])
    print(f"红球：{sorted(latest_reds)}")
    print(f"蓝球：{int(latest['蓝球'])}")