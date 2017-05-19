
from functools import reduce
from itertools import ifilter
FAKE_DB = {
    1: {"asset_name": "fred", "department":"model", "subcontext":"hi", "snapshot_type":"maya_model", "version":1, "level":None},
    2: {"asset_name": "fred", "department":"model", "subcontext":"md", "snapshot_type":"maya_model", "version":1, "level":None},
    3: {"asset_name": "fred", "department":"model", "subcontext":"lo", "snapshot_type":"maya_model", "version":1, "level":None},
    4: {"asset_name": "chicken", "department":"model", "subcontext":"hi", "snapshot_type":"maya_model", "version":1, "level":None},
    5: {"asset_name": "chicken", "department":"model", "subcontext":"md", "snapshot_type":"maya_model", "version":1, "level":None},
    6: {"asset_name": "chicken", "department":"model", "subcontext":"lo", "snapshot_type":"maya_model", "version":1, "level":None},
    7: {"asset_name": "robot", "department":"model", "subcontext":"hi", "snapshot_type":"maya_model", "version":1, "level":None},
    8: {"asset_name": "robot", "department":"model", "subcontext":"md", "snapshot_type":"maya_model", "version":1, "level":None},
    9: {"asset_name": "robot", "department":"model", "subcontext":"lo", "snapshot_type":"maya_model", "version":1, "level":None},
    10: {"asset_name": "fred", "department":"model", "subcontext":"hi", "snapshot_type":"maya_model", "version":2, "level":None},
}

class AssetManager(object):
    fakeDb = FAKE_DB
    def __init__(self):
        self._current = 1

    def __iter__(self):
        return self

    def next(self):
        if self._current > len(self.fakeDb):
            self._current = 1
            raise StopIteration
        
        idx = self._current
        self._current +=1 
        return (idx, self.fakeDb.get(idx))

    @classmethod
    def dbSize(cls):
        return len(cls.getDb())
    
    @classmethod
    def getDb(cls):
        return cls.fakeDb
    
    @classmethod
    def nextId(cls):
        return reduce( lambda x, y: x if x>y else y, cls.fakeDb.iterkeys()) + 1
    
    @classmethod
    def fromSnapshotId(cls,snapshot_id):
        sn = cls.fakeDb.get(snapshot_id,None)
        if sn is None:
            return None
        return Snapshot(snapshot_id,**sn)

    @classmethod
    def getLatestFromSnapshot(cls, sn):
     
        def inStack( sn2):
            sn2 = Snapshot(sn2[0],**sn2[1])
            if sn.asset_name == sn2.asset_name and \
               sn.department == sn2.department and \
               sn.subcontext == sn2.subcontext and \
               sn.snapshot_type == sn2.snapshot_type and \
               sn.level == sn2.level:
                return True
            return False
        try:
            latest = reduce( lambda x, y:  x if x[1].get("version") > y[1].get("version") else y, ifilter(inStack, cls.fakeDb.iteritems()))
        except TypeError:
            return None
        return Snapshot(latest[0],**latest[1])
        
    @classmethod
    def getLatestFromSnapshotId(cls, snapshot_id):
        sn = cls.fromSnapshotId(snapshot_id)
        if sn is None:
            return None
        return cls.getLatestFromSnapshot(sn)
    
class Snapshot(object):
    fakeDb = FAKE_DB
    def __init__(self, snapshot_id, asset_name, department, subcontext, snapshot_type, version, level):
        self._snapshot_id = snapshot_id
        self._asset_name = asset_name
        self._department = department
        self._subcontext = subcontext
        self._snapshot_type = snapshot_type
        self._version = version
        self._level = level

    
    @property
    def snapshot_id(self):
        return self._snapshot_id

    @property
    def asset_name(self):
        return self._asset_name

    @property
    def department(self):
        return self._department

    @property
    def subcontext(self):
        return self._subcontext

    @property
    def snapshot_type(self):
        return self._snapshot_type

    @property
    def version(self):
        return self._version

    @property
    def level(self):
        return self._level

    def getDict(self):
        return {
            "snapshot_id": self.snapshot_id,
            "asset_name":self.asset_name,
            "department": self.department,
            "subcontext": self.subcontext,
            "snapshot_type": self.snapshot_type,
            "version": self.version,
            "level": self.level
            }

    @property
    def context(self):
        return "%s/%s/%s" % (self.department, self.subcontext, self.snapshot_type)
    
    def __repr__(self):
        return "<Snapshot id: %d asset_name: %s context: %s/%s/%s version: %d level: %s>" %(self.snapshot_id, self.asset_name, self.department, self.subcontext, self.snapshot_type, self.version, self.level)
    
    @classmethod
    def fromSnapshotId(cls,snapshot_id):
        sn = cls.fakeDb.get(snapshot_id,None)
        if sn is None:
            return None
        return Snapshot(snapshot_id,**sn)


