#!/usr/bin/env python
# coding: utf-8

# In[1]:


import amplpy
import pandas as pd
from string import ascii_lowercase
from amplpy import AMPL, Environment


# In[2]:


print("Enter the kind of puzzle you want to solve : \n")

puzzle = int(input("Enter 1 for 3-In-A-Row, or 2 for ABC-Path: "))

ampl = AMPL(Environment("C:/Users/mayan/OneDrive/Documents/AMPL/ampl_mswin64"))

ampl.setOption("solver", "cplex")

if puzzle == 1:
    
    ampl.reset()
    ampl.read('p2t05mod3.mod')
    ampl.readData('p2t05dat3.dat')
    
    #ask for user input for 3 in a row
    size = int(input("Enter the size of the grid (that is number of rows or columns in the grid) : \n"))
    
    invalid = int(input("Enter the number of minimum invalid consecutive cells : \n"))
    
    lst = []
    lst_lst = []
    
    print("Enter hints when asked for, in the following format \n")
    print("Enter B for Blue, W for White and G for Grey \n")
    
    for each in range(size):
        lst_lst = list(input(f"Input the hints for row - {each+1} : \n",))
        lst.append(lst_lst)
    
    S = ampl.getParameter('S')
    S.getValues()
    S.setValues([size])
    
    n = ampl.getParameter('n')
    n.getValues()
    n.setValues([invalid])
    
    index0_lst = [i+1 for i in range(size)]
    index1_lst = [i+1 for i in range(size)]
    
    #Fetch and change the blue parameter
    
    lst_blue = []
    for each in range(len(lst)):
        lst_blue.append([1 if x == 'B' else 0 for x in lst[each]])
    
    blue = ampl.getParameter('blue')
    
    blue.getValues()
    
    blue.setValues({
        (index0, index1): lst_blue[i][j]
        for i, index0 in enumerate(index0_lst)
        for j, index1 in enumerate(index1_lst)
    })
    
    #Fetch and change the white parameter
    
    lst_white = []
    for each in range(len(lst)):
        lst_white.append([1 if x == 'W' else 0 for x in lst[each]])
    
    white = ampl.getParameter('white')
    
    white.getValues()
    
    white.setValues({
        (index0, index1): lst_white[i][j]
        for i, index0 in enumerate(index0_lst)
        for j, index1 in enumerate(index1_lst)
    })
    
    try:
        invalid <= size
    except:
        raise ValueError('Number of invalid consecutive cells should be less than the size of the grid')
    
    try:
        size%2 == 0
    except:
        raise ValueError('Size of the grid should be a multiple of 2')
    
    
    ampl.solve()
    
    y = ampl.getVariable('y')
    y_df = y.getValues().toPandas()
    
    y = ampl.getVariable('y')
    y_df = y.getValues().toPandas()
    y_df=y_df.astype(int)
    y_df.index=pd.MultiIndex.from_tuples(y_df.index,names=('row','column'))
    y_df['row']=y_df.index.get_level_values(0).astype(int)
    y_df['column']=y_df.index.get_level_values(1).astype(int)
    y_output=y_df.pivot(index='row',columns='column',values='y.val')
    y_output.replace([1,0],['Blue','White'],inplace=True)
    y_output.columns.name = None
    y_output.index.name = None
    print(y_output)
    
else:
    
    ampl.reset()
    ampl.read('p2t05modA.mod')
    ampl.readData('p2t05datA.dat')
    
    #ask for user input for abc path
    
    size = int(input("Enter the size of the grid: \n"))
    
    num_letters = int(input("Enter the number of alphabets to be filled in the grid: \n"))
    
    row_A = int(input("Enter the row number of the letter \"A\": \n"))
    col_A = int(input("Enter the column number of the letter \"A\": \n"))
    
    top = list(input("Enter the hints (letters shown at top) at the top of the grid: \n").lower())
    bottom = list(input("Enter the hints (letters shown at bottom) at the bottom of the grid: \n").lower())
    left = list(input("Enter the hints (letters shown at left) at the left side of the grid: \n").lower())
    right = list(input("Enter the hints (letters shown at right) at the right side of the grid: \n").lower())
    
    left_diag = list(input("Enter the letters shown at the top left and bottom right side of the diagonal in the grid: \n").lower())
    right_diag = list(input("Enter the letters shown at the top right and bottom left side of the diagonal in the grid: \n").lower())
    
    #define the dictionary of alphabets with values as their respective position
    letters = {letter: index for index, letter in enumerate(ascii_lowercase, start=1)} 
    
    #Fetch and change the parameters
    
    N = ampl.getParameter('N')
    N.getValues()
    N.setValues([size])
    
    n = ampl.getParameter('n')
    n.getValues()
    n.setValues([num_letters])
    
    ia = ampl.getParameter('ia')
    ia.getValues()
    ia.setValues([row_A])
    
    ja = ampl.getParameter('ja')
    ja.getValues()
    ja.setValues([col_A])
    
    t = ampl.getParameter('t')
    t.getValues()
    t.setValues([letters[character] for character in top if character in letters])
    
    b = ampl.getParameter('b')
    b.getValues()
    b.setValues([letters[character] for character in bottom if character in letters])
    
    l = ampl.getParameter('l')
    l.getValues()
    l.setValues([letters[character] for character in left if character in letters])
    
    r = ampl.getParameter('r')
    r.getValues()
    r.setValues([letters[character] for character in right if character in letters])
    
    dl = ampl.getSet('dl')
    dl.getValues()
    dl.setValues([letters[character] for character in left_diag if character in letters])
    
    dr = ampl.getSet('dr')
    dr.getValues()
    dr.setValues([letters[character] for character in right_diag if character in letters])
    
    ampl.solve()
    
    x = ampl.getVariable('x')
    x_df = x.getValues().toPandas()
    
    try:
        num_letters = size**2
    except:
        raise ValueError("Please make sure that number of letters is the square of the size of the grid")
    
    col_list = []
    row_list = []
    letter_num_list = []
    for letter in range(1, num_letters+1):
        for row in range(1, size+1):
            for col in range(1, size+1):
                if int(x.get(letter, row, col).value()) == 1:
                    col_list.append(col)
                    row_list.append(row)
                    letter_num_list.append(letter)
    
    letter_list = []
    for each in letter_num_list:
        letter_list.append(list(letters.keys())[list(letters.values()).index(each)].upper())
        
    index = list(range(1, size+1))
    columns = list(range(1, size+1))
    
    df = pd.DataFrame(index = index, columns = columns)
    df = df.fillna(0)
    
    for index, value in enumerate(letter_list):
        df.iloc[row_list[index]-1, col_list[index]-1] = value
    
    print(df)

