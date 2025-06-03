import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
df = pd.read_csv('ssq_latest_100.csv')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def analyze_numbers():
    # 分析红球出现频率
    red_numbers = pd.Series([])
    for i in range(1, 7):
        red_numbers = pd.concat([red_numbers, df[f'红球{i}']])
    red_freq = red_numbers.value_counts().sort_index()
    
    # 分析蓝球出现频率
    blue_freq = df['蓝球'].value_counts().sort_index()
    
    # 计算连号情况
    consecutive_count = 0
    for _, row in df.iterrows():
        red_nums = sorted([row[f'红球{i}'] for i in range(1, 7)])
        for i in range(len(red_nums)-1):
            if red_nums[i+1] - red_nums[i] == 1:
                consecutive_count += 1
    
    # 计算重号（与上一期相同的号码）
    repeat_count = 0
    for i in range(len(df)-1):
        current_nums = set([df.iloc[i][f'红球{j}'] for j in range(1, 7)])
        next_nums = set([df.iloc[i+1][f'红球{j}'] for j in range(1, 7)])
        repeat_count += len(current_nums.intersection(next_nums))
    
    # 绘制红球频率图
    plt.figure(figsize=(15, 6))
    plt.subplot(1, 2, 1)
    red_freq.plot(kind='bar')
    plt.title('红球出现频率')
    plt.xlabel('号码')
    plt.ylabel('出现次数')
    
    # 绘制蓝球频率图
    plt.subplot(1, 2, 2)
    blue_freq.plot(kind='bar')
    plt.title('蓝球出现频率')
    plt.xlabel('号码')
    plt.ylabel('出现次数')
    
    plt.tight_layout()
    plt.savefig('lottery_analysis.png')
    
    # 输出统计结果
    print('\n=== 双色球数据分析 ===')
    print(f'\n分析期数：{len(df)}期')
    print('\n红球出现频率（前5名）：')
    print(red_freq.nlargest(5))
    print('\n蓝球出现频率（前5名）：')
    print(blue_freq.nlargest(5))
    print(f'\n连号出现次数：{consecutive_count}次')
    print(f'平均每期连号次数：{consecutive_count/len(df):.2f}次')
    print(f'\n重号总数：{repeat_count}个')
    print(f'平均每期重号数：{repeat_count/(len(df)-1):.2f}个')

if __name__ == '__main__':
    analyze_numbers()