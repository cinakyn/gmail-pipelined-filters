import xml.etree.ElementTree as ET
import xml.dom.minidom
import copy
import io


class Clause(object):
    def __init__(self, text):
        self.is_reverse = False
        self.text = text

    def reverse(self):
        c = Clause(self.text)
        c.is_reverse = not self.is_reverse
        return c

    def __str__(self):
        if self.is_reverse:
            return "-" + self.text
        return self.text


AND = -1
OR = 1


class Operation(object):
    def __init__(self, op, children):
        self.op = copy.deepcopy(op)
        self.children = copy.deepcopy(children)

    def reverse(self):
        o = Operation(-self.op, self.children)
        for i in range(len(o.children)):
            o.children[i] = o.children[i].reverse()
        return o

    def __str__(self):
        output = map(lambda x: str(x), self.children)
        if self.op == AND:
            output = " AND ".join(output)
        else:
            output = " OR ".join(output)
        return "({})".format(output)


class Option(object):
    def __init__(self, apply_label=True, skip_inbox=False):
        self.apply_label = apply_label
        self.skip_inbox = skip_inbox


class Filter(object):
    def __init__(self, name, clause, option=None):
        self.name = name
        self.clause = copy.deepcopy(clause)
        if option == None:
            self.option = Option()
        else:
            self.option = copy.deepcopy(option)

    def exclude(self, prev_filters):
        cs = [self.clause]
        cs.extend(map(lambda x: x.clause.reverse(), prev_filters))
        return Filter(self.name, Operation(AND, cs), self.option)

    def __str__(self):
        return str(self.clause)

    def debug(self):
        return "{} -- {}".format(self.name, str(self.clause))

    def entries(self):
        out = []
        # self first
        root = ET.Element("entry")
        ET.SubElement(root, "category", term="filter")
        ET.SubElement(root, "title").text = "Mail Filters"
        ET.SubElement(root, "content")
        ET.SubElement(root, "apps:property", name="hasTheWord", value=str(self))
        if self.option.apply_label:
            ET.SubElement(root, "apps:property", name="label", value=self.name)
        if self.option.skip_inbox:
            ET.SubElement(root, "apps:property", name="shouldArchive", value="true")
        ET.SubElement(root, "apps:property", name="sizeOperator", value="s_sl")
        ET.SubElement(root, "apps:property", name="sizeUnit", value="s_smb")
        out.append(root)
        return out


class Pipeline(object):
    def __init__(self, filters):
        self.filters = filters

    def save(self, fname):
        entries = []
        for i, f in enumerate(self.filters):
            f = f.exclude(self.filters[:i])
            entries.extend(f.entries())
            print(f.debug())
            print()
        o = io.StringIO()
        o.write("<?xml version='1.0' encoding='UTF-8'?><feed xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'><title>Mail Filters</title>")
        for e in entries:
            o.write(ET.tostring(e, encoding="unicode"))
        o.write("</feed>")
        o.seek(0)
        dom = xml.dom.minidom.parse(o)
        with open(fname, "w") as f:
            f.write(dom.toprettyxml())
        print("done. go gmail and export {}.".format(fname))

