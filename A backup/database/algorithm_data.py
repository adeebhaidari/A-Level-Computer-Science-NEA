'''
for solving f2l, the program will only look at 3 faces, the faces at index 0 2 and 3. so the states of the faces will be converted into a string such that the p[rogfrma will e able to convert any of group of 3 faceas andf compare ifb that state can be solcved with an algorithm, if not then localised A* will be used until a state is found that can be solved
the first 9 characters will be the state of the face at index 2, 2nd 9 characters will be the state at face index 3 and last 9 face index 5.
the numbers for the key of this dictionary represent the center face colour relative to the way the cube has been rotated around the y-axis
-> the format is:
    face index, face coordindta (x,y), target colour based from the 3 faces
    this will repeat 3 times in total for faces index 2 3 and 5
'''
'''
for identifying the f2l state, the string will be in the form corner edger where the first half the string will contain information about the corner and the second half about the edge
    it will be so that the first character is the face index, second character the face coordinate (x,y) and this will be done for all the stickers
'''

f2l_algorithms = [
    ('F2L', '20103003301351225222', 'U R U" R"'),
    ('F2L', 'X22X2XXXX0XXX3XXXXXXXXXXX33', 'y" U" R" U R'),
    ('F2L', 'XX0X2XXXX3XXX3XXXXXXX3XXXX2', 'y" R" U" R'),
    ('F2L', 'XX2X2XXXX0XXX3XXXXX2XXXXXX3', 'R U R"'),

    ('F2L', 'XX0X2XXXX3XXX3XXXXX3XXXXXX2', 'U" R U" R" U y" R" U" R'),
    ('F2L', 'Case 1.2', 'U" R U R" U R U R"'),
    ('F2L', 'Case 1.3', 'U" R U2" R" U y" R" U" R'),
    ('F2L', 'Case 1.4', 'R" U2" R2 U R2" U R'),
    ('F2L', 'Case 1.5', 'y" U R" U R U" R" U" R'),
    ('F2L', 'Case 1.6', 'U" R U" R" U R U R"'),

    ('F2L', 'Case 2.1', 'U" R U R" U2 R U" R"'),
    ('F2L', 'Case 2.2', 'y" U R" U" R U2" R" U R'),
    ('F2L', 'Case 2.3', 'U" R U2" R" U2 R U" R"'),
    ('F2L', 'Case 2.4', 'y" U R" U2 R U2" R" U R'),

    ('F2L', 'Case 3.1', 'U R U2 R" U R U" R"'),
    ('F2L', 'Case 3.2', 'y" U" R" U2 R U" R" U R'),
    ('F2L', 'Case 3.3', 'R U R" U2 R U R"'),
    ('F2L', 'Case 3.4', 'F" L" U2 L F'),

    ('F2L', 'Incorrectly Connected 1', 'y" R" U R U2" y R U R"'),
    ('F2L', 'Incorrectly Connected 2', 'R U" R" U2 y" R" U" R'),
    ('F2L', 'Incorrectly Connected 3', 'R U2" R" U" R U R"'),
    ('F2L', 'Incorrectly Connected 4', 'y" R" U2 R U R" U" R'),
    ('F2L', 'Incorrectly Connected 5', 'R U R" U2" R U R" U R U" R"'),
    ('F2L', 'Incorrectly Connected 6', 'F U R U" R" F" R U" R"'),

    ('F2L', 'Corner in Place 1', 'R" F" R U R U" R" F'),
    ('F2L', 'Corner in Place 2', 'U R U" R" U" F" U F'),
    ('F2L', 'Corner in Place 3', 'R U" R" U R U" R"'),
    ('F2L', 'Corner in Place 4', 'y" R" U R U" R" U R'),
    ('F2L', 'Corner in Place 5', 'R" F R F" U R U" R"'),
    ('F2L', 'Corner in Place 6', 'R U R" U" R U R"'),

    ('F2L', 'Edge in Place 1', 'U" R" F R F" R U" R"'),
    ('F2L', 'Edge in Place 2', 'U R U" R" U R U" R" U R U" R"'),
    ('F2L', 'Edge in Place 3', 'U" R U" R" U2 R U" R"'),
    ('F2L', 'Edge in Place 4', 'U R U R" U2 R U R"'),
    ('F2L', 'Edge in Place 5', 'U" R U R" U y" R" U" R'),
    ('F2L', 'Edge in Place 6', 'U F" U" F U" R U R"'),

    ('F2L', 'Edge and Corner 1', 'R U" R" d R" U2 R U2" R" U R'),
    ('F2L', 'Edge and Corner 2', 'R U R" U" R U2 R" U" R U R"'),
    ('F2L', 'Edge and Corner 3', 'R U" R" U R U2" R" U R U" R"'),
    ('F2L', 'Edge and Corner 4', 'R U" R" F R U R" U" F" R U" R"'),
    ('F2L', 'Edge and Corner 5', 'R U R" U" R U" R" U2 y" R" U" R')
]

