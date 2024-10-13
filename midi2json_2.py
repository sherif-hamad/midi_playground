import mido
import json
import math

# A mapping from MIDI note durations to musical terms
duration_mapping = {
    480: "noire",         # Quarter note
    240: "croche",        # Eighth note
    120: "doubleCroche",  # Sixteenth note
}

def quantize_duration(ticks):
    # Quantize duration to the nearest standard duration in ticks
    closest_duration = min(duration_mapping.keys(), key=lambda x: abs(x - ticks))
    return closest_duration

def midi_to_json(midi_file, theme_name="Theme 1"):
    mid = mido.MidiFile(midi_file)
    events = []
    ticks_per_beat = mid.ticks_per_beat

    current_notes = []
    start_time = 0

    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                # Start of a note
                note_name = note_to_name(msg.note)
                current_notes.append(note_name)
                start_time += msg.time  # Accumulate the time for the current note's start

            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                # End of a note
                if current_notes:
                    # Quantize the duration based on the elapsed time
                    duration = quantize_duration(msg.time)

                    # Log the event with all current notes
                    events.append({
                        "notes": current_notes,  # All notes playing together
                        "duration": duration_mapping[duration],
                        "start_time": start_time
                    })
                    current_notes = []  # Clear the current notes after logging
                    start_time = 0  # Reset start_time for the next event

    # Final JSON structure
    result = [
        {
            "name": theme_name,
            "events": events
        }
    ]

    return json.dumps(result, indent=4)


def note_to_name(note_number):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = note_number // 12 - 1
    note = note_names[note_number % 12]
    return f"{note}{octave}"


# Example usage
midi_file_path = 'testtheme1.mid'
json_output = midi_to_json(midi_file_path)
print(json_output)
