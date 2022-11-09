Running on the latest python : 3.10



SOFTWARE FUNCTIONALITIES:
Contains functionality to generate a rainbow table and crack password hashes given a hash function and reduction function. 

Reduction function:
A simple standard reduction function of hash decimal value modula number of passwords is used (H(p)10 % number of passwords).


With a randomly generated rainbow table of 25143 rows and 5 chain length 


	OPTIONS:
		1) Generate a rainbow table using a passwords file defined by user seperated by nextline.Every password used to generate the rainbow table will be tagged with a used word beside the password string.
		2) Crack a MD5 hash using the rainbow table with option to reference the password file defined by user
		3) Refreshes the tagged password file, untagging the used tag to be used again to generate rainbow table again.
		4) Exit the program


REQUIRED DEPENDENCIES
pip3 install -r requirements.txt
Password file can only be in .txt file for now

COMMAND LINE INTERFACE:
make sure your directory pointer is in where the software file is located.
WINDOWS RUN COMMAND : py CSCI262Assignment.py Password.txt
LINUX RUN COMMAND : ./CSCI262Assignment.py Password.txt
PLEASE NOTE- LINUX SYSTEMS ARE CASE SENTITIVE FOR FILENAMES WINDOWS IS OPTIONAL.


You may run without arguments, the program will ask you for your password reference file .



NOTES:

Crack function will return any password not transformed in the rainbow table (In short not tagged used) 

every used password transformed to rainbow table will be tagged used beside the password itself

THERE IS A FUNCTION TO REMOVE THE TAG IF THE PASSWORD IS EVER NEEDED TO BE HASHED AND TRANSFORMED TO RAINBOW TABLE AGAIN.

hashlib MD5: 
https://docs.python.org/3/library/hashlib.html
Binary search:
https://www.geeksforgeeks.org/binary-search/