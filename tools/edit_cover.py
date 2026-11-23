"""Edit the series cover: remove both 'Years 4 to 10' lines and the corner watermark (author name kept by request)."""
from PIL import Image, ImageFilter
import numpy as np, sys
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB'); A = np.asarray(im).astype(float); O = A.copy(); R = A.copy()

def feather(h, w, f):
    my = np.minimum(np.arange(h), np.arange(h)[::-1]); mx = np.minimum(np.arange(w), np.arange(w)[::-1])
    m = np.minimum(np.clip(my[:, None] / f, 0, 1), np.clip(mx[None, :] / f, 0, 1)); return m[..., None]

def put(patch, x, y, f=4):
    h, w = patch.shape[:2]; m = feather(h, w, f)
    R[y:y+h, x:x+w] = R[y:y+h, x:x+w] * (1 - m) + patch * m

# 1. exhibit tag: '- YEARS 4 TO 10 -' (y 655-673, x 112-350) -> blank tag paper from the gap just below
put(O[674:710, 100:364], 100, 646, 5)          # 36 rows: 646-681
put(O[674:710, 100:364], 100, 700, 5)          # clear 'SEAL BROKEN BY' (709-726)
put(O[698:738, 100:364], 100, 671, 6)          # re-place it 27px higher so the tag lines stay evenly spaced

# 2. title card rule line: clear 'HISTORY CASE FILES • YEARS 4 TO 10' and both rules (y ~1010-1038)
band = np.concatenate([O[1036:1061, 180:968], O[1036:1047, 180:968][::-1]], 0)   # 36 rows of blank card paper
put(band, 180, 1005, 6)
# re-place 'HISTORY CASE FILES' centred on the card (rules 194..954 -> centre 574; text 297..597 = 300 wide)
txt = O[1007:1041, 289:606]; nx = 574 - 150 - 8
put(txt, nx, 1007, 6)
# rules: rebuild from the original rule strokes (y 1023-1024), left 194..402, right 746..954
rule = O[1016:1032, 200:270]
for x in range(194, 402 - 4, 60): put(rule[:, :min(70, 402 - x)], x, 1016, 3)
for x in range(746, 954 - 4, 60): put(rule[:, :min(70, 954 - x)], x, 1016, 3)

# 3. corner watermark (x 1052-1137, y 1669-1694) -> paper texture from just to its left
put(O[1658:1706, 930:1048], 1034, 1658, 10)

Image.fromarray(np.clip(R, 0, 255).astype('uint8')).save(out, 'JPEG', quality=84, optimize=True, progressive=True)
print('saved', out)
