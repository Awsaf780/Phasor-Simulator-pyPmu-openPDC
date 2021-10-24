from synchrophasor.pmu import Pmu
from synchrophasor.frame import ConfigFrame2, DataFrame
import random

__author__ = "Edited: Awsaf Mahmood"


if __name__ == "__main__":

    pmu_id = 780
    data_rate = 30
    port = 8080
    ip = '127.0.0.1'
    method = 'tcp'
    buffer = 2048
    set_timestamps = True
    log_level = 'INFO'  # or use DEBUG

    ieee_cfg2_sample = ConfigFrame2(pmu_id,
                                    1000000,    # Time Base
                                    1,          # Number of PMUs included in data frame
                                    "NSU Station",  # Station Name
                                    port,           # Data Stream ID
                                    (False, False, True, False), # Data format - POLAR; PH - REAL; AN - REAL; FREQ - REAL;
                                    4,              # Number of Phasor
                                    3,              # Number of Analog Values
                                    1,              # Number of Digital Status Words

                                    ["VA", "VB", "VC", "I1", "ANALOG1", "ANALOG2", "ANALOG3",
                                     "BREAKER 1 STATUS", "BREAKER 2 STATUS", "BREAKER 3 STATUS",
                                     "BREAKER 4 STATUS", "BREAKER 5 STATUS", "BREAKER 6 STATUS",
                                     "BREAKER 7 STATUS", "BREAKER 8 STATUS", "BREAKER 9 STATUS",
                                     "BREAKER A STATUS", "BREAKER B STATUS", "BREAKER C STATUS",
                                     "BREAKER D STATUS", "BREAKER E STATUS", "BREAKER F STATUS",
                                     "BREAKER G STATUS"],    # Channel Names

                                    [(915527, "v"), (915527, "v"), (915527, "v"), (45776, "i")], # Conversion factor for phasor channels
                                    [(1, "pow"), (1, "rms"), (1, "peak")],                       # Conversion factor for analog channels
                                    [(0x0000, 0xffff)],                                          # Mask words for digital status words
                                    60,         # Nominal Frequency
                                    22,         # Configuration Change Count
                                    data_rate)  # Data Rate

    pmu = Pmu(pmu_id, data_rate, port, ip, method, buffer, set_timestamps)
    pmu.logger.setLevel(log_level)

    pmu.set_configuration(ieee_cfg2_sample)
    pmu.set_header()

    pmu.set_id(pmu_id)  # Override PMU ID set by set_configuration method.
    pmu.set_data_rate(data_rate)  # Override reporting DATA_RATE set by set_configuration method.

    pmu.run()  # PMU starts listening for incoming connections

    while True:
        if pmu.clients:  # Check if there is any connected PDCs
            ieee_data_sample = DataFrame(pmu_id, ("ok", True, "timestamp", False, False, False, 0, "<10", 0),
                                         [(random.randint(14635, 15635), 10), (-7318, -12676), (-7318, 12675), (1092, 0)], 2500, 0,
                                         [100, 1000, 10000], [0x3c12], ieee_cfg2_sample)

            pmu.send(ieee_data_sample)  # Sending sample data frame specified in IEEE C37.118.2 - Annex D (Table D.1)

    pmu.join()