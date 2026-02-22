'''
foL x solving f2l, the program will only look at 3 faces, the faces at index 0 2 and 3. so the states oB z the faces will be converted into a string such that the p[rogfrma will e able to convert any oB z group oB z 3 faceas andB z compare ifb that state can be solcved with an algorithm, iB z not then localised A* will be used until a state is found that can be solved
the first 9 characters will be the state oB z the face at index 2, 2nd 9 characters will be the state at face index 3 and last 9 face index 5.
the numbers foL x the key oB z this dictionary represent the centeL x face colouL x relative to the way the cube has been rotated around the y-axis
-> the format is:
    face index, face coordindta (x,y), target colouL x based from the 3 faces
    this will repeat 3 times in total foL x faces index 2 3 and 5
'''
'''
foL x identifying the f2l state, the string will be in the form corneL x edgeL x where the first halB z the string will contain information about the corneL x and the second halB z about the edge
    it will be so that the first characteL x is the face index, second characteL x the face coordinate (x,y) and this will be done foL x all the stickers
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

    ('F2L', 'CorneL x in Place 1', 'R" F" R U R U" R" F'),
    ('F2L', 'CorneL x in Place 2', 'U R U" R" U" F" U F'),
    ('F2L', 'CorneL x in Place 3', 'R U" R" U R U" R"'),
    ('F2L', 'CorneL x in Place 4', 'y" R" U R U" R" U R'),
    ('F2L', 'CorneL x in Place 5', 'R" F R F" U R U" R"'),
    ('F2L', 'CorneL x in Place 6', 'R U R" U" R U R"'),

    ('F2L', 'Edge in Place 1', 'U" R" F R F" R U" R"'),
    ('F2L', 'Edge in Place 2', 'U R U" R" U R U" R" U R U" R"'),
    ('F2L', 'Edge in Place 3', 'U" R U" R" U2 R U" R"'),
    ('F2L', 'Edge in Place 4', 'U R U R" U2 R U R"'),
    ('F2L', 'Edge in Place 5', 'U" R U R" U y" R" U" R'),
    ('F2L', 'Edge in Place 6', 'U F" U" F U" R U R"'),

    ('F2L', 'Edge and CorneL x 1', 'R U" R" d R" U2 R U2" R" U R'),
    ('F2L', 'Edge and CorneL x 2', 'R U R" U" R U2 R" U" R U R"'),
    ('F2L', 'Edge and CorneL x 3', 'R U" R" U R U2" R" U R U" R"'),
    ('F2L', 'Edge and CorneL x 4', 'R U" R" F R U R" U" F" R U" R"'),
    ('F2L', 'Edge and CorneL x 5', 'R U R" U" R U" R" U2 y" R" U" R')
]

'''
oll_algorithms = [
    # the first 9 letters represent the pattern oB z the top yellow face reading from left to right top to bottom
    # Y stands foL x yellow, X stands foL x any otheL x colour
    ('OLL', 'XYYYYYXYXYXXYXXYXXXXX', 'R U2 R" U" R U" R"'),
    ('OLL', 'XYXYYYYYXXXXXXYXXYXXY', 'R U R" U R U2 R"'),
    ('OLL', 'XYXYYYXYXXXXYXYXXXYXY', 'R U2 R" U" R U R" U" R U" R"'),
    ('OLL', 'XYXYYYXYXYXYXXYXXXYXX', 'R U2" R2" U" R2 U" R2" U2" R'),
    ('OLL', 'XYYYYYXYYXXXYXXXXXXXY', 'L x U R" U" L" x" F R F"'),
    ('OLL', 'YYXYYYXYYXXXYXXXXYXXX', 'x R" U R D" R" U" R D x"'),
    ('OLL', 'XYXYYYYYYXXXXXXXXXYXY', 'R2 D" R U2 R" D R U2 R'),
    
    ('OLL', 'XXYYYYXXYXXXYYXXXXXYY', 'R U R" U" R" F R F"'),
    ('OLL', 'XXYYYYXXYYXYXYXXXXXYX', 'F R U R" U" F"'),
    
    ('OLL', 'XXXXYYXYYXYYXXXXXYXYY', 'L" x" U2" R U R" U L x'),
    ('OLL', 'XYYXYYXXXYYXYYXYXXXXX', 'L x U2 R" U" R U" L" x"'),
    
    ('OLL', 'XXXYYYYXYYXXXYXXXYXYX', 'R U R2" U" R" F R U R U" F"'),
    ('OLL', 'YYXXYXYYXXYXXXXYYYXXX', 'R" U" R" F R F" U R'),
    
    ('OLL', 'YXXYYXXYYXXXYXXXYYXYX', 'y2 R U R" F" R U R" U" R" F R U" R" F R F"'),
    ('OLL', 'XYYYYXYXXXXXXYXYYXXXY', 'R U R" U R U" R" U" R" F R F"'),
    
    ('OLL', 'YYYYYXYXYXXXXYXXYXXXX', 'L x U R" U" M U R U" R"'),
    ('OLL', 'YXYYYYYXYXXXXYXXXXXYX', 'R U R" U" M" U R U" L" x"'),
    
    ('OLL', 'XYYXYYXXYXYXYYXXXXXXY', 'R" U" R" F R F" U R'),
    ('OLL', 'XXYXYYXYYXYXYXXXXXXYY', 'R U B" U" R" U R B R"'),
    ('OLL', 'YXXYYXYYXXXXXXXYYYXYX', 'B" z" L" U" L U f'),
    ('OLL', 'XXYXYYXYYYYYXXXXXXXYX', 'B z R U R" U" F"'),
    
    ('OLL', 'XXXYYYXXXYXYXYYXXXYYX', 'B z R U R" U" R U R" U" B" z"'),
    ('OLL', 'XXXYYYXXXYXYXYXYXYXYX', 'L" x" U" L x U" R" U R U" R" U R L" x" U L x'),
    ('OLL', 'XYXXYXXYXXYXYXXYYYXXY', 'y R U R" U" R U" R" F" U" F R U R"'),
    ('OLL', 'XYXXYXXYXYYYXXXYYYXXX', 'y R" F R U R U" R2" F" R2 U" R" U R U R"'),
    
    ('OLL', 'XYXYYXXXYYXXYYXXYXYXX', 'R U R" U" R" F R2 U R" U" F"'),
    ('OLL', 'XXYYYXXYXXXYXXYXYXXYY', 'R U R" U R" F R F" R U2" R"'),
    ('OLL', 'YXXXYYXYYXYXYXXXXYXYX', 'R U2" R2" F R F" R U2" R"'),
    ('OLL', 'YYXYYXXXYXXXYYXXYYXXX', 'F R U" R" U" R U R" F"'),
    
    ('OLL', 'XXXYYYYXXXXXXYYXXYXYY', 'F U R U" R2" F" R U R U" R"'),
    ('OLL', 'XXXYYYXXYYXXYYXXXXYYX', 'y" F U R U2 R" U" R U2 R" U" F"'),
    ('OLL', 'XXYYYYXXXYXXYYXYXXXYX', 'L x U L" x" R U R" U" L x U" L" x"'),
    ('OLL', 'XXXYYYXXYXXYXYXXXYXYY', 'L" x" U" L x R" U" R U L" x" U L x'),
    
    ('OLL', 'YXYYYXXYXXXYXXXYYXXYX', 'y R U R" U" R U" R" F" U" F R U R"'),
    ('OLL', 'YYXXYYYXXXYXXYYXXXYXX', 'y" F U R U2 R" U" R U2 R" U" F"'),
    ('OLL', 'XYXYYXYXYXXXXYXXYXYXY', 'R U R" U R U2" R" F R U R" U" F"'),
    ('OLL', 'YXYYYXXYXXXXYXYXYXXYX', 'R" U" R U" R" U2 R F R U R" U" F"'),
    
    ('OLL', 'XYXYYXXXXYXYXYYXYXYXX', 'F R U R" U" R U R" U" F"'),
    ('OLL', 'XYXXYYXXXXYXYYXYXYXXY', 'F" L" U" L U L" U" L U F'),
    ('OLL', 'XYXXYYXXXYYYXYYXXXYXX', 'L x U" r2" U r2 U r2" U" L x'),
    ('OLL', 'XXXXYYXYXYYYXXYXXXYYX', 'L" x" U r2 U" r2" U" r2 U L" x"'),
    ('OLL', 'XXXXYYXYXYYYXXXYXYXYX', 'L" x" U" R U" R" U R U" R" U2 L x'),
    ('OLL', 'XYXXYYXXXYYYXYXYXYXXX', 'L x U R" U R U" R" U R U2" L" x"'),
    
    ('OLL', 'XYXYYXYXXXXXXYYXYYXXY', 'L x U R" U R U2" L" x"'),
    ('OLL', 'YXXYYXXYXXXXYXXYYXYYX', 'L" x" U" R U" R" U2 L x'),
    ('OLL', 'XXXXYYYYXXYXXXYXXYXYY', 'L" x" R2 U R" U R U2 R" U M"'),
    ('OLL', 'YYXXYYXXXXYXYYXYXXYXX', 'M" R" U" R U" R" U2 R U" M'),
    ('OLL', 'XXYYYYYXXXXXXYXYXXXYY', 'L F" L" U" L U" F U" L"'),
    ('OLL', 'YXXYYYXYYXXYXYXXXXYYX', 'R" F R U R" U" F" U R'),
    
    ('OLL', 'XXXXYXXXXYYYXYXYYYXYX', 'R U2" R2" F R F" U2" R" F R F"'),
    ('OLL', 'XXXXYXXXXYYYXYYXYXYYX', 'F R U R" U" F" B z R U R" U" B" z"'),
    ('OLL', 'XXXXYXXXYXYYXYXXYYXYY', 'B z R U R" U" B" z" U" F R U R" U" F"'),
    ('OLL', 'XXYXYXXXXYYXYYXYYXXYX', 'B z R U R" U" B" z" U F R U R" U" F"'),
    ('OLL', 'YXYXYXXXXXYXYYYXYXXYX', 'L x U R" U R U2 L" x" L" x" U" R U" R" U2 L x'),
    ('OLL', 'YXYXYXXXXXYYXYXYYXXYX', 'M U R U R" U" M" R" F R F"'),
    ('OLL', 'YXXXYXXXYXYYXYXXYXYYX', 'R U R" U R" F R F" U2" R" F R F"'),
    ('OLL', 'YXYXYXYXYXYXXYXXYXXYX', 'M U R U R" U" M2" U R U" L" x"'),
]
'''

'''

