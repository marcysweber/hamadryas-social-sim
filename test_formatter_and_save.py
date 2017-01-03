from unittest import TestCase
from run import SerialRunner
from formatter import Formatter
from saver import Saver


class TestFormatter(TestCase):
    def test_run_hama(self):
        runner = SerialRunner("HamadryasSim", 50, 2)
        output = runner.run()

        formatter = Formatter(output)
        for_out = formatter.format()

        self.assertTrue(for_out)
        self.assertEqual(len(output) + 1, len(for_out))

    def test_run_sav(self):
        runner = SerialRunner("SavannahSim", 50, 2)
        output = runner.run()

        formatter = Formatter(output)
        for_out = formatter.format()

        self.assertTrue(for_out)
        self.assertEqual(len(output) + 1, len(for_out))

    def test_save_hama(self):
        runner = SerialRunner("HamadryasSim", 50, 2)
        output = runner.run()

        formatter = Formatter(output)
        for_out = formatter.format()

        self.assertTrue(for_out)
        self.assertEqual(len(output) + 1, len(for_out))

        saver = Saver(for_out, "hamatest.csv")
        saver.save()

        open_file = open("hamatest.csv").read()
        self.assertTrue(open_file)

    def test_save_sav(self):
        runner = SerialRunner("SavannahSim", 50, 2)
        output = runner.run()

        formatter = Formatter(output)
        for_out = formatter.format()

        self.assertTrue(for_out)
        self.assertEqual(len(output) + 1, len(for_out))

        saver = Saver(for_out, "savtest.csv")
        saver.save()

        open_file = open("savtest.csv").read()
        self.assertTrue(open_file)
