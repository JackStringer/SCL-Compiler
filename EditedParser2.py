
# Jack Stringer
# Kevin Jansen
# CS4308
# Section W01
# Project Deliverable 3

import os
import sys

# filename = input("Enter the name of the file:\n")
source = open('welcome2.scl', 'r')
test = source.read()
output = open('output.txt', 'r+')
output.truncate(0)
output.write(test.upper())
output.close()
output = open('output.txt', 'r')
parseOut = open('parseOut.txt', 'w')
parseOut.truncate(0)

words = 0
characters = 0
lines = 0

# Loop below will gather the contents of the file for lines, word, and chars
for line in test:
    wordslist = line.split()
    lines = lines + 1
    words = words + len(wordslist)
    characters = characters + len(line)

# print(lines, ' Lines')
# print(words, ' Words')
# print(characters, ' Characters')

# BNF based token lists of the specific lexemes for count-checking with later loops
datatype = ['TUNSIGNED', 'CHAR', 'INTEGER', 'MVOID', 'DOUBLE', 'LONG', 'SHORT', 'FLOAT', 'REAL', 'TSTRING', 'TBOOL',
            'TBYTE', 'POINTER']
actions_def = ['READ', 'IMPORT', 'INPUT', 'DISPLAY', 'DISPLAYN', 'MCLOSE', 'IDENTIFIER', 'MOPEN', 'MFILE', 'INCREMENT',
               'DECREMENT', 'RETURN', 'CALL', 'IF', 'ELSE', 'THEN', 'ENDIF', 'FOR', 'EQUOP', 'DO', 'ENDFOR', 'REPEAT',
               'UNTIL', 'ENDREPEAT', 'WHILE', 'DO', 'ENDWHILE', 'CASE', 'MENDCASE', 'MBREAK', 'MEXIT', 'ENDFUN',
               'POTCONDITION']
elementIdentifier = ['STRING', 'LETTER', 'ICON', 'HCON', 'FCON', 'MTRUE', 'MFALSE', 'LP', 'RP']
punaryElement = ['MINUS', 'NEGATE']
termPunary = ['STAR', 'DIVOP', 'MOD', 'LSHIFT', 'RSHIFT']
exprTerm = ['MINUS', 'BAND', 'BOR', 'BXOR']
expressions = ['NOT', 'GREATER', 'EQUAL', 'LESS']
conditions = ['OR', 'AND', '==']
relationalOperators = ['<', '>', '>=', '<=', '!=']
keywords = ['POINTER', 'BEGIN', ',', '//', 'MTRUE', 'MFALSE', '.', '[', 'IMPLEMENTATIONS', 'FUNCTION', 'MAIN', 'IS',
            'VARIABLES']
identifiers = ['DEFINE', 'SET', 'SYMBOL', 'OF', 'TYPE']
assignmentOperator = ['=', '+', '-', '/', '*', 'sqrt']
parserList = []
pCol = []
pLine = []

# Resetting our currently read lexeme
lexeme = ''
id = 0 #counter for identifier based progression and reading
identName = []
identType = []
identValue = []
stringList = []
parseArray = []
opFound = 0
z = 1
operator = ''
isNot = 0
yes = 0
stid = 0 #counter for string literal locations


