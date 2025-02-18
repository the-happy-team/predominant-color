import gradio as gr

from os import listdir

from dominant_color import get_dominant_colors

NUM_CNT = 8
NUM_HLS = 4
NUM_RAW = 12

cnt_colors = [gr.ColorPicker(visible=False) for _ in range(NUM_CNT)]
cnt_pcts = [gr.Textbox(visible=False) for _ in range(NUM_CNT)]

hls_colors = [gr.ColorPicker(visible=False) for _ in range(NUM_HLS)]
hls_pcts = [gr.Textbox(visible=False) for _ in range(NUM_HLS)]

raw_colors = [gr.ColorPicker(visible=False) for _ in range(NUM_RAW)]
raw_pcts = [gr.Textbox(visible=False) for _ in range(NUM_RAW)]

my_examples = [
  [f"./imgs/{fname}"] for fname in listdir("./imgs") if fname.endswith("jpg")
]

def dom_col(img_in):
  palette_cnt, palette_hls, palette_pcts, hex_pcts, img_out = get_dominant_colors(img_in, k=NUM_HLS)

  def get_pct_md(pct):
    return f"### {round(pct*100, 2)}%"

  def get_hex_pct_md(cp):
    return get_pct_md(palette_pcts.get(cp, 0))

  cnt_colors = [gr.ColorPicker(h) for h in palette_cnt]
  cnt_pcts = [gr.Textbox(get_hex_pct_md(h)) for h in palette_cnt]
  hls_colors = [gr.ColorPicker(h) for h in palette_hls]
  hls_pcts = [gr.Textbox(get_hex_pct_md(h)) for h in palette_hls]
  raw_colors = [gr.ColorPicker(hp[0]) for hp in hex_pcts[:NUM_RAW]]
  raw_pcts = [gr.Textbox(get_pct_md(hp[1])) for hp in hex_pcts[:NUM_RAW]]

  return cnt_colors + cnt_pcts + hls_colors + hls_pcts + raw_colors + raw_pcts + [img_out]

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
        outputs=[*cnt_colors, *cnt_pcts,
                 *hls_colors, *hls_pcts,
                 *raw_colors, *raw_pcts,
                 gr.Image(type="pil", label="img_out")],
        cache_examples=True,
        examples=my_examples,
        allow_flagging="never",
        fill_width=True
      )

    with gr.Column(scale=0, variant="default"):
      with gr.Column(scale=0, variant="panel"):
        gr.Markdown("# By Count")
        for i,o in enumerate(cnt_colors):
          with gr.Row():
            gr.ColorPicker(get_color, inputs=[o], show_label=False, scale=0, container=False)
            gr.Markdown(get_color_md, inputs=[o], show_label=False)
            gr.Markdown(get_md, inputs=[cnt_pcts[i]], show_label=False)

      with gr.Column(scale=0, variant="panel"):
        gr.Markdown("# By HLS")
        for i,o in enumerate(hls_colors):
          with gr.Row():
            gr.ColorPicker(get_color, inputs=[o], show_label=False, scale=0, container=False)
            gr.Markdown(get_color_md, inputs=[o], show_label=False)
            gr.Markdown(get_md, inputs=[hls_pcts[i]], show_label=False)

      with gr.Column(scale=0, variant="panel"):
        gr.Markdown("# By Raw Count")
        for i,o in enumerate(raw_colors):
          with gr.Row():
            gr.ColorPicker(get_color, inputs=[o], show_label=False, scale=0, container=False)
            gr.Markdown(get_color_md, inputs=[o], show_label=False)
            gr.Markdown(get_md, inputs=[raw_pcts[i]], show_label=False)


if __name__ == "__main__":
   demo.launch()
