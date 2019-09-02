from collections import defaultdict
import glob

OMA_NAMES = [
    'Clagr3_prot', 'Usnflo1_prot', 'Xanpa2_prot',
    'umbilicaria_muehlenbergii2']

GO_FILES = {
    "Clagr3_prot": 'cladonia.annot',
    "umbilicaria_muehlenbergii2": "umbilicaria.annot",
    "Usnflo1_prot": "usnea.annot",
    "Xanpa2_prot": "xanthoria.annot"
    }

KO_FILES = {
    "Clagr3_prot": 'cladonia_grayi.csv',
    "umbilicaria_muehlenbergii2": "umbilicaria_muehlenbergii.csv",
    "Usnflo1_prot": "usnea_florida.csv",
    "Xanpa2_prot": "xanthoria_parietina.csv"
    }

PFAM_FILES = {
    "Clagr3_prot": 'cladonia_grayi.pfam',
    "umbilicaria_muehlenbergii2": "umbilicaria_muehlenbergii.pfam",
    "Usnflo1_prot": "usnea_florida.pfam",
    "Xanpa2_prot": "xanthoria_parietina.pfam"
    }

# READ PFAM annotations
pfam_annotations = {}
for species in OMA_NAMES:
    pfam_annotations[species] = defaultdict(list)
    for line in open("pfam/" + PFAM_FILES[species], 'r'):
        if not line.startswith("#"):
            la = line.strip().split()
            if len(la) == 15:
                pfam_annotations[species][la[0].strip()].append(
                    "{} ({})".format(la[6], la[5]))

# READ GO annotations

go_annotations = {}
for species in OMA_NAMES:
    go_annotations[species] = defaultdict(list)
    for line in open("go/" + GO_FILES[species], 'r'):
        if not line.startswith("#"):
            la = line.strip().split()
            if len(la) >= 2:
                identifier = la[0].split("|")[-1].strip()
                go_annotations[species][identifier].append(
                    "{}".format(la[1]))

# READ KO annotations

ko_annotations = {}
for species in OMA_NAMES:
    ko_annotations[species] = defaultdict(list)
    for line in open("kegg/" + KO_FILES[species], 'r'):
        if not line.startswith("#"):
            la = line.strip().split()
            if len(la) >= 2:
                identifier = la[0].split("|")[-1].strip()
                ko_annotations[species][identifier].append(
                    "{}".format(la[1]))

# ITERATE OVER HOGs
print('hog\tgo\tkegg\tpfam')
hogs = glob.glob('hogs/*.fa')
for hog in hogs:
    annotations = {
        'pfam': [],
        'kegg': [],
        'go': []}
    for line in open(hog, 'r'):
        if line.startswith(">"):
            la = line.strip().split("[")
            identifier = la[0].split("|")[-1].strip()
            identifier = identifier.replace(">", '')
            species = la[-1].replace("]", '')
            annotations['go'] += go_annotations[species][identifier]
            annotations['kegg'] += ko_annotations[species][identifier]
            annotations['pfam'] += pfam_annotations[species][identifier]

    print("{}\t{}\t{}\t{}".format(hog.split("/")[-1],
        ",".join(list(set(annotations['go']))),
        ",".join(list(set(annotations['kegg']))),
        ",".join(list(set(annotations['pfam'])))))