# Main function for scanning file character by character until either lexemes are matched, or errors are produced
# k = character iterator through list
def scan(lexeme, linelength, file, linenum):
    k = 0
    colNum = 1
    while k != linelength:
        # lexeme currently blank; as loop continues, we add each next character and try to match again
        lexeme += (file[k])
        # Datatype is first list checked for keywords
        if datatype.count(lexeme) != 0:  # if count is higher than 0, keyword matched within database
           # print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
            parserList.append(lexeme)
            pCol.append(colNum)
            pLine.append(linenum)
            lexeme = ''  # erase last lexeme for new comparison
            k += 1
            colNum += 1
        # 2nd token list most complicated as we check for unique cases, strings, etc in this loop
        elif actions_def.count(lexeme) != 0:
            if lexeme == 'DO' and file[k + 1] == 'U':  # Ensures double is not ignored for DO (look ahead)
               # print('keyword ', 'symbol:', 'DOUBLE', 'on line ', linenum, ' in column ', colNum+4)
                k += 5
                colNum += 4
                parserList.append('DOUBLE')
                pCol.append(colNum)
                pLine.append(linenum) 
                lexeme = ''
            elif lexeme == 'IF':  # 2nd token list, IF lexeme checked once as unique case
                # print current lexeme since it will already = IF
               # print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                parserList.append(lexeme)
                pCol.append(colNum)
                pLine.append(linenum)
                lexeme = ''  # reset lexeme
                k += 1
                colNum += 1
                while file[k] == ' ':  # checks if space is after IF for continued sentence
                    k += 1
                    colNum += 1
                while file[k] != ' ' and file[k + 1] != '\n':  # case where if doesnt have space and line isnt at end
                    lexeme += file[k]
                    k += 1
                    colNum += 1
                # unique lexeme cases for expression token
                if lexeme == 'NOT' or lexeme == 'GREATER' or lexeme == 'EQUAL' or lexeme == 'LESS':
                    tempCN = colNum - 1  # temporary col to fix incorrect increment for 2nd while case within this loop
                    # -1 column value since we already used to look ahead and need to print correct
                  #  print('expression ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', tempCN)
                    parserList.append(lexeme)
                    pCol.append(colNum-1)
                    pLine.append(linenum)
                    lexeme = ''
                    k += 1
                    colNum += 1
                    while file[k] == ' ':  # increments k location indefinitely for spaces until letter hit
                        k += 1
                        colNum += 1
                    while file[k] != ' ' and file[k + 1] != '\n':  # case where k is on a char, and not at end of line
                        lexeme += file[k]
                        k += 1
                        colNum += 1
                    # -1 column value again, same as tempCN due to look ahead previously
                    # case of identifiers; looked at multiple times in code based on which keywords accept identifiers
                  #  print('identifier ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum - 1)
                    parserList.append(lexeme)
                    pCol.append(colNum-1)
                    pLine.append(linenum)
                    lexeme = ''
                    # else case for identifiers that follow different syntax model than above
                else:
                    tempCN = colNum - 1
                  #  print('identifier ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', tempCN)
                    parserList.append(lexeme)
                    pCol.append(colNum-1)
                    pLine.append(linenum)
                    lexeme = ''
            # still within action_def 2nd token list from above, logically separated further and printed
            elif lexeme == 'DISPLAY' or lexeme == 'INPUT' or lexeme == 'SET' or lexeme == 'IMPORT':
              #  print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                parserList.append(lexeme)
                pCol.append(colNum-1)
                pLine.append(linenum)
                lexeme = ''
                k += 1
                colNum += 1
                while file[k] == ' ':
                    k += 1
                    colNum += 1
                lexeme += file[k]
                # Looking at first case of "
                if lexeme == '"':
                    k += 1
                    colNum += 1
                    # increment k position indefinitely until another quote is found. Error if never ending.
                    while file[k] != '"':
                        # Stores location of first quote in case a 2nd quote is never found
                        quoteRow = file[k]
                        quoteCol = colNum
                        lexeme += file[k]
                        k += 1
                        colNum += 1
                        # If not 2nd quotation mark by end of file, error with location of first quotation
                        if file[k] == characters and file[k] != '"':
                            print("Never ending quotation at line " + quoteRow + " and column " + quoteCol)
                            k = linelength
                    lexeme += file[k]
                    #  as long as 2nd quote is found, creates a single string of all contents to print
                  #  print('string literal', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                    parserList.append(lexeme)
                    stringList.append(lexeme)
                    pCol.append(colNum-1)
                    pLine.append(linenum)
                    lexeme = ''
                    k += 1
                    colNum += 1
                else:
                    # display, input, set, & import may all lead to identifiers and not being within a string literal
                    while file[k] != ' ' and file[k + 1] != '\n':
                        k += 1
                        colNum += 1
                        lexeme += file[k]
                    tempCN = colNum - 1  # decrement and use temp due to previous look ahead determination
                   # print('identifier ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', tempCN)
                    parserList.append(lexeme)
                    pCol.append(colNum-1)
                    pLine.append(linenum)
                    lexeme = ''
                    k += 1
                    colNum += 1
            elif lexeme == 'RETURN':
               # print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                parserList.append(lexeme)
                pCol.append(colNum)
                pLine.append(linenum)
                lexeme = ''
                k += 1
                colNum += 1
                while file[k] == ' ':  # skips ahead indefinitely for spaces
                    k += 1
                    colNum += 1
                lexeme += file[k]
                while file[k] != ' ' and file[k + 1] != '\n':  # not end of line and has now landed on a character
                    k += 1
                    colNum += 1
                tempCN = colNum - 1  # decrement and use temp due to previous look ahead.
                # Integer constant case when after a non-string-literal Return
               # print('integer constant ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', tempCN)
                parserList.append(lexeme)
                pCol.append(colNum-1)
                pLine.append(linenum)
                lexeme = ''
            else:
                # case where return leads to expanded expression due to keyword before constant/identifier
              #  print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                parserList.append(lexeme)
                pCol.append(colNum-1)
                pLine.append(linenum)
                lexeme = ''
                k += 1
                colNum += 1
        # using more specific lists due to BNF to evaluate as same keyword token grouping
        elif elementIdentifier.count(lexeme) != 0:
           # print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
            parserList.append(lexeme)
            pCol.append(colNum)
            pLine.append(linenum)
            lexeme = ''
            k += 1
            colNum += 1
        # using more specific lists due to BNF to evaluate as same keyword token grouping
        elif punaryElement.count(lexeme) != 0:
          #  print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
            parserList.append(lexeme)
            pCol.append(colNum)
            pLine.append(linenum)
            lexeme = ''
            k += 1
            colNum += 1
        # using more specific lists due to BNF to evaluate as same keyword token grouping
        elif termPunary.count(lexeme) != 0:
           # print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
            parserList.append(lexeme)
            pCol.append(colNum)
            pLine.append(linenum)
            lexeme = ''
            k += 1
            colNum += 1
        # using more specific lists due to BNF to evaluate as same keyword token grouping
        elif exprTerm.count(lexeme) != 0:
           # print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
            parserList.append(lexeme)
            pCol.append(colNum)
            pLine.append(linenum)
            lexeme = ''
            k += 1
            colNum += 1
        # using more specific lists due to BNF to evaluate as expression.
        # 2nd expression lexeme check without keywords can thus find user-variables or identifiers
        elif expressions.count(lexeme) != 0:
          #  print('expression ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
            parserList.append(lexeme)
            pCol.append(colNum)
            pLine.append(linenum)
            lexeme = ''
            k += 1
            colNum += 1
            while file[k] == ' ':
                k += 1
                colNum += 1
                # once character found after whitespace that is not a newline
            while file[k] != ' ' and file[k + 1] != '\n':
                lexeme += file[k]
                k += 1
                colNum += 1
                # identifier found if expression without keyword/arithmetic operator next
                # must decrement col for print to fix from looking ahead to determine end of lexeme
            parserList.append(lexeme)
            if conditions.count(lexeme) == 0:
            #    print('identifier ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                lexeme = ''
            else:
             #   print('conditional ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                lexeme = ''
        # using more specific lists due to BNF to evaluate as same keyword token grouping
        elif conditions.count(lexeme) != 0:
          #  print('conditional ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
            parserList.append(lexeme)
            pCol.append(colNum)
            pLine.append(linenum)
            lexeme = ''
            k += 1
            colNum += 1
        elif relationalOperators.count(lexeme) != 0:
            # these have a larger k and colNum increment to match the operators being 2 character size
            if lexeme == '<' and file[k + 1] == '=':
                lexeme = '<='
                k += 2
                colNum += 2
                # decrement colNum to print due to looking ahead at white space
             #   print('relational operator ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum - 1)
                parserList.append(lexeme)
                pCol.append(colNum-1)
                pLine.append(linenum)
                lexeme = ''
            elif lexeme == '>' and file[k + 1] == '=':
                lexeme = '>='
                k += 2
                colNum += 2
                # decrement colNum to print due to looking ahead at white space
              #  print('relational operator ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum - 1)
                parserList.append(lexeme)
                pCol.append(colNum-1)
                pLine.append(linenum)
                lexeme = ''
            elif lexeme == '!' and file[k + 1] == '=':
                lexeme = '!='
                k += 2
                colNum += 2
                # decrement colNum to print due to looking ahead at white space
             #   print('relational operator ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum - 1)
                parserList.append(lexeme)
                pCol.append(colNum-1)
                pLine.append(linenum)
                lexeme = ''
            elif lexeme == '>' and file[k + 1] == ' ':
                lexeme = '>'
                k += 2
                colNum += 2
                # decrement colNum to print due to looking ahead at white space
             #   print('relational operator ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum - 1)
                parserList.append(lexeme)
                pCol.append(colNum-1)
                pLine.append(linenum)
                lexeme = ''
            elif lexeme == '<' and file[k + 1] == ' ':
                lexeme = '<'
                k += 2
                colNum += 2
                # decrement colNum to print due to looking ahead at white space
              #  print('relational operator ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum - 1)
                parserList.append(lexeme)
                pCol.append(colNum-1)
                pLine.append(linenum)
                lexeme = ''
            else:
                k += 1
                colNum += 1
                # relational operators have multiple possible LS and RS lexemes; keyword possibility
              #  print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                parserList.append(lexeme)
                pCol.append(colNum)
                pLine.append(linenum)
                lexeme = ''
            while file[k] == ' ':
                k += 1
                colNum += 1
            # once a character is reached after space incrementing, it must be an identifier here after the operator
            while file[k] != ' ' and file[k + 1] != '\n':
                lexeme += file[k]
                k += 1
                colNum += 1
          #  print('identifier ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum - 1)
            parserList.append(lexeme)
            pCol.append(colNum)
            pLine.append(linenum)
            lexeme = ''
        elif keywords.count(lexeme) != 0:
            # comment line established as keyword
            # we garbage dispose of any comment code and continue on
            if lexeme == '//':
              #  print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                k = linelength
            # comma preludes an expression where the next term is an identifier from the user or keyword
            elif lexeme == ',':
              #  print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                parserList.append(lexeme)
                pCol.append(colNum)
                pLine.append(linenum)
                lexeme = ''
                k += 1
                colNum += 1
                while file[k] == ' ':
                    k += 1
                    colNum += 1
                lexeme += file[k]
                # once character is found after whitespace and it is not newline
                while file[k] != ' ' and file[k + 1] != '\n':
                    k += 1
                    colNum += 1
                    lexeme += file[k]
              #  print('identifier ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                parserList.append(lexeme)
                pCol.append(colNum)
                pLine.append(linenum)
                lexeme = ''
                k += 1
                colNum += 1
            # if no comma expression, then next character part of keyword "lexeme" matched
            else:
              #  print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                parserList.append(lexeme)
                pCol.append(colNum)
                pLine.append(linenum)
                lexeme = ''
                k += 1
                colNum += 1

        elif identifiers.count(lexeme) != 0:
         #   print('keyword ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
            parserList.append(lexeme)
            pCol.append(colNum)
            pLine.append(linenum)
            lexeme = ''
            # searches +2 to check past key identifier words and land right on first character of variable
            k += 1
            colNum += 1
            while file[k] == ' ':
                k += 1
                colNum += 1
            while file[k] != " ":
                lexeme += file[k]
                k += 1
                colNum += 1                # remove 1 from colNum due to white space look ahead
            if lexeme == 'TYPE':
             #   print('identifier', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                parserList.append(lexeme)
                pCol.append(colNum)
                pLine.append(linenum)
                lexeme = ''
                k += 1
                colNum += 1
            else:
              #  print('variable', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                parserList.append(lexeme)
                pCol.append(colNum)
                pLine.append(linenum)
            lexeme = ''

        elif assignmentOperator.count(lexeme) != 0:
            # protects from unique case where there is only a single escape char, and not a comment
            if lexeme == '/' and file[k + 1] == '/':
                k += 1
                colNum += 1
            else:
             #   print('assignment operator ', 'symbol:', lexeme, 'on line ', linenum, ' in column ', colNum)
                parserList.append(lexeme)
                pCol.append(colNum)
                pLine.append(linenum)
                lexeme = ''
                # uses +2 to search past operator to first character. +1 later if still blank space
                k += 2
                colNum += 2

                while file[k] != " ":
                    lexeme += file[k]
                    k += 1
                    colNum += 1
                # associates k character with real constant as long as it is not white space or end of file
              #  print('real constant', 'symbol', lexeme, 'on line ', linenum, ' in column ', colNum)
                parserList.append(lexeme)
                pCol.append(colNum)
                pLine.append(linenum)
                lexeme = ''

        # pushes past whitespace that is between tokens and literal strings
        elif lexeme == " ":
            lexeme = ''
            k += 1
            colNum += 1

        elif lexeme != '\n' and k == linelength - 1:
            parserList.append(lexeme)
            # error if unknown character or something doesn't match with scanner
            if (datatype.count(lexeme) == 0 and actions_def.count(lexeme) == 0 and identifiers.count(lexeme) == 0
                    and keywords.count(lexeme) == 0 and elementIdentifier.count(lexeme) == 0 and expressions.count(
                        lexeme) == 0
                    and assignmentOperator.count(lexeme) == 0 and relationalOperators.count(
                        lexeme) == 0 and punaryElement.count(lexeme) == 0
                    and conditions.count(lexeme) == 0 and exprTerm.count(lexeme) == 0 and termPunary.count(
                        lexeme) == 0):
             #   print("Lexical Error: Unrecognized character at line : ", linenum, " and column : ", colNum)
                k = linelength
        else:
            k += 1
            colNum += 1


