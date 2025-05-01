
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

st.set_page_config(page_title="Arabic Text Image Generator", layout="centered")

st.title("توليد صورة تحتوي على نص عربي مشكول")

# Arabic text with full tashkeel
arabic_text = """أَتَعْرِفُ مَا مَعْنَىٰ الْيَقِينِ بِاللَّهِ؟

الْيَقِينُ بِاللَّهِ هُوَ الَّذِي يُحَقِّقُ الْمُسْتَحِيلَ، الْيَقِينُ بِاللَّهِ هُوَ تَكُونُ
كُلُّ الْأَبْوَابِ مُغْلَقَةً وَكُلُّ الظُّرُوفِ صَعْبَةً وَكُلُّ الْمُؤَشِّرَاتِ تُوحِي
بِعَكْسِ مَا تَمَنَّاهُ لَٰكِنَّكَ عَلَىٰ يَقِينٍ بِأَنَّ اللَّهَ سَيُصْلِحُ كُلَّ شَيْءٍ
وَسَيَتَكَفَّلُ بِكُلِّ شَيْءٍ.. يَقُولُ ابْنُ الْقَيِّمِ مُتَحَدِّثًا عَنِ الْيَقِينِ بِاللَّهِ لَوْ
أَنَّ أَحَدَكُمْ هَمَّ بِإِزَالَةِ جَبَلٍ وَهُوَ وَاثِقٌ بِاللَّهِ لَأَزَالَهُ.. فَثِقْ بِاللَّهِ، وَثِقْ
بِتَدَابِيرِهِ وَاجْعَلْ يَقِينَكَ بِاللَّهِ هُوَ سِرَّ الرِّضَا بِكُلِّ شَيْءٍ يَحْدُثُ لَكَ"""


# Reshape and bidi transform
reshaped_text = arabic_reshaper.reshape(arabic_text)
bidi_text = get_display(reshaped_text)

# Image parameters
img_width, img_height = 1080, 1920
bg_color = "#FFF9F0"  # light cream
main_color = "#6A1B1A"  # maroon/brown
highlight_color = "#006C6D"  # teal for 'الْيَقِينِ'
font_path = "NotoNaskhArabic-Regular.ttf"
font_size = 40

# Create image
img = Image.new("RGB", (img_width, img_height), bg_color)
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(font_path, font_size)

# Draw text with special coloring
lines = arabic_text.splitlines()
y = 100
for line in lines:
    reshaped_line = arabic_reshaper.reshape(line)
    bidi_line = get_display(reshaped_line)
    bbox = draw.textbbox((0, 0), bidi_line, font=font)
width = bbox[2] - bbox[0]
    x = (img_width - width) // 2

    if "أَتَعْرِفُ" in line:
        parts = line.split("الْيَقِينِ")
        px = x
        for i, part in enumerate(parts):
            reshaped = get_display(arabic_reshaper.reshape(part))
            draw.text((px, y), reshaped, font=font, fill=main_color)
            px += draw.textlength(reshaped, font=font)
            if i < len(parts) - 1:
                yaqeen = get_display(arabic_reshaper.reshape("الْيَقِينِ"))
                draw.text((px, y), yaqeen, font=font, fill=highlight_color)
                px += draw.textlength(yaqeen, font=font)
    else:
        draw.text((x, y), bidi_line, font=font, fill=main_color)
    y += font_size + 15

# Display and download
st.image(img)
img.save("output.png")
with open("output.png", "rb") as file:
    st.download_button("تحميل الصورة", file, "output.png")
