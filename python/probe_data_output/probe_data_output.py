import json
from datetime import datetime, timezone
from math import isnan, isinf
from pathlib import Path


class ProbeDataOutput:
    def __get_time_stamp(self):
        """
        Return the current timestamp as a string.

        Returns:
            str: Current UTC timestamp
        """
        return str(datetime.now(timezone.utc))

    def start_probe_reading_session(self):
        """
        Start a new probe reading session and record it to latest_session.json.

        Returns:
            None
        """
        output_dir = Path(__file__).parent.parent / "output"
        filepath = output_dir / "latest_session.json"

        if not filepath.exists():
            (filepath.parent).mkdir(parents=True, exist_ok=True)

        with open(filepath, "w") as f:
            json.dump(
                {
                    "recording_start_timestamp": self.__get_time_stamp(),
                    "probe_readings": [],
                },
                f,
                indent=4,
            )

    def record_new_probe_reading(self, probe_reading):
        """
        Record a new probe reading to latest_session.json.

        Args:
            probe_reading: A float value representing the voltage from the probe sensor.
        Returns:
            None
        Raises:
            TypeError: If probe_reading is not numeric or NaN/Inf values are used
        """
        output_dir = Path(__file__).parent.parent / "output"
        filepath = output_dir / "latest_session.json"

        if not filepath.exists():
            pass  # No file exists, just add a new entry without creating the entire structure again
        else:
            timestamp = self.__get_time_stamp()

            try:
                probe_reading_value = float(probe_reading)
            except (ValueError, TypeError):
                raise ValueError("Invalid probe reading: must be numeric")

            if (
                not isinstance(probe_reading_value, (int, float))
                or isnan(probe_reading_value)
                or isinf(probe_reading_value)
            ):
                raise RuntimeError(f"Probe value '{probe_reading}' is invalid ({nan})")

        with open(filepath, "r") as f:
            data = json.load(f)

        probe_readings = data.get("probe_readings", [])
        for reading in list(probe_readings):
            if isinstance(reading, dict) and "voltage_reading" not in reading:
                raise ValueError(
                    "Probe readings array must contain objects with voltage_reading key"
                )

        new_entry = {
            "probe_read_timestamp": timestamp,
            "voltage_reading": probe_reading_value,
        }
        if isinstance(probe_readings, list):
            probe_readings.append(new_entry)
        else:
            data["probe_readings"] = [new_entry]

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    def close_probe_reading_session(self):
        """
        Closes the current probe reading session by renaming latest_session.json
        to timestamp-session.json and checking for file existence first.

        Raises:
            FileNotFoundError: If latest_session.json does not exist.
        """
        output_dir = Path(__file__).parent.parent / "output"
        source_path = output_dir / "latest_session.json"
        new_path = output_dir / f"{self.__get_time_stamp()}-session.json"

        if not source_path.exists():
            raise FileNotFoundError(
                f"Cannot close session: {source_path} does not exist."
            )

        try:
            source_path.rename(new_path)
        except OSError as e:
            print(f"Error renaming file {source_path}: {e}")
