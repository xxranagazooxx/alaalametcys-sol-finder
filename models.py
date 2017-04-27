#!/usr/bin/env python
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('main.db')

SECTIONS = [
    ("C/P", "Chemical and Physical"),
    ("CARS", "Critical Analysis and Reasoning"),
    ("B/B", "Biology and Biochemistry"),
    ("P/S", "Psychology and Sociology")]

MODULES = [
    ("FL1", "Full Length 1"),
    ("FL2", "Full Length 2"),
    ("OG", "Original Guide"),
    ("Sample", "Unscored Sample"),
    ("QB", "Question Pack"),
    ("SB", "Section Bank")]

class BaseModel(Model):
    class Meta:
        database = db

class Module(BaseModel):
    name = CharField(unique=True)
    longname = CharField(unique=True)

    def __repr__(self):
        return "<module: %s>" % self.name

class Section(BaseModel):
    name = CharField(unique=True)
    longname = CharField(unique=True)

    def __repr__(self):
        return "<section: %s>" % self.name

class Solution(BaseModel):
    # Used for a particular solution
    #  module = SB/FL/QP/...
    #  section = CP/BB/PS/Cars...

    #TODO: use related_name fields
    #TODO: 1 Mod - Many Section
    #      1 Sec - Many Solutions
    module = ForeignKeyField(Module)
    section = ForeignKeyField(Section)

    num = IntegerField()
    #TODO: link should be unique
    link = CharField()
    title = CharField()
    snippet = CharField(null=True)

    #suspect_flag = #for hits that return but dont match filter
    suspect = BooleanField(default=False)

    #todo
    #search_image = if image found
    #snippet = preview
    #ranking

    def __repr__(self):
        return "<id: %d | q#: %d | mod: %s | sec: %s>" % \
            (self.id, self.num, self.module.name, self.section.name)

class DBRefresh(BaseModel):
    """
    this model to maintain history of updates to db
    """

    lastrun = DateField()
    section = ForeignKeyField(Section)
    module = ForeignKeyField(Module)

################################################################################
# Helpers
################################################################################

def setup_db():
    # init db
    db.connect()
    db.create_tables([Section, Module, Solution])

    # init sections
    for (s,l) in SECTIONS:
        Section.create(name=s, longname=l)

    # init modules
    for (s,l) in MODULES:
        Module.create(name=s, longname=l)

    # example Solutions
    #s = Solution.create(
    #    section=(Section.get(name="P/S")),
    #    module=(Module.get(name="FL1")),
    #    link="blegh.com",
    #    title="donk",
    #    abstract="kow")
    #s.save()
    db.close()

def add_solution(sname, mname, qnum, args):

    sname = sname.upper()
    mname = mname.upper()

    # get section model
    smodel = Section.get(Section.name.contains(sname)|
                Section.longname.contains(sname))

    mmodel = Module.get(Module.name.contains(mname)|
                Module.longname.contains(mname))

    s = Solution.create(
        section = smodel,
        module = mmodel,
        num = qnum,
        link = args.get('link'),
        title = args.get('title'),
        snippet = args.get('snippet'),
        suspect = args.get('suspect'))
    s.save()


def get_solution(module, section, num):

    #XXX: expects sanitized input

    module = module.upper()
    section = section.upper()

    ret = Solution\
        .select()\
        .join(Module, on=(Module.id==Solution.module_id))\
        .join(Section, on=(Section.id==Solution.section_id))\
        .where(Section.name.contains(section))\
        .where(Module.name==module)\
        .where(Solution.num==num)\
        .order_by(Solution.suspect).dicts()

    return list(ret)

def vote(sol_id, user_id, amt):

    #TODO: 
    # vote one per person
    # vote +1/-1

    raise NotImplementedError