class Element(object):
    def __init__(self, snapshot):
        self._snapshot = snapshot
        self._mutations = {}

    @property
    def snapshot_id(self):
        return self._snapshot.snapshot_id

    @property
    def asset_name(self):
        return self._mutations.get("asset_name", self._snapshot.asset_name)

    @asset_name.setter
    def asset_name(self, value):
        self._mutations["asset_name"] = value
                
    @property
    def department(self):
        return self._mutations.get("department", self._snapshot.department)

    @department.setter
    def department(self, value):
        self._mutations["department"] = value
        
    @property
    def subcontext(self):
        return self._mutations.get("subcontext", self._snapshot.subcontext)

    @subcontext.setter
    def subcontext(self, value):
        self._mutations["subcontext"] = value
        
    @property
    def snapshot_type(self):
        return self._mutations.get("snapshot_type", self._snapshot.snapshot_type)

    @snapshot_type.setter
    def snapshot_type(self, value):
        self._mutations["snapshot_type"] = value
        
    @property
    def version(self):
        return self._mutations.get("version", self._snapshot.version)

    
    @property
    def level(self):
        return self._mutations.get("level", self._snapshot.level)

    @level.setter
    def level(self, value):
        self._mutations["level"] = value
        
    @property
    def context(self):
        return "%s/%s/%s" % (self.department, self.subcontext, self.snapshot_type)

    def __repr__(self):
        return "<Element id: %d asset_name: %s context: %s/%s/%s version: %d level: %s>" %(self.snapshot_id, self.asset_name, self.department, self.subcontext, self.snapshot_type, self.version, self.level)

    @property 
    def orig(self):
        return self._snapshot

    @property 
    def dirty(self):
        return len(self._mutations) > 0


class Manager(object):
    
    def __init__(self):
        self._elements=[]
        self._current = 0
        
    def getDb(self):
        return AssetManager.fakeDb
    
    def add(self, element):
        self._elements.append(element)

    def fromSnapshotId(self, snapshot_id):
        for e in self._elements:
            if e.snapshot_id == snapshot_id:
                return e

        snap = AssetManager.fromSnapshotId(snapshot_id)
        if snap is None:
            raiseRuntimeError("unable to get snapshot with id %d", snapshot_id)
        e = Element(snap)
        if e is None:
            raise RuntimeError("unable to add snapshot with id %d" % snapshot_id)
        self.add(e)
        return e

    
    def __iter__(self):
        return self

    def next(self):
        if self._current == len(self._elements):
            self._current = 0
            raise StopIteration
        idx = self._current
        self._current +=1 
        return self._elements[idx]
        
    def update(self):
        errors = []
        for e in self._elements:
            if e.dirty:
               latest_snap = AssetManager.getLatestFromSnapshot(e)
               next_version = latest_snap.version + 1 if latest_snap is not None else 1
        
               next_id = AssetManager.nextId()
               new_snap = Snapshot(next_id, e.asset_name, e.department, e.subcontext, e.snapshot_type, next_version, e.level)
               dct = new_snap.getDict()
               dct.pop('snapshot_id',None)
               AssetManager.getDb()[next_id] = dct 
               
               e._snapshot = new_snap
               
               
        if len(errors) > 0:
            raise RuntimeError("Problems updating %s" % errors)

if __name__ == "__main__":
    import unittest

    class TestAssetManager(unittest.TestCase):
        def setUp(self):
            self.am = AssetManager()
            
        def test_fromSnapshotId(self):
            sn = self.am.fromSnapshotId(1)
            self.assertTrue(isinstance(sn,Snapshot))
            self.assertTrue(sn.snapshot_id == 1)

        def test_fromSnapshotIdOutOfBounds(self):
            self.assertTrue(self.am.fromSnapshotId(11) == None)
            
        def test_nextId(self):
            self.assertTrue(self.am.nextId() == 11)

        def test_getLatest(self):
            latest = self.am.getLatestFromSnapshotId(1)
            self.assertTrue(latest.version == 2)

            
    class TestElement(unittest.TestCase):
        
        def setUp(self):
            self.m = Manager()
            
        def test_update(self):
            e = self.m.fromSnapshotId(1)
            e.asset_name="funnyBunny"
            e.snapshot_type = "bunnyhaha"
            self.assertTrue(len(e._mutations) == 2 )
            self.assertTrue(e.asset_name == "funnyBunny")
            self.assertTrue(e.snapshot_type == "bunnyhaha")

            
    class TestManager(unittest.TestCase):
        def setUp(self):
            self.m = Manager()
            
        def test_fromSnapshotId(self):
            e = self.m.fromSnapshotId(1)
            self.assertTrue(e.snapshot_id == 1)
            self.assertTrue(isinstance(e,Element))

        def test_dirty(self):
            e = self.m.fromSnapshotId(1)
            e.asset_name="funnyBunny"
            self.assertTrue(e.dirty)
            
        def test_update(self):
            e = self.m.fromSnapshotId(1)
            e.asset_name="funnyBunny"
            e.snapshot_type = "bunnyhaha"
            self.m.update()
            self.assertTrue(e.snapshot_id == 11)
            self.assertTrue(AssetManager().dbSize() == 11)
                        
    unittest.main()
    # print "testing"
    # am = AssetManager()
    # m = Manager()
    
    
    # e = m.fromSnapshotId(1)
    # e.asset_name= "gary"
    # e.subcontext = "md"

    # print "managed elements:"
    # for x in m: print x

    # print "updating"
    
    # m.update()
    # print "updated...elements:"
    # for x in m: print x

    # print "asset managed data"
    # for x inin am: print x
    
