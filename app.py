import gradio as gr

from dominant_color import get_dominant_colors, rgb255_to_hex_str

NUM_COLORS = 4
NUM_OUTS = 2 * NUM_COLORS

all_outputs = [gr.ColorPicker(visible=False) for _ in range(NUM_OUTS)]
disp_outputs = []

def dom_col(img_in):
  rgb_by_cnt, rgb_by_hls = get_dominant_colors(img_in, k=NUM_COLORS)
  palette_cnt = [[int(v) for v in c] for c in rgb_by_cnt[:NUM_COLORS]]
  palette_hls = [[int(v) for v in c] for c in rgb_by_hls[:NUM_COLORS]]
  palette_hex = [rgb255_to_hex_str(c) for c in (palette_cnt + palette_hls)]
  return [gr.ColorPicker(h) for h in palette_hex]

def get_color(cp):
  return cp

def get_color_md(cp):
  return f"### {cp}"

with gr.Blocks() as demo:
  with gr.Row():
    with gr.Column(scale=3):
      gr.Markdown("# Dominant color calculator")
      gr.Interface(
        dom_col,
        inputs=gr.Image(type="pil"),
        outputs=all_outputs,
        cache_examples=True,
        examples=[["./imgs/03.webp"], ["./imgs/11.jpg"]],
        allow_flagging="never",
        fill_width=True
      )

    with gr.Column(scale=1, variant="panel"):
      gr.Markdown("# By HLS")
      for o in all_outputs[-4:]:
        with gr.Row():
          gr.ColorPicker(get_color, inputs=[o], show_label=False, scale=0, container=False)
          gr.Markdown(get_color_md, inputs=[o], show_label=False)

    with gr.Column(scale=0, variant="default"):
      gr.Markdown("")
      '''
      gr.Markdown("# By Count")
      for o in all_outputs[:4]:
        with gr.Row():
          gr.ColorPicker(get_color, inputs=[o], show_label=False, scale=0, container=False)
          gr.Markdown(get_color_md, inputs=[o], show_label=False)
      '''

if __name__ == "__main__":
   demo.launch()
