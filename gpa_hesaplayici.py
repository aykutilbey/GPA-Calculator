import streamlit as st

# Sayfa yapılandırması
st.set_page_config(page_title="GPA Hesaplayıcı", page_icon="🎓", layout="centered")

# Başlık
st.title("🎓 GPA Hesaplayıcı")
st.markdown("---")

# Harf notları ve karşılık gelen puanlar
harf_notlari = {
    "AA": 4.0,
    "BA": 3.5,
    "BB": 3.0,
    "CB": 2.5,
    "CC": 2.0,
    "DC": 1.5,
    "DD": 1.0,
    "FD": 0.5,
    "FF": 0.0
}

# Session state ile ders listesi yönetimi
if 'dersler' not in st.session_state:
    st.session_state.dersler = []
if 'onceki_bilgiler_girildi' not in st.session_state:
    st.session_state.onceki_bilgiler_girildi = False

# Önceki dönem bilgileri
st.subheader("📚 Önceki Dönem Bilgileriniz")

col1, col2 = st.columns(2)

with col1:
    onceki_toplam_kredi = st.number_input(
        "Toplam Alınan Kredi", 
        min_value=0, 
        max_value=300, 
        value=0,
        help="Şimdiye kadar aldığınız toplam kredi (0 ise ilk dönemsiniz)"
    )

with col2:
    onceki_gpa = st.number_input(
        "Mevcut GPA", 
        min_value=0.0, 
        max_value=4.0, 
        value=0.0,
        step=0.01,
        format="%.2f",
        help="Şu anki GPA'niz (0.00 ise ilk dönemsiniz)"
    )

if onceki_toplam_kredi > 0 and onceki_gpa > 0:
    st.info(f"📊 Mevcut durumunuz: {onceki_toplam_kredi} kredi, {onceki_gpa:.2f} GPA")
elif onceki_toplam_kredi == 0:
    st.info("🆕 İlk döneminiz - Hoş geldiniz!")

st.markdown("---")

# Toplu ders ekleme
st.subheader("➕ Bu Dönem Aldığınız Dersleri Ekleyin")

ders_sayisi = st.number_input(
    "Kaç ders eklemek istiyorsunuz?", 
    min_value=1, 
    max_value=15, 
    value=5,
    help="Aynı anda birden fazla ders ekleyebilirsiniz"
)

st.markdown("##### Ders Bilgilerini Girin:")

yeni_dersler = []

for i in range(ders_sayisi):
    tekrar_mi = st.checkbox(
        f"Ders {i+1} - Tekrar Dersi mi?", 
        key=f"tekrar_{i}",
        help="Bu dersi daha önce aldıysanız işaretleyin"
    )
    
    if tekrar_mi:
        col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
    else:
        col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        ders_adi = st.text_input(
            f"Ders Adı", 
            key=f"ders_{i}",
            value=f"{i+1}",
            placeholder=f"Ders {i+1}"
        )
    
    with col2:
        kredi = st.number_input(
            f"Kredi", 
            min_value=1, 
            max_value=10, 
            value=3,
            key=f"kredi_{i}"
        )
    
    with col3:
        harf_notu = st.selectbox(
            f"{'Yeni ' if tekrar_mi else ''}Not", 
            options=list(harf_notlari.keys()),
            key=f"not_{i}"
        )
    
    eski_harf_notu = None
    if tekrar_mi:
        with col4:
            eski_harf_notu = st.selectbox(
                f"Eski Not", 
                options=list(harf_notlari.keys()),
                index=len(harf_notlari) - 1,  # FF varsayılan
                key=f"eski_not_{i}",
                help="Daha önce aldığınız not"
            )
    
    if ders_adi:
        yeni_dersler.append({
            'ders': ders_adi,
            'kredi': kredi,
            'not': harf_notu,
            'puan': harf_notlari[harf_notu],
            'tekrar': tekrar_mi,
            'eski_not': eski_harf_notu,
            'eski_puan': harf_notlari[eski_harf_notu] if eski_harf_notu else None
        })
    
    if i < ders_sayisi - 1:
        st.markdown("")

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Dersleri Ekle", use_container_width=True, type="primary"):
        if yeni_dersler:
            st.session_state.dersler = yeni_dersler
            st.success(f"✅ {len(yeni_dersler)} ders eklendi!")
            st.rerun()
        else:
            st.warning("⚠️ Lütfen en az bir ders adı girin!")

with col2:
    if st.button("🔄 Temizle", use_container_width=True):
        st.session_state.dersler = []
        st.rerun()

st.markdown("---")

# Eklenen dersleri göster ve hesapla
if st.session_state.dersler:
    st.subheader("📋 Bu Dönem Aldığınız Dersler")
    
    # Tablo şeklinde göster
    for idx, ders in enumerate(st.session_state.dersler):
        if ders.get('tekrar'):
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1.2, 1.2, 1])
            
            with col1:
                st.text(f"🔄 {ders['ders']}")
            with col2:
                st.text(f"{ders['kredi']} kredi")
            with col3:
                st.text(f"Eski: {ders['eski_not']}")
            with col4:
                st.text(f"Yeni: {ders['not']}")
            with col5:
                not_artisi = ders['puan'] - ders['eski_puan']
                if not_artisi > 0:
                    st.text(f"+{not_artisi:.1f} ⬆️")
                elif not_artisi < 0:
                    st.text(f"{not_artisi:.1f} ⬇️")
                else:
                    st.text("Aynı")
        else:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.text(ders['ders'])
            with col2:
                st.text(f"{ders['kredi']} kredi")
            with col3:
                st.text(ders['not'])
            with col4:
                st.text(f"{ders['puan']:.1f} puan")
    
    st.markdown("---")
    
    # Bu dönem hesaplamaları
    bu_donem_kredi = sum(ders['kredi'] for ders in st.session_state.dersler)
    bu_donem_agirlikli = sum(ders['kredi'] * ders['puan'] for ders in st.session_state.dersler)
    bu_donem_gpa = bu_donem_agirlikli / bu_donem_kredi if bu_donem_kredi > 0 else 0
    
    # Tekrar olmayan (yeni) derslerin kredileri
    yeni_ders_kredileri = sum(
        ders['kredi']
        for ders in st.session_state.dersler 
        if not ders.get('tekrar')
    )
    
    # Tekrar derslerin eski ağırlıklı puanlarını hesapla
    tekrar_ders_eski_agirlikli = sum(
        ders['kredi'] * ders['eski_puan'] 
        for ders in st.session_state.dersler 
        if ders.get('tekrar') and ders.get('eski_puan') is not None
    )
    
    # Genel GPA hesaplama
    # Önceki toplam ağırlıklı puandan tekrar derslerin eski notlarını çıkar
    onceki_agirlikli = (onceki_toplam_kredi * onceki_gpa) - tekrar_ders_eski_agirlikli
    
    # Yeni toplam kredi = önceki kredi + sadece yeni derslerin kredileri (tekrar dersler zaten dahil)
    yeni_toplam_kredi = onceki_toplam_kredi + yeni_ders_kredileri
    yeni_toplam_agirlikli = onceki_agirlikli + bu_donem_agirlikli
    yeni_gpa = yeni_toplam_agirlikli / yeni_toplam_kredi if yeni_toplam_kredi > 0 else 0
    
    # Sonuçları göster
    st.subheader("📊 Sonuçlar")
    
    # Bu dönem sonuçları
    st.markdown("##### 🆕 Bu Dönem")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Bu Dönem Kredi", bu_donem_kredi)
    
    with col2:
        st.metric("Bu Dönem GPA", f"{bu_donem_gpa:.2f}")
    
    st.markdown("---")
    
    # Genel sonuçlar
    st.markdown("##### 🎯 Genel Durum")
    
    col1, col2 = st.columns(2)
    
    with col1:
        gpa_degisim = yeni_gpa - onceki_gpa if onceki_gpa > 0 else 0
        st.metric(
            "Yeni GPA", 
            f"{yeni_gpa:.2f}",
            delta=f"{gpa_degisim:+.2f}" if onceki_gpa > 0 else None
        )
    
    with col2:
        st.metric("Toplam Kredi", yeni_toplam_kredi)
    
    # Progress bar
    st.progress(min(yeni_gpa / 4.0, 1.0))
    
    # Detaylı bilgi
    if onceki_toplam_kredi > 0:
        st.markdown("---")
        with st.expander("📈 Detaylı Analiz"):
            st.write(f"**Önceki Durum:** {onceki_toplam_kredi} kredi, {onceki_gpa:.2f} GPA")
            st.write(f"**Bu Dönem:** {bu_donem_kredi} kredi, {bu_donem_gpa:.2f} GPA")
            st.write(f"**Yeni Durum:** {yeni_toplam_kredi} kredi, {yeni_gpa:.2f} GPA")
            
            if gpa_degisim > 0:
                st.success(f"🎉 GPA'niz {abs(gpa_degisim):.2f} puan arttı!")
            elif gpa_degisim < 0:
                st.warning(f"⚠️ GPA'niz {abs(gpa_degisim):.2f} puan düştü.")
            else:
                st.info("GPA'niz aynı kaldı.")

else:
    st.info("👆 Yukarıdan ders bilgilerinizi girin ve 'Dersleri Ekle' butonuna basın!")

# Alt bilgi
st.markdown("---")
st.caption("💡 İpucu: Önceki dönem bilgilerinizi girin, ardından bu dönem derslerinizi toplu olarak ekleyin.")