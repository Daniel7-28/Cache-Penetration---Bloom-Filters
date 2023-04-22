# Cache-Penetration---Bloom-Filters
## Project 2 of Analysis of Algorithm and Design Class (ICOM4038/CIIC4025)
The Goal of project one is to create a Bloom Filter, based on multiple hashes. 
The Bloom Filter will be created dynamically based on dummy inputs (emails) from a 
file that must be evaluated at run time. The input comma-separated files will contain 1 column: Email.
Based on the email key, the program will build the Bloom Filter based on **file 1** inputs. Then it will 
need to check **file 2** entries against the bloom filter and provide its assessment.
The program will output to the command line the original e-mail and the Bloom Filter result.
### Output example:
weseGLCIEPTUusDlU@aol.com,Probably in the DB \
uEUSgDKJN@hotmail.com,Not  in the DB \
PLekUVqtWnRVWShep,Not  in the DB \
BXgWIGaZRv@aol.com,Probably in the DB \
The formulas used in the programs are from this Bloom Filter Calculator: https://hur.st/bloomfilter/