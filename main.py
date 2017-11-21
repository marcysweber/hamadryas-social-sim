from run import SerialRunner, ParallelRunner
from formatter import Formatter
from saver import Saver


def run(simulation_name, file_name, recognition, attraction_strength, duration, codispersal=False):
    runner = ParallelRunner(simulation_name, duration, recognition,
                            attraction_strength, 100, 7, codispersal)
    output = runner.run()

    formatter = Formatter(output)
    for_out = formatter.format()

    saver = Saver(for_out, file_name)
    saver.save()


def main():
    #run("HamadryasSim", "hama_test100.csv", False, 0, 100)
    #run("HamadryasSim", "hama_test150.csv", False, 0, 150)
    #run("HamadryasSim", "hama_test200.csv", False, 0, 200)
    #run("HamadryasSim", "hama_test250.csv", False, 0, 250)
    #run("HamadryasSim", "hama_test300.csv", False, 0, 300)
    #run("HamadryasSim", "hama_test350.csv", False, 0, 350)
    #run("HamadryasSim", "hama_test400.csv", False, 0, 400)

    #run("HamadryasSim", "hama_out_no_recognition.csv", False, 0, 300)
    #run("HamadryasSim", "hama_out_attraction_2.csv", True, 2, 300)
    #run("HamadryasSim", "hama_out_attraction_10.csv", True, 10, 300)

    run("HamadryasSim", "hama_out_attraction_10_codisp.csv", True, 10, 300, True)

    #run("HamadryasSim", "hama_out_takeover_rates.csv", False, 0, 300)

if __name__ == "__main__":
    main()
