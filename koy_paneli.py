import streamlit as st
import json
import os

st.set_page_config(page_title="Düzağaç Yönetim", layout="wide")

# Veri İşlemleri
def veri_oku(dosya_adi):
    if not os.path.exists(f"{dosya_adi}.json"): return []
    with open(f"{dosya_adi}.json", "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def veri_yaz(dosya_adi, veri_listesi):
    with open(f"{dosya_adi}.json", "w", encoding="utf-8") as f:
        for madde in veri_listesi:
            json.dump(madde, f, ensure_ascii=False)
            f.write("\n")

# Şifre Girişi
sifre = st.sidebar.text_input("Yönetici Şifresi:", type="password")

if sifre == "1234":
    st.title("🌳 Yönetim Paneli")
    tab1, tab2, tab3 = st.tabs(["📢 Duyurular", "🖼 Galeri", "🕋 Vefat"])

    with tab1:
        st.subheader("Duyuru Ekle")
        baslik = st.text_input("Duyuru Başlığı")
        icerik = st.text_area("İçerik")
        if st.button("Duyuruyu Paylaş"):
            liste = veri_oku("duyurular")
            liste.append({"baslik": baslik, "icerik": icerik})
            veri_yaz("duyurular", liste)
            st.success("Eklendi!")
            st.rerun()
        
        st.write("---")
        st.subheader("Mevcut Duyuruları Sil")
        d_liste = veri_oku("duyurular")
        for i, d in enumerate(d_liste):
            c1, c2 = st.columns([5, 1])
            c1.write(d['baslik'])
            if c2.button("SİL", key=f"d_{i}"):
                d_liste.pop(i)
                veri_yaz("duyurular", d_liste)
                st.rerun()

    with tab2:
        st.subheader("Galeriye Resim Ekle")
        url = st.text_input("Resim URL (Link)")
        notu = st.text_input("Kısa Not")
        if st.button("Resmi Kaydet"):
            g_liste = veri_oku("galeri")
            g_liste.append({"url": url, "not": notu})
            veri_yaz("galeri", g_liste)
            st.success("Resim eklendi!")
            st.rerun()

        st.write("---")
        st.subheader("Galeriden Resim Sil")
        g_liste = veri_oku("galeri")
        for i, g in enumerate(g_liste):
            c1, c2 = st.columns([5, 1])
            try: c1.image(g['url'], width=100)
            except: c1.write("Hatalı Resim")
            if c2.button("SİL", key=f"g_{i}"):
                g_liste.pop(i)
                veri_yaz("galeri", g_liste)
                st.rerun()

    with tab3:
        st.subheader("Vefat İlanı Ekle")
        v_isim = st.text_input("İsim Soyisim")
        v_detay = st.text_area("Cenaze Bilgileri")
        if st.button("Vefatı Kaydet"):
            v_liste = veri_oku("vefatlar")
            v_liste.append({"isim": v_isim, "detay": v_detay})
            veri_yaz("vefatlar", v_liste)
            st.success("İlan eklendi!")
            st.rerun()

        st.write("---")
        st.subheader("Vefat İlanlarını Sil")
        v_liste = veri_oku("vefatlar")
        for i, v in enumerate(v_liste):
            c1, c2 = st.columns([5, 1])
            c1.write(v['isim'])
            if c2.button("SİL", key=f"v_{i}"):
                v_liste.pop(i)
                veri_yaz("vefatlar", v_liste)
                st.rerun()
else:
    st.info("Lütfen sol taraftan şifrenizi girin.")