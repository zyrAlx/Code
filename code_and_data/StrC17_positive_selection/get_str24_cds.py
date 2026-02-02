import logging

logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

Afile_path = "str24_ID.txt"
Bfile_path = "OR_ID_relationship.txt"
fasta_input_path = "all_or_cds.fasta"
output_fasta_path = "str24_csd.fasta"

def load_afile(filepath):
    with open(filepath, "r") as file:
        return [line.strip() for line in file]

def load_bfile(filepath):
    abbr = {}
    with open(filepath, "r") as file:
        lines = [line.strip() for line in file]
        for i in range(0, len(lines), 2):
            key = lines[i]
            value = lines[i + 1][1:] if i + 1 < len(lines) else None
            if value:
                abbr[key] = value
    return abbr

def parse_fasta(filepath):
    sequences = {}
    current_id = None
    current_seq = []
    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if current_id:
                    sequences[current_id] = "".join(current_seq)
                current_id = line[1:] 
                current_seq = []
            else:
                current_seq.append(line)
        if current_id:
            sequences[current_id] = "".join(current_seq)
    return sequences

def write_fasta(output_path, results):
    with open(output_path, "w") as file:
        for key, (identifier, sequence) in results.items():
            file.write(f">{key}\n{sequence}\n")

def process_files():
    Afile = load_afile(Afile_path)
    abbr = load_bfile(Bfile_path)
    fasta_sequences = parse_fasta(fasta_input_path)
    
    results = {}
    for key in Afile:
        if key in abbr:
            value = abbr[key]
            if value in fasta_sequences:
                results[key] = (value, fasta_sequences[value])
            else:
                logging.warning(f"Sequence not found for identifier '{value}' from key '{key}'.")
        else:
            logging.warning(f"Key '{key}' not found in Bfile.")
    
    if results:
        write_fasta(output_fasta_path, results)
        print(f"处理完成，结果已保存到 {output_fasta_path}")
    else:
        print("未找到任何匹配的序列，未生成输出文件。")


process_files()