'''
oll_algorithms = [
    # the first 9 letters represent the pattern of the top yellow face reading from left to right top to bottom
    # Y stands for yellow, X stands for any other colour
    ('OLL', 'XYYYYYXYXYXXYXXYXXXXX', 'R U2 R" U" R U" R"'),
    ('OLL', 'XYXYYYYYXXXXXXYXXYXXY', 'R U R" U R U2 R"'),
    ('OLL', 'XYXYYYXYXXXXYXYXXXYXY', 'R U2 R" U" R U R" U" R U" R"'),
    ('OLL', 'XYXYYYXYXYXYXXYXXXYXX', 'R U2" R2" U" R2 U" R2" U2" R'),
    ('OLL', 'XYYYYYXYYXXXYXXXXXXXY', 'r U R" U" r" F R F"'),
    ('OLL', 'YYXYYYXYYXXXYXXXXYXXX', 'x R" U R D" R" U" R D x"'),
    ('OLL', 'XYXYYYYYYXXXXXXXXXYXY', 'R2 D" R U2 R" D R U2 R'),
    
    ('OLL', 'XXYYYYXXYXXXYYXXXXXYY', 'R U R" U" R" F R F"'),
    ('OLL', 'XXYYYYXXYYXYXYXXXXXYX', 'F R U R" U" F"'),
    
    ('OLL', 'XXXXYYXYYXYYXXXXXYXYY', 'r" U2" R U R" U r'),
    ('OLL', 'XYYXYYXXXYYXYYXYXXXXX', 'r U2 R" U" R U" r"'),
    
    ('OLL', 'XXXYYYYXYYXXXYXXXYXYX', 'R U R2" U" R" F R U R U" F"'),
    ('OLL', 'YYXXYXYYXXYXXXXYYYXXX', 'R" U" R" F R F" U R'),
    
    ('OLL', 'YXXYYXXYYXXXYXXXYYXYX', 'y2 R U R" F" R U R" U" R" F R U" R" F R F"'),
    ('OLL', 'XYYYYXYXXXXXXYXYYXXXY', 'R U R" U R U" R" U" R" F R F"'),
    
    ('OLL', 'YYYYYXYXYXXXXYXXYXXXX', 'r U R" U" M U R U" R"'),
    ('OLL', 'YXYYYYYXYXXXXYXXXXXYX', 'R U R" U" M" U R U" r"'),
    
    ('OLL', 'XYYXYYXXYXYXYYXXXXXXY', 'R" U" R" F R F" U R'),
    ('OLL', 'XXYXYYXYYXYXYXXXXXXYY', 'R U B" U" R" U R B R"'),
    ('OLL', 'YXXYYXYYXXXXXXXYYYXYX', 'f" L" U" L U f'),
    ('OLL', 'XXYXYYXYYYYYXXXXXXXYX', 'f R U R" U" F"'),
    
    ('OLL', 'XXXYYYXXXYXYXYYXXXYYX', 'f R U R" U" R U R" U" f"'),
    ('OLL', 'XXXYYYXXXYXYXYXYXYXYX', 'r" U" r U" R" U R U" R" U R r" U r'),
    ('OLL', 'XYXXYXXYXXYXYXXYYYXXY', 'y R U R" U" R U" R" F" U" F R U R"'),
    ('OLL', 'XYXXYXXYXYYYXXXYYYXXX', 'y R" F R U R U" R2" F" R2 U" R" U R U R"'),
    
    ('OLL', 'XYXYYXXXYYXXYYXXYXYXX', 'R U R" U" R" F R2 U R" U" F"'),
    ('OLL', 'XXYYYXXYXXXYXXYXYXXYY', 'R U R" U R" F R F" R U2" R"'),
    ('OLL', 'YXXXYYXYYXYXYXXXXYXYX', 'R U2" R2" F R F" R U2" R"'),
    ('OLL', 'YYXYYXXXYXXXYYXXYYXXX', 'F R U" R" U" R U R" F"'),
    
    ('OLL', 'XXXYYYYXXXXXXYYXXYXYY', 'F U R U" R2" F" R U R U" R"'),
    ('OLL', 'XXXYYYXXYYXXYYXXXXYYX', 'y" F U R U2 R" U" R U2 R" U" F"'),
    ('OLL', 'XXYYYYXXXYXXYYXYXXXYX', 'r U r" R U R" U" r U" r"'),
    ('OLL', 'XXXYYYXXYXXYXYXXXYXYY', 'r" U" r R" U" R U r" U r'),
    
    ('OLL', 'YXYYYXXYXXXYXXXYYXXYX', 'y R U R" U" R U" R" F" U" F R U R"'),
    ('OLL', 'YYXXYYYXXXYXXYYXXXYXX', 'y" F U R U2 R" U" R U2 R" U" F"'),
    ('OLL', 'XYXYYXYXYXXXXYXXYXYXY', 'R U R" U R U2" R" F R U R" U" F"'),
    ('OLL', 'YXYYYXXYXXXXYXYXYXXYX', 'R" U" R U" R" U2 R F R U R" U" F"'),
    
    ('OLL', 'XYXYYXXXXYXYXYYXYXYXX', 'F R U R" U" R U R" U" F"'),
    ('OLL', 'XYXXYYXXXXYXYYXYXYXXY', 'F" L" U" L U L" U" L U F'),
    ('OLL', 'XYXXYYXXXYYYXYYXXXYXX', 'r U" r2" U r2 U r2" U" r'),
    ('OLL', 'XXXXYYXYXYYYXXYXXXYYX', 'r" U r2 U" r2" U" r2 U r"'),
    ('OLL', 'XXXXYYXYXYYYXXXYXYXYX', 'r" U" R U" R" U R U" R" U2 r'),
    ('OLL', 'XYXXYYXXXYYYXYXYXYXXX', 'r U R" U R U" R" U R U2" r"'),
    
    ('OLL', 'XYXYYXYXXXXXXYYXYYXXY', 'r U R" U R U2" r"'),
    ('OLL', 'YXXYYXXYXXXXYXXYYXYYX', 'r" U" R U" R" U2 r'),
    ('OLL', 'XXXXYYYYXXYXXXYXXYXYY', 'r" R2 U R" U R U2 R" U M"'),
    ('OLL', 'YYXXYYXXXXYXYYXYXXYXX', 'M" R" U" R U" R" U2 R U" M'),
    ('OLL', 'XXYYYYYXXXXXXYXYXXXYY', 'L F" L" U" L U" F U" L"'),
    ('OLL', 'YXXYYYXYYXXYXYXXXXYYX', 'R" F R U R" U" F" U R'),
    
    ('OLL', 'XXXXYXXXXYYYXYXYYYXYX', 'R U2" R2" F R F" U2" R" F R F"'),
    ('OLL', 'XXXXYXXXXYYYXYYXYXYYX', 'F R U R" U" F" f R U R" U" f"'),
    ('OLL', 'XXXXYXXXYXYYXYXXYYXYY', 'f R U R" U" f" U" F R U R" U" F"'),
    ('OLL', 'XXYXYXXXXYYXYYXYYXXYX', 'f R U R" U" f" U F R U R" U" F"'),
    ('OLL', 'YXYXYXXXXXYXYYYXYXXYX', 'r U R" U R U2 r" r" U" R U" R" U2 r'),
    ('OLL', 'YXYXYXXXXXYYXYXYYXXYX', 'M U R U R" U" M" R" F R F"'),
    ('OLL', 'YXXXYXXXYXYYXYXXYXYYX', 'R U R" U R" F R F" U2" R" F R F"'),
    ('OLL', 'YXYXYXYXYXYXXYXXYXXYX', 'M U R U R" U" M2" U R U" r"'),
]
'''