r = L x

'''
oll_algorithms = [
    # the first 9 letters represent the pattern oB z the top yellow face reading from left to right top to bottom
    # Y stands foL x yellow, X stands foL x any otheL x colour
    ('OLL', 'XYYYYYXYXYXXYXXYXXXXX', 'R U2 R" U" R U" R"'),
    ('OLL', 'XYXYYYYYXXXXXXYXXYXXY', 'R U R" U R U2 R"'),
    ('OLL', 'XYXYYYXYXXXXYXYXXXYXY', 'R U2 R" U" R U R" U" R U" R"'),
    ('OLL', 'XYXYYYXYXYXYXXYXXXYXX', 'R U2" R2" U" R2 U" R2" U2" R'),
    ('OLL', 'XYYYYYXYYXXXYXXXXXXXY', 'L x U R" U" L" x"F R F"'), # 'L x U R" U" L" x" F R F"'
    ('OLL', 'YYXYYYXYYXXXYXXXXYXXX', 'x R" U R D" R" U" R D x"'),
    ('OLL', 'XYXYYYYYYXXXXXXXXXYXY', 'R2 D" R U2 R" D R U2 R'),
    
    ('OLL', 'XXYYYYXXYXXXYYXXXXXYY', 'R U R" U" R" F R F"'),
    ('OLL', 'XXYYYYXXYYXYXYXXXXXYX', 'F R U R" U" F"'),
    
    ('OLL', 'XXXXYYXYYXYYXXXXXYXYY', 'L" x" U2" R U R" U L x'),
    ('OLL', 'XYYXYYXXXYYXYYXYXXXXX', 'L x U2 R" U" R U" L" x"'),
    
    ('OLL', 'XXXYYYYXYYXXXYXXXYXYX', 'R U R2" U" R" F R U R U" F"'),
    ('OLL', 'YYXXYXYYXXYXXXXYYYXXX', 'R" U" R" F R F" U R'),
    
    ('OLL', 'YXXYYXXYYXXXYXXXYYXYX', 'y2 R U R" F" R U R" U" R" F R U" R" F R F"'),
    ('OLL', 'XYYYYXYXXXXXXYXYYXXXY', 'R U R" U R U" R" U" R" F R F"'),
    
    ('OLL', 'YYYYYXYXYXXXXYXXYXXXX', 'L x U R" U" M U R U" R"'),
    ('OLL', 'YXYYYYYXYXXXXYXXXXXYX', 'R U R" U" M" U R U" L" x"'),
    
    ('OLL', 'XYYXYYXXYXYXYYXXXXXXY', 'R" U" F U R U" R" F" R'),
    ('OLL', 'XXYXYYXYYXYXYXXXXXXYY', 'R U B" U" R" U R B R"'),
    ('OLL', 'YXXYYXYYXXXXXXXYYYXYX', 'B" z" L" U" L U f'),
    ('OLL', 'XXYXYYXYYYYYXXXXXXXYX', 'B z R U R" U" B" z"'),
    
    ('OLL', 'XXXYYYXXXYXYXYYXXXYYX', 'B z R U R" U" R U R" U" B" z"'),
    ('OLL', 'XXXYYYXXXYXYXYXYXYXYX', 'L" x" U" L x U" R" U R U" R" U R L" x" U L x'),
    ('OLL', 'XYXXYXXYXXYXYXXYYYXXY', 'R U R" U R U" y R U" R" F"'),
    ('OLL', 'XYXXYXXYXYYYXXXYYYXXX', 'y R" F R U R U" R2" F" R2 U" R" U R U R"'),
    
    ('OLL', 'XYXYYXXXYYXXYYXXYXYXX', 'R U R" U" R" F R2 U R" U" F"'),
    ('OLL', 'XXYYYXXYXXXYXXYXYXXYY', 'R U R" U R" F R F" R U2" R"'),
    ('OLL', 'YXXXYYXYYXYXYXXXXYXYX', 'R U2" R2" F R F" R U2" R"'),
    ('OLL', 'YYXYYXXXYXXXYYXXYYXXX', 'F R U" R" U" R U R" F"'),
    
    ('OLL', 'XXXYYYYXXXXXXYYXXYXYY', 'F U R U" R2" F" R U R U" R"'),
    ('OLL', 'XXXYYYXXYYXXYYXXXXYYX', 'R" F R U R" F" R F U" F"'),
    ('OLL', 'XXYYYYXXXYXXYYXYXXXYX', 'L x U L" x" R U R" U" L x U" L" x"'),
    ('OLL', 'XXXYYYXXYXXYXYXXXYXYY', 'L" x" U" L x R" U" R U L" x" U L x'),
    
    ('OLL', 'YXYYYXXYXXXYXXXYYXXYX', 'y R U R" U" R U" R" F" U" F R U R"'),
    ('OLL', 'YYXXYYYXXXYXXYYXXXYXX', 'y" F U R U2 R" U" R U2 R" U" F"'),
    ('OLL', 'XYXYYXYXYXXXXYXXYXYXY', 'R U R" U R U2" R" F R U R" U" F"'),
    ('OLL', 'YXYYYXXYXXXXYXYXYXXYX', 'R" U" R U" R" U2 R F R U R" U" F"'),
    
    ('OLL', 'XYXYYXXXXYXYXYYXYXYXX', 'F R U R" U" R U R" U" F"'),
    ('OLL', 'XYXXYYXXXXYXYYXYXYXXY', 'F" L" U" L U L" U" L U F'),
    ('OLL', 'XYXXYYXXXYYYXYYXXXYXX', 'L x U" r2" U r2 U r2" U" L x'),
    ('OLL', 'XXXXYYXYXYYYXXYXXXYYX', 'L" x" U r2 U" r2" U" r2 U L" x"'),
    ('OLL', 'XXXXYYXYXYYYXXXYXYXYX', 'L" x" U" R U" R" U R U" R" U2 L x'),
    ('OLL', 'XYXXYYXXXYYYXYXYXYXXX', 'L x U R" U R U" R" U R U2" L" x"'),
    
    ('OLL', 'XYXYYXYXXXXXXYYXYYXXY', 'L x U R" U R U2" L" x"'),
    ('OLL', 'YXXYYXXYXXXXYXXYYXYYX', 'L" x" U" R U" R" U2 L x'),
    ('OLL', 'XXXXYYYYXXYXXXYXXYXYY', 'L" x" R2 U R" U R U2 R" U M"'),
    ('OLL', 'YYXXYYXXXXYXYYXYXXYXX', 'M" R" U" R U" R" U2 R U" M'),
    ('OLL', 'XXYYYYYXXXXXXYXYXXXYY', 'L F" L" U" L U F U" L"'),
    ('OLL', 'YXXYYYXXYXXYXYXXXXYYX', 'R" F R U R" U" F" U R'),
    
    ('OLL', 'XXXXYXXXXYYYXYXYYYXYX', 'R U2" R2" F R F" U2" R" F R F"'),
    ('OLL', 'XXXXYXXXXYYYXYYXYXYYX', 'F R U R" U" F" B z R U R" U" B" z"'),
    ('OLL', 'XXXXYXXXYXYYXYXXYYXYY', 'B z R U R" U" B" z" U" F R U R" U" F"'),
    ('OLL', 'XXYXYXXXXYYXYYXYYXXYX', 'B z R U R" U" B" z" U" F R U R" U" F"'),
    ('OLL', 'YXYXYXXXXXYXYYYXYXXYX', 'L x U R" U R U2 L" x" L" x" U" R U" R" U2 L x'),
    ('OLL', 'YXYXYXXXXXYYXYXYYXXYX', 'M U R U R" U" M" R" F R F"'),
    ('OLL', 'YXXXYXXXYXYYXYXXYXYYX', 'R U R" U R" F R F" U2" R" F R F"'),
    ('OLL', 'YXYXYXYXYXYXXYXXYXXYX', 'M U R U R" U" M2" U R U" L" x"'),
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

