from ParserLib import parse_sentence, parse_grammar, generate_valid_parses
import string

# Run this Python script to use the parser.
# python Parse.py
# Parser supports capitalization and punctuation in input sentences.


# Prompt user for CNF grammar file. Parse file contents into dictionaries containing symbols used in each form of production in the grammar.
input_filepath = input("Enter path to CNF grammar file: ")
aw_productions, abc_productions = parse_grammar(input_filepath)  

# Prompt user for input sentence. 
sentence = input("Enter a sentence, or enter 'quit' to terminate: ")  

while True:
    # Process input sentence.
    processed_sentence = sentence.lower().translate(str.maketrans('', '', string.punctuation))  # Remove punctuation & capitalization
    word_list = processed_sentence.split(" ")   # Split string into list of words.

    # Terminate program if user entered "quit".
    if processed_sentence == "quit":    
        print("Terminating program...")
        break

    valid_parses = parse_sentence(word_list, aw_productions, abc_productions)  # Apply CYK Algorithm to input sentence, using parsed CNF grammar

    # Print valid parses in bracketed notation.
    print("")
    if valid_parses is None:  # If CYK parser returned no parses
        print("NO VALID PARSES")
    else:   # Loop through list of valid parses and print each entry.
        counter = 0
        for parse in valid_parses:    
            counter+= 1
            print("Parse {}: {}".format(counter, parse))

    # Prompt user for input sentence again
    sentence = input("\nEnter a sentence, or enter 'quit' to terminate: ") 