oll_algorithms = [
    # the first 9 letters represent the pattern of the top yellow face reading from left to right top to bottom
    # Y stands for yellow, X stands for any other colour
    ('OLL', 'XYYYYYXYXYXXYXXYXXXXX', 'R U2 R" U" R U" R"'),
    ('OLL', 'XYXYYYYYXXXXXXYXXYXXY', 'R U R" U R U2 R"'),
    ('OLL', 'XYXYYYXYXXXXYXYXXXYXY', 'R U2 R" U" R U R" U" R U" R"'),
    ('OLL', 'XYXYYYXYXYXYXXYXXXYXX', 'R U2" R2" U" R2 U" R2" U2" R'),
    ('OLL', 'XYYYYYXYYXXXYXXXXXXXY', 'r U R" U" r" F R F"'),
    ('OLL', 'YYXYYYXYYXXXYXXXXYXXX', 'x R" U R D" R" U" R D x"'),
    ('OLL', 'XYXYYYYYYXXXXXXXXXYXY', 'R2 D" R U2 R" D R U2 R'),
    
    ('OLL', 'XXYYYYXXYXXXYYXXXXXYY', 'R U R" U" R" F R F"'),
    ('OLL', 'XXYYYYXXYYXYXYXXXXXYX', 'F R U R" U" F"'),
    
    ('OLL', 'XXXXYYXYYXYYXXXXXYXYY', 'r" U2" R U R" U r'),
    ('OLL', 'XYYXYYXXXYYXYYXYXXXXX', 'r U2 R" U" R U" r"'),
    
    ('OLL', 'XXXYYYYXYYXXXYXXXYXYX', 'R U R2" U" R" F R U R U" F"'),
    ('OLL', 'YYXXYXYYXXYXXXXYYYXXX', 'R" U" R" F R F" U R'),
    
    ('OLL', 'YXXYYXXYYXXXYXXXYYXYX', 'y2 R U R" F" R U R" U" R" F R U" R" F R F"'),
    ('OLL', 'XYYYYXYXXXXXXYXYYXXXY', 'R U R" U R U" R" U" R" F R F"'),
    
    ('OLL', 'YYYYYXYXYXXXXYXXYXXXX', 'r U R" U" M U R U" R"'),
    ('OLL', 'YXYYYYYXYXXXXYXXXXXYX', 'R U R" U" M" U R U" r"'),
    
    ('OLL', 'XYYXYYXXYXYXYYXXXXXXY', 'R" U" F U R U" R" F" R'),
    ('OLL', 'XXYXYYXYYXYXYXXXXXXYY', 'R U B" U" R" U R B R"'),
    ('OLL', 'YXXYYXYYXXXXXXXYYYXYX', 'f" L" U" L U f'),
    ('OLL', 'XXYXYYXYYYYYXXXXXXXYX', 'f R U R" U" f"'),
    
    ('OLL', 'XXXYYYXXXYXYXYYXXXYYX', 'f R U R" U" R U R" U" f"'),
    ('OLL', 'XXXYYYXXXYXYXYXYXYXYX', 'r" U" r U" R" U R U" R" U R r" U r'),
    ('OLL', 'XYXXYXXYXXYXYXXYYYXXY', 'R U R" U R U" y R U" R" F"'),
    ('OLL', 'XYXXYXXYXYYYXXXYYYXXX', 'y R" F R U R U" R2" F" R2 U" R" U R U R"'),
    
    ('OLL', 'XYXYYXXXYYXXYYXXYXYXX', 'R U R" U" R" F R2 U R" U" F"'),
    ('OLL', 'XXYYYXXYXXXYXXYXYXXYY', 'R U R" U R" F R F" R U2" R"'),
    ('OLL', 'YXXXYYXYYXYXYXXXXYXYX', 'R U2" R2" F R F" R U2" R"'),
    ('OLL', 'YYXYYXXXYXXXYYXXYYXXX', 'F R U" R" U" R U R" F"'),
    
    ('OLL', 'XXXYYYYXXXXXXYYXXYXYY', 'F U R U" R2" F" R U R U" R"'),
    ('OLL', 'XXXYYYXXYYXXYYXXXXYYX', 'R" F R U R" F" R F U" F"'),
    ('OLL', 'XXYYYYXXXYXXYYXYXXXYX', 'r U r" R U R" U" r U" r"'),
    ('OLL', 'XXXYYYXXYXXYXYXXXYXYY', 'r" U" r R" U" R U r" U r'),
    
    ('OLL', 'YXYYYXXYXXXYXXXYYXXYX', 'y R U R" U" R U" R" F" U" F R U R"'),
    ('OLL', 'YYXXYYYXXXYXXYYXXXYXX', 'y" F U R U2 R" U" R U2 R" U" F"'),
    ('OLL', 'XYXYYXYXYXXXXYXXYXYXY', 'R U R" U R U2" R" F R U R" U" F"'),
    ('OLL', 'YXYYYXXYXXXXYXYXYXXYX', 'R" U" R U" R" U2 R F R U R" U" F"'),
    
    ('OLL', 'XYXYYXXXXYXYXYYXYXYXX', 'F R U R" U" R U R" U" F"'),
    ('OLL', 'XYXXYYXXXXYXYYXYXYXXY', 'F" L" U" L U L" U" L U F'),
    ('OLL', 'XYXXYYXXXYYYXYYXXXYXX', 'r U" r2" U r2 U r2" U" r'),
    ('OLL', 'XXXXYYXYXYYYXXYXXXYYX', 'r" U r2 U" r2" U" r2 U r"'),
    ('OLL', 'XXXXYYXYXYYYXXXYXYXYX', 'r" U" R U" R" U R U" R" U2 r'),
    ('OLL', 'XYXXYYXXXYYYXYXYXYXXX', 'r U R" U R U" R" U R U2" r"'),
    
    ('OLL', 'XYXYYXYXXXXXXYYXYYXXY', 'r U R" U R U2" r"'),
    ('OLL', 'YXXYYXXYXXXXYXXYYXYYX', 'r" U" R U" R" U2 r'),
    ('OLL', 'XXXXYYYYXXYXXXYXXYXYY', 'r" R2 U R" U R U2 R" U M"'),
    ('OLL', 'YYXXYYXXXXYXYYXYXXYXX', 'M" R" U" R U" R" U2 R U" M'),
    ('OLL', 'XXYYYYYXXXXXXYXYXXXYY', 'L F" L" U" L U F U" L"'),
    ('OLL', 'YXXYYYXXYXXYXYXXXXYYX', 'R" F R U R" U" F" U R'),
    
    ('OLL', 'XXXXYXXXXYYYXYXYYYXYX', 'R U2" R2" F R F" U2" R" F R F"'),
    ('OLL', 'XXXXYXXXXYYYXYYXYXYYX', 'F R U R" U" F" f R U R" U" f"'),
    ('OLL', 'XXXXYXXXYXYYXYXXYYXYY', 'f R U R" U" f" U" F R U R" U" F"'),
    ('OLL', 'XXYXYXXXXYYXYYXYYXXYX', 'f R U R" U" f" U" F R U R" U" F"'),
    ('OLL', 'YXYXYXXXXXYXYYYXYXXYX', 'r U R" U R U2 r" r" U" R U" R" U2 r'),
    ('OLL', 'YXYXYXXXXXYYXYXYYXXYX', 'M U R U R" U" M" R" F R F"'),
    ('OLL', 'YXXXYXXXYXYYXYXXYXYYX', 'R U R" U R" F R F" U2" R" F R F"'),
    ('OLL', 'YXYXYXYXYXYXXYXXYXXYX', 'M U R U R" U" M2" U R U" r"'),
]

