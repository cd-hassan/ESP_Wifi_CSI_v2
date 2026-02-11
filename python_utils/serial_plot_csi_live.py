import argparse
import csv
import math
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import collections
from wait_timer import WaitTimer
from read_stdin import readline, print_until_first_csi_line


def parse_csi_line(line):
    if "CSI_DATA" not in line:
        return None

    parts = line.split(',')
    if len(parts) <= 25:
        return None

    raw = parts[25]
    start = raw.find('[')
    end = raw.rfind(']')
    if start != -1 and end != -1 and end > start:
        raw = raw[start + 1:end]

    csi_data = [int(x) for x in raw.split() if x]
    if not csi_data:
        return None

    imaginary = []
    real = []
    for i, val in enumerate(csi_data):
        if i % 2 == 0:
            imaginary.append(val)
        else:
            real.append(val)

    csi_size = len(csi_data)
    amplitudes = []
    if imaginary and real:
        for j in range(int(csi_size / 2)):
            amplitude_calc = math.sqrt(imaginary[j] ** 2 + real[j] ** 2)
            amplitudes.append(amplitude_calc)

    return amplitudes


class LogWriter:
    def __init__(self, log_dir, interval_sec):
        self.log_dir = log_dir
        self.interval_sec = interval_sec
        self.start_ts = None
        self.file = None
        self.writer = None

    def _open_new_file(self, now):
        if not self.log_dir:
            return

        os.makedirs(self.log_dir, exist_ok=True)
        self.start_ts = now
        stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime(now))
        file_path = os.path.join(self.log_dir, f"csi_log_{stamp}.csv")
        self.file = open(file_path, "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)
        self.writer.writerow([
            "timestamp",
            "mode",
            "subcarrier",
            "amplitude",
            "motion_score",
        ])

    def write(self, now, mode, subcarrier, amplitude, motion_score):
        if not self.log_dir:
            return

        if self.file is None or (now - self.start_ts) >= self.interval_sec:
            self.close()
            self._open_new_file(now)

        if self.writer:
            self.writer.writerow([now, mode, subcarrier, amplitude, motion_score])

    def close(self):
        if self.file:
            self.file.close()
            self.file = None
            self.writer = None


def render_plots(amp_window, subcarrier_window, motion_window, subcarrier, mode_label):
    df = np.asarray(amp_window, dtype=np.float32)
    if df.size == 0:
        return

    ax_amp.clear()
    ax_motion.clear()

    x_vals = range(len(subcarrier_window))
    ax_amp.plot(x_vals, subcarrier_window, color="r")
    ax_amp.set_ylabel("Amplitude")
    ax_amp.set_title(f"Amplitude plot of Subcarrier {subcarrier} ({mode_label})")

    ax_motion.plot(range(len(motion_window)), motion_window, color="b")
    ax_motion.set_xlabel("Time")
    ax_motion.set_ylabel("Motion score")

    fig.canvas.flush_events()
    plt.show()


def iter_lines_from_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        for raw in handle:
            line = raw.strip()
            if line:
                yield line


def main():
    parser = argparse.ArgumentParser(description="Plot ESP32 CSI data (live or replay).")
    parser.add_argument("--subcarrier", type=int, default=44, help="Subcarrier index to plot.")
    parser.add_argument("--max-points", type=int, default=200, help="Max points shown in plots.")
    parser.add_argument("--plot-interval", type=float, default=0.2, help="Seconds between plot updates.")
    parser.add_argument("--stats-interval", type=float, default=1.0, help="Seconds between stats prints.")
    parser.add_argument("--replay-file", type=str, default=None, help="Replay a CSV file instead of stdin.")
    parser.add_argument("--replay-interval", type=float, default=0.02, help="Seconds between replay lines.")
    parser.add_argument("--log-dir", type=str, default=None, help="Directory to write CSV logs.")
    parser.add_argument("--log-interval-min", type=float, default=10.0, help="Minutes per log file.")
    args = parser.parse_args()

    mode_label = "Replay" if args.replay_file else "Live"

    print_stats_wait_timer = WaitTimer(args.stats_interval)
    render_plot_wait_timer = WaitTimer(args.plot_interval)

    amp_window = collections.deque(maxlen=args.max_points)
    subcarrier_window = collections.deque(maxlen=args.max_points)
    motion_window = collections.deque(maxlen=args.max_points)

    packet_count = 0
    total_packet_counts = 0
    last_motion = 0.0

    log_writer = LogWriter(args.log_dir, args.log_interval_min * 60.0)

    if not args.replay_file:
        print_until_first_csi_line()
        line_source = (readline() for _ in iter(int, 1))
    else:
        line_source = iter_lines_from_file(args.replay_file)

    for line in line_source:
        amplitudes = parse_csi_line(line)
        if amplitudes is None:
            continue

        if args.subcarrier >= len(amplitudes):
            continue

        amp_window.append(amplitudes)
        subcarrier_amp = amplitudes[args.subcarrier]
        subcarrier_window.append(subcarrier_amp)

        if len(subcarrier_window) > 1:
            window_vals = np.asarray(subcarrier_window, dtype=np.float32)
            last_motion = float(np.std(window_vals))
        motion_window.append(last_motion)

        now = time.time()
        log_writer.write(now, mode_label, args.subcarrier, subcarrier_amp, last_motion)

        packet_count += 1
        total_packet_counts += 1

        if print_stats_wait_timer.check():
            print_stats_wait_timer.update()
            print("Packet Count:", packet_count, "per second.", "Total Count:", total_packet_counts)
            packet_count = 0

        if render_plot_wait_timer.check() and len(amp_window) > 2:
            render_plot_wait_timer.update()
            render_plots(amp_window, subcarrier_window, motion_window, args.subcarrier, mode_label)

        if args.replay_file:
            time.sleep(args.replay_interval)


if __name__ == "__main__":
    plt.ion()
    fig, (ax_amp, ax_motion) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    fig.canvas.draw()
    plt.show(block=False)
    main()
