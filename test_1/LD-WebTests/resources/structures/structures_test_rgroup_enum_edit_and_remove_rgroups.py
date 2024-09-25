ONE_THREE_SUSTITUTED_CYCLOHEXANE_SCAFFOLD = "\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 8 8 2 0 0\nM  V30 BEGIN ATOM\nM  V30 1 C -3.477107 -1.171429 0.000000 0\nM  V30 2 C -2.239927 -0.457143 0.000000 0\nM  V30 3 C -2.239927 0.971429 0.000000 0\nM  V30 4 C -3.477107 1.685714 0.000000 0\nM  V30 5 C -4.714286 0.971429 0.000000 0\nM  V30 6 C -4.714286 -0.457143 0.000000 0\nM  V30 7 R# -5.951465 -1.171429 0.000000 101 MASS=1 RGROUPS=(1 1)\nM  V30 8 R# -3.477107 3.114286 0.000000 102 MASS=2 RGROUPS=(1 2)\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 2 3\nM  V30 3 1 3 4\nM  V30 4 1 4 5\nM  V30 5 1 5 6\nM  V30 6 1 6 1\nM  V30 7 1 6 7\nM  V30 8 1 4 8\nM  V30 END BOND\nM  V30 BEGIN SGROUP\nM  V30 1 DAT 0 ATOMS=(1 7) FIELDDISP=\"    0.0000    0.0000    DR    ALL  0 0\" -\nM  V30 QUERYTYPE=SMARTSQ QUERYOP== FIELDDATA=\"[*:101]\"\nM  V30 2 DAT 0 ATOMS=(1 8) FIELDDISP=\"    0.0000    0.0000    DR    ALL  0 0\" -\nM  V30 QUERYTYPE=SMARTSQ QUERYOP== FIELDDATA=\"[*:102]\"\nM  V30 END SGROUP\nM  V30 END CTAB\nM  END\n$$$$\n"

RGROUP_A_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 2 1 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 C -0.500000 0.000000 0.000000 0\nM  V30 2 C 0.500000 0.000000 0.000000 0 ATTCHPT=1\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n>  <_CXSMILES_Data>  \n|$;;_AP1$|\n\n$$$$\n'

RGROUP_B_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 1 0 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 Cl 0.000000 0.000000 0.000000 0 ATTCHPT=1\nM  V30 END ATOM\nM  V30 END CTAB\nM  END\n>  <_CXSMILES_Data>  \n|$;_AP1$,lp:0:3|\n\n$$$$\n'

EDITED_RGROUP_B_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 1 0 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 F 0.000000 0.000000 0.000000 0 ATTCHPT=1\nM  V30 END ATOM\nM  V30 END CTAB\nM  END\n>  <_CXSMILES_Data>  \n*F |$_AP1;$|\n\n$$$$\n'

EDITED_RGROUP_A_FOR_ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SCAFFOLD = '\n     RDKit          2D\n\n  0  0  0  0  0  0  0  0  0  0999 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 3 2 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 C -0.475714 0.476286 0.000000 0\nM  V30 2 C 0.760857 -0.239143 0.000000 0 ATTCHPT=1\nM  V30 3 C -1.713429 -0.237143 0.000000 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 1 1 2\nM  V30 2 1 1 3\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n>  <_CXSMILES_Data>  \n*CCC |$_AP1;;;$|\n\n$$$$\n'

ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SMILES_LIST = ['CCC1CCCC(F)C1', 'CCCC1CCCC(CC)C1', 'CCCC1CCCC(Cl)C1', 'FC1CCCC(Cl)C1']

ONE_THREE_SUBSTITUTED_CYCLOHEXANE_SMILES_LIST_REMOVE_RGROUP = ['CCC1CCCC(CC)C1', 'CCC1CCCC(Cl)C1']
