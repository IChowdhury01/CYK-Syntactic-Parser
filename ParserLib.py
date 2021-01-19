# Library containing functions and utilities for the CYK syntactic parser.

# Opens and reads through the CNF grammar file, parses each production, and stores non-terminal symbols into dictionaries. One dict per production form.
def parse_grammar(grammar_filepath): 
    # Open file from path.   
    with open(grammar_filepath, "r") as f: 
        # Declare dictionaries
        abc_productions = {}     # Symbols from A -> B C productions
        aw_productions = {}     # A -> w productions

        # Loop through each production (line) in grammar file.
        for production in f.readlines():   
            # Split each production into left (A) and right (B C or w) sides
            left_side, right_side = production.split("-->")  
            
            # Remove spaces
            left_side = left_side.strip() 
            right_side = right_side.strip()
           
            # Check how many symbols are on the right side
            if " " not in right_side:                       # 1 symbol (w)
                # Create dict entry for new words
                if right_side not in aw_productions: 
                    aw_productions[right_side] = []  
                
                # Add non-terminal A (key = w, value = A).
                aw_productions[right_side].append(left_side)  
            else:                                           # 2 symbols (B C)
                # Create entry for new non-terminals.
                if left_side not in abc_productions:  
                    abc_productions[left_side] = []   
                
                # Key = A, Value = B and C
                abc_productions[left_side].append(right_side.split(" "))
    
    return aw_productions, abc_productions   


# Given a list of words from an input sentence and a parsed CNF grammar, apply the CYK Parsing algorithm to parse the sentence.
def parse_sentence(word_list, aw_productions, abc_productions):
    num_words = len(word_list)  # Number of words in sentence
    
    # Initialize parse table as upper-triangular matrix.
    parse_table = {}
    for i in range(0, num_words + 1):
        for j in range(0, num_words + 1):
            if j > i:   # Condition for upper-triangular matrix.
                parse_table[i, j] = []

    # CYK/CKY Algorithm implementation. Referenced Figure 13.5 and section 13.2.3 in Speech and Language Processing (3rd ed.)
    for j in range(1, num_words + 1):   # Iterate over columns
        for g in aw_productions[word_list[j - 1]]:  # Iterate over rows
            parse_table[(j - 1, j)].append([g, (j - 1, j)])   # Fill table
        
        for i in range(j - 2, -1, -1):  # Iterate over regions where substring can be split in two.
            for k in range(i + 1, j):
                for ntsA in abc_productions.keys():    # Loop through all nonterminal symbols (A) in dictionary
                    ntsBC = abc_productions[ntsA]        # Loop through nonterminal symbols (B C) in dictionary
                    
                    # Find if symbols B, C are in the parse table. If so, fill table.
                    for symbol in ntsBC:      
                        if symbol[0] in list(map(lambda a: a[0], parse_table[(i, k)])) and \
                            symbol[1] in list(map(lambda b: b[0], parse_table[(k, j)])):  
                                parse_table[(i, j)].append([ntsA, (i, k, symbol[0]), (k, j, symbol[1])])

    # Find starting symbol in table cell (0,N). Loop through table from starting symbol, and return valid parses.        
    start_symbol = 'S'
    if start_symbol in list(map(lambda c: c[0], parse_table[(0, num_words)])):
        return generate_valid_parses(parse_table, word_list, 0, num_words, start_symbol)
    else:
        return None     # If no valid parses, will return nothing.


# Loops through parse table and returns valid parses in bracketed notation array.
def generate_valid_parses(parse_table, input_wordlist, i, j, start):
    valid_parses = []    # Array to be filled with valid parses in bracketed notation    
    
    for entry in parse_table[(i, j)]:
        if entry[0] == start:   # Search for starting symbol. 
            if len(entry) == 2: # If substring was split in two.
                return ["[{} {}]".format(start, input_wordlist[i])] 
            else:
                left = generate_valid_parses(parse_table, input_wordlist, *entry[1])  # Recursively loop through table.
                right = generate_valid_parses(parse_table, input_wordlist, *entry[2])
                
                # Create 2D array from left and right elements. Store indices in list.
                index_list = []
                for i in left:
                    for j in right:
                        index_list.append([i,j])

                # Fill valid parse list.
                for l, r in index_list:
                    valid_parses.append("[{} {} {}]".format(start, l, r))
    
    return valid_parses