switch = 0
linenum = 1

while switch != 1:
    # splitting a file into lines, and removing tabs with an equivalent spacing to fit formulas above
    file = output.readline()
    newline = ''
    # will maintain the same column spacing as a tabbed file has, despite removing them
    currentline = file
    currentline = currentline.replace('\t', '            ')
    linelength = len(currentline)

    # if end of file, switch to out of loop. Blank lines within file are still seen with \t or \n
    if linelength == 0:
        switch = 1
    # if not end of file, repeatedly call function to scan for keywords, literals, etc defined above
    else:
        scan(lexeme, linelength, currentline, linenum)
    linenum += 1


p = 0 #counters initialized, needed for parse
c = 1
t = 1
lenCheck = ''
counter = 0
tempList= []
ifbool = 'no' #remembers if there is a current if statement
#print(parserList)

while p < parserList.__len__():  #parse will run while counter p is within the length of the token list
    currentToken = parserList[p] #current token
    nextToken = parserList[p+1]  #next token

    if parserList[p] == 'IMPORT':
        if nextToken[0] == '': # If the next token does not have quotations, prints syntax error
            print("Syntax Error at ", currentToken, " on Line Number: ", pLine[p], " and Column Number:", pCol[p],". Expected Filename")
            sys.exit()
        else:
          #  print("Keyword Statement: ", c, ':', "IMPORT", nextToken) #prints command number, and command, this will happen with all commands.
          #  print('\tImporting: ', nextToken)
            parseOut.write("Keyword Statement: ")
            parseOut.write(str(c))
            parseOut.write(':')
            parseOut.write('IMPORT')
            parseOut.write(nextToken)
            parseOut.write('\tImporting: ')
            parseOut.write(nextToken)
            p += 2
            c += 1

    if parserList[p] == 'IMPLEMENTATIONS':
        #print("Keyword Statement: ", c, ':', "IMPLENTATIONS")
        parseOut.write("\nKeyword Statement: ")
        parseOut.write(str(c))
        parseOut.write(':')
        parseOut.write('IMPLEMENTATIONS')
        p += 1
        c += 1

    if parserList[p] == 'FUNCTION':
        if parserList[p+1] == 'MAIN': #determine which function the user is creating, and stores it as a function name for error handling.
            fname = 'MAIN'
            if parserList[p+2] == 'IS':
               # print("Main Statement: ", c, ':', "FUNCTION MAIN IS")
                parseOut.write("\nMain Statement: ")
                parseOut.write(str(c))
                parseOut.write(':')
                parseOut.write('FUNCTION MAIN IS')
                p += 3 #plus 3 to get past function main is
                c += 1
            else:
                print("Syntax Error at line:", pLine[p] ," Column:",pCol[p] , "Expected keyword IS")
                sys.exit()
        else:
          #  print("Function Statement: ", c, "FUNCTION")
            parseOut.write("\nFunction Statement: ")
            parseOut.write(str(c))
            parseOut.write(':')
            parseOut.write('FUNCTION')
            p += 1 #this is if it only is called function
            c += 1
            fname = parserList[p+1]

    if parserList[p] == 'VARIABLES':
      #  print("Keyword Statement: ", c, ':', "VARIABLES")
        parseOut.write("\nKeyword Statement: ")
        parseOut.write(str(c))
        parseOut.write(':')
        parseOut.write('VARIABLES')
        p += 1
        c += 1

    if parserList[p] == 'DEFINE': #checks to see if it is a proper declaration first or prints to syntax error
        identValue.append(0)
        if parserList[p+2] != 'OF' and parserList[p+2] != 'POINTER':
            print("Syntax Error at line:", pLine[p] ," Column:",pCol[p] , "Improper Variable Declaration")
            sys.exit()
        if parserList[p+2] == 'OF':
            if parserList[p+4].lower() == 'double' or parserList[p+4].lower() == 'float' or parserList[p+4].lower() == \
                    'string' or parserList[p + 4].lower() == 'char' or parserList[p+4].lower() == 'int' or \
                    parserList[p+4].lower() == 'true' or parserList[p+4].lower() == 'false':
                identName.append(parserList[p + 1])
                identType.append(parserList[p + 4])
                identity = identName.index(parserList[p + 1])
              #  print('Declaration Statement: ', c, ':', 'DEFINE', parserList[p+1], parserList[p+2], parserList[p+3], parserList[p+4])
              #  print('\tIdentifier(', parserList[p + 1], ') of type ', identType[identity])
                parseOut.write("\nDeclaration Statement: ")
                parseOut.write(str(c))
                parseOut.write(':')
                parseOut.write('DEFINE ')
                parseOut.write(parserList[p+1])
                parseOut.write(' ')
                parseOut.write(parserList[p+2])
                parseOut.write(' ')
                parseOut.write(parserList[p+3])
                parseOut.write(' ')
                parseOut.write(parserList[p+4])
                parseOut.write('\tIdentifier(')
                parseOut.write(parserList[p + 1])
                parseOut.write(') of type ')
                parseOut.write(identType[identity])
                p += 5
                c += 1
            else:
                print("Lexical Error at line:", pLine[p], " Column:", pCol[p], "System does not support declaration: ",
                      parserList[p+4])
                sys.exit()
        elif parserList[p+2] == 'POINTER':
            if parserList[p+5].lower() == 'double' or parserList[p+5].lower() == 'float' or parserList[p + 5].lower() \
                    == 'string' or parserList[p + 5].lower() == 'char' or parserList[p + 5].lower() == 'int' \
                    or parserList[p + 5].lower() == 'true' or parserList[p + 5].lower() == 'false':
                identName.append(parserList[p + 1])
                identType.append(parserList[p + 5])
                identity = identName.index(parserList[p + 1])
              #  print('Declaration Statement: ', c, ':', 'DEFINE', parserList[p+1], parserList[p+2], parserList[p+3], parserList[p+4], parserList[p+5])
              #  print('\tIdentifier(', parserList[p + 1], ') of type ', identType[identity])
                parseOut.write("\nDeclaration Statement: ")
                parseOut.write(str(c))
                parseOut.write(':')
                parseOut.write('DEFINE ')
                parseOut.write(parserList[p+1])
                parseOut.write(' ')
                parseOut.write(parserList[p+2])
                parseOut.write(' ')
                parseOut.write(parserList[p+3])
                parseOut.write(' ')
                parseOut.write(parserList[p+4])
                parseOut.write(' ')
                parseOut.write(parserList[p+5])
                parseOut.write('\tIdentifier(')
                parseOut.write(parserList[p + 1])
                parseOut.write(') of type ')
                parseOut.write(identType[identity])
                p += 6
                c += 1
            else:
                print("Lexical Error at line:", pLine[p], " Column:", pCol[p], "System does not support declaration: ",
                      parserList[p+5])
                sys.exit()
        else:
            print("Syntax Error at line:", pLine[p], " Column:", pCol[p], "Improper Variable Declaration")
            sys.exit()

    if parserList[p] == 'BEGIN':
       # print('Start Statement: ', c, ':', 'BEGIN')
        parseOut.write("\nKeyword Statement: ")
        parseOut.write(str(c))
        parseOut.write(':')
        parseOut.write('BEGIN')
        p += 1
        c += 1



    if parserList[p] == 'DISPLAY':  # handles longer display commands by checking for commas
        if parserList[p-1] == 'THEN':
            if yes == 1:         
                if stringList.count(parserList[p+1]) != 0:  # checks for string literals as next
                    if parserList[p+2] == ',':
                        identity = identName.index(parserList[p + 3])
                       # print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1],parserList[p+2],parserList[p+3])
                       # print('\tString Literal: ', parserList[p + 1])
                       # print('\tIdentifier(', parserList[p + 3], ') of type ', identType[identity])
                        print(parserList[p+1],identValue[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+2])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+3])
                        parseOut.write('\tString Literal:')
                        parseOut.write(parserList[p + 1])
                        parseOut.write('\tIdentifier(')
                        parseOut.write(parserList[p + 3])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity]) 
                        parseOut.write(parserList[p+1])
                        parseOut.write(identValue[identity])
                        p += 4
                        c += 1
                    else:
                       # print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1])
                       # print('\tString Literal: ', parserList[p + 1])
                        print(parserList[p+1])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write('\tString Literal:')
                        parseOut.write(parserList[p + 1])
                        p += 2
                        c += 1
                elif identName.count(parserList[p+1]) != 0:
                    if parserList[p+2] == ',':
                        identity = identName.index(parserList[p + 1])
                      #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1],parserList[p+2],parserList[p+3])
                      #  print('\tIdentifier(', parserList[p + 1], ') of type ', identType[identity])
                        identity = identName.index(parserList[p + 3])
                      #  print('\tIdentifier(', parserList[p + 3], ') of type ', identType[identity])
                        print(identValue[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+2])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+3])
                        parseOut.write('\tIdentifier(:')
                        parseOut.write(parserList[p + 1])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity])
                        parseOut.write('\tIdentifier(:')
                        parseOut.write(parserList[p + 3])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity]) 
                        parseOut.write(' ')
                        parseOut.write(identValue[identity])
                        p += 4
                        c += 1
                    else:
                        identity = identName.index(parserList[p + 1])
                      #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1])
                      #  print('\tIdentifier(', parserList[p+1], ') of type ', identType[identity])
                        print(identValue[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write('\tIdentifier(:')
                        parseOut.write(parserList[p + 1])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity])
                        parseOut.write(' ')
                        parseOut.write(identValue[identity])
                        p += 2
                        c += 1
                else:
                    print('Syntax Error at Line:', pLine[p+1],' Column: ', pCol[p+1], 'Variable', parserList[p+1], 'is not defined')
                    sys.exit()
            if yes == 0:  
                if stringList.count(parserList[p+1]) != 0:  # checks for string literals as next
                    if parserList[p+2] == ',':
                        identity = identName.index(parserList[p + 3])
                      #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1],parserList[p+2],parserList[p+3])
                      #  print('\tString Literal: ', parserList[p + 1])
                      #  print('\tIdentifier(', parserList[p + 3], ') of type ', identType[identity])
                      #  print(parserList[p+1],identValue[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+2])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+3])
                        parseOut.write('\tString Literal:')
                        parseOut.write(parserList[p + 1])
                        parseOut.write('\tIdentifier(')
                        parseOut.write(parserList[p + 3])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity]) 
                        parseOut.write(parserList[p+1])
                        parseOut.write(identValue[identity])
                        p += 4
                        c += 1
                    else:
                      #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1])
                      #  print('\tString Literal: ', parserList[p + 1])
                      #  print(parserList[p+1])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write('\tIDENTIFIER:')
                        parseOut.write(parserList[p + 1])
                        p += 2
                        c += 1
                elif identName.count(parserList[p+1]) != 0:
                    if parserList[p+2] == ',':
                        identity = identName.index(parserList[p + 1])
                      #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1],parserList[p+2],parserList[p+3])
                      #  print('\tIdentifier(', parserList[p + 1], ') of type ', identType[identity])
                        identity = identName.index(parserList[p + 3])
                      #  print('\tIdentifier(', parserList[p + 3], ') of type ', identType[identity])
                      #  print(identValue[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+2])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+3])
                        parseOut.write('\tIdentifier(:')
                        parseOut.write(parserList[p + 1])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity])
                        parseOut.write('\tIdentifier(:')
                        parseOut.write(parserList[p + 3])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity]) 
                        parseOut.write(' ')
                        parseOut.write(identValue[identity])
                        p += 4
                        c += 1
                    else:
                        identity = identName.index(parserList[p + 1])
                       # print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1])
                       # print('\tIdentifier(', parserList[p+1], ') of type ', identType[identity])
                      #  print(identValue[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write('\tString Literal:')
                        parseOut.write(parserList[p + 1])                      
                        p += 2
                        c += 1 
        elif parserList[p-1] == 'ELSE':
            if yes == 1:
                if stringList.count(parserList[p+1]) != 0:  # checks for string literals as next
                    if parserList[p+2] == ',':
                        identity = identName.index(parserList[p + 3])
                       # print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1],parserList[p+2],parserList[p+3])
                       # print('\tString Literal: ', parserList[p + 1])
                       # print('\tIdentifier(', parserList[p + 3], ') of type ', identType[identity])
                       # print(parserList[p+1],identValue[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+2])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+3])
                        parseOut.write('\tString Literal:')
                        parseOut.write(parserList[p + 1])
                        parseOut.write('\tIdentifier(')
                        parseOut.write(parserList[p + 3])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity]) 
                        parseOut.write(parserList[p+1])
                        parseOut.write(identValue[identity])
                        p += 4
                        c += 1
                    else:
                       # print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1])
                       # print('\tString Literal: ', parserList[p + 1])
                       # print(parserList[p+1])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write('\tString Literal:')
                        parseOut.write(parserList[p + 1])
                        p += 2
                        c += 1
                elif identName.count(parserList[p+1]) != 0:
                    if parserList[p+2] == ',':
                        identity = identName.index(parserList[p + 1])
                      #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1],parserList[p+2],parserList[p+3])
                       # print('\tIdentifier(', parserList[p + 1], ') of type ', identType[identity])
                        identity = identName.index(parserList[p + 3])
                       # print('\tIdentifier(', parserList[p + 3], ') of type ', identType[identity])
                       # print(identValue[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+2])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+3])
                        parseOut.write('\tIdentifier(:')
                        parseOut.write(parserList[p + 1])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity])
                        parseOut.write('\tIdentifier(:')
                        parseOut.write(parserList[p + 3])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity]) 
                        parseOut.write(' ')
                        parseOut.write(identValue[identity])
                        p += 4
                        c += 1
                    else:
                        identity = identName.index(parserList[p + 1])
                      #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1])
                      #  print('\tIdentifier(', parserList[p+1], ') of type ', identType[identity])
                      #  print(identValue[identity])
                      #  print(identValue[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write('\tIdentifier(:')
                        parseOut.write(parserList[p + 1])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity])
                        parseOut.write(' ')
                        parseOut.write(identValue[identity])
                        p += 2
                        c += 1
            if yes == 0:  
                if stringList.count(parserList[p+1]) != 0:  # checks for string literals as next
                    if parserList[p+2] == ',':
                        identity = identName.index(parserList[p + 3])
                      #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1],parserList[p+2],parserList[p+3])
                      #  print('\tString Literal: ', parserList[p + 1])
                      #  print('\tIdentifier(', parserList[p + 3], ') of type ', identType[identity])
                        print(parserList[p+1],identValue[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+2])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+3])
                        parseOut.write('\tString Literal:')
                        parseOut.write(parserList[p + 1])
                        parseOut.write('\tIdentifier(')
                        parseOut.write(parserList[p + 3])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity]) 
                        parseOut.write(parserList[p+1])
                        parseOut.write(identValue[identity])

                        p += 4
                        c += 1
                    else:
                       # print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1])
                       # print('\tString Literal: ', parserList[p + 1])
                        print(parserList[p+1])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write('\tString Literal:')
                        parseOut.write(parserList[p + 1])
                        p += 2
                        c += 1
                elif identName.count(parserList[p+1]) != 0:
                    if parserList[p+2] == ',':
                        identity = identName.index(parserList[p + 1])
                      #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1],parserList[p+2],parserList[p+3])
                      #  print('\tIdentifier(', parserList[p + 1], ') of type ', identType[identity])
                        identity = identName.index(parserList[p + 3])
                      #  print('\tIdentifier(', parserList[p + 3], ') of type ', identType[identity])
                        print(identValue[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+2])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+3])
                        parseOut.write('\tIdentifier(:')
                        parseOut.write(parserList[p + 1])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity])
                        parseOut.write('\tIdentifier(:')
                        parseOut.write(parserList[p + 3])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity]) 
                        parseOut.write(' ')
                        parseOut.write(identValue[identity])
                        p += 4
                        c += 1
                    else:
                        identity = identName.index(parserList[p + 1])
                      #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1])
                      #  print('\tIdentifier(', parserList[p+1], ') of type ', identType[identity])
                        print(identValue[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('DISPLAY ')
                        parseOut.write(parserList[p+1])
                        parseOut.write('\tString Literal:')
                        parseOut.write(parserList[p + 1])
                        parseOut.write(identValue[identity])
                        p += 2
                        c += 1
        else:     
            if stringList.count(parserList[p+1]) != 0:  # checks for string literals as next
                if parserList[p+2] == ',':
                    identity = identName.index(parserList[p + 3])
                  #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1],parserList[p+2],parserList[p+3])
                  #  print('\tString Literal: ', parserList[p + 1])
                  #  print('\tIdentifier(', parserList[p + 3], ') of type ', identType[identity])
                    print(parserList[p+1],identValue[identity])
                    parseOut.write("\nKeyword Statement: ")
                    parseOut.write(str(c))
                    parseOut.write(':')
                    parseOut.write('DISPLAY ')
                    parseOut.write(parserList[p+1])
                    parseOut.write(' ')
                    parseOut.write(parserList[p+2])
                    parseOut.write(' ')
                    parseOut.write(parserList[p+3])
                    parseOut.write('\tString Literal:')
                    parseOut.write(parserList[p + 1])
                    parseOut.write('\tIdentifier(')
                    parseOut.write(parserList[p + 3])
                    parseOut.write(') of type ')
                    parseOut.write(identType[identity]) 
                  # parseOut.write(parserList[p+1])
                  #  parseOut.write(str(identValue[identity]))
                    p += 4
                    c += 1
                else:
                  #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1])
                  #  print('\tString Literal: ', parserList[p + 1])
                    print(parserList[p+1])
                    parseOut.write("\nKeyword Statement: ")
                    parseOut.write(str(c))
                    parseOut.write(':')
                    parseOut.write('DISPLAY ')
                    parseOut.write(parserList[p+1])
                    parseOut.write('\tString Literal:')
                    parseOut.write(parserList[p + 1])
                    parseOut.write(str(identValue[identity]))
                    p += 2
                    c += 1
            elif identName.count(parserList[p+1]) != 0:
                if parserList[p+2] == ',':
                    identity = identName.index(parserList[p + 1])
                  #  print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1],parserList[p+2],parserList[p+3])
                  #  print('\tIdentifier(', parserList[p + 1], ') of type ', identType[identity])
                    identity = identName.index(parserList[p + 3])
                  #  print('\tIdentifier(', parserList[p + 3], ') of type ', identType[identity])
                    print(identValue[identity])
                    parseOut.write("\nKeyword Statement: ")
                    parseOut.write(str(c))
                    parseOut.write(':')
                    parseOut.write('DISPLAY ')
                    parseOut.write(parserList[p+1])
                    parseOut.write(' ')
                    parseOut.write(parserList[p+2])
                    parseOut.write(' ')
                    parseOut.write(parserList[p+3])
                    parseOut.write('\tIdentifier(:')
                    parseOut.write(parserList[p + 1])
                    parseOut.write(') of type ')
                    parseOut.write(identType[identity])
                    parseOut.write('\tIdentifier(:')
                    parseOut.write(parserList[p + 3])
                    parseOut.write(') of type ')
                    parseOut.write(identType[identity]) 
                    parseOut.write(' ')
                    parseOut.write(identValue[identity])
                    p += 4
                    c += 1
                else:
                    identity = identName.index(parserList[p + 1])
                   # print('Keyword Statement: ', c, ':', 'DISPLAY', parserList[p+1])
                   # print('\tIdentifier(', parserList[p+1], ') of type ', identType[identity])
                    print(identValue[identity])
                    parseOut.write("\nKeyword Statement: ")
                    parseOut.write(str(c))
                    parseOut.write(':')
                    parseOut.write('DISPLAY ')
                    parseOut.write(parserList[p+1])
                    parseOut.write('\tString Literal:')
                    parseOut.write(parserList[p + 1])
                    parseOut.write(identValue[identity])
                    p += 2
                    c += 1
            else:
                print('Syntax Error at Line:', pLine[p+1],' Column: ', pCol[p+1], 'Variable', parserList[p+1], 'is not defined')
                sys.exit()


    if parserList[p] == 'SET':
        if parserList[p+2] == '=':
            identCheck = parserList[p+1]
            if identName.count(identCheck)!= 0:
                identity = identName.index(parserList[p + 1])
                identValue[identity] = parserList[p+3]
                if identType[identity].lower() == 'double' or identType[identity].lower() == 'float':
                    if isinstance(eval(parserList[p+3]), float):
                      #  print('Assignment Statement', c, ':', 'SET', parserList[p+1], parserList[p+2], parserList[p+3])
                      #  print('\tIdentifier(', parserList[p+1], ') of type ', identType[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('SET ')
                        parseOut.write(parserList[p+1])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+2])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+3])
                        parseOut.write('\tIdentifier(')
                        parseOut.write(parserList[p+1])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity])
                        p += 4
                        c += 1

                    else:
                        print("Syntax Error at line:", pLine[p+2], " Column:", pCol[p+2], " Variable", parserList[p+1],
                              'expected type ',identType[identity] ,' but instead got: ', parserList[p+3])
                        sys.exit()
                elif identType[identity].lower() == 'int':
                    if isinstance(eval(parserList[p+3]), int):
                       # print('Assignment Statement', c, ':', 'SET', parserList[p+1], parserList[p+2], parserList[p+3])
                       # print('\tIdentifier(', parserList[p+1], ') of type ', identType[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('SET ')
                        parseOut.write(parserList[p+1])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+2])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+3])
                        parseOut.write('\tIdentifier(')
                        parseOut.write(parserList[p+1])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity])
                        p += 4
                        c += 1
                    else:
                        print("Syntax Error at line:", pLine[p + 2], " Column:", pCol[p + 2], " Variable",
                              parserList[p + 1],
                              'expected type ', identType[identity], ' but instead got: ', parserList[p + 3])
                        sys.exit()
                elif identType[identity].lower() == 'string':
                    lenCheck = parserList[p+3]
                    if lenCheck.__len__() >= 4:
                        if isinstance(eval(parserList[p+3]), str):
                          #  print('Assignment Statement', c, ':', 'SET', parserList[p+1], parserList[p+2], parserList[p+3])
                          #  print('\tIdentifier(', parserList[p+1], ') of type ', identType[identity])
                            parseOut.write("\nKeyword Statement: ")
                            parseOut.write(str(c))
                            parseOut.write(':')
                            parseOut.write('SET ')
                            parseOut.write(parserList[p+1])
                            parseOut.write(' ')
                            parseOut.write(parserList[p+2])
                            parseOut.write(' ')
                            parseOut.write(parserList[p+3])
                            parseOut.write('\tIdentifier(')
                            parseOut.write(parserList[p+1])
                            parseOut.write(') of type ')
                            parseOut.write(identType[identity])
                            p += 4
                            c += 1
                        else:
                            print("Syntax Error at line:", pLine[p + 2], " Column:", pCol[p + 2], " Variable",
                                  parserList[p + 1],
                                  'expected type ', identType[identity], ' but instead got: ', parserList[p + 3])
                            sys.exit()
                    else:
                        print("Syntax Error at line:", pLine[p + 2], " Column:", pCol[p + 2], " Variable",
                                  parserList[p + 1], 'expected type ', identType[identity],
                              ' but STRING of size 0 or 1 are stored as CHAR type')
                        sys.exit()
                elif identType[identity].lower() == 'char':
                    lenCheck = parserList[p + 3]
                    if lenCheck.__len__() < 4:
                        if isinstance(eval(parserList[p+3]), str):
                          #  print('Assignment Statement', c, ':', 'SET', parserList[p+1], parserList[p+2], parserList[p+3])
                          #  print('\tIdentifier(', parserList[p+1], ') of type ', identType[identity])
                            parseOut.write("\nKeyword Statement: ")
                            parseOut.write(str(c))
                            parseOut.write(':')
                            parseOut.write('SET ')
                            parseOut.write(parserList[p+1])
                            parseOut.write(' ')
                            parseOut.write(parserList[p+2])
                            parseOut.write(' ')
                            parseOut.write(parserList[p+3])
                            parseOut.write('\tIdentifier(')
                            parseOut.write(parserList[p+1])
                            parseOut.write(') of type ')
                            parseOut.write(identType[identity])
                            p += 4
                            c += 1
                        else:
                            print("Syntax Error at line:", pLine[p + 2], " Column:", pCol[p + 2], " Variable",
                                  parserList[p + 1],
                                  'expected type ', identType[identity], ' but instead got: ', parserList[p + 3])
                            sys.exit()
                    else:
                        if isinstance(eval(parserList[p+3]), str):
                            print("Syntax Error at line:", pLine[p + 2], " Column:", pCol[p + 2], " Variable",
                                      parserList[p + 1], 'expected type ', identType[identity],
                                  ' but length of: ', parserList[p+3], ' is larger than 1')
                            sys.exit()
                        else:
                            print("Syntax Error at line:", pLine[p + 2], " Column:", pCol[p + 2], " Variable",
                                  parserList[p + 1], 'expected type ', identType[identity],
                                  ' but got: ', parserList[p + 3])
                            sys.exit()
                elif identType[identity].lower() == 'true' or identType[identity].lower() == 'false':
                    if isinstance(eval(parserList[p+3]), bool):
                      #  print('Assignment Statement', c, ':', 'SET', parserList[p+1], parserList[p+2], parserList[p+3])
                      #  print('\tIdentifier(', parserList[p+1], ') of type ', identType[identity])
                        parseOut.write("\nKeyword Statement: ")
                        parseOut.write(str(c))
                        parseOut.write(':')
                        parseOut.write('SET ')
                        parseOut.write(parserList[p+1])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+2])
                        parseOut.write(' ')
                        parseOut.write(parserList[p+3])
                        parseOut.write('\tIdentifier(')
                        parseOut.write(parserList[p+1])
                        parseOut.write(') of type ')
                        parseOut.write(identType[identity])
                        p += 4
                        c += 1
                    else:
                        print("Syntax Error at line:", pLine[p + 2], " Column:", pCol[p + 2], " Variable",
                              parserList[p + 1],
                              'expected type ', identType[identity], ' but instead got: ', parserList[p + 3])
                        sys.exit()
            else:
                print("Syntax Error at Line:", pLine[p+2] ," Column:",pCol[p+2] , "Variable", identCheck ,"is not defined")
                sys.exit()

    if parserList[p] == 'INPUT':
        if stringList.count(parserList[p+1]) != 0:  # checks for string literals as next
            if parserList[p+2] == ',':
                identity = identName.index(parserList[p + 3])
               # print('Keyword Statement: ', c, ':', 'INPUT', parserList[p+1],parserList[p+2],parserList[p+3])
               # print('\tString Literal: ', parserList[p + 1])
               # print('\tIdentifier(', parserList[p + 3], ') of type ', identType[identity])
                print(parserList[p+1])

                parseOut.write("\nKeyword Statement: ")
                parseOut.write(str(c))
                parseOut.write(':')
                parseOut.write('INPUT ')
                parseOut.write(parserList[p+1])
                parseOut.write(' ')
                parseOut.write(parserList[p+2])
                parseOut.write(' ')
                parseOut.write(parserList[p+3])
                parseOut.write('\tString Literal:')
                parseOut.write(parserList[p + 1])
                parseOut.write('\tIdentifier(')
                parseOut.write(parserList[p+3])
                parseOut.write(') of type ')
                parseOut.write(identType[identity])
                identValue[identity] = input()
                p += 4
                c += 1
            else:
              #  print('Keyword Statement: ', c, ':', 'INPUT', parserList[p+1])
              #  print('\tString Literal: ', parserList[p + 1])
                parseOut.write("\nKeyword Statement: ")
                parseOut.write(str(c))
                parseOut.write(':')
                parseOut.write('INPUT ')
                parseOut.write(parserList[p+1])
                parseOut.write('\tString Literal:')
                parseOut.write(parserList[p + 1])
                p += 2
                c += 1
        elif identName.count(parserList[p+1]) != 0:
            if parserList[p+2] == ',':
                identity = identName.index(parserList[p + 1])
              #  print('Keyword Statement: ', c, ':', 'INPUT', parserList[p+1],parserList[p+2],parserList[p+3])
              #  print('\tIdentifier(', parserList[p + 1], ') of type ', identType[identity])
                identity = identName.index(parserList[p + 3])
              #  print('\tIdentifier(', parserList[p + 3], ') of type ', identType[identity])
                print(parserList[p+1])
                parseOut.write("\nKeyword Statement: ")
                parseOut.write(str(c))
                parseOut.write(':')
                parseOut.write('INPUT ')
                parseOut.write(parserList[p+1])
                parseOut.write(' ')
                parseOut.write(parserList[p+2])
                parseOut.write(' ')
                parseOut.write(parserList[p+3])
                parseOut.write('\tIdentifier(')
                parseOut.write(parserList[p+3])
                parseOut.write(') of type ')
                parseOut.write(identType[identity])
                identValue[identity] = input()
                p += 4
                c += 1
            else:
                identity = identName.index(parserList[p + 1])
              #  print('Keyword Statement: ', c, ':', 'INPUT', parserList[p+1])
              #  print('\tIdentifier(', parserList[p+1], ') of type ', identType[identity])
                identValue[identity] = input()
                parseOut.write("\nKeyword Statement: ")
                parseOut.write(str(c))
                parseOut.write(':')
                parseOut.write('INPUT ')
                parseOut.write(parserList[p+1])
                parseOut.write('\tIdentifier(')
                parseOut.write(parserList[p+3])
                parseOut.write(') of type ')
                parseOut.write(identType[identity])
                p += 2
                c += 1

    if parserList[p] == 'IF':   # will create a templist of the whole if statement, which should always end with then.

        if identName.count(parserList[p+1]) != 0:
           identity = identName.index(parserList[p + 1])
           if identType[identity].lower() == 'char' or identType[identity].lower() =='str' or identType[identity].lower() == 'bool':
               var1 = identValue[identity]
           else:
               var1 = eval(identValue[identity])
        else:
           if identType[identity].lower() == 'char' or identType[identity].lower() =='str' or identType[identity].lower() == 'bool':
               var1 = identValue[identity]
           else:
               var1 = eval(identValue[identity])

        while parserList[p+t] != 'THEN':
            tempList.append(parserList[p+t])
            t += 1
        tempList.append('THEN')
        t +=1

        if identName.count(parserList[p-1]) != 0:
           identity = identName.index(parserList[p - 1])
           if identType[identity].lower() == 'char' or identType[identity].lower() =='str' or identType[identity].lower() == 'bool':
               var2 = identValue[identity]
           else:
               var2 = eval(identValue[identity])

        opFound = 0
        z = 1
        operator = ''
        isNot = 0
        yes = 0    

        while opFound != 1:
            if parserList[p+z] == 'NOT':
                isNot = 1
                z += 1
            if parserList[p+z] == '<':
                operator = '<'
                opFound = 1
            if parserList[p+z] == '>':
                operator = '>'
                opFound = 1
            if parserList[p+z] == '<=':
                operator = '<='
                opFound = 1
            if parserList[p+z] == '>=':
                operator = '>='
                opFound = 1
            if parserList[p+z] == '!=':
                operator = '!='
                opFound = 1
            if parserList[p+z] == '==':
                operator = '=='
                opFound = 1
            if parserList[p+z] == 'GREATER' and parserList[p+z+1] != 'OR':
                operator = 'GREATER'
                opFound = 1
            if parserList[p+z] == 'GREATER' and parserList[p+z+1] == 'OR':
                operator = 'GREATER OR EQUAL'
                opFound = 1
            if parserList[p+z] == 'LESSER' and parserList[p+z+1] != 'OR':
                operator = 'LESSER'
                opFound = 1
            if parserList[p+z] == 'LESSER' and parserList[p+z+1] == 'OR':
                operator = 'LESSER OR EQUAL'
                opFound = 1
            else:
                z += 1

        if operator == '<':
            if var1 < var2:
                yes = 1
        if operator == '>':
            if var1 < var2:
                yes = 1
        if operator == '<=':
            if var1 <= var2:
                yes = 1
        if operator == '>=':
            if var1 >= var2:
                yes = 1
        if operator == '!=':
            if var1 != var2:
                yes = 1
        if operator == '==':
            if var1 == var2:
                yes = 1
        if operator == 'GREATER' and isNot == 1:
            if var1 < var2:
                yes = 1
        if operator == 'GREATER' and isNot == 0:
            if var1 > var2:
                yes = 1
        if operator == 'LESSER' and isNot == 1:
            if var1 > var2:
                yes = 1
        if operator == 'LESSER' and isNot == 0:
            if var1 < var2:
                yes = 1
        if operator == 'GREATER OR EQUAL' and isNot == 1:
            if var1 < var2:
                yes = 1
        if operator == 'GREATER OR EQUAL' and isNot == 0:
            if var1 >= var2:
                yes = 1
        if operator == 'LESSER OR EQUAL' and isNot == 1:
            if var1 > var2:
                yes = 1
        if operator == 'LESSER OR EQUAL' and isNot == 0:
            if var1 <= var2:
                yes = 1

       # print('Boolean Expression Statement: ', c, ':', 'IF ', end='', flush=True)
        parseOut.write('\nBoolean Expression Statement: ')
        parseOut.write(str(c))
        parseOut.write(':')
        parseOut.write('IF')
        while counter < t-1:    # then prints that list as the current command
          #  print('\t',tempList[counter], ' ',  end='', flush=True)
            parseOut.write('\t')
            parseOut.write(tempList[counter])
            parseOut.write(' ')
            if identName.count(tempList[counter]) != 0:
                identity = identName.index(tempList[counter])
               # print('\n\tIdentifier(', tempList[counter], ') of type ', identType[identity])
                parseOut.write('\n\tIdentifier(')
                parseOut.write(tempList[counter])
                parseOut.write(') of type ')
                parseOut.write(identType[identity])
            counter += 1
        tempList = [] #clear counters incase there is multiple if's in a program
        counter = 0
        p += t
        c += 1
        ifbool ='yes' #changes this to yes so that the parser knows there is an open if for error handling.
        print('')
        t = 1

    if parserList[p] == 'ELSE': #checks to see if there is an open if to use else with
        if ifbool == 'yes':
          #  print('Expression Statement: ', c, ':', 'ELSE')
            parseOut.write('\nExpression Statement: ')
            parseOut.write(str(c))
            parseOut.write(':')
            parseOut.write('ELSE')
            p += 1
            c += 1
        else:
            print('Syntax Error at line:', pLine[p], 'On Column:' ,pCol[p], 'ELSE without IF') #else without if syntax error

    if parserList[p] == 'ENDIF': #also checks to see if there is an open if. Once completing the print, it will close the open if.
        if ifbool == 'yes':
           # print('Keyword Statement: ', c, ':', 'ENDIF')
            parseOut.write('\nKeyword Statement: ')
            parseOut.write(str(c))
            parseOut.write(':')
            parseOut.write('ENDIF')
            p += 1
            c += 1
            ifbool = 'no'
        else:
            print('Syntax Error at line:', pLine[p], 'On Column:' ,pCol[p], 'ENDIF without IF') #otherwise syntax error

    if parserList[p] == 'RETURN':
       # if isinstance(eval(parserList[p+1]), int):
       # print('Keyword Statement: ', c, ':', 'RETURN')
       # print('\tReturn Value of :', parserList[p+1])
        parseOut.write('\nKeyword Statement: ')
        parseOut.write(str(c))
        parseOut.write(':')
        parseOut.write('RETURN')
        parseOut.write('\tReturn Value of :')
        parseOut.write(parserList[p+1])
        p += 2
        c += 1
        #else:
            #print('Syntax Error at line', pLine[p], 'On Column:' ,pCol[p], 'Expected Integer Return')
            #sys.exit()
    if parserList[p] == 'ENDFUN': #checks to see if the function you end is one that is open. Othewise syntax error.
        if parserList[p+1] == fname:
           # print('End Statement: ', c, ':', 'ENDFUN', parserList[p+1])
            parseOut.write('\nEnd Statement: ')
            parseOut.write(str(c))
            parseOut.write(':')
            parseOut.write('ENDFUN ')
            parseOut.write(parserList[p+1])
            p += 2
            c += 1
            fname = ''
        else:
            print('Syntax Error on line:', pLine[p], 'On Column:', pCol[p], 'Improper Function Close')

print('\nEnd of source file\n')
