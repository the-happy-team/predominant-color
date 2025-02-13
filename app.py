import gradio as gr
from PIL import Image as PImage

from dominant_color import get_dominant_colors, rgb255_to_hex_str

NUM_OUTS = 4
all_outputs = [gr.ColorPicker(visible=False) for _ in range(NUM_OUTS)]

def dom_col(img_in):
  rgb_by_cnt, rgb_by_hls = get_dominant_colors(img_in)
  palette_cnt = [[int(v) for v in c] for c in rgb_by_cnt[:NUM_OUTS]]
  palette_hls = [[int(v) for v in c] for c in rgb_by_hls[:NUM_OUTS]]
  return palette_cnt, palette_hls

def dom_col_hls(img_in):
  _, palette_hls = dom_col(img_in)
  palette_hex = [rgb255_to_hex_str(c) for c in palette_hls]
  return [gr.ColorPicker(h, label=f"{h}", show_label=True, visible=True) for h in palette_hex]

with gr.Blocks() as demo:
  gr.Markdown("""
              # Dominant color calculator
              """)

  gr.Interface(
    dom_col_hls,
    inputs=gr.Image(type="pil"),
    outputs=all_outputs,
    cache_examples=True,
    examples=[["./imgs/03.webp"], ["./imgs/11.jpg"]],
    allow_flagging="never",
  )

if __name__ == "__main__":
   demo.launch()
