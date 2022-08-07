import math
import time
from datetime import datetime

import epics
import matplotlib.pyplot as plt
import pandas as pd
from IPython import display


class PvMonitor:
    def __init__(
        self,
        pv_list: List[str],
        interval: float = 0.0,
        time_window: float = 20.0,
        sample_callback: Callable = None,
    ):
        """
        PVMonitor class for coninuously monitoring a list of PVs.
        :param pv_list: list of PVs to monitor
        :param interval: time between samples (seconds)
        :param time_window: time window for plotting (seconds)
        :param sample_callback: function to call to get additional data to add to the sample
        """
        self.pv_list = pv_list

        self.data = pd.DataFrame()
        self.interval = interval
        self.dump_file = dump_file
        self.time_window = time_window
        self.sample_callback = sample_callback

    def run(self):
        n_cols = 5
        n_rows = math.ceil(len(self.pv_list) / n_cols)
        fig, ax = plt.subplots(n_rows, n_cols)
        fig.set_size_inches(n_cols * 4, n_rows * 4)
        fig.tight_layout()

        while 1:
            try:
                self.sample()
                self.plot(fig, ax)
                time.sleep(self.interval)
            except KeyboardInterrupt:
                break

    def plot(self, fig, axes):
        display.clear_output(wait=True)
        try:
            start_time = (
                time.time() - self.time_window
            )  # self.data["time"].to_numpy()[-1] - self.time_window
        except KeyError:
            start_time = 0

        for i, name in enumerate(self.pv_list):
            ax = axes.flatten()[i]
            ax.clear()
            self.data[self.data["time"] > time.time() - self.time_window].set_index(
                "datetime"
            ).plot(y=name, ax=ax, style="+")

        fig.tight_layout()
        display.display(fig)

    def sample(self):
        new_data = dict(zip(self.pv_list, epics.caget_many(self.pv_list)))
        new_data["time"] = time.time()

        if self.sample_callback is not None:
            new_data = dict(**new_data, **self.sample_callback())

        new_data["datetime"] = pd.to_datetime(new_data["time"], unit="s")
        print(pd.DataFrame(new_data, index=[0]))

        self.data = pd.concat(
            (self.data, pd.DataFrame(new_data, index=[0])), ignore_index=True
        )
