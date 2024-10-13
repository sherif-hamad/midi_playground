import pygame.midi
import time
import json

# Initialize Pygame MIDI
pygame.midi.init()

# Print available MIDI output devices
print("Available MIDI output devices:")
for i in range(pygame.midi.get_count()):
    device_info = pygame.midi.get_device_info(i)
    name = device_info[1].decode()  # Device name
    is_output = device_info[3]  # Output device flag
    if is_output:
        print(f"Output Device {i}: {name}")

# Select Device 0: Microsoft MIDI Mapper (change as needed)
device_index = 0  # Change this to the desired device index
player = pygame.midi.Output(device_index)


# Define note duration function
def note_durations(tempo):
    beat_duration = 60 / tempo
    ronde = 4 * beat_duration  # Whole note
    blanche = 2 * beat_duration  # Half note
    noire = 1 * beat_duration  # Quarter note
    croche = 0.5 * beat_duration  # Eighth note
    doubleCroche = 0.25 * beat_duration  # Sixteenth note
    tripleCroche = 0.125 * beat_duration  # Thirty-second note

    return ronde, blanche, noire, croche, doubleCroche, tripleCroche


# Load themes from a JSON file
with open('theme_generated.json', 'r') as f:
    loaded_themes = json.load(f)


def play_theme(theme_name, note, third, fifth, octave, tempo):
    # Get the theme
    theme = next((t for t in loaded_themes if t["name"] == theme_name), None)
    if theme is None:
        print(f"Theme '{theme_name}' not found.")
        return

    ronde, blanche, noire, croche, doubleCroche, tripleCroche = note_durations(tempo)

    # Note mapping for variables
    note_mapping = {
        "note": note,
        "third": note + third,  # Add mapping for third
        "fifth": note + fifth,
        "octave": note + octave,
    }

    for event in theme["events"]:
        notes = [note_mapping[n] for n in event["notes"]]  # Map note names to MIDI values
        duration = eval(event["duration"])  # Get duration based on tempo
        velocity = event["velocity"]  # Get the velocity for this event

        # Play the notes
        for n in notes:
            player.note_on(n, velocity)

        time.sleep(duration)  # Hold the note for the specified duration

        # Turn off the notes after the duration
        for n in notes:
            player.note_off(n, velocity)


# Example values for note, minorThird, fifth, octave, and tempo
note = 60  # C
minorThird = 3  # Minor third interval (Eb)
majorThird = 4  # Major third interval (E)
fifth = 7  # Perfect fifth interval (G)
octave = 12  # Octave above
tempo = 120  # BPM

# Play the themes with the specified parameters
play_theme("Theme 1", note, minorThird, fifth, octave, tempo)
play_theme("Theme 1", note + 5, minorThird, fifth, octave, tempo)
play_theme("Theme 1", note - 2, majorThird, fifth, octave, tempo)
play_theme("Theme 1", note + 3, majorThird, fifth, octave, tempo)

# Close the player and quit Pygame MIDI
player.close()
pygame.midi.quit()
