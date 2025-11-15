from pathlib import Path


def main() -> None:
    path = Path("public/ben-kimim.html")
    text = path.read_text(encoding="utf-8", errors="ignore")

    marker = '<section class="values-section">'
    start = text.find(marker)
    if start == -1:
        raise SystemExit("values-section not found")

    # Move back to the comment line before the section for cleaner replacement.
    comment_start = text.rfind("\n", 0, start)
    if comment_start == -1:
        comment_start = start

    end = text.find("</section>", start)
    if end == -1:
        raise SystemExit("values-section closing </section> not found")
    end += len("</section>")

    new_block = """    <!-- Değerler Bölümü -->
    <section class="values-section">
        <div class="container">
            <div class="section-header">
                <h2>Değerlerimiz</h2>
                <p>Çalışmalarımı temellendiren ilkeler</p>
            </div>
            
            <div class="values-grid">
                <div class="value-item">
                    <div class="value-icon">
                        <i class="fas fa-gift"></i>
                    </div>
                    <h3>Ücretsiz Hizmet</h3>
                    <p>Türk milleti için tamamen ücretsiz ve reklamsız hizmet sunuyorum</p>
                </div>
                
                <div class="value-item">
                    <div class="value-icon">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <h3>Doğruluk ve Güvenilirlik</h3>
                    <p>Bilgilerin doğruluğu ve güvenilirliği benim için en önemli öncelik</p>
                </div>
                
                <div class="value-item">
                    <div class="value-icon">
                        <i class="fas fa-hands-helping"></i>
                    </div>
                    <h3>Toplumsal Fayda</h3>
                    <p>Tüm çalışmalarımı topluma katkı sağlamak amacıyla yapıyorum</p>
                </div>
            </div>
        </div>
    </section>

"""

    text = text[: comment_start + 1] + new_block + text[end:]
    text = text.replace("<!-- Referanslar Blm -->", "<!-- Referanslar Bölümü -->")

    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()

