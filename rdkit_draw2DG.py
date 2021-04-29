#!/usr/bin/env python
# coding: utf-8

# rdkit_draw2DG
# Vincent Scalfani
# Adapted from https://gist.github.com/greglandrum/431483ac1f9edb03b09c8577031c10e0
# BSD-3-Clause License
# Tested with RDKit v2020.09.2
# If RDKit is installed via conda, you will need to activate your env first

from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D
import argparse
import sys

parser = argparse.ArgumentParser(description="rdkit_draw2DG is a command line interface" 
         " that uses RDKit to draw molecules from input SMILES. The output creates a"
         " saved PNG file with the molecules displayed in a grid along with their name property."
         " See below for additional options such as SMARTS pattern highlighting."
         " Written by Vincent Scalfani")

parser.add_argument('smi', metavar="SMILES_INPUT", type=argparse.FileType('r'), help="input SMILES file; use '-' for stdin."
                    " The SMILES input file must contain a name column and no heading line. Required format is: SMILES in COL 0, name in COL 1."
                    " Additional data staring at COL 2 is accepted without warning, but COL 2,3,4...N are not used.")
parser.add_argument("-d", type=str, dest="DELIM", default="\t", help="specify DELIM as string, default: TAB")
parser.add_argument("-s", dest="SMARTS", type=str, default=None, help="optional SMARTS pattern to highlight,"
                    " enclose SMARTS in single quotes to preserve literal value in Bash, default: None")
parser.add_argument("-m", metavar="N", type=int, dest="maxMols", default=18, help="max number of molecules to draw, default: 18")
parser.add_argument("-o", type=str, dest="FILE", default="rdkit_drawing_2Dgrid.png", help="output file name, default: rdkit_drawing_2Dgrid.png")

def drawG():
    args = parser.parse_args()
    suppl = Chem.SmilesMolSupplier()
    smi_data = args.smi.read()
    suppl.SetData(smi_data, titleLine=False, delimiter=args.DELIM, nameColumn=1)
    smi_data = None # clears memory, see: https://www.mail-archive.com/rdkit-discuss@lists.sourceforge.net/msg01897.html

    mol_list = []
    for mol in suppl:
        if mol is not None: 
            mol_list.append(mol)
    
    mol_name_list = []
    for mol in suppl:
        if mol is not None: 
            mol_name_list.append(mol.GetProp('_Name'))
    
    if len(mol_list) > args.maxMols:
       mol_list = mol_list[0:args.maxMols]
       mol_name_list = mol_name_list[0:args.maxMols]

    if args.SMARTS is None:
        # draw molecules
        molsPerRow = 3
        nRows = len(mol_list)//molsPerRow
        if len(mol_list)%molsPerRow:
           nRows+=1
        panelx = 300
        panely = 300
        canvasx = panelx * molsPerRow
        canvasy = panely * nRows
        drawer = rdMolDraw2D.MolDraw2DCairo(canvasx,canvasy,panelx,panely)
        drawer.DrawMolecules(mol_list, legends=[mol_name for mol_name in mol_name_list])
        drawer.FinishDrawing()

        out_filename = args.FILE
        with open(out_filename,'wb') as out:
            out.write(drawer.GetDrawingText())

        print("saved drawing of " + str(len(mol_list)) + " molecules as " + str(out_filename))

    else:
       pattern = Chem.MolFromSmarts(args.SMARTS)
       hats = []
       hbnds = []
       for mol in mol_list:
           ats = mol.GetSubstructMatch(pattern)
           hats.append(ats)
           bnds = []
           for bnd in mol.GetBonds():
               if bnd.GetBeginAtomIdx() in ats and bnd.GetEndAtomIdx() in ats:
                   bnds.append(bnd.GetIdx())
           hbnds.append(bnds)

       molsPerRow = 3
       nRows = len(mol_list)//molsPerRow
       if len(mol_list)%molsPerRow:
           nRows+=1
       panelx = 300
       panely = 300
       canvasx = panelx * molsPerRow
       canvasy = panely * nRows
       drawer = rdMolDraw2D.MolDraw2DCairo(canvasx,canvasy,panelx,panely)
       drawer.DrawMolecules(mol_list,highlightAtoms=hats,highlightBonds=hbnds, legends=[mol_name for mol_name in mol_name_list])
       drawer.FinishDrawing()

       out_filename = args.FILE
       with open(out_filename,'wb') as out:
           out.write(drawer.GetDrawingText())

       print("saved drawing of " + str(len(mol_list)) + " molecules with SMARTS pattern highlight: " + args.SMARTS + " as " + str(out_filename))

if __name__=="__main__":
    drawG()
   
