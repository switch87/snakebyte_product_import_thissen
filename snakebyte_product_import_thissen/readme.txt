# Snakebyte Product Import Thissen

## Overzicht
De `snakebyte_product_import_thissen` module is ontworpen om productinformatie van de Thissen-website te crawlen en op te slaan in een Odoo 15 backend-applicatie. Deze module stelt gebruikers in staat om producten te beoordelen en later te integreren in hun eigen productcatalogus.

Deze module is gescheiden van de OpenAI-functionaliteit, zodat productverrijking in een aparte module kan worden beheerd.

## Functionaliteiten
1. **Automatische Crawling**:
   - Crawlt overzichtspagina's van producten in de categorie `biljart-toebehoren` op de Thissen-website.
   - Verzamelt basisinformatie zoals naam, prijs en URL.

2. **Opslag in Odoo**:
   - Slaat producten op in een speciaal model (`thissen.product`).
   - Producten worden standaard ingesteld op de status "Pending Review".

3. **Backend Beoordeling**:
   - Producten kunnen worden beoordeeld en gemarkeerd als "Approved" of "Rejected" in de Odoo-backend.

## Vereisten
- **Odoo 15**: Zorg ervoor dat je een werkende Odoo 15-instantie hebt.
- **Python-pakketten**:
  - `selenium`
  - `webdriver-manager`
- **Browserdriver**: Google Chrome en de ChromeDriver moeten beschikbaar zijn op het systeem.

## Installatie
1. Clone de repository naar de Odoo-addons directory:
   ```bash
   git clone https://github.com/your-repo/snakebyte_product_import_thissen.git
   ```

2. Activeer de Python-omgeving en installeer de benodigde pakketten:
   ```bash
   pip install selenium webdriver-manager
   ```

3. Start Odoo opnieuw:
   ```bash
   ./odoo-bin -c odoo.conf -u snakebyte_product_import_thissen
   ```

4. Activeer de module in Odoo.

## Structuur
```plaintext
snakebyte_product_import_thissen/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── thissen_crawler.py
├── models/
│   ├── __init__.py
│   └── thissen_product.py
├── security/
│   ├── __init__.py
│   └── ir.model.access.csv
├── views/
│   ├── thissen_menu.xml
│   ├── thissen_product_view.xml
```

### Belangrijke Bestanden
- **`thissen_crawler.py`**: Bevat de Selenium-crawler voor het harvesten van productinformatie van de Thissen-website.
- **`thissen_product.py`**: Definieert het Odoo-model voor het opslaan van producten.
- **`ir.model.access.csv`**: Biedt toegangscontrole voor het productmodel.
- **`thissen_menu.xml`**: Voeg een menu-item toe in de Odoo-backend.

## Gebruik
1. **Producten Crawlen**:
   - Start het crawling-proces via een Python-script of door een geconfigureerde Odoo-knop (indien later toegevoegd).
   - Producten worden opgeslagen in de backend onder het menu-item "Thissen Products".

2. **Producten Beoordelen**:
   - Ga naar de backend onder "Thissen Products".
   - Controleer de ingevoerde producten.
   - Stel de status in op "Approved" of "Rejected".

## Toekomstige Uitbreidingen
- **OpenAI-integratie**:
  - Verrijking van productinformatie met behulp van OpenAI.
  - Automatische toewijzing van categorieën en SEO-optimalisatie.

- **Automatische Integratie**:
  - Producten goedkeuren en direct integreren in de productcatalogus.

## Bijdragen
Contributies zijn welkom! Maak een pull request of open een issue voor suggesties en bugfixes.

## Licentie
Deze module is gelicenseerd onder de MIT-licentie. Hiermee wordt commerciële exploitatie toegestaan, inclusief het vragen van geld voor de module.

---
Gemaakt door Snakebyte 🚀

