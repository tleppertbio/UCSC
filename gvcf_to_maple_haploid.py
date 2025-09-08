#!/usr/bin/env python3
# Program gvcf_to_maple_haploid.py
# Tami Leppert
# 9/2/2025
# v 1.0
#

import sys
import os
import gzip
import argparse

def read_vcf(vcf_file_path):

    #  Reads a VCF.gzipd file and returns its content as a list of lines, 
    #  skipping comment lines.
    #
    #  Arguments:
    #      vcf_file_path (str): Path to the VCF file (gzipped).
    #
    #  Returns:
    #     list: A list of strings, where each string is a line from the VCF file.


    # lines to return
    lines = []
    global maple_fileout
    # Initialize the output maplefile name
    maple_fileout="initialize"

    
    # read gzip *.g.vcf.gz file
    try:
        # open the gzip file in text mode for automatic decompression
        with gzip.open(vcf_file_path, 'rt') as file:

            # replace string "g.vcf.gz" with "maple" for output file
            maple_fileout = vcf_file_path.replace("g.vcf.gz","maple")

            for line in file:                       # Read each line
                if not line.startswith('#'):        # If the line does not begin with a comment '#'
                    lines.append(line.strip())      # Save the lines in the array lines.
                    
    except FileNotFoundError:
         print(f"Error: The file '{vcf_file_path}' was not found.")
         
    except gzip.BadGzipFile:
        try:
            # for non gzip file
            with open(vcf_file_path, 'r') as file:

                # replace string "g.vcf" with "maple" for output file                
                maple_fileout = vcf_file_path.replace("g.vcf","maple")

                for line in file:
                    if not line.startswith('#'):
                        lines.append(line.strip())
                        
        except Exception as e:
             print(f"Error reading file non-gzip: {e}")
             return None
         
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return lines

#            
#END of def read_vcf(vcf_file_path):
#


def process_arguments_vcf():

    #  Checks to see that 4 arguments are entered on the command line
    #
    #  Arguments:
    #      1) vcf_file_path (str): Path to the VCF file (gzipped).
    #      2) DP_min_val as a command line argument
    #      3) GQ_min_val as a command line argument
    #      4) "AND" or "OR" as a command line argument to select choice A or choice B
    #
    #  No return unless 4 valid arguments have been entered.
    #
    parser = argparse.ArgumentParser(description="A script that takes four command-line arguments.")
    parser.add_argument("arg1", help="The first argument, the name of the g.vcf.gz file.")
    parser.add_argument("arg2", help="The second argument, the value (integer) of the minimum read depth allowed; recommend using 20.")
    parser.add_argument("arg3", help="The third argument, the value (integer) of the minimum confidence quality allowed; recommend using 99.")
    parser.add_argument("arg4", help="The fourth argument, the text 'AND' or the text 'OR' (no quotes). Usage example: min_read_depth AND min_conf ; recommend using AND.")

    global vcf_filename    # The first argument
    global DP_min_val      # The second argument
    global DP_min_val_int  # The second argument cast to integer
    global GQ_min_val      # The third argument
    global GQ_min_val_int  # The third argument cast to integer
    global choice          # The fourth argument
    vcf_filename = ""      # Initialize filename
    
    # Check to see if 4 arguments have been entered
    if len(sys.argv) != 5:  # Script name + 4 arguments 
        print(f"Error: Please provide 4 parameters, a vcf file name to process, a DP_min_val, a GQ_min_val and 'AND' or 'OR' choice.")
    else:
        vcf_filename = sys.argv[1]        
        DP_min_val = sys.argv[2]
        GQ_min_val = sys.argv[3]
        choice = sys.argv[4]
        
        if not os.path.exists(vcf_filename):
            print(f"Error: The first argument '{vcf_filename}' is not a file.")
            sys.exit(1)
            
        try:
            DP_min_val_int = int(DP_min_val)
        except ValueError:
            print(f"Error: The second argument '{DP_min_val}' is not an integer.")
            sys.exit(1)            
        except TypeError:
            print(f"Error: The second argument '{DP_min_val}' is not an integer, invalid type.")
            sys.exit(1)            
        if not DP_min_val.isdigit:
            print(f"Error: The second argument '{DP_min_val}' is not an integer, invalid type.")
            sys.exit(1)            
            
        try:
            GQ_min_val_int = int(GQ_min_val)
        except ValueError:
            print(f"Error: The third argument '{GQ_min_val}' is not an integer.")
            sys.exit(1)            
        except TypeError:
            print(f"Error: The third argument '{GQ_min_val}' is not an integer, invalid type.")
            sys.exit(1)            
        if not GQ_min_val.isdigit:
            print(f"Error: The third argument '{GQ_min_val}' is not an integer, invalid type.")
            sys.exit(1)
            
        if (choice != "AND") and (choice != "OR"):
            print(f"Error: The fourth argument '{choice}' must be 'AND' or 'OR'.")
            sys.exit(1)            