pll_algorithms = [
    ('PLL', 'Ub Perm', 'R2 U R U R" U" R" U" R" U R"'),
    ('PLL', 'Ua Perm', 'R U" R U R U R U" R" U" R2'),
    ('PLL', 'H Perm', 'M2" U M2" U2 M2" U M2"'),
    ('PLL', 'Z Perm', 'M2" U M2" U M" U2 M2" U2 M" U2'),

    ('PLL', 'Aa Perm', 'x R" U R" D2 R U" R" D2 R2 x"'),
    ('PLL', 'Ab Perm', 'x R2" D2 R U R" D2 R U" R x"'),
    ('PLL', 'E Perm', 'x" R U" R" D R U R" D" R U R" D R U" R" D" x'),

    ('PLL', 'Ra Perm', 'R U" R" U" R U R D R" U" R D" R" U2 R" U"'),
    ('PLL', 'Rb Perm', 'R" U2 R U2" R" F R U R" U" R" F" R2 U"'),
    ('PLL', 'Ja Perm', 'R" U L" U2 R U" R" U2 R L U"'),
    ('PLL', 'Jb Perm', 'R U R" F" R U R" U" R" F R2 U" R" U"'),
    ('PLL', 'T Perm', 'R U R" U" R" F R2 U" R" U" R U R" F"'),
    ('PLL', 'F Perm', 'R" U" F" R U R" U" R" F R2 U" R" U" R U R" U R'),

    ('PLL', 'V Perm', 'R" U R" U" y R" F" R2 U" R" U R" F R F'),
    ('PLL', 'Y Perm', 'F R U" R" U" R U R" F" R U R" U" R" F R F"'),
    ('PLL', 'Na Perm', 'R U R" U R U R" F" R U R" U" R" F R2 U" R" U2 R U" R"'),
    ('PLL', 'Nb Perm', 'R" U R U" R" F" U" F R U R" F R" F" R U" R'),

    ('PLL', 'Ga Perm', 'R2 U R" U R" U" R U" R2 D U" R" U R D" U'),
    ('PLL', 'Gb Perm', 'y" D R" U" R U D" R2 U R" U R U" R U" R2" U"'),
    ('PLL', 'Gc Perm', 'R2 U" R U" R U R" U R2 D" U R U" R" D U"'),
    ('PLL', 'Gd Perm', 'D" R U R" U" D R2 U" R U" R" U R" U R2 U')
]

pll_mappings = {
    '131212323444': 'Ub Perm',
    '121232313444': 'Ua Perm',
    '141232323414': 'Z Perm',
    '131242313424': 'H Perm',
    
    '214123431341': 'E Perm',
    '122331243414': 'Aa Perm',
    '244112323431': 'Ab Perm',
    
    '131223412344': 'T Perm',
    '111243432324': 'F Perm',
    '441222334113': 'Ja Perm',
    '111233422344': 'Jb Perm',
    '141223432314': 'Ra Perm',
    '411232324143': 'Rb Perm',
    
    '311224143432': 'V Perm',
    '341224133412': 'Y Perm',
    '133422311244': 'Na Perm',
    '331224113442': 'Nb Perm',
    
    '141233412324': 'Ga Perm',
    '132311243424': 'Gb Perm',
    '121243412334': 'Gc Perm',
    '131213442324': 'Gd Perm'
    }

