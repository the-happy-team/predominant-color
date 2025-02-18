import gradio as gr

from dominant_color import get_dominant_colors

NUM_COLORS = 4
NUM_OUTS = 2 * NUM_COLORS + NUM_COLORS

out_colors = [gr.ColorPicker(visible=False) for _ in range(NUM_OUTS)]
out_pcts = [gr.Textbox(visible=False) for _ in range(NUM_OUTS)]

def dom_col(img_in):
  palette_cnt, palette_hls, palette_pcts, hex_pcts, img_out = get_dominant_colors(img_in, k=NUM_COLORS)
  palette_hex = palette_cnt + palette_hls

  def get_pct_md(cp):
    return f"### {round(palette_pcts.get(cp, 0)*100, 2)}%"

  # TODO: use hex_pcts for something
  return [gr.ColorPicker(h) for h in palette_hex] + [gr.Textbox(get_pct_md(h)) for h in palette_hex] + [img_out]

def get_color(cp):
  return cp

def get_color_md(cp):
  return f"### {cp}"

def get_md(x):
  return x

with gr.Blocks() as demo:
  with gr.Row():
    with gr.Column(scale=1):
      gr.Markdown("# Dominant color calculator")
      gr.Interface(
        dom_col,
        inputs=gr.Image(type="pil"),
        outputs=[*out_colors, *out_pcts, gr.Image(type="pil", label="img_out")],
        cache_examples=True,
        examples=[["./imgs/03.webp"], ["./imgs/11.jpg"]],
        allow_flagging="never",
        fill_width=True
      )

    with gr.Column(scale=0, variant="default"):
      with gr.Column(scale=0, variant="panel"):
        gr.Markdown("# By Count")
        for i,o in enumerate(out_colors[:2*NUM_COLORS]):
          with gr.Row():
            gr.ColorPicker(get_color, inputs=[o], show_label=False, scale=0, container=False)
            gr.Markdown(get_color_md, inputs=[o], show_label=False)
            gr.Markdown(get_md, inputs=[out_pcts[i]], show_label=False)

      with gr.Column(scale=0, variant="panel"):
        gr.Markdown("# By HLS")
        for i,o in enumerate(out_colors[-NUM_COLORS:]):
          with gr.Row():
            gr.ColorPicker(get_color, inputs=[o], show_label=False, scale=0, container=False)
            gr.Markdown(get_color_md, inputs=[o], show_label=False)
            gr.Markdown(get_md, inputs=[out_pcts[-NUM_COLORS+i]], show_label=False)


if __name__ == "__main__":
   demo.launch()