#            
#END of def process_arguments_vcf():
#



########################################
########################################
# Main
########################################

# Read a VCF.gzipd file, processes its contents and outputs a maple file
#
# Arguments:
#      inputfile.g.vcf.gz as a command line argument
#      DP_min_val as a command line argument
#      GQ_min_val as a command line argument
#      "AND" or "OR" as a command line argument to select choice A or choice B
#
# Returns:
#      a maple file - processed with the following filters;
#         if the DP (read depth of the segment) is >= DP_min_val
#         if the GQ (genome quality confidence value) is >= GQ_min_val
#         choice A) (DP >= DP_min_val) OR (GQ >= GQ_min_val)
#         choice B) (DP >= DP_min_val) AND (GQ >= GQ_min_val)
#
#         recommended values DP_min_val = 20, GQ_min_val = 99, choice B (AND)
#
#
# Each line consists of 10 columns:
# 1      2        3   4        5        6             7               8               9                10
# CHROM  POS      ID  REF      ALT      QUAL          FILTER          INFO            FORMAT           SRR25455197
# string position '.' ref_base alt_base quality_score filter_value(.) info(key+value) format(key only) sample_data
#
# ALL possibilities for column 4 and 5
# T <NON_REF>              # Reference and no alternate        
# T A,<NON_REF>            # Reference and alternate
# A AAGGCT,<NON_REF>       # insertion of AGGCT
# TAAAACTATGC T,<NON_REF>  # deletion of AAAACTATGC
#
# ALL possibilities for column 8
# see.. https://gatk.broadinstitute.org/hc/en-us/articles/360035531692-VCF-Variant-Call-Format
# DP:integer:="Approximate read depth (reads with MQ=255 or with bad mates are filtered)"
# MLEAC:integer,:A:="Maximum likelihood expectation (MLE) for the allele counts (not necessarily the same as the AC), for each ALT allele, in the same order as listed"
# MLEAF:float,:A:x.xx:="Maximum likelihood expectation (MLE) for the allele frequency (not necessarily the same as the AF), for each ALT allele, in the same order as listed"
# MQRankSum="Z-score:float:x.xxx: From Wilcoxon rank sum test of Alt vs. Ref read mapping qualities"
# RAW_MQandDP:integer:2:xxxxxx,xxx:="Raw data (sum of squared MQ and total depth) for improved RMS Mapping Quality calculation. Incompatible with deprecated RAW_MQ formulation."
# ReadPosRankSum:float:(-)x.xxx:="Z-score from Wilcoxon rank sum test of Alt vs. Ref read position bias"
# BaseQRankSum:float:(-_x.xxx:="Z-score from Wilcoxon rank sum test of Alt Vs. Ref base qualities"
# END:integer:="Stop position of the interval" (always by itself)
#
# ALL possibilities for column 10 (label/format is found in column 9)
# see.. https://gatk.broadinstitute.org/hc/en-us/articles/360035531692-VCF-Variant-Call-Format        
# GT:integer:0,1,.,x="Genotype" (. = n) (0 = reference) (x = which non reference base/sequence)
 ##The genotype of this sample at this site. For a diploid organism, the GT field indicates the two alleles
 ##carried by the sample, encoded by a 0 for the REF allele, 1 for the first ALT allele, 2 for the second ALT
 ##allele, etc. When there is a single ALT allele (by far the more common case), GT will be either:
 ##Tami- in spite of c. auris not being diploid, I believe the 0= reference allele was used.
