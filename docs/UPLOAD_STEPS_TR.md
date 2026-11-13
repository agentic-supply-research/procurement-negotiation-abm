# GitHub yükleme notu (Türkçe)

Bu klasör, yeni bir GitHub deposuna yüklenmek üzere hazırlanmıştır. Bu aşamada hiçbir GitHub hesabına giriş yapılmadı ve çevrim içi depo oluşturulmadı.

Önerilen depo adı: `procurement-negotiation-abm`. GitHub'da boş bir depo oluştururken başka bir README, `.gitignore` veya lisans seçmeyin; bunlar pakette bulunuyor.

Depoyu yüklemeden önce `docs/RELEASE_CHECKLIST.md` dosyasındaki kaynak veri paylaşım koşullarını ve lisansı kontrol edin. Ardından dosyaları bilgisayarınızda klasöre çıkarıp terminalde aşağıdaki komutları kullanabilirsiniz:

```bash
git init
git add .
git commit -m "Initial reproducible research release"
git branch -M main
git remote add origin <GITHUB_DEPO_ADRESI>
git push -u origin main
```

`<GITHUB_DEPO_ADRESI>` gerçek depo oluşturulunca değiştirilecek bir yer tutucudur. Bu adımları henüz uygulamayın; GitHub'a yükleme ve makaleye kalıcı link ekleme işlemlerini birlikte gerçekleştirebiliriz.
