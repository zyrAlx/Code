mkdir -p trans
cd trans

perl ../translatorX.pl -i ../str24_cds_rm_stop_codon.fasta -p F -o mafft_translatorx
cd ..
mkdir -p alignments_mafft
cp trans/mafft_translatorx.nt_ali.fasta alignments_mafft/str24_nuc_mafft_aln.fasta
cp trans/mafft_translatorx.aa_ali.fasta alignments_mafft/str24_prot_mafft_aln.fasta

cd alignments_mafft
mkdir -p pal2nal_checks

perl ../pal2nal.pl str24_prot_mafft_aln.fasta str24_nuc_mafft_aln.fasta -output fasta > pal2nal_checks/str24_pal2nal_mafft_out.fasta
# Convert output file to one line fasta file
perl ../one_line_fasta.pl pal2nal_checks/str24_pal2nal_mafft_out.fasta


num=$( grep '>' str24_nuc_mafft_aln.fasta | wc -l )
len=$( sed -n '2,2p' str24_nuc_mafft_aln.fasta | sed 's/\r//' | sed 's/\n//' | wc --m )
perl ../FASTAtoPHYL.pl str24_nuc_mafft_aln.fasta $num $len 
mv str24_nuc_mafft_aln.phy str24_mafft.phy
cp str24_mafft.phy ..
cd ..