# Probe Reading Output Structure

This is what the output structure for a probe recording session looks like.

```JSON
{
    "recording_start_timestamp":"1781646609",
    "probe_readings":[
        {
            "probe_read_timestamp":"1781646609",
            "voltage_reading":2.2
        },
        {
            "probe_read_timestamp":"1781646609",
            "voltage_reading":1.7
        },
    ]
}
```

"recording_start_timestamp" is when the probe recording starts a new session.
"probe_read_timestamp" is when the probe recieves another voltage reading.
"voltage_reading" is the read voltage value from the probe.

A session is the probe program recording, moving, and stopping when reaching the maximum spindle length.
