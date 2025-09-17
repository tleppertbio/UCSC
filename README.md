
# gvcf_to_maple_haploid.py

**What does this gvcf_to_maple_haploid.py do**
Reads an interprets a C. auris .g.vcf.gz sample file and returns its content in .maple format.

---

## How to Invoke/Execute

gvcf_to_maple_haploid.py takes 4 command line Arguments:  

     1) vcf_file_path (str): Path to the .g.vcf.gz file (can read non gzipped files).                                                           
     2) DP_min_val: Minimum Read Depth - bases/sequences with read depth < this value will be returned as 'n'          
        recommended value 20 - minimum read depth of 20 to pass                                                        
     3) GQ_min_val: Minimum Genotype Quality - bases/sequences with GQ < this value will be returned as 'n'             
        recommended value 99 - minimum GQ score of 99 to pass                                                          
     4) "AND" or "OR" - used as: DP_min_val AND GQ_min_val, or used as DP_min_val OR GQ_min_val criteria.              
        recommended value AND - DP_min_val AND GQ_min_val - both DP_min_val AND GQ_min_val must pass to meet criteria  
        
Example:                                                                                                                   
  gvcf_to_maple_haploid.py SRR21943188.g.vcf.gz 20 99 AND                                                               
                                                                                                                                                                                                                                                
---

<br>

## Input .g.vcf file format
A 10 column table occurs after leading comment lines (lines with '#' in column 1).

|1    |2    |3    |4    |5    |6    |7     |8    |9     |10         |
|-----|-----|-----|-----|-----|-----|------|-----|------|-----------|
|CHROM|POS  |ID   |REF  |ALT  |QUAL |FILTER|INFO |FORMAT|SRR25455197|      

<br>
                                                                                                                 
### All possibilities for column 4 and 5
Note: Column 5 may contain more than one alternate allele - each separated by a ','

|Column 4    |Column 5               |                           |
|------------|-----------------------|---------------------------|
|T           |<NON_REF>              |Reference and no alternate |
|T           |A,<NON_REF>            |Reference and alternate    |
|A           |AAGGCT,<NON_REF>       |insertion of AGGCT         |
|TAAAACTATGC |T,<NON_REF>            |deletion of AAAACTATGC     |

<br>
    
### All possibilities for column 8                                                                                         
see.. https://gatk.broadinstitute.org/hc/en-us/articles/360035531692-VCF-Variant-Call-Format for .g.vcf documentation 

