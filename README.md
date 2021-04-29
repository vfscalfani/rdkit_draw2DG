# rdkit_draw2DG

`rdkit_draw2DG` is a very basic command line interface that uses [RDKit](https://www.rdkit.org/) to draw molecules from 
input SMILES in a 2D grid. I wrote it to learn how to use Python [argparse](https://docs.python.org/3/library/argparse.html), and to be 
able to quickly draw molecules from standard input (stdin) within a terminal session. `rdkit_draw2DG` uses the [rdkit.Chem.Draw.rdMolDraw2D](https://www.rdkit.org/docs/source/rdkit.Chem.Draw.rdMolDraw2D.html?highlight=rdmoldraw2d#module-rdkit.Chem.Draw.rdMolDraw2D) module and adapts code from this [Grid Highlighting gist](https://gist.github.com/greglandrum/431483ac1f9edb03b09c8577031c10e0). I tested `rdkit_draw2DG` with RDKit v2020.09.2.


## Help File

Access the help documention with `-h`:

```console

$ python3 rdkit_draw2DG.py -h
usage: rdkit_draw2DG.py [-h] [-d DELIM] [-s SMARTS] [-m N] [-o FILE]
                        SMILES_INPUT

rdkit_draw2DG is a command line interface that uses RDKit to draw molecules
from input SMILES. The output creates a saved PNG file with the molecules
displayed in a grid along with their name property. See below for additional
options such as SMARTS pattern highlighting. Written by Vincent Scalfani

positional arguments:
  SMILES_INPUT  input SMILES file; use '-' for stdin. The SMILES input file
                must contain a name column and no heading line. Required
                format is: SMILES in COL 0, name in COL 1. Additional data
                staring at COL 2 is accepted without warning, but COL
                2,3,4...N are not used.

optional arguments:
  -h, --help    show this help message and exit
  -d DELIM      specify DELIM as string, default: TAB
  -s SMARTS     optional SMARTS pattern to highlight, enclose SMARTS in single
                quotes to preserve literal value in Bash, default: None
  -m N          max number of molecules to draw, default: 18
  -o FILE       output file name, default: rdkit_drawing_2Dgrid.png

``` 

## Example 1

test_smiles.smi

```console
$ head test_smiles.smi
CC1CC=C(C=C1)C(=O)C2=CCC3=C(CC2N)C=CCC3	153201771	WKBCGMHOLSNYQO-UHFFFAOYSA-N	(6-amino-2,5,6,9-tetrahydro-1H-benzo[7]annulen-7-yl)-(4-methylcyclohexa-1,5-dien-1-yl)methanone
CC1CCC(C=C1)C(=O)C2=CCC(C=C2)N	147357860	DGQXCDQUWUWGER-UHFFFAOYSA-N	(4-aminocyclohexa-1,5-dien-1-yl)-(4-methylcyclohex-2-en-1-yl)methanone
C1CC(=CC=C1)C(=O)C2C=CC=CC2N	147140581	BSAKIRIALHJUQG-UHFFFAOYSA-N	(6-aminocyclohexa-2,4-dien-1-yl)-cyclohexa-1,3-dien-1-ylmethanone
CC1=C(C(CC=C1)(C)C)C(=O)CC(C)N	141222187	YZPPIOKXSCMFGS-UHFFFAOYSA-N	3-amino-1-(2,6,6-trimethylcyclohexa-1,3-dien-1-yl)butan-1-one
CCC(=O)C1=CC=CCC1N	135128895	GJWJWPHFPOYXLY-UHFFFAOYSA-N	1-(6-aminocyclohexa-1,3-dien-1-yl)propan-1-one
CCC(C1=CC(CCC1=O)(C)C)N	68984090	DGOHPZCFQGRGJK-UHFFFAOYSA-N	2-(1-aminopropyl)-4,4-dimethylcyclohex-2-en-1-one
CCC(C1=CC(CC(=C)C1=O)(C)C)N	68982992	XXDUHTYUKXBEBJ-UHFFFAOYSA-N	2-(1-aminopropyl)-4,4-dimethyl-6-methylidenecyclohex-2-en-1-one
CC(C1=CC(CCC1=O)(C)C)N	68982704	NTWUXJWZGQXMSM-UHFFFAOYSA-N	2-(1-aminoethyl)-4,4-dimethylcyclohex-2-en-1-one
CC(C1=CC(CC(=C)C1=O)(C)C)N	68982156	GRVVQHSYQPHJGH-UHFFFAOYSA-N	2-(1-aminoethyl)-4,4-dimethyl-6-methylidenecyclohex-2-en-1-one

```

Read the SMILES from standard in (stdin), draw first 6 molecules, and save file as example_draw2DG_01.png. 

```console

$ cat test_smiles.smi | python3 rdkit_draw2DG.py - -m6 -o example_draw2DG_01.png
saved drawing of 6 molecules as example_draw2DG_01.png

```

![example_draw2DG_01](/images/example_draw2DG_01.png)


## Example 2

Read the SMILES from standard in (stdin), draw first 6 molecules, highlight the substructure pattern matching 
SMARTS '[#7]-[#6]-[#6](=[#6])-[#6]=O' and save file as example_draw2DG_02.png. 

```console
$ cat test_smiles.smi | python3 rdkit_draw2DG.py - -m6 -s '[#7]-[#6]-[#6](=[#6])-[#6]=O' -o example_draw2DG_02.png
saved drawing of 6 molecules with SMARTS pattern highlight: [#7]-[#6]-[#6](=[#6])-[#6]=O as example_draw2DG_02.png

```

![example_draw2DG_02](/images/example_draw2DG_02.png)


## TODO

1. more testing
2. error handling for incorrect input
3. make the name and heading columns in SMILES file optional
4. make name labels in drawings optional and allow selection of a specific column for the labels
5. add option to align molecules by common template


