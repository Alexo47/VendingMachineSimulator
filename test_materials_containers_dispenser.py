import unittest
from vending_machine_simulator import MaterialsContainersDispenser

material1 = 'coffee'
material2 = 'banana'
material1_capacity = 100
initial_volume = 0
material2_capacity = -1


class TestMaterialsContainersDispenser(unittest.TestCase):


    def test_get_capacity_material_container(self):
        dispenser = MaterialsContainersDispenser()
        self.assertTrue(dispenser.allocate_material_container(material1, material1_capacity))
        self.assertEqual(dispenser.get_capacity_material_container(material1), material1_capacity)
        self.assertEqual(dispenser.get_capacity_material_container(material2), material2_capacity)

    def test_refill_material_container(self):
        dispenser = MaterialsContainersDispenser()
        self.assertTrue(dispenser.allocate_material_container(material1, material1_capacity))
        self.assertEqual(dispenser.refill_material_container(material1), material1_capacity)
        self.assertEqual(dispenser.refill_material_container(material2), material2_capacity)

    def test_get_volume_material_container(self):
        dispenser = MaterialsContainersDispenser()
        self.assertTrue(dispenser.allocate_material_container(material1, material1_capacity))
        self.assertEqual(dispenser.get_volume_material_container(material1), initial_volume)
        self.assertEqual(dispenser.get_volume_material_container(material2), material2_capacity)
        self.assertEqual(dispenser.refill_material_container(material1), material1_capacity)
        self.assertEqual(dispenser.get_volume_material_container(material1), material1_capacity)


if __name__ == '__main__':
    unittest.main()