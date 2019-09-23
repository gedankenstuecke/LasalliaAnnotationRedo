from goatools.obo_parser import GODag

obodag = GODag("go-basic.obo")

for i,line in enumerate(open('new_annotations.csv')):
    if i > 0:
        la = line.split("\t")
        gos = la[1].split(',')
        print(la[0])
        outline = []
        for go in gos:
            if go.startswith("GO:"):
                outline.append("{} ({})".format(
                    obodag.get(go).name,
                    go))
        print(",".join(outline))
