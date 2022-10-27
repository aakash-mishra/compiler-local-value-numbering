import argparse 
import ply.ply.lex as lex
import ply.ply.yacc as yacc

tokens = ["BINOP", "ID", "SEMI", "ASSIGN"]
t_ignore = ' '
t_SEMI = ';'
t_ASSIGN = '='
t_ID = '[a-z]'
t_BINOP = '\+ | \-'

global_ctr = 0
stored_statements = {}
variables = {}
replaced = 0
def t_NEWLINE(t):
    "\\n"
    t.lexer.lineno += 1
    pass

def t_error(t):
    print("lexing error")

def p_error(p):
    print("unable to parse")

'''
stm_list : stm stm_list
stm_list : stm
stm : ID ASSIGN ID BINOP ID SEMI
'''

def p_stm_list(p):
    """
    stm_list : stm stm_list
    """
    pass
def p_stm(p):
    """
    stm_list : stm
    """
    pass
def p_plus_stm(p):
    """
    stm : ID ASSIGN ID BINOP ID SEMI
    """
    # matches things like x = a + b
    operand1 = p[3]
    operand2 = p[5]
    assign_var = p[1]
    if(operand1 not in variables):
        global global_ctr
        variables[operand1] = global_ctr
        global_ctr += 1
        # declare new variables
        print("\tdouble " + str(operand1) + str(variables[operand1]) + ";") # double k0;
    operand1 = p[3] + str(variables[operand1]) # operand1 becomes k1 for ex
    
    if(operand2 not in variables):
        variables[operand2] = global_ctr
        global_ctr += 1
        print("\tdouble " + str(operand2 + str(variables[operand2])) + ";") # double g1;
    operand2 = p[5] + str(variables[operand2])

    # always assign new number to assignment
    variables[assign_var] = global_ctr
    new_assign_variable = assign_var + str(global_ctr)
    print("\tdouble " + new_assign_variable + ";") # double d2;
    global_ctr += 1

    # once variables are numbered and declared
    # add expression to stored_statements
    expr = operand1 + p[4] + operand2 # only the rhs
    new_expr = new_assign_variable + " = " + operand1 + p[4] + operand2 + ";"
    if(expr in stored_statements.keys()):
        # possible replacement found
        global replaced
        replaced += 1
        new_expr = new_assign_variable + " = " + stored_statements.get(expr) + ";"
    # also need to check for the reverse expression
    elif(p[4] == '+' and (operand2 + "+" + operand1) in stored_statements.keys()):
            replaced += 1
            rev_expr = operand2 + "+" + operand1
            new_expr = new_assign_variable + " = " + stored_statements.get(rev_expr) + ";"
    else:
        # no replacement found
        stored_statements[expr] = new_assign_variable # ex: {"x1 + y2 : a3"}
    
    print("\t" + new_expr)    
    # print("State at the end of this line: ")
    # print("variables " + str(variables))
    # print("stored statemenets " + str(stored_statements))

def reassign_vars():
    # walk through the variables map and re assign stuff
    for key,value in variables.items():
        print("\t" + key + " = " + key + str(value) + ";") # a = a5

def local_value_numbering(f):
    f = open(f)
    s = f.read()
    f.close()
    pre = s.split("// Start optimization range")[0]
    post = s.split("// Start optimization range")[1].split("// End optimization range")[1]
    to_optimize = s.split("// Start optimization range")[1].split("// End optimization range")[0]
    lexer = lex.lex()
    # global global_ctr
    # global stored_statements
    # global variables
    # global replaced
    # stored_statements = {}
    # global_ctr = 0
    # variables = {}
    # replaced = 0
    parser = yacc.yacc(debug=True)
    # this would print things before the local block    
    print(pre)
    # this would print the optimized local block (with apt declarations)
    parser.parse(to_optimize)
    # this would reassign newly initialized variables back to their original variables
    reassign_vars()
    # this would print things after the local block
    print(post)

    # You should keep track of how many instructions you replaced
    print("// replaced: " + str(replaced))    
    

# if you run this file, you can give it one of the python test cases
# in the test_cases/ directory.
# see solutions.py for what to expect for each test case.
if __name__ == '__main__': 
    parser = argparse.ArgumentParser()   
    parser.add_argument('cppfile', help ='The cpp file to be analyzed') 
    args = parser.parse_args()
    local_value_numbering(args.cppfile)
