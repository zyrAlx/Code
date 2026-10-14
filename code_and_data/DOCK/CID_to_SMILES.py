import pubchempy as pcp
import csv
import sys

if len(sys.argv) < 3:
    print("Usage: python CID_to_SMILES.py input_filename output_filename")
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]

# 读取 CID 列表
with open(input_file, 'r') as file:
    cids = [line.strip() for line in file]

# 查询 SMILES
results = []
for cid in cids:
    try:
        compound = pcp.Compound.from_cid(cid)
        smiles = compound.isomeric_smiles
        results.append((cid, smiles))
    except Exception as e:
        print(f"Error retrieving SMILES for CID {cid}: {e}")

# 写入到 CSV 文件
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['CID', 'SMILE'])  # 写入标题行
    writer.writerows(results)