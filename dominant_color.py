import cv2

import numpy as np

from colorsys import hls_to_rgb, rgb_to_hls

from PIL import Image as PImage

# CRITERIA: MAX_ITER, EPSILON_ACCURACY
# cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS

CV_KMEANS_PARAMS = {
  "K": 8,
  "bestLabels": None,
  "criteria": (cv2.TERM_CRITERIA_EPS, -1, 0.02),
  "attempts": 8,
  "flags": cv2.KMEANS_RANDOM_CENTERS
}

def resize_PIL(pimg, max_dim=256):
  iw, ih = pimg.size
  resize_ratio = min(max_dim / iw, max_dim / ih)
  new_size = (int(iw * resize_ratio), int(ih * resize_ratio))
  return pimg.resize(new_size)

def rgb01_to_rgb255(c):
  return tuple(np.multiply(c, 255).astype(np.uint8))

def rgb255_to_rgb01(c):
  return tuple(np.multiply(c, 1.0 / 255.0).astype(np.float32))

def hls_to_rgb255(c):
  return rgb01_to_rgb255(hls_to_rgb(*c))

def rgb255_to_hex_str(c):
  r, g, b = c
  return "#{:02x}{:02x}{:02x}".format(r, g, b)

def hls_order(c):
  _,l,s = c[1]
  l_term = 2 * abs(l - 0.5)
  return l_term + (1.0 - s) if l_term < 0.5 else 1.5 * l_term

def hls_order_from_rgb255(c):
  return hls_order(rgb_to_hls(*rgb255_to_rgb01(c)))

def get_dominant_colors(pimg, k=4, max_dim=256):
  CV_KMEANS_PARAMS["K"] = 2*k

  rpimg = resize_PIL(pimg, max_dim)
  np_img = np.array(rpimg).astype(np.float32)
  _, labels, centers = cv2.kmeans(np_img.reshape(-1, 3), **CV_KMEANS_PARAMS)
  centers = centers.astype(np.uint8)

  _, counts = np.unique(labels, return_counts=True)
  by_count = np.argsort(-counts)

  rgb2count = {rgb255_to_hex_str(k):v for k,v in zip(centers, counts)}
  rgb2pct = {rgb255_to_hex_str(k):v/(sum(counts)) for k,v in zip(centers, counts)}

  # all centers, ordered by count
  rgb_by_count = [tuple(centers[c]) for c in by_count]

  # keep original center indexes
  centers_hls = [(i, rgb_to_hls(*rgb255_to_rgb01(c))) for i,c in enumerate(centers)]

  # get top k hls values, get original RGB from center indexes
  by_hls = sorted(centers_hls, key=hls_order)
  rgb_by_hls = [tuple(centers[h[0]]) for h in by_hls[:k]]

  # order the k hls values by count
  rgb_by_hls_count = sorted(rgb_by_hls, key=lambda x: rgb_by_count.index(x))

  # get hex values
  rgb_by_count_hex = [rgb255_to_hex_str(c) for c in rgb_by_count]
  rgb_by_hls_count_hex = [rgb255_to_hex_str(c) for c in rgb_by_hls_count]

  npxs = []
  for c in labels.reshape(-1):
    npxs.append(tuple(centers[c]))

  npimg = PImage.new("RGB", rpimg.size)
  npimg.putdata(npxs)

  return rgb_by_count_hex, rgb_by_hls_count_hex, rgb2pct, resize_PIL(npimg, 480)
