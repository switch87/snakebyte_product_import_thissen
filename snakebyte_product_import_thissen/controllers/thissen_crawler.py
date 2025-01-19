import requests
from bs4 import BeautifulSoup

class ThissenCrawler:
    def __init__(self, env):
        self.env = env

    def load_existing_products(self):
        """Laadt bestaande producten uit de database om duplicaten te vermijden."""
        existing_urls = self.env['thissen.product'].sudo().search([]).mapped('url')
        return set(existing_urls)

    def crawl_overview_pages(self):
        """Crawlt de overzichtspagina's en slaat producten op in de Odoo-database."""
        existing_products = self.load_existing_products()
        base_url = "https://www.thissen.be/nl_be/shop/category/biljart-toebehoren-1985/page/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        page = 1
        while True:
            page_url = f"{base_url}{page}"
            print(f"Fetching products from: {page_url}")

            response = requests.get(page_url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch page {page}. HTTP {response.status_code}.")
                break

            soup = BeautifulSoup(response.content, "html.parser")

            # Controleer het actieve paginanummer
            active_page_element = soup.select_one("li.page-item.active a.page-link")
            if active_page_element:
                active_page_number = int(active_page_element.text.strip())
                if active_page_number < page:
                    print(f"Active page number {active_page_number} is less than requested page {page}. Stopping.")
                    break
            else:
                print("Active page number not found. Assuming all pages are scanned.")
                break

            product_elements = soup.select(".o_wsale_products_item_title a")
            if not product_elements:
                print(f"No more products found on page {page}. Stopping.")
                break

            for product_element in product_elements:
                product_url = product_element.get("href")
                if not product_url.startswith("http"):
                    product_url = f"https://www.thissen.be{product_url}"
                if product_url in existing_products:
                    print(f"Skipping already listed product: {product_url}")
                    continue

                name = product_element.text.strip()
                price_element = product_element.find_next("span", class_="oe_currency_value")
                price = price_element.text.strip() if price_element else "No price available"

                # Product opslaan in Odoo
                self.env['thissen.product'].sudo().create({
                    'name': name,
                    'price': price,
                    'url': product_url,
                    'status': 'pending_detail_crawl'
                })
                print(f"Product saved: {name} - {price} - {product_url}")

            page += 1

    def get_product_details(self, product):
        """Crawlt een productpagina voor gedetailleerde informatie."""
        product_url = product.url
        print(f"Fetching details from: {product_url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(product_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch product page {product_url}. HTTP {response.status_code}.")
            return

        soup = BeautifulSoup(response.content, "html.parser")

        try:
            name = soup.select_one('h1[itemprop="name"]').text.strip()
            price_element = soup.select_one('.oe_currency_value')
            price = price_element.text.strip() if price_element else "No price available"
            description_element = soup.select_one('meta[name="description"]')
            description = description_element['content'].strip() if description_element else "No description available"
            sku_element = soup.select_one('.default_code')
            sku = sku_element.text.strip() if sku_element else "No SKU available"
            image_element = soup.select_one('img.product_detail_img')
            image_url = image_element['src'] if image_element else "No image available"

            # Variants and stock
            variants = []
            variant_elements = soup.select('ul.o_wsale_product_attribute li.o_variant_pills')
            if variant_elements:
                for variant in variant_elements:
                    variant_name = variant.select_one('span').text.strip()
                    variant_stock = "In Stock" if "active" in variant.get('class', []) else "Out of Stock"
                    variants.append({'variant_name': variant_name, 'stock': variant_stock})
            else:
                stock_status = "Out of Stock" if "out_of_stock" in soup.text else "In Stock"
                variants.append({'variant_name': "Default", 'stock': stock_status})

            # Update product in Odoo
            product.write({
                'name': name,
                'price': price,
                'description': description,
                'sku': sku,
                'image_url': image_url,
                'te_verbeteren_met_ai': True,  # Default true
                'variants': [(0, 0, {
                    'variant_name': v['variant_name'],
                    'stock': v['stock']
                }) for v in variants],
                'status': 'pending_review'
            })
            print(f"Updated product: {name}")
        except Exception as e:
            print(f"Error processing product {product_url}: {e}")

    def crawl_detailed_pages(self):
        products = self.env['thissen.product'].sudo().search([('status', '=', 'pending_detail_crawl')])
        if not products:
            print("No products to process for detailed crawl.")
            return
    
        batch_size = 10  # Verwerk 10 producten per batch
        for i in range(0, len(products), batch_size):
            batch = products[i:i + batch_size]
            print(f"Processing batch {i // batch_size + 1} with {len(batch)} products.")
            for product in batch:
                self.get_product_details(product)
    
        print("Detailed crawl completed.")
    