# DP:integer:"Approximate read depth; some reads may have been filtered"
# GQ:integer:"Genotype Quality"
# MIN_DP:integer:"Minimum DP observed within the GVCF block"
# PL:integer:"Normalized, Phred-scaled likelihoods for genotypes as defined in the VCF specification"
# MIN_PL:integer:"Minimum PL observed within the GVCF block"
# AD:integer:Allelic depths for the ref and alt alleles in the order listed"
# SB:integer:"Per-sample component statistics which comprise the Fisher's Exact Test to detect strand bias."
#
# EXAMPLE:
# 0             1  2  3     4                       5    6      7      8                9
# CHROM       POS ID REF   ALT                     QUAL FILTER INFO    FORMAT           SRR25455197
#CP043531.1      1 .  A   <NON_REF>                   .   .     END=372 GT:DP:GQ:MIN_DP:PL 0:0:0:0:0,0
#CP043531.1    373 .  C   <NON_REF>                   .   .     END=487 GT:DP:GQ:MIN_DP:PL 0:97:99:54:0,1730
#CP043531.1    488 .  T   C,<NON_REF>             4572.04 .     DP=102;MLEAC=1,0;MLEAF=1.00,0.00;RAW_MQandDP=367200,102 GT:AD:DP:GQ:PL:SB 1:0,102,0:102:99:4582,0,4582:0,0,67,35
#CP043531.1    524 . TC   T,<NON_REF>             5345.01 .     DP=119;MLEAC=1,0;MLEAF=1.00,0.00;RAW_MQandDP=428400,119 GT:AD:DP:GQ:PL:SB 1:0,119,0:119:99:5355,0,5355:0,0,82,37    ##deletion event
#CP043531.1    544 .  A   C,AGCAC,AGCCC,<NON_REF> 5056.04 .     DP=113;MLEAC=1,0,0,0;MLEAF=1.00,0.00,0.00,0.00;RAW_MQandDP=406800,113 GT:AD:DP:GQ:PL:SB 1:0,109,1,0,0:110:99:5066,0,4891,4794,4910:0,0,73,37
#CP043531.1   1202 .  G   T,<NON_REF>             4209.04 .     BaseQRankSum=2.013;DP=139;MLEAC=1,0;MLEAF=1.00,0.00;MQRankSum=0.000;RAW_MQandDP=500400,139;ReadPosRankSum=-1.304 GT:AD:DP:GQ:PL:SB 1:2,135,0:137:99:4219,0,4238:0,2,71,64
#CP043531.1  25273 .  T   TAC,TCCC,TCCCC,TACCCC,TCCCCC,<NON_REF>  4047.01 . DP=97;MLEAC=0,0,1,0,0,0;MLEAF=0.00,0.00,1.00,0.00,0.00,0.00;RAW_MQandDP=349200,97 GT:AD:DP:GQ:PL:SB 3:0,0,0,90,0,0,0:90:99:4057,4139,3457,0,3597,3998,4025:0,0,38,52
#CP043531.1 901271 .  A   AT,<NON_REF>                0   .     MLEAC=0,0;MLEAF=NaN,NaN GT:GQ:PL        .:0:0,0,0 ##insertion event
#
#


# Check the command line arguments
process_arguments_vcf()


# Read the contents of the gvcf file into vcf_data - an array of strings
if vcf_filename != "":
    vcf_data = read_vcf(vcf_filename)
else:
    sys.exit(1)

# Initialize g.vcf.gz chromosome string
chromosome="initialize"
chromosome_number = 0

# If input file was read into vcf_data
if vcf_data:

    # Check the output maplefile name
    if ".maple" in maple_fileout:
        try:
            # open maplefile for writing
            with open(maple_fileout, 'w') as outfile:

                # process lines in input file
                for line in vcf_data:

                    # split line into array aline by tab separator
                    aline = line.split('\t')

                    # Check to see if this is a new chromosome; using filename as chromosome number:
                    if aline[0] != chromosome:
                        chromosome_number += 1
                        chromosome_text = maple_fileout.replace(".maple","_") + str(chromosome_number)
                        chromosome = aline[0]                       #save the g.vcf.gz new chromosome string
                        output_string=f">{chromosome_text}\n"       #make header for maple file data for next chromosome

                        outfile.write(output_string)   #print the header to the maple file

                    # Check to see if this is a reference segment.  Note col 8 always starts with 'GT:'
                    # When col 4 is only "<NON_REF>" aline[9] always starts with 0: aline[8] is always 'GT:DP:GQ'
                    # When col 4 is only "<NON_REF>" there are no multiple choice alternate alleles
                    # Check the DP and GQ pass the user criteria        
                    if (aline[4] == "<NON_REF>") and (aline[8].startswith("GT:DP:GQ")) and (aline[9].startswith("0:")):
                        missing_call = 0
                        # split aline[9] by ':' into values for 'GT:DP:GQ:'
                        stats = aline[9].split(':')

                        # check if critera is not met for validated reference sequence
                        if (choice == 'AND'):
                            if (int(stats[1]) < DP_min_val_int) or (int(stats[2]) < GQ_min_val_int):
                                missing_call = 1
                        elif (choice == 'OR'):
                            if ((int(stats[1]) < DP_min_val_int) and (int(stats[2]) < GQ_min_val_int)):
                                missing_call = 1

                        # if critera is not met for validated reference sequence, print sequence as 'missing' or 'n'
                        if missing_call:
                            end_of_sequence = aline[7].split('=')

                            # This section is specifically for C. auris
                            # If you are using this code for another organism, then the number of chromosomes and the
                            # size of each chromosome will need to be altered here.
                            # At the end of a chromosome, the increment will be 0 - not 1, we are not going to the next base
                            increment = 1
                            if (chromosome_number == 1) and (int(end_of_sequence[1]) == 3148135) and (int(aline[1]) != 1): increment = 0
                            elif (chromosome_number == 2) and (int(end_of_sequence[1]) == 2554418) and (int(aline[1]) != 1): increment = 0
                            elif (chromosome_number == 3) and (int(end_of_sequence[1]) == 2336890) and (int(aline[1]) != 1): increment = 0
                            elif (chromosome_number == 4) and (int(end_of_sequence[1]) == 1318327) and (int(aline[1]) != 1): increment = 0
                            elif (chromosome_number == 5) and (int(end_of_sequence[1]) == 1007026) and (int(aline[1]) != 1): increment = 0
                            elif (chromosome_number == 6) and (int(end_of_sequence[1]) == 1004684) and (int(aline[1]) != 1): increment = 0
                            elif (chromosome_number == 7) and (int(end_of_sequence[1]) == 880293) and (int(aline[1]) != 1): increment = 0
                            
                            output_string = f"n\t{aline[1]}\t{str(int(end_of_sequence[1])-int(aline[1])+int(increment))}\n"
                            outfile.write(output_string)

                    # Check to see if the reference allele is only one base, if it is print as 'missing' or 'n'
                    # This indicates a deletion - note there could possibly be an exception which is not addressed here.
                    # If the reference allele is n bases long and the best alternate allele is the same length, then this 
                    # would not be an insertion event, but the maple cannot have a multi base string (? is this true?)
                    elif len(aline[3]) > 1:
                        output_string = f"n\t{aline[1]}\n"
                        outfile.write(output_string)
                
                    # Check to see if this is a alternate segment.  Note col 8 always starts with 'GT:'
                    # When col 4 has more than one option (has ',') as in ",<NON_REF>" aline[8] is always 'GT:AD:DP:GQ'
                    # When col 4 ",<NON_REF>" there can be multiple alternate alleles, the best alternate is the value of GT
                    # Check the value of GT, ##DISCARD THIS -> check the AD is > DP_min_val, use DP instead of individual AD
                    # Check the DP and GQ pass the user criteria
                    # Check the alternate allele is only one base (no inserts allowed!)
                    elif (",<NON_REF>" in aline[4]) and (aline[8].startswith("GT:AD:DP:GQ")):
                        missing_call = 0
                        # split aline[9] by ':' into values for 'GT:DP:GQ:'
                        stats = aline[9].split(':')

                        allele = int(stats[0])             # index of GT 
                        AD_values = stats[1].split(',')    # split the stats for the AD values
                        allele_AD = int(AD_values[allele])   # find the AD for the GT - will not use

                        # We use the DP value rather than the individual AD
                        # check if critera is not met for validated alternate sequence
                        if (choice == 'AND'):
                            if (int(stats[2]) < DP_min_val_int) or (int(stats[3]) < GQ_min_val_int):
                                missing_call = 1
                        elif (choice == 'OR'):
                            if ((int(stats[2]) < DP_min_val_int) and (int(stats[3]) < GQ_min_val_int)):
                                missing_call = 1

                        # check if alternate allele is only one base
                        # regardless of DP or GQ values - both an insertion and criteria not met are flagged as 'n'
                        alleles = aline[4].split(',')    # split the alternate alleles by separator ','
                        if len(alleles[allele-1]) != 1:  # if allele length > 1 base, then it isn't valid - set missing_call = 1
                            missing_call = 1

                        # if critera is not met for validated alternate sequence, print sequence as 'missing' or 'n'
                        if missing_call:
                            output_string = f"n\t{aline[1]}\n"
                            outfile.write(output_string)

                        # else print the alternate genotype and its position
                        else:
                            output_string = f"{alleles[allele-1]}\t{aline[1]}\n"   # print the correct alternate, indexed by allele-1
                            outfile.write(output_string)
                
                    # Check to see if this is a bad call
                    # When aline[8] is 'GT:GQ:PL' - there is no read depth
                    elif (aline[8].startswith("GT:GQ:PL")):
                        output_string = f"n\t{aline[1]}\n"
                        outfile.write(output_string)

        except IOError as e:   ## closes try: with open(maple_fileout, 'w') as outfile:
            print(f"An error occurred, writing to output file. {e}")
            sys.exit(1)
            
    else:  # if '.maple' is not in output filename
        print(f"An error occurred, cannot use output file, input filename not .g.vcf.gz or .g.vcf and no .maple in output filename")
        sys.exit(1)