DP:integer:="Approximate read depth (reads with MQ=255 or with bad mates are filtered)"                                
MLEAC:integer,:A:="Maximum likelihood expectation (MLE) for the allele counts (not necessarily the same as the AC), for each ALT allele, in the same order as listed"                                                                          
MLEAF:float,:A:x.xx:="Maximum likelihood expectation (MLE) for the allele frequency (not necessarily the same as the AF), for each ALT allele, in the same order as listed"                                                                    
MQRankSum="Z-score:float:x.xxx: From Wilcoxon rank sum test of Alt vs. Ref read mapping qualities"                     
RAW_MQandDP:integer:2:xxxxxx,xxx:="Raw data (sum of squared MQ and total depth) for improved RMS Mapping Quality calculation. Incompatible with deprecated RAW_MQ formulation."                                                                
ReadPosRankSum:float:(-)x.xxx:="Z-score from Wilcoxon rank sum test of Alt vs. Ref read position bias"                 
BaseQRankSum:float:(-_x.xxx:="Z-score from Wilcoxon rank sum test of Alt Vs. Ref base qualities"                       
END:integer:="Stop position of the interval" (always by itself)                                                        

<br>
                                     
### All possibilities for column 10 (label/format in column 9)                                                    
see.. https://gatk.broadinstitute.org/hc/en-us/articles/360035531692-VCF-Variant-Call-Format  

GT:integer:0,1,.,x="Genotype" (. = n) (0 = reference) (x = which non reference base/sequence)                          
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*The genotype of this sample at this site. For a diploid organism, the GT field indicates the two alleles*            
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*carried by the sample, encoded by a 0 for the REF allele, 1 for the first ALT allele, 2 for the second ALT*            
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*allele, etc. When there is a single ALT allele (by far the more common case), GT will be either:*               
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Tami- in spite of c. auris not being diploid, I believe the 0= reference allele was used.*                       
DP:integer:"Approximate read depth; some reads may have been filtered"                                                 
GQ:integer:"Genotype Quality"                                                                                          
MIN_DP:integer:"Minimum DP observed within the GVCF block"                                                             
PL:integer:"Normalized, Phred-scaled likelihoods for genotypes as defined in the VCF specification"                    
MIN_PL:integer:"Minimum PL observed within the GVCF block"                                                             
AD:integer:Allelic depths for the ref and alt alleles in the order listed"                                             
SB:integer:"Per-sample component statistics which comprise the Fisher's Exact Test to detect strand bias."             

<br>

### EXAMPLE:

|1          |2     |3  |4  |5                                     |6      |7     |8                                                                                                                |9                 |10                                                              |Added comment by Tami|                               
|-----------|------|---|---|--------------------------------------|-------|------|-----------------------------------------------------------------------------------------------------------------|------------------|----------------------------------------------------------------|---------------------|
|CHROM      |POS   |ID |REF|ALT                                   |QUAL   |FILTER|INFO                                                                                                             |FORMAT            |SRR25455197                                                     |                     |
|CP043531.1 |    1 | . |A  |<NON_REF>                             |.      |.     |END=372                                                                                                          |GT:DP:GQ:MIN_DP:PL|0:0:0:0:0,0                                                     |                     |
|CP043531.1 |  373 | . |C  |<NON_REF>                             |.      |.     |END=487                                                                                                          |GT:DP:GQ:MIN_DP:PL|0:97:99:54:0,1730                                               |                     |
|CP043531.1 |  488 | . |T  |C,<NON_REF>                           |4572.04|.     |DP=102;MLEAC=1,0;MLEAF=1.00,0.00;RAW_MQandDP=367200,102                                                          |GT:AD:DP:GQ:PL:SB |1:0,102,0:102:99:4582,0,4582:0,0,67,35                          |                     |
|CP043531.1 |  524 | . |TC |T,<NON_REF>                           |5345.01|.     |DP=119;MLEAC=1,0;MLEAF=1.00,0.00;RAW_MQandDP=428400,119                                                          |GT:AD:DP:GQ:PL:SB |1:0,119,0:119:99:5355,0,5355:0,0,82,37                          |*deletion event*     |                                       
|CP043531.1 |  544 | . |A  |C,AGCAC,AGCCC,<NON_REF>               |5056.04|.     |DP=113;MLEAC=1,0,0,0;MLEAF=1.00,0.00,0.00,0.00; RAW_MQandDP=406800,113                                           |GT:AD:DP:GQ:PL:SB |1:0,109,1,0,0:110:99:5066,0,4891,4794,4910:0,0,73,37            |                     |               
|CP043531.1 | 1202 | . |G  |T,<NON_REF>                           |4209.04|.     |BaseQRankSum=2.013;DP=139;MLEAC=1,0;MLEAF=1.00,0.00; MQRankSum=0.000;RAW_MQandDP=500400,139;ReadPosRankSum=-1.304|GT:AD:DP:GQ:PL:SB |1:2,135,0:137:99:4219,0,4238:0,2,71,64                          |                     |
|CP043531.1 |25273 | . |T  |TAC,TCCC,TCCCC,TACCCC,TCCCCC,<NON_REF>|4047.01|.     |DP=97;MLEAC=0,0,1,0,0,0;MLEAF=0.00,0.00,1.00,0.00,0.00,0.00; RAW_MQandDP=349200,97                               |GT:AD:DP:GQ:PL:SB |3:0,0,0,90,0,0,0:90:99:4057,4139,3457,0,3597,3998,4025:0,0,38,52|                     |
|CP043531.1 |901271| . |A  |AT,<NON_REF>                          |0      |.     |MLEAC=0,0;MLEAF=NaN,NaN                                                                                          |GT:GQ:PL          |.:0:0,0,0                                                       |*insertion event*    |                                                                                                       
                                                                                                                                                                                                                                                 
Algorithm notes:                                                                                                                        
A reference segment (may be more than one base) - is indicated by column 5 has only '<NON_REF>'                 
When column 5 is only "<NON_REF>", column 10 always starts with 0: column 9 always starts with 'GT:DP:GQ'        
When column 5 is only "<NON_REF>", there are never multiple choice alternate alleles                      
Check reference allele passes the DP and GQ user defined criteria, if not print 'n'                                                      
                                                                                                                         
Check to see if the reference allele more than one base, if so skip output for this position in the maple file          
Multiple base reference usually indicates a deletion event- note the exception is not addressed here. 
The exception: If the reference allele is n bases long and the best alternate allele is the same length,  
this would not be an insertion event, but the maple cannot have a multi base string- multiple bases are not handled at this time.  
                                                                                                                         
Check to see if this is a alternate segment.  Note column 10, first integer indicates which alternate allele to use.
When column 5 has more than one option (is has a ',') as in ",<NON_REF>", column 9 is always 'GT:AD:DP:GQ'  
When column 5 ",<NON_REF>" there can be multiple alternate alleles, the best alternate is indicated by the value of GT.
When GT == '.', skip this entry
A possible future modification: check the AD is > DP_min_val, use DP instead of individual AD                                                                                                                     
For the alternate allele, check the DP and GQ pass the user criteria, if not print 'n'                                          
For the alternate allele, check the alternate allele is only one base (no inserts allowed!), skip if multiple bases.                                                                    
  
Check to see if this is a bad call, this occurs when column 9 is 'GT:GQ:PL' - there is no read depth, skip this position.

Specifically for C. auris      
At the start of each chromosome the header '>SRR#_chrom#' is printed in the .maple file.
At the end of the chromosome, the position counter is advanced to the base after the end of the chromosome.  

Date of project 9/2/2025  
Version of project v 1.0 
