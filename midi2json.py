import mido
import json

# Define a root note in MIDI (e.g., C4 is 60)
ROOT_NOTE = 60  # This will always be treated as "C"

# A mapping from MIDI note durations to musical terms
duration_mapping = {
    480: "noire",         # Quarter note
    240: "croche",        # Eighth note
    120: "doubleCroche",  # Sixteenth note
}

# Define intervals relative to the root
interval_mapping = {
    0: "note",         # Root
    3: "minor third",  # Minor third
    4: "major third",  # Major third
    7: "fifth",        # Perfect fifth
    10: "minor seventh", # Minor seventh
    11: "major seventh"  # Major seventh
}

def quantize_duration(time, ticks_per_beat):
    # Quantize to the nearest duration based on the ticks_per_beat
    possible_durations = list(duration_mapping.keys())
    quantized_duration = min(possible_durations, key=lambda x: abs(x - time))
    return duration_mapping.get(quantized_duration, "unknown")

def get_interval(note):
    # Calculate the interval relative to the root note (C)
    interval = (note - ROOT_NOTE) % 12
    return interval_mapping.get(interval, f"other interval ({interval})")

def midi_to_json(midi_file, theme_name="Theme 1"):
    mid = mido.MidiFile(midi_file)
    events = []
    ticks_per_beat = mid.ticks_per_beat  # MIDI file's ticks per beat (resolution)

    for track in mid.tracks:

        for msg in track:
            if msg.type == 'note_off' and msg.velocity > 0 and msg.time>0:
                # Get the interval relative to the root note
                interval_name = get_interval(msg.note)

                # Quantize the duration
                duration = quantize_duration(msg.time, ticks_per_beat)

                # Adding the event to the output list
                events.append({
                    "notes": [interval_name],  # Now based on relative intervals
                    "duration": duration,
                    "velocity": msg.velocity
                })

    # Final JSON structure
    result = [
        {
            "name": theme_name,
            "events": events
        }
    ]

    return json.dumps(result, indent=4)


# Example usage
midi_file_path = 'testtheme1.mid'
json_output = midi_to_json(midi_file_path)
print(json_output)
