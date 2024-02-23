import unittest
from vending_machine_simulator import MaterialsContainersDispenser

mat1 = 'coffee'
mat2 = 'macchiatto'
mat1_capacity = 50
mat1_drink_volume = 30
initial_volume = 0

mat2_capacity = -1


class TestMaterialsContainersDispenser(unittest.TestCase):

    def setUp(self) -> None:
        self.dispenser = MaterialsContainersDispenser()

    def test_get_capacity_material_container(self):
        self.assertTrue(self.dispenser.allocate_material_container(mat1, mat1_capacity))
        self.assertEqual(self.dispenser.get_capacity_material_container(mat1), mat1_capacity)
        self.assertEqual(self.dispenser.get_capacity_material_container(mat2), mat2_capacity)

    def test_refill_material_container(self):
        self.assertTrue(self.dispenser.allocate_material_container(mat1, mat1_capacity))
        self.assertEqual(self.dispenser.refill_material_container(mat1), mat1_capacity)
        self.assertEqual(self.dispenser.refill_material_container(mat2), mat2_capacity)

    def test_get_volume_material_container(self):
        self.assertTrue(self.dispenser.allocate_material_container(mat1, mat1_capacity))
        self.assertEqual(self.dispenser.get_volume_material_container(mat1), initial_volume)
        self.assertEqual(self.dispenser.get_volume_material_container(mat2), mat2_capacity)
        self.assertEqual(self.dispenser.refill_material_container(mat1), mat1_capacity)
        self.assertEqual(self.dispenser.get_volume_material_container(mat1), mat1_capacity)

    def test_dispense_material_container(self):
        self.assertTrue(self.dispenser.allocate_material_container(mat1, mat1_capacity))
        self.assertEqual(self.dispenser.get_volume_material_container(mat1), initial_volume)
        self.assertEqual(self.dispenser.refill_material_container(mat1), mat1_capacity)
        self.assertEqual(self.dispenser.get_volume_material_container(mat1), mat1_capacity)
        self.assertTrue(self.dispenser.takeout_material_container(mat1, mat1_drink_volume))
        self.assertFalse(self.dispenser.takeout_material_container(mat1, mat1_drink_volume))

if __name__ == '__main__':
    unittest.main()