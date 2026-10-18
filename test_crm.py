"""Tests for the crm.py module. Uses a temp file for the store."""
import json
import tempfile
import unittest
from pathlib import Path

import crm


class TestStore(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        self.tmp.close()
        self.path = Path(self.tmp.name)
        self.store = crm.Store(self.path)

    def tearDown(self):
        self.path.unlink(missing_ok=True)

    def _make(self, name="Test", phone="940-555-0001", **kw):
        return crm.Customer(
            id=crm.uuid.uuid4().hex if hasattr(crm, "uuid") else "fixed-id-1234",
            name=name, phone=phone,
            **{k: v for k, v in kw.items() if k in crm.Customer.__dataclass_fields__ and k not in ("id", "name", "phone")},
        )

    def test_add_and_find(self):
        # Workaround: generate a customer with explicit id
        c = crm.Customer(id="abc-123", name="Alice", phone="940-555-0001")
        self.store.add(c)
        self.store.save()
        s2 = crm.Store(self.path)
        self.assertEqual(len(s2.customers), 1)
        self.assertEqual(s2.find("abc-123").name, "Alice")

    def test_update_status(self):
        c = crm.Customer(id="id-001", name="Bob", phone="940-555-0002")
        self.store.add(c)
        updated = self.store.update("id-001", status="quoted", notes="sent estimate")
        self.assertEqual(updated.status, "quoted")
        self.assertEqual(updated.notes, "sent estimate")
        self.assertNotEqual(updated.updated_at, c.updated_at)

    def test_delete(self):
        c = crm.Customer(id="id-del", name="Del", phone="940-555-0003")
        self.store.add(c)
        self.assertTrue(self.store.delete("id-del"))
        self.assertIsNone(self.store.find("id-del"))

    def test_search(self):
        self.store.add(crm.Customer(id="a", name="Jane Doe", phone="940-555-0004", county="Palo Pinto"))
        self.store.add(crm.Customer(id="b", name="John Smith", phone="817-555-0005", county="Hood"))
        self.store.add(crm.Customer(id="c", name="Bob Jones", phone="940-555-0006", notes="call about perc test"))
        out = self.store.search("perc")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].id, "c")
        out2 = self.store.search("Doe")
        self.assertEqual(len(out2), 1)
        self.assertEqual(out2[0].id, "a")

    def test_filter(self):
        self.store.add(crm.Customer(id="a", name="A", phone="1", county="Palo Pinto", status="lead"))
        self.store.add(crm.Customer(id="b", name="B", phone="2", county="Hood", status="quoted"))
        self.store.add(crm.Customer(id="c", name="C", phone="3", county="Palo Pinto", status="quoted"))
        out = self.store.filter(county="Palo Pinto")
        self.assertEqual(len(out), 2)
        out2 = self.store.filter(status="quoted")
        self.assertEqual(len(out2), 2)
        out3 = self.store.filter(county="Palo Pinto", status="quoted")
        self.assertEqual(len(out3), 1)
        self.assertEqual(out3[0].id, "c")


class TestCLISmoke(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        self.tmp.close()
        self.path = Path(self.tmp.name)

    def tearDown(self):
        self.path.unlink(missing_ok=True)

    def test_add_then_list(self):
        crm.main(["--store", str(self.path), "add", "Test User", "940-555-0100", "--county", "Palo Pinto", "--service", "perc test"])
        crm.main(["--store", str(self.path), "list"])
        # store should have one entry
        s = crm.Store(self.path)
        self.assertEqual(len(s.customers), 1)
        self.assertEqual(s.customers[0].name, "Test User")
        self.assertEqual(s.customers[0].county, "Palo Pinto")

    def test_stats(self):
        crm.main(["--store", str(self.path), "add", "X", "1"])
        crm.main(["--store", str(self.path), "add", "Y", "2"])
        crm.main(["--store", str(self.path), "stats"])  # should not raise


if __name__ == "__main__":
    unittest.main()
