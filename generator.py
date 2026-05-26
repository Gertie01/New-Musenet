import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import miditoolkit
import random
import numpy as np
import time

class MidiComposer:
    def __init__(self, model_id="SkyTNT/midi-model"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id).to(self.device)

    def generate(self, prompt, bpm, grid, time_sig, key_sig, instruments, duration):
        # Construct the control prompt for the model
        # The SkyTNT model uses specific tokens for metadata
        instr_str = ", ".join([str(i) for i in instruments])
        full_prompt = f"STYLE={prompt} BPM={bpm} GRID={grid} TIME_SIG={time_sig} KEY={key_sig} INSTRUMENTS=[{instr_str}, DRUMS] "
        
        input_ids = self.tokenizer.encode(full_prompt, return_tensors="pt").to(self.device)
        
        # Calculate approximate token length based on duration (very heuristic)
        # 1 second ~ 20-30 tokens depending on complexity
        max_len = min(4096, input_ids.shape[1] + (duration * 25))
        
        with torch.no_grad():
            output_tokens = self.model.generate(
                input_ids,
                max_length=max_len,
                temperature=0.95,
                top_p=0.92,
                do_sample=True,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        generated_text = self.tokenizer.decode(output_tokens[0], skip_special_tokens=False)
        
        # Save to file
        filename = f"generated_track_{int(time.time())}.mid"
        self._tokens_to_midi(generated_text, filename, bpm)
        return filename

    def _tokens_to_midi(self, tokens, output_path, bpm):
        # This is a simplified placeholder for the model's specific midi decoding logic
        # Usually involves parsing tokens like 'note:60:120' or 'wait:10'
        # Since the actual SkyTNT model has a specific midi_model.utils, we'd use that in a real env
        
        midi = miditoolkit.midi.parser.MidiFile()
        midi.ticks_per_beat = 480
        
        # Create a basic MIDI structure if decoding logic is complex
        # In practice, we use the library provided by the model author
        try:
            from midi_model.utils import tokens_to_midi
            midi = tokens_to_midi(tokens)
        except ImportError:
            # Fallback mock for structure
            track = miditoolkit.midi.containers.Instrument(program=0, is_drum=False, name='Piano')
            midi.instruments.append(track)
        
        midi.dump(output_path)
        return output_path