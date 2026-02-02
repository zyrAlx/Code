import re
import sys
from scipy.stats import chi2

def extract_values(filepath):
    """
    从文件中提取 np、lnL 和 dN/dS 的值。
    """
    with open(filepath, 'r') as file:
        content = file.read()
    
    # 匹配 np 和 lnL
    match = re.search(r'np: (\d+)\):\s*([\S]+)', content)
    if not match:
        raise ValueError(f"无法从文件 {filepath} 中提取 np 和 lnL 值。")

    np_value = int(match.group(1))  # np 的值
    lnL_value = float(match.group(2))  # lnL 的值
    
    # 匹配 w (dN/dS) 或 omega (dN/dS)
    w_match = re.search(r'w \(dN/dS\) for branches:\s*(.+)', content)
    if not w_match:
        w_match = re.search(r'omega \(dN/dS\) =\s*(.+)', content)
    w_value = w_match.group(1).strip() if w_match else "未找到 dN/dS 信息"
    
    return np_value, lnL_value, w_value

def calculate_pvalue(npA, lnLA, npB, lnLB):
    """
    计算 p-value。
    """
    # 计算 df 和 2diff
    df = abs(npA - npB)
    if df == 0:
        raise ValueError("自由度 df 为 0，无法计算 p-value。")
    
    diff = abs(lnLA - lnLB)
    chi2_stat = 2 * diff  # 2diff
    
    # 计算 p-value
    p_value = 1 - chi2.cdf(chi2_stat, df)
    return p_value

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python script.py <文件A路径> <文件B路径>")
        sys.exit(1)
    
    fileA = sys.argv[1]
    fileB = sys.argv[2]
    
    try:
        # 提取文件 A 和 B 的 np, lnL 和 dN/dS 信息
        npA, lnLA, wA = extract_values(fileA)
        npB, lnLB, wB = extract_values(fileB)
        
        # 计算 p-value
        p_value = calculate_pvalue(npA, lnLA, npB, lnLB)
        
        # 输出结果
        print(f"文件 A: npA = {npA}, lnLA = {lnLA}, dN/dS = {wA}")
        print(f"文件 B: npB = {npB}, lnLB = {lnLB}, dN/dS = {wB}")
        print(f"自由度 (df): {abs(npA - npB)}")
        print(f"统计量 (2diff): {2 * abs(lnLA - lnLB)}")
        print(f"p-value: {p_value}")
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
