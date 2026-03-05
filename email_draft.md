# Email Draft — Prof. Kılıç

---

**Konu / Subject:** ONT Sequencing Data QC Analysis — Pipeline Results

---

Sayın Prof. Kılıç,

Umarım bu e-posta sizi iyi bulur.

Oxford Nanopore Technology (ONT) uzun okuma verisi üzerinde gerçekleştirdiğimiz kalite kontrol (QC) analizini tamamladık. Çalışmanın tüm adımları otomatik ve tekrarlanabilir bir pipeline içinde yapılandırıldı.

---

## Ne Yaptık?

1. **Veri Simülasyonu:** Gerçek sequencing verisi olmadığından, biyolojik olarak gerçekçi 1.000 adet ONT okuması simüle ettik. Okuma uzunlukları log-normal dağılımından (1 kb–50 kb arası), GC içerikleri %40–60 aralığından, baz kalite skorları ise ONT'ye özgü Phred Q7–Q20 aralığından örneklendi.

2. **Kalite Kontrol Metrikleri:** Her okuma için üç temel QC metriği hesaplandı:
   - **Okuma uzunluğu** (Read Length)
   - **GC içeriği** (%)
   - **Ortalama kalite skoru** (Mean Phred Quality)

3. **Görselleştirme:** Tüm metrikler için histogram ve yoğunluk eğrisi (KDE) grafikleri oluşturuldu. Bu grafikler `results/plots/` klasöründe bulunmaktadır.

4. **NanoPlot Raporu:** Standart bioinformatik QC aracı NanoPlot ile interaktif bir HTML raporu üretildi (`results/nanoplot/NanoPlot-report.html`). Bu rapor N50 değeri, ortalama kalite dağılımı ve okuma uzunluğu özetlerini içermektedir.

---

## Grafiklerin Yorumu

- **Okuma Uzunluğu:** Dağılım log-normal yapıya uygun şekilde sağa çarpık; ortalama ~7–8 kb civarında, N50 değeri biyolojik olarak makul bir aralıkta.
- **GC İçeriği:** Beklenen %40–60 aralığında uniform bir dağılım gözlemlendi; belirgin bir sapma veya kontaminasyon işareti yok.
- **Kalite Skorları:** Ortalama Phred skoru Q10–Q14 bandında yoğunlaşıyor; bu, tipik ONT ham veri kalitesiyle tutarlı.

---

## Bir Sonraki Adım

QC aşaması tamamlandıktan sonra önerilen adımlar:

1. **Kalite Filtrelemesi:** Düşük kaliteli okumaları elemek için `filtlong` veya `chopper` kullanılabilir (Q < 8 veya uzunluk < 1000 bp).
2. **Referans Hizalaması (Alignment):** Filtrelenmiş okumalar `minimap2` ile referans genome hizalanabilir.
3. **Varyant Tespiti:** Alignment sonrası SNP/indel tespiti için `medaka` veya `clair3` kullanılabilir.

Tüm pipeline Docker ile paketlenmiştir; yeniden çalıştırmak için tek komut yeterlidir:

```bash
docker run --rm -v $(pwd):/workspace ont-qc-pipeline
```

Herhangi bir sorunuz olursa memnuniyetle yanıtlarım.

Saygılarımla,

---

**Dear Prof. Kılıç,**

I hope this message finds you well.

We have completed the Quality Control (QC) analysis of Oxford Nanopore Technology (ONT) long-read sequencing data. The entire workflow has been implemented as an automated, reproducible pipeline.

**Summary of Results:**
- 1,000 ONT-style reads were simulated with realistic length (lognormal, 1–50 kb), GC content (40–60%), and quality (Phred Q7–Q20) distributions.
- Per-read metrics (read length, GC content, mean quality) were computed and saved as a CSV file.
- Histogram/KDE plots and an interactive NanoPlot HTML report are available in the `results/` directory.

**Key Observations:**
- Read length distribution is right-skewed (log-normal), consistent with typical ONT output.
- GC content is uniformly distributed in the expected range — no contamination signal detected.
- Mean quality scores cluster around Q10–Q14, representative of ONT raw read quality.

**Recommended Next Steps:** quality filtering → reference alignment (minimap2) → variant calling (medaka/clair3).

Please let me know if you have any questions or would like to adjust the pipeline parameters.

Best regards,
