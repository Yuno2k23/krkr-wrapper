"""
 Kirikiri Wrapper

    To enable the use of English text word-wrapping in the game engine,
 you need patched versions of some .tjs system files, plus you need to
 preprocess your scripts with this program to add appropriate wrapping
 hints to the text.

 Original Script: Edward Keyes, http://www.insani.org/tools/, 08/07/2006
 Modified Script: Yuno, https://neetprojects.github.io, 10/09/2023
 
 New features:
 - Updated script
 - Better code documentation
 - Better command system:
        Unwrap function
        Encoding option
 - Bug fixed:
        In some tests, the original tool placed the wrap tag
        between 3 and 4 times before the word,
        which takes up unnecessary space and makes the file heavier.
        Now the tool places only 1 tag per word!
"""

import string
import re
import sys
import codecs
import argparse

# Wrapping process
def add_wrap_tags(file1, file2, encoding1, encoding2):
    try:
        with codecs.open(file1, 'r', encoding= f'{encoding1}') as inp_file:
            with codecs.open(file2, 'w', encoding= f'{encoding2}') as out_file:

                # Regular expressions
                separatebybrackets = re.compile(r'[^\[]+|\[[^\]]*\]\s*')
                separateintowords = re.compile(r'[^ \-]+(?:[ \-]+|$)|\s+')
                matchlinecommand = re.compile(r'\[line(\d+)\]')

                line = inp_file.readline()
                scriptsection = False

                # Main Loop
                while line != '':

                    line = line.rstrip() # Remove trailing whitespace from the line
                    
                    # If it's not script, empty line or comment:
                    if (not scriptsection) and (line != '') and (line[0] not in ('@', '*', ';') and (line[-1] not in ('\\'))):

                        pieces = [] # Text pieces list

                        # Loop to find text between brackets and other separate words
                        for match in separatebybrackets.finditer(line):
                            # Split by bracketed commands...
                            if match.group()[0] == '[':
                                pieces.append(match.group())
                            else:
                                # ... and then into words for non-bracketed text
                                for submatch in separateintowords.finditer(match.group()):
                                    pieces.append(submatch.group())

                        newpieces = []  # New Text pieces list

                        # Concatenate [line] commands back into regular text if not spaced
                        addtoprevious = False
                        for piece in pieces :
                            if matchlinecommand.match(piece) :
                                if newpieces[-1][-1] in (' ','-') :
                                    newpieces.append(piece)
                                else :
                                    newpieces[-1] += piece
                                addtoprevious = True
                            else :
                                if addtoprevious and (newpieces[-1][-1] not in (' ','-')) :
                                    newpieces[-1] += piece
                                else :
                                    newpieces.append(piece)
                                addtoprevious = False

                        line = ''

                        # Loop to add the wrap tags to the line
                        for piece in newpieces:

                            # If the text piece doesn't start with square brackets or if starts with line command:
                            if (piece[0] != '[') or matchlinecommand.match(piece):
                                wraptext = piece # Wrap the piece

                                """
                                For some reason, in the Fate scripts, they use [line(number)] to 
                                put a certain number of hyphens in the line, example:

                                [line3]what?
                                ---what?

                                That's pretty stupid, so this code basically
                                replaces that code with straight hyphens.
                                """
                                for match in matchlinecommand.finditer(piece):
                                    wraptext = re.sub(r'\[line' + match.group(1) + r'\]', '--' * int(match.group(1)), wraptext, 1)

                                wraptext = wraptext.rstrip() # Remove trailing whitespace from the line
                                wraptext = wraptext.replace('"', '-')  # Replace quotes with a hyphen to avoid quoted quotes
                                line += '[wrap text="' + wraptext + '"]' + piece # FINALLY Put the wrap tag with the text in front

                            else:
                                line += piece # Just add the text

                    else:
                        if line == '@iscript':
                            scriptsection = True
                        elif line == '@endscript':
                            scriptsection = False

                    # Force Windows linefeeds
                    out_file.write(line + '\r\n') # '\x0D\x0A' <-- basically the same but using hex
                    # Next Line
                    line = inp_file.readline()

        print(f"Wrapping finished! Output file saved as {file2} using {encoding2}.")

    # If you put the wrong encoding to the input file:
    except UnicodeDecodeError:
        print(f'ERROR: [{file1}] IS NOT IN [{encoding1}]!')



# Unwrapping Process
def rem_wrap_tags(file1, file2, encoding1, encoding2):
    try:
        with codecs.open(file1, 'r', encoding= f'{encoding1}') as inp_file:
            with codecs.open(file2, 'w', encoding= f'{encoding2}') as out_file:
                for line in inp_file:

                    # Identify and remove wrap tags
                    line = re.sub(r'\[wrap text="[^"]*"\]', '', line)
                    # Write the resulting lines to the output file
                    out_file.write(line)

        print(f"Unwrapping finished! Output file saved as {file2} using {encoding2}.")

    # If you put the wrong encoding to the input file:
    except UnicodeDecodeError:
        print(f'ERROR: [{file1}] IS NOT IN [{encoding1}]!')



# Main process
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # Functions
    parser.add_argument("action", choices= ["wrap", "unwrap"], help= "Chooses between wrapping and unwrapping")
    # Files
    parser.add_argument("input_file", help= "Path or name of the .ks file")
    parser.add_argument("output_file", help= "Path or name of the resulting .ks file")
    # Encodings
    parser.add_argument('--input-encoding', '--ie', help= 'Input file encoding, SHIFT-JIS by default', default= 'shift-jis')
    parser.add_argument('--output-encoding', '--oe', help= 'Output file encoding, SHIFT-JIS by default', default= 'shift-jis')

    args, unknown_args = parser.parse_known_args()

    # Run wrap function
    if args.action == "wrap":
        add_wrap_tags(args.input_file, args.output_file, args.input_encoding, args.output_encoding)

    # Run unwrap funcion
    elif args.action == "unwrap":
        rem_wrap_tags(args.input_file, args.output_file, args.input_encoding, args.output_encoding)
