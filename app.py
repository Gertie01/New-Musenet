import gradio as gr
import random
import os
from generator import MidiComposer

composer = MidiComposer()

def generate_track(style_prompt):
    # Randomization logic as per requirements
    bpm = random.randint(75, 160)
    grid = random.choice(["1/3", "1/4", "1/6"])
    time_sig = random.choice(["4/4", "3/4"])
    duration_seconds = random.randint(30, 240)
    
    # Key signatures
    keys = ["C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"]
    modes = ["Major", "Minor"]
    key_sig = f"{random.choice(keys)} {random.choice(modes)}"

    # Select 10 random instruments (excluding drums)
    # General MIDI 0-127
    available_instruments = list(range(0, 128))
    selected_instruments = random.sample(available_instruments, 10)
    
    result_path = composer.generate(
        prompt=style_prompt,
        bpm=bpm,
        grid=grid,
        time_sig=time_sig,
        key_sig=key_sig,
        instruments=selected_instruments,
        duration=duration_seconds
    )
    
    info_text = f"Generated with:\nBPM: {bpm}\nGrid: {grid}\nTime Signature: {time_sig}\nKey: {key_sig}\nDuration: {duration_seconds}s"
    return result_path, info_text

with gr.Blocks(title="Harmonic MIDI Composer") as demo:
    gr.Markdown("# 🎵 SkyTNT MIDI Composer")
    gr.Markdown("Compose harmonious tracks with 10 random instruments, drums, and randomized parameters.")
    
    with gr.Row():
        style_input = gr.Textbox(label="Song Style Prompt", placeholder="e.g. Uplifting cinematic orchestral, Jazz fusion, Lo-fi chill hop...")
    
    generate_btn = gr.Button("Generate Random Track", variant="primary")
    
    with gr.Row():
        output_midi = gr.File(label="Download MIDI")
        output_info = gr.Textbox(label="Track Parameters", interactive=False)

    generate_btn.click(
        fn=generate_track,
        inputs=[style_input],
        outputs=[output_midi, output_info]
    )

if __name__ == '__main__':
    demo.launch()