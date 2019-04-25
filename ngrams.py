"""
Michael Regan
mr3543@columbia.edu

Ngram python script
Takes the News Category Dataset and outputs an XLSX workbook with ngrams for n = {1,2} 

Args:
    json_filename (str): path to News Category Dataset
    xlsx_filename (str): name of xlsx workbook for output

Returns:
    xlsx workbook with ngrams for n = {1,2} in separate worksheets

"""


import sys, json, re, string, xlsxwriter, collections
from nltk.util import ngrams


def get_text(filename):

    """Helper function to read JSON file and aggregate headline and short_description text

    Args:
        filename (str): path to JSON file
    
    Returns:
        text (str): aggregated text from headline and short_description items, all puncuation 
                    removed except for periods

    """

    hl_text = ""
    sd_text = "" 
    with open(filename) as file:
        for line in file:
            json_dict = json.loads(line)
            hl_text += json_dict['headline'] + " "
            sd_text += json_dict['short_description'] + " "

    text = hl_text + ' ' + sd_text 

    #remove puncuation except for periods from aggregated text, convert to lowercase
    punctuation_re = "[" + re.sub("\.","",string.punctuation) + "]"
    text = re.sub(punctuation_re,"",text).lower()
	
    return text

    
def main(json_filename,xlsx_filename):
	
	"""Calls 'get_text' to format JSON file. Generates ngrams for n = {1,2}, and writes
	to Excel file

	Args: 
		json_filename (str): path to JSON file
		xlsx_filename (str): path to xlsx output file 
	
	Returns: None

	"""

	text = get_text(json_filename)
	tokens = text.split()
	
	ngrams_1 = collections.Counter(ngrams(tokens,1))
	ngrams_2 = collections.Counter(ngrams(tokens,2))
	
	#write to xlsx
	workbook = xlsxwriter.Workbook(xlsx_filename)
	worksheet_1 = workbook.add_worksheet()
	worksheet_2 = workbook.add_worksheet()

	row = 0 
	col = 0
	for key,val in ngrams_1.items():
		worksheet_1.write(row,col,key[0])
		worksheet_1.write(row, col +1, val)         
		row += 1
	
	row = 0
	col = 0
	for key,val in ngrams_2.items():
		worksheet_2.write(row,col,key[0] + ", " + key[1])
		worksheet_2.write(row,col +1, val)
		row += 1
	
	workbook.close()


if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])




    
