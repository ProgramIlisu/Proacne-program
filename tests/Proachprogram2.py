import re
from playwright.sync_api import Page, expect

TEST_COMPOSITION = """Water, Cetearyl Alcohol, Caprylic/Capric Triglyceride, Persea Gratissima (Avocado) Oil, Butyrospermum Parkii (Shea) Butter, Glycerin, Potassium Cetyl Phosphate, Cyclopentasiloxane, 3-o-ethyl Ascorbic Acid, Tocopheryl Acetate, Malic Acid, Succinic Acid, Lactic Acid, Glycolic Acid, Tocopherol, Panthenol, Sodium Hyaluronate Crosspolymer, Sodium Hyaluronate, Sodium Acetylated Hyaluronate, Hydrolyzed Sodium Hyaluronate, Centella Asiatica (Gotu kola) Extract, Helianthus Annuus (Sunflower) Seed Oil, Ceteareth-20, Cera Alba, Dimethiconol, Xanthan Gum, Pentylene Glycol, Tetrasodium Glutamate Diacetate, Sodium Hydroxide, Phenoxyethanol Ethylhexylglycerin, Potassium Sorbate, Sodium Benzoate, Parfum, Hexyl Cinnamal, Linalool, CI 19140."""


def test_proacne_check_composition(page: Page):
    """Тест проверки состава на комедогенность"""
    
    page.goto("https://proacne-program.com/check", wait_until="domcontentloaded")
    
    textarea = page.locator("textarea")
    expect(textarea).to_be_visible()
    
    # Заполняем поле
    textarea.click()
    textarea.fill(TEST_COMPOSITION)
    
    # Клик по кнопке "Проверить"
    page.evaluate("""
        const buttons = document.querySelectorAll('.t-btn');
        for (const btn of buttons) {
            if (btn.textContent.includes('Проверить')) {
                btn.click();
                break;
            }
        }
    """)
    
    # Ждем, пока результат точно загрузится
    page.wait_for_timeout(3000)
    
        
    # Ищем элемент, содержащий текст результата
    result_message = page.get_by_text(re.compile("Осторожно!|Поздравляем|Не рекомендуется", re.IGNORECASE)).first
        
    # Ждем, пока текст появится в элементе (игнорирует CSS-скрытие)
    expect(result_message).to_contain_text(re.compile("Осторожно!|Поздравляем|Не рекомендуется", re.IGNORECASE), timeout=15000)
        
    # Выводим текст результата в консоль
    result_text = result_message.text_content()
    print(f"\n📋 Результат проверки: {result_text}")

    # Прокручиваем страницу в самый низ, чтобы увидеть результат
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    # Оставляем браузер открытым на 3 сек для визуальной проверки
    page.wait_for_timeout(3000) 