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
    ('OLL', 'YXYYYYYXYXXXXYXXXXXYX', 'R U R" U" L R" x U R U" L" x"'),
    
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
    ('OLL', 'XYXXYYXXXYYYXYYXXXYXX', 'L x U" L2 x2 U L2 x2 U L2 x2 U" L x'),
    ('OLL', 'XXXXYYXYXYYYXXYXXXYYX', 'L" x" U L2 x2 U" L2 x2 U" L2 x2 U L" x"'),
    ('OLL', 'XXXXYYXYXYYYXXXYXYXYX', 'L" x" U" R U" R" U R U" R" U2 L x'),
    ('OLL', 'XYXXYYXXXYYYXYXYXYXXX', 'L x U R" U R U" R" U R U2" L" x"'),
    
    ('OLL', 'XYXYYXYXXXXXXYYXYYXXY', 'L x U R" U R U2" L" x"'),
    ('OLL', 'YXXYYXXYXXXXYXXYYXYYX', 'L" x" U" R U" R" U2 L x'),
    ('OLL', 'XXXXYYYYXXYXXXYXXYXYY', 'L" x" R2 U R" U R U2 R" U L R" x'),
    ('OLL', 'YYXXYYXXXXYXYYXYXXYXX', 'L R" x R" U" R U" R" U2 R U" M'),
    ('OLL', 'XXYYYYYXXXXXXYXYXXXYY', 'L F" L" U" L U F U" L"'),
    ('OLL', 'YXXYYYXXYXXYXYXXXXYYX', 'R" F R U R" U" F" U R'),
    
    ('OLL', 'XXXXYXXXXYYYXYXYYYXYX', 'R U2" R2" F R F" U2" R" F R F"'),
    ('OLL', 'XXXXYXXXXYYYXYYXYXYYX', 'F R U R" U" F" B z R U R" U" B" z"'),
    ('OLL', 'XXXXYXXXYXYYXYXXYYXYY', 'B z R U R" U" B" z" U" F R U R" U" F"'),
    ('OLL', 'XXYXYXXXXYYXYYXYYXXYX', 'B z R U R" U" B" z" U" F R U R" U" F"'),
    ('OLL', 'YXYXYXXXXXYXYYYXYXXYX', 'L x U R" U R U2 L" x" L" x" U" R U" R" U2 L x'),
    ('OLL', 'YXYXYXXXXXYYXYXYYXXYX', 'M U R U R" U" L R" x R" F R F"'),
    ('OLL', 'YXXXYXXXYXYYXYXXYXYYX', 'R U R" U R" F R F" U2" R" F R F"'),
    ('OLL', 'YXYXYXYXYXYXXYXXYXXYX', 'M U R U R" U" M2" U R U" L" x"'),
]

pll_algorithms = [
    ('PLL', 'Ub Perm', 'R2 U R U R" U" R" U" R" U R"'),
    ('PLL', 'Ua Perm', 'R U" R U R U R U" R" U" R2'),
    ('PLL', 'H Perm', 'M2" U M2" U2 M2" U M2"'),
    ('PLL', 'Z Perm', 'M2" U M2" U L R" x U2 M2" U2 L R" x U2'),

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