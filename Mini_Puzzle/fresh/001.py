import base64
from extraction_tools import SalphaseionSolver

# 1. Decode the ABBA section (The Thinker)
# I'm using a slice of the actual text from your uploaded salphaseion.html
abba_data = "d b b i b f b h c c b e g b i h a b e b e i h b e g g e g e b e b b g e h h e b h h f b a b f d h b e f f c d b b f c c c g b f b e e g g e c b e d c i b f b f f g i g b e e e a b e a b b a b b a b a b b a a a a b a b b b a b a a a b b b a a b a a b b a b a a b a b b b b a a a a b b b a a b b a b b b a b a b a b b"
thinker = SalphaseionSolver.decode_abba(abba_data)

# 2. Decode the Hex section (The Matrix Sum)
hex_data = "agdafaohaeiecggchgicbbhcgbehcfcoabicfdhhcdbcacagbdaiobbbgbeadeddecfobfdhdgdobdgoooiiigdocdaoofidfh"
matrix_sum = SalphaseionSolver.decode_hex_section(hex_data)

print(f"THINKER NAME: {thinker}")
print(f"MATRIX SUM: {matrix_sum}")