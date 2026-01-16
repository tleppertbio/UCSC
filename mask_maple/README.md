
# mask_maple.py

**What does this mask_maple.py do**
Reads a list of .maple sample files and a .bed mask file and returns the masked .maple files in a user defined directory.

---

## How to Invoke/Execute

mask_maple.py takes 3 command line Arguments:  

     1) -l file containing a list of .maple files, file paths to files are relative to current directory.
     2) -m a .bed file (string): .bed file contains masking regions.
     3) -d directory to use to store all the processed masked .maple files, file path relative to current directory
        
Example:                                                                                                                   
  mask_maple.py -l maple.list -m mask.bed -d masked_maples
                                                                                                                                                                                                                                                
---

<br>

## Input file with list of .maple files.
A file with list of .maple files, paths are relative to the current directory.
All files in the input file list will be masked and written to the output masked .maple files
The path to the input .maple file is not considered in the output filename.
An example of four different ways to write paths to .maple files.

/file/to/maple/SRR111222.maple
subdirectory/SRR2223333.maple
../SRR113444.maple
SRR114666.maple


<br>

## Input .maple file format
A 3 column tab separated table occurs after leading header line (line with '>' in column 1).
Header lines can occur multiple times in multi chromosome .maple files, in this program, we
require .maple files to only contain data for one chromosome at a time.  The following 8 line
file is an example of a .maple file and contains examples of different kinds of information.

>SRR114666|State|County|Clade
n	1	5
A	8
-	10	2
G	14
C	15
T	35
n	40	12

line 1 begins with '>' and is a header for the file
line 2 begins with 'n' - the next two columns 1 and 4 indicate that there are 'n's from sequence 1 through to sequence 4.
                   'n' and '-' data will have 3 columns of data, the original 'n' or '-' then in the second column, a start
		   sequence position and in the third column, the total number of n's from the start sequence.
		   In this case there are 4 'n's starting at sequence position 1 and ending at sequence position 4
line 3 begins with 'A' and the sequence position is 8.
line 4 begins with '-', like the 'n', there are two columns that follow.  The column following the '-' is the start sequence
                   position of the sequence that is '-' or missing.  The third column is the total number of '-'s from the
		   start of the missing sequence 10 to the final position of the series, sequence position 11.
line 5 begins with 'G' and the sequence position is 14.
line 6 begins with 'C' and the sequence position is 15.
line 7 begins with 'T' and the sequence position is 35.
line 8 begins with 'n', the n's on this line span from sequence position 40 to sequence position 51.
		   
		  

<br>
                                                                                                                 
## Input .bed file format
A 5 column tab separated table.  The first column is the string that represents the RefSeq number, these numbers are
associated with a chromosome.  Note again here, the .maple files should only contain 1 chromosome at a time and likewise,
the .bed file should also only contain one chromosome at a time.  This program does NOT check to see if you are using
the same chromosome number in the .bed file you specify and the .maple files you list.  Make sure the .maple files are
for the same chromosome that you have listed in the .bed file!!!  This program ignores the first column in the .bed file.
The second column is the [start-position - 1] of the masking region and the third column is the end position of the masking
region.  The final two columns are ignored by this program.

The start position from the bed automatically has +1 added to the start sequence index.  The .bed file and the .maple
files do not share the same indexing algorithm.  The .maple file starts indexing the sequence at position 1, the .bed file
starts the indexing of the sequence at position 0.  You will see in the mask_maple.py algorithm that the start_pos will
have +1 added as it is read in.  The end position will not have this offset applied.  The end position in the .bed file
is known as 'half-open' index. This means that the end position indicated is the actual index of the sequence where the
masking will end.

<br>
                                     
### Algorithm

S = start_pos
E = end_pos
* = location
+ = represents the length of the extension (for 'n' base or '-' deletion regions only)

while (end_pos < location)
    S----------E    if location is after masking region - then read the next masking region
                    *                                                                                   

if (extension != 0)                                                                                  
  if (start_pos <= location) and (end_pos < location+extension) and (end_pos >= location):             
    S----------E    'n's or '-'s after masking region are not masked                                      
             *++++
	     
  elif (start_pos >= location+extension):
        S----------E  'n's or '-'s prior to masking region are not masked                                      
 *++++
 
  elif (start_pos > location) and (start_pos < location+extension) and (end_pos > location+extension): 
    S----------E    'n's or '-'s prior to masking region are not masked                                      
 *++++
 
  elif (start_pos > location) and (start_pos < location+extension) and (end_pos < location+extension): 
    S----------E    'n's or '-'s prior to and after masking region are not masked                            
  *+++++++++++++++

  else implied default
    S----------E    Do not print, mask these positions                                                  
        *++++

elif (extension == 0)                                                                                  
  if (start_pos > location)                                                                          
    S----------E    Do not mask this position                                                         
  *    

  else implied default
  S----------E    Do not print, mask this position                                                  
        *                                                                                            

<br>

Date of project 1/13/2026
Version of project v 3.0 
