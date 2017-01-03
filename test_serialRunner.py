from unittest import TestCase

from run import SerialRunner, ParallelRunner

class TestSerialRunner(TestCase):
    def test_run_hama(self):
        runner = SerialRunner("HamadryasSim", 50, 5)
        output = runner.run()
        self.assertTrue(output)
        self.assertEqual(len(output), 5)

    def test_run_sav(self):
        runner = SerialRunner("SavannahSim", 50, 5)
        output = runner.run()
        self.assertTrue(output)
        self.assertEqual(len(output), 5)


class TestParallelRunner(TestCase):
    def test_run_hama(self):
        runner = ParallelRunner("HamadryasSim", 50, 5, 2)
        output = runner.run()
        self.assertTrue(output)
        self.assertEqual(len(output), 5)

    def test_run_sav(self):
        runner = ParallelRunner("SavannahSim", 50, 5, 2)
        output = runner.run()
        self.assertTrue(output)
        self.assertEqual(len(output), 5)
