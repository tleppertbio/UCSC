#!/usr/bin/env python3
# Program mask_maple.py
# Tami Leppert
# 1/13/2026
# v 3.0
#
# maple file format:
# fin contains three columns
# 1st column is either '-' or 'n' or 'A', 'G', 'C' or 'T'
# second column is position
# third column is number of consecutive positions (only if first column is 'n')
#
# bed file format:
# First three columns
# 1st column chromosome number (we will run by chromosome) - so not checked
# 2nd column start position
# 3rd column end position
#
# Any edits found in the maple files between any of the start to end positions
# are not printed in the output maple file.
# Any n regions found in the maple files overlapping any start or end positions,
# any - deletion regions found in the maple files overlapping any start or end positions
# are adjusted to show only those regions outside of the masking region
#
# program make_maple.py reads two input files
# the first file is a list of maple files
# the second file is a bed file - edited for the chromosome corresponding to the directory of maple files
# and writes a new .maple file with edits to mask removed.
#
# S = start_pos
# E = end_pos
# * = location
# + = represents the length of the extension (for n base or '-' deletion regions only)
#
#while (end_pos < location)                                                                                                               
#    S----------E    if location is after masking region - then read the next masking region                                              
#                    *        
#if (extension != 0)                                                                                  
#  if (start_pos <= location) and (end_pos < location+extension) and (end_pos >= location):             
#    S----------E    'n's or '-'s after masking region are not masked                                      
#             *++++
#  elif (start_pos >= location+extension):
#        S----------E   'n's or '-'s prior to masking region are not masked                                      
# *++++
#  elif (start_pos > location) and (start_pos < location+extension) and (end_pos > location+extension): 
#    S----------E    'n's or '-'s prior to masking region are not masked                                      
# *++++                                                                                               
#  elif (start_pos > location) and (start_pos < location+extension) and (end_pos < location+extension): 
#    S----------E    'n's or '-'s prior to and after masking region are not masked                            
#  *+++++++++++++++
#  else implied default
#    S----------E    Do not print, mask this position                                                  
#        *++++                                                                                        
# if (extension == 0)                                                                                  
#    S----------E    Do not print, mask this position                                                  
#        *                                                                                            
#  if (end_pos < location)                                                                            
#    S----------E    Do not mask this position
#                    *                                                                                   
#  elif (start_pos > location)                                                                          
#    S----------E    Do not mask this position                                                         
#  *
#  else impled default
#    S----------E    Do not print, mask this position                                                  
#        *

import sys
import os
import argparse

def process_arguments_mask():

    #  Checks to see that 3 arguments are entered on the command line
    #
    #  Arguments:
    #      1) maple_file_list (str): file of list of maple files to mask.
    #      2) .bed file (str): .bed file containing masking regions
    #      3) directory to use to store all processed masked .maple files
    #
    #  No return unless 3 valid arguments have been entered.
    #
    parser = argparse.ArgumentParser(description='''A script that takes three command-line arguments.
     Reads:
      a file containing a list of maple files to mask
      a file containing masking regions
      a directory to contain the masked maple files
     Returns:
      a maple format file - processed as follows, maple regions within the masking region are omitted.
        if an 'n' or '-' region spans the masking region, then only those sequences outside of the masking
        region are written to the output maple file.'''
    ,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-l','--list_maple_files',help='The name of the input ile containing the maple files to mask.',required=True)
    parser.add_argument('-m','--mask_file', help='The name of the input .bed file containing the masking regions.',required=True)
    parser.add_argument('-d','--output_directory', help='The name of the output directory containing the masked maple files.',required=True)    
    parser.add_argument('-v','--verbose',action='store_true',help='Enable verbose output')
    args = parser.parse_args()

    global list_maple_files   # The first argument
    global mask_file          # The second argument
    global output_dir         # The third argument
    global list_maple_text    # The text of the list filename
    global mask_file_text     # The text of the mask file
    global output_dir_text    # The text of the output directory
    list_maple_files = ""     # Initialize list filename
    mask_file = ""            # Initialize mask filename
    output_dir = ""           # Initialize output directory

    list_maple_files = args.list_maple_files
    list_maple_text = list_maple_files
    mask_file = args.mask_file
    mask_file_text = mask_file
    output_dir = args.output_directory
    output_dir_text = output_dir
    
#            
#END of def process_arguments_mask():
#

# Check the command line arguments
process_arguments_mask()

# open input files
try:  # open list of maple files
    with open(list_maple_text, 'r') as flistin:  # open list of maple files to read    

        try:  # open bed file with masking regions
            with open(mask_file_text, 'r') as fbedin:     # open bed file which contains masking regions            

                # for each line in current maple file file
                for line in flistin:

                    try:  # open next maple file in list of maple files
                        # debug print("line: " + line.strip())
                        
                        with open(line.strip(), 'r') as fin:  # Open the maple file for reading
                            dirs = line.split('/')            # split line by '/'
                            dir_len = len(dirs)               # get number of '/'s
                            if dir_len >= 1:
                                SRR_file = dirs[dir_len-1]        # get filename (last of '/') if any
                            else:
                                print(f"Error in format of contents of list of maples - {e}")
                                print(f"Can be list of files separated by newline.")
                                print(f"Can be list of files in another directory e.g. ../this.maple")
    
                            try:   # open file for writing masked maples in new directory 
                                with open(output_dir_text + "/" + SRR_file.strip(),'w') as fout:   # open file for writing masked maples in new directory
                                    

                                    # Reset the bed file after every maple file search
                                    fbedin.seek(0)
    
                                    # for each mask region in bed file
                                    for region in fbedin:
        
                                        positions = region.strip().split('\t')  # split the line into columns
                                        if len(positions) >= 2:
                                            start_pos = int(positions[1])+1         # start_position of mask region (zero-based, half-open coordinates)
                                            end_pos = int(positions[2])             # end_position of mask region   (no need to modify the index)
                                        else:
                                            print(f"Error in format of contents of mask file, no tabs? - {e}")
                                        
                                        for aline in fin:  # For each line in the maple file

                                            # if at the header line, write to output masked file and skip to the next line
                                            if '>' in aline:
                                                fout.write(aline)
                                                aline = fin.readline()

                                            columns = aline.strip().split('\t') # split the line into columns, may be two or three columns
                                            if len(columns) >= 2:
                                                location = int(columns[1])          # location is the sequence position of the edit
                                                if_n = columns[0]                   # if_n is type of base '-','n','A','C','G' or 'T'
                                                extension = 0                       # extension is > 0 only if base is 'n' or '-' then 'n' or '-' can span 
                                                if (if_n == 'n') or (if_n == '-'):          # more than one position '-', 'n' spans can span a masking region
                                                    extension = int(columns[2])     # we will check if the location+extension region spans any masking region
                                            else:
                                                print(f"Error in format of contents of maple file, no tabs? - {e}")

                                            # if location in the maple file is > the end_position of the current region, then read next masking region
                                            while (location > end_pos) and region:
                                                region = fbedin.readline()

                                                if region:
                                                    positions = region.strip().split('\t') # split the line into columns
                                                    if len(positions) >= 2:
                                                        start_pos = int(positions[1])+1        # start_position of the mask region (zero-based, half-open coords)
                                                        end_pos = int(positions[2])            # end_position of the mask region   (no need to modify the index)
                                                    else:
                                                        print(f"Error in format of contents of mask file, no tabs? - {e}")
                                                
                                            # debug if location == 3147913:
                                            # debug    i = 10
                
                                            if (extension > 0) and region and aline:
                                                #  if (start_pos <= location) and (end_pos < location+extension) and (end_pos >= location):             
                                                #    S----------E    'n's or '-'s after of masking region are not masked                                      
                                                #             *++++

                                                if (start_pos <= location) and (end_pos < location+extension) and (end_pos >= location):
                                                    to_length = location+extension-end_pos-1
                                                    if to_length > 0:
                                                        fout.write('n\t' + str(end_pos+1) + '\t' + str(to_length) + '\n')                    

                                                #  if (start_pos >= location+extension):
                                                #        S----------E   'n's or '-'s prior to masking region are not masked                                      
                                                # *++++
                                                elif (start_pos >= location+extension):
                                                    fout.write(aline)
                    
                                                #  if (start_pos > location) and (start_pos < location+extension) and (end_pos > location+extension): 
                                                #    S----------E    'n's or '-'s prior to masking region are not masked                                      
                                                # *++++                                                                                               

                                                elif (start_pos > location) and (start_pos < location+extension) and (end_pos > location+extension):
                                                    fout.write('n\t' + str(location) + '\t' + str(start_pos-location) + '\n')                    
                    
                                                #  if (start_pos > location) and (start_pos < location+extension) and (end_pos < location+extension): 
                                                #    S----------E    'n's or '-'s prior to and after masking region are not masked                            
                                                #  *+++++++++++++++

                                                elif (start_pos > location) and (start_pos < location+extension) and (end_pos < location+extension): 
                                                    fout.write('n\t' + str(location) + '\t' + str(start_pos-location) + '\n')
                                                    to_length = location+extension-end_pos-1
                                                    if to_length > 0:
                                                        fout.write('n\t' + str(end_pos+1) + '\t' + str(to_length) + '\n')
                                                    
                                            elif (extension == 0) and region and aline:  # if the extension ==  0
                            
                                                #  if (end_pos < location)                                                                            
                                                #    S----------E    Do not mask this position
                                                #                    *                                                                                   
                                                #  if (start_pos > location)                                                                          
                                                #    S----------E    Do not mask this position                                                         
                                                #  *
                                                if (start_pos > location) or (end_pos < location):
                                                    fout.write(aline)
                                            else:
                                                fout.write(aline)
                    
                                        #end for aline in fin:  # For each line in the maple file                                                    
                                    #end for region in fbedin:  # file containing masked regions
                                #end with open("mask_chrom1/" + SRR_file.strip(),'w') as fout:   # open file for writing masked maples in new directory
                                
                            except FileNotFoundError as e:  # for output masked maple file written in new directory
                                print(f"Error: The file was not found - {e}")
                            except IOError as e:
                                print(f"Error reading the file - {e}")

                        #end with open(line.strip(), 'r') as fin:  # Open the maple file for reading
                        
                    except FileNotFoundError as e:  # for next maple file in list of maple files, fin
                        print(f"Error: The file was not found - {e}")
                    except IOError as e:
                        print(f"Error reading the file - {e}")
                        
                #end for line in flistin:
            #end with open("fasTAN.bed", 'r') as fbedin:     # open bed file which contains masking regions
            
        except FileNotFoundError as e:   # for bed file with masking regions, fbedin
            print(f"Error: The file was not found - {e}")
        except IOError as e:
            print(f"Error reading the file - {e}")
            
    #end with open("chrom_nhin.list", 'r') as flistin:  # open list of maple files to read
    
except FileNotFoundError as e:    # for list of maple files, flistin
    print(f"Error: The file was not found - {e}")
except IOError as e:
    print(f"Error reading the file - {e}")
