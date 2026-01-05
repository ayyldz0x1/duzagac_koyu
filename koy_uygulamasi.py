import streamlit as st
import json
import os
import requests

# 1. Sayfa Ayarları
st.set_page_config(page_title="Düzağaç Köyü", layout="centered")

# 2. Veri Okuma Fonksiyonu
def veri_oku(dosya_adi):
    if not os.path.exists(f"{dosya_adi}.json"): return []
    with open(f"{dosya_adi}.json", "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

# 3. Üst Panel ve Hava Durumu
col1, col2 = st.columns([2, 1])
with col1: 
    st.markdown("<h2 style='color:#4CAF50;'>🌳 Düzağaç Köyü</h2>", unsafe_allow_html=True)
with col2:
    try:
        hava = requests.get("https://wttr.in/Kozan,Adana?format=%C+%t", timeout=2).text
        st.markdown(f"<div style='text-align:center;color:white;background:#1B5E20;padding:8px;border-radius:15px;font-weight:bold;'>🌤 {hava}</div>", unsafe_allow_html=True)
    except:
        st.markdown("<div style='text-align:center;color:white;background:#1B5E20;padding:8px;border-radius:15px;'>🌤 18°C</div>", unsafe_allow_html=True)

# 4. Menü Navigasyonu
sayfa = st.radio("Menü Seçiniz:", ["Anasayfa", "Duyurular", "Galeri", "Vefat İlanları"], horizontal=True)
st.write("---")

# 5. Sayfa İçerikleri
if sayfa == "Anasayfa":
    st.subheader("Hoş Geldiniz")
    
    # Yerel Video Oynatma
    video_yolu = "koy_videosu.mp4" 
    if os.path.exists(video_yolu):
        st.video(video_yolu)
    else:
        st.info("Köy videosu yükleniyor...")
    
    st.write("Düzağaç köyümüzün dijital dünyasına hoş geldiniz.")

elif sayfa == "Duyurular":
    st.subheader("📢 Köyümüzden Duyurular")
    duyurular = veri_oku("duyurular")
    if duyurular:
        for d in reversed(duyurular):
            with st.expander(d['baslik']):
                st.write(d['icerik'])
    else:
        st.info("Henüz duyuru bulunmuyor.")

elif sayfa == "Galeri":
    st.subheader("🖼 Köy Galerisi")
    galeri = veri_oku("galeri")
    if galeri:
        cols = st.columns(2)
        for i, g in enumerate(galeri):
            with cols[i % 2]:
                try: 
                    st.image(g['url'], caption=g['not'], use_container_width=True)
                except: 
                    st.warning("Resim yüklenemedi.")
    else:
        st.info("Galeri henüz boş.")

elif sayfa == "Vefat İlanları":
    st.subheader("🕋 Vefat İlanları")
    vefatlar = veri_oku("vefatlar")
    if vefatlar:
        for v in reversed(vefatlar):
            st.error(f"**{v['isim']}**\n\n{v['detay']}")
    else:
        st.write("Kayıtlı vefat ilanı bulunmamaktadır.")

# 6. Sosyal Medya İkonları
st.write("---")
s1, s2, s3 = st.columns(3)
s1.markdown("[![Instagram](https://img.icons8.com/color/48/0/instagram-new.png)](https://www.instagram.com/duzagacky/)")
s2.markdown("[![Facebook](https://img.icons8.com/color/48/0/facebook-new.png)](https://www.facebook.com/DuzagacKoyuKozan/)")
s3.markdown("[![WhatsApp](https://img.icons8.com/color/48/0/whatsapp.png)](https://chat.whatsapp.com/J9tfpgXd3iu8HM1FBxC2U7)")