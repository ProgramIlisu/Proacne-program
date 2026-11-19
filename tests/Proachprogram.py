from playwright.sync_api import sync_playwright
import time

def test_check_cosmetics():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://proacne-program.com/check")

        ingredients_text = """Water, Cetearyl Alcohol, Caprylic/Capric Triglyceride, Persea Gratissima (Avocado) Oil, Butyrospermum Parkii (Shea) Butter, Glycerin, Potassium Cetyl Phosphate, Cyclopentasiloxane, 3-o-ethyl Ascorbic Acid, Tocopheryl Acetate, Malic Acid, Succinic Acid, Lactic Acid, Glycolic Acid, Tocopherol, Panthenol, Sodium Hyaluronate Crosspolymer, Sodium Hyaluronate, Sodium Acetylated Hyaluronate, Hydrolyzed Sodium Hyaluronate, Centella Asiatica (Gotu kola) Extract, Helianthus Annuus (Sunflower) Seed Oil, Ceteareth-20, Cera Alba, Dimethiconol, Xanthan Gum, Pentylene Glycol, Tetrasodium Glutamate Diacetate, Sodium Hydroxide, Phenoxyethanol Ethylhexylglycerin, Potassium Sorbate, Sodium Benzoate, Parfum, Hexyl Cinnamal, Linalool, CI 19140."""

        # 1. Заполняем поле ввода
        textarea = page.locator("textarea")
        textarea.wait_for(state="visible")
        textarea.press_sequentially(ingredients_text, delay=5)

        # 2. Кликаем по кнопке
        page.get_by_text("Проверить", exact=True).click()

        # 3. КЛЮЧЕВОЕ ИЗМЕНЕНИЕ: Ждём, пока страница перезагрузится и "успокоится"
        # networkidle означает, что сетевые запросы завершены
        page.wait_for_load_state('networkidle', timeout=15000)

        # 4. Прокручиваем страницу в самый низ, чтобы увидеть результат
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # 5. Небольшая пауза, чтобы результат точно отрисовался
        page.wait_for_timeout(3000)

        # Делаем скриншот для проверки
        page.screenshot(path="result_after_check.png")

        browser.close()

if __name__ == "__main__":
    test_check_cosmetics()