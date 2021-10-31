from synchrophasor.pmu import Pmu
from synchrophasor.frame import ConfigFrame2, DataFrame
import random

__author__ = "Edited: Awsaf Mahmood"


if __name__ == "__main__":

    pmu_id = 780
    data_rate = 30
    port = 9000
    ip = '127.0.0.1'
    method = 'tcp'
    buffer = 2048
    set_timestamps = True
    log_level = 'INFO'  # or use DEBUG

    ieee_cfg2_sample = ConfigFrame2(pmu_id,
                                    1000000,  # Time Base
                                    1,  # Number of PMUs included in data frame
                                    "NSU Station",  # Station Name
                                    port,  # Data Stream ID
                                    (False, False, True, False),
                                    # Data format - POLAR; PH - REAL; AN - REAL; FREQ - REAL;
                                    6,  # Number of Phasor
                                    6,  # Number of Analog Values
                                    1,  # Number of Digital Status Words

                                    ["VA", "VB", "VC", "I1", "I2", "I3",

                                     "ANALOG1", "ANALOG2", "ANALOG3", "ANALOG4", "ANALOG5", "ANALOG6",
                                     "BREAKER 1 STATUS", "BREAKER 2 STATUS", "BREAKER 3 STATUS",
                                     "BREAKER 4 STATUS", "BREAKER 5 STATUS", "BREAKER 6 STATUS",
                                     "BREAKER 7 STATUS", "BREAKER 8 STATUS", "BREAKER 9 STATUS",

                                     "BREAKER A STATUS", "BREAKER B STATUS", "BREAKER C STATUS",
                                     "BREAKER D STATUS", "BREAKER E STATUS", "BREAKER F STATUS",
                                     "BREAKER G STATUS"],  # Channel Names

                                    [(915527, "v"), (915527, "v"), (915527, "v"), (45876, "i"), (45776, "i"),
                                     (45776, "i")],  # Conversion factor for phasor channels
                                    [(1, "pow"), (1, "rms"), (1, "peak"), (1, "pow"), (1, "rms"), (1, "peak")],
                                    # Conversion factor for analog channels
                                    [(0x0000, 0xffff)],  # Mask words for digital status words
                                    50,  # Nominal Frequency
                                    1,  # Configuration Change Count
                                    data_rate)  # Data Rate

    ieee_data_sample = DataFrame(pmu_id, ("ok", True, "timestamp", False, False, False, 0, "<10", 0),
                                 [(random.randint(14435, 14445), random.randint(10, 15)),
                                  (random.randint(7918, 7928), -12176),
                                  (random.randint(9618, 9628), 12165),
                                  (random.randint(1092, 1292), 5),
                                  (random.randint(1092, 1292), 5),
                                  (random.randint(1092, 1292), 9)],

                                 2500, 0,
                                 [100, 1000, 10000, 100, 1000, 10000],
                                 [0x3c12],
                                 ieee_cfg2_sample)

    print(ieee_cfg2_sample.get_ph_units())
    values_list = ieee_data_sample.get_phasors()

    for value in values_list:
        print(value)

    print(ieee_data_sample)