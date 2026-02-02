from Bio import SeqIO

def parse_gff_for_exons(gff_file):
    """
    提取exon信息
    返回：{parent_id: [(seq_id, start, end, strand), ...]}
    """
    exon_info = {}
    with open(gff_file, 'r') as gff:
        for line in gff:
            if line.startswith("#") or line.strip() == "":
                continue
            parts = line.strip().split("\t")
            if len(parts) < 9 or parts[2].lower() != "exon": 
                continue
            seq_id = parts[0]
            start = int(parts[3])
            end = int(parts[4])
            strand = parts[6]
            attributes = parts[8]
            
            parent_id = None
            for attr in attributes.split(";"):
                if "Parent=" in attr:
                    parent_id = attr.split("=")[1]
                    break
            if not parent_id:
                continue

            if parent_id not in exon_info:
                exon_info[parent_id] = []
            exon_info[parent_id].append((seq_id, start, end, strand))
    
    for parent_id in exon_info:
        exon_info[parent_id].sort(key=lambda x: x[1])
    
    return exon_info

def extract_cds_from_exons(fasta_file, exon_info, output_file):
    """
    根据FASTA文件和exon信息提取CDS序列，并保存到新的FASTA文件中。
    """
    fasta_sequences = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    
    with open(output_file, "w") as outfile:
        for parent_id, exons in exon_info.items():
            cds_sequence = []
            for seq_id, start, end, strand in exons:
                if seq_id not in fasta_sequences:
                    print(f"Warning: Sequence ID {seq_id} not found in FASTA file.")
                    continue
                seq = fasta_sequences[seq_id].seq[start-1:end] 
                if strand == "-":
                    seq = seq.reverse_complement()
                cds_sequence.append(seq)
            
            full_cds = "".join(str(seq) for seq in cds_sequence)
            
            outfile.write(f">{parent_id}\n")
            outfile.write(f"{full_cds}\n")

    print(f"CDS sequences have been saved to {output_file}")


if __name__ == "__main__":
    gff_file = "belPan_41.gff"
    fasta_file = "belPan_part-4.fasta" 
    output_file = "belPan_41_cds.fasta"
    
    exon_info = parse_gff_for_exons(gff_file)
    print(f"Found {len(exon_info)} exons grouped by Parent.")
    
    extract_cds_from_exons(fasta_file, exon_info, output_file)
