import csv
import time
from datetime import date
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--headless')
chrome_options.add_argument('window-size=1440x900')

driver = webdriver.Chrome(options=chrome_options)

list = ['https://reissue.co/product/the-ordinary-niacinamide-10----zinc-1-', 'https://reissue.co/product/cosrx-low-ph-good-morning-gel-cleanser', 'https://reissue.co/product/thayer-s-alcohol-free-rose-petal-witch-hazel-toner', 'https://reissue.co/product/pixi-glow-tonic', 'https://reissue.co/product/the-ordinary-aha-30----bha-2--peeling-solution', 'https://reissue.co/product/cosrx-acne-pimple-master-patch', 'https://reissue.co/product/cosrx-advanced-snail-96-mucin-power-essence', 'https://reissue.co/product/cosrx-aloe-soothing-sun-cream-spf50-pa---', 'https://reissue.co/product/drunk-elephant-c-firma--day-serum', 'https://reissue.co/product/cosrx-x-soko-glam-triple-c-lightning-liquid', 'https://reissue.co/product/the-ordinary-hyaluronic-acid-2----b5', 'https://reissue.co/product/aztec-secret-indian-healing-clay-deep-pore-cleansing', 'https://reissue.co/product/the-ordinary-100--organic-cold-pressed-rose-hip-seed-oil', 'https://reissue.co/product/drunk-elephant-b-hydra-intensive-hydration-gel', 'https://reissue.co/product/cetaphil-gentle-skin-cleanser', 'https://reissue.co/product/the-ordinary-glycolic-acid-7--toning-solution', 'https://reissue.co/product/hada-labo-goku-jyun-hyaluronic-acid-moist-lotion', 'https://reissue.co/product/cerave-hydrating-cleanser', 'https://reissue.co/product/drunk-elephant-t-l-c--sukari-babyfacial-', 'https://reissue.co/product/krave-beauty-matcha-hemp-hydrating-cleanser', 'https://reissue.co/product/glossier-milky-jelly-cleanser', 'https://reissue.co/product/dr--jart-cicapair-tiger-grass-color-correcting-treatment', 'https://reissue.co/product/herbivore-blue-tansy-resurfacing-clarity-mask', 'https://reissue.co/product/belif-the-true-cream-aqua-bomb', 'https://reissue.co/product/hada-labo-goku-jyun-premium-hyaluronic-acid-lotion', 'https://reissue.co/product/laneige-lip-sleeping-mask', 'https://reissue.co/product/cosrx-salicylic-acid-daily-gentle-cleanser', 'https://reissue.co/product/-bio-oil--bio-oil', 'https://reissue.co/product/nature-republic-soothing---moisture-aloe-vera-92--soothing-gel', 'https://reissue.co/product/klairs-freshly-juiced-vitamin-drop', 'https://reissue.co/product/the-ordinary-alpha-arbutin-2----ha', 'https://reissue.co/product/glow-recipe-watermelon-glow-sleeping-mask', 'https://reissue.co/product/krave-beauty-beat-the-sun-spf47-pa----', 'https://reissue.co/product/garnier-micellar-water-all-in-1-cleansing-water', 'https://reissue.co/product/glossier-solution', 'https://reissue.co/product/drunk-elephant-protini--polypeptide-cream', 'https://reissue.co/product/biologique-recherche-exfoliating-lotion-p50', 'https://reissue.co/product/neutrogena--hydro-boost-water-gel', 'https://reissue.co/product/drunk-elephant-shaba-complex--eye-serum', 'https://reissue.co/product/cerave-pm-facial-moisturizing-lotion', 'https://reissue.co/product/whamisa-organic-flowers-toner-deep-rich', 'https://reissue.co/product/ole-henriksen-banana-bright--eye-cr-me', 'https://reissue.co/product/biore--uv-aqua-rich-watery-essence-sunscreen-spf50--pa---', 'https://reissue.co/product/caudalie-instant-detox-mask', 'https://reissue.co/product/sunday-riley-u-f-o-ultra-clarifying-face-oil', 'https://reissue.co/product/the-ordinary-azelaic-acid-suspension-10-', 'https://reissue.co/product/cosrx-hyaluronic-acid-hydra-power-essence', 'https://reissue.co/product/the-body-shop-tea-tree-oil', 'https://reissue.co/product/herbivore-jasmine-green-tea-balancing-toner', 'https://reissue.co/product/vichy-min-ral-89-hyaluronic-acid-face-moisturizer', 'https://reissue.co/product/clinique-moisture-surge-72-hour-auto-replenishing-hydrator', 'https://reissue.co/product/mario-badescu-facial-spray-with-aloe--herbs-and-rosewater', 'https://reissue.co/product/the-ordinary-salicylic-acid-2--solution', 'https://reissue.co/product/sunday-riley-saturn-sulfur-acne-treatment-mask', 'https://reissue.co/product/cosrx-bha-blackhead-power-liquid', 'https://reissue.co/product/lush-mask-of-magnaminty', 'https://reissue.co/product/kiehl-s-calendula-herbal-extract-alcohol-free-toner', 'https://reissue.co/product/klairs-midnight-blue-calming-cream', 'https://reissue.co/product/the-ordinary-caffeine-solution-5----egcg', 'https://reissue.co/product/hada-labo-goku-jyun-hyaluronic-acid-light-lotion', 'https://reissue.co/product/avene-thermal-spring-water', 'https://reissue.co/product/mario-badescu-anti-acne-serum', 'https://reissue.co/product/summer-fridays-jet-lag-mask', 'https://reissue.co/product/farmacy-green-clean', 'https://reissue.co/product/pyunkang-yul-essence-toner', 'https://reissue.co/product/dr-dennis-gross-alpha-beta-extra-strength-daily-peel---packettes', 'https://reissue.co/product/clinique-dramatically-different-moisturizing-gel', 'https://reissue.co/product/innisfree-super-volcanic-pore-clay-mask', 'https://reissue.co/product/saturday-skin-featherweight-daily-moisturizing-cream', 'https://reissue.co/product/cosrx-ultimate-nourishing-rice-overnight-spa-mask', 'https://reissue.co/product/kiehl-s--midnight-recovery-concentrate', 'https://reissue.co/product/cosrx-aha-bha-clarifying-treatment-toner', 'https://reissue.co/product/cosrx-ultimate-moisturizing-honey-overnight-mask', 'https://reissue.co/product/the-ordinary-natural-moisturizing-factors---ha', 'https://reissue.co/product/the-body-shop-skin-defence-multi-protection-essence-spf50', 'https://reissue.co/product/biossance-100--squalane-oil', 'https://reissue.co/product/garnier-micellar-water-all-in-1-cleansing-water-waterproof-make-up', 'https://reissue.co/product/neutrogena-hydro-boost-hydrating-100--hydrogel-mask', 'https://reissue.co/product/cosrx-two-in-one-poreless-power-liquid', 'https://reissue.co/product/kiehl-s--rare-earth-deep-pore-cleansing-face-mask', 'https://reissue.co/product/glossier-priming-moisturizer', 'https://reissue.co/product/saturday-skin-wide-awake-brightening-eye-cream', 'https://reissue.co/product/the-ordinary-lactic-acid-10----ha', 'https://reissue.co/product/benton-snail-bee-high-content-essence', 'https://reissue.co/product/kiehl-s-creamy-eye-treatment-with-avocado', 'https://reissue.co/product/the-ordinary-lactic-acid-5----ha', 'https://reissue.co/product/la-roche-posay-thermal-spring-water', 'https://reissue.co/product/bioderma-sensibio-micellar-water', 'https://reissue.co/product/glossier-super-pure', 'https://reissue.co/product/mario-badescu-enzyme-cleansing-gel', 'https://reissue.co/product/the-face-shop-jeju-volcanic-lava-self-heating-clay-mask', 'https://reissue.co/product/hada-labo-goku-jyun-cleansing-oil', 'https://reissue.co/product/clinique-take-the-day-off-cleansing-balm', 'https://reissue.co/product/benton-aloe-bha-skin-toner', 'https://reissue.co/product/biossance-squalane---vitamin-c-rose-oil', 'https://reissue.co/product/heimish-all-clean-balm', 'https://reissue.co/product/origins-ginzing-energy-boosting-gel-moisturizer', 'https://reissue.co/product/laneige-water-sleeping-mask', 'https://reissue.co/product/yes-to-detoxifying-charcoal-2-in-1-scrub---cleanser-stick', 'https://reissue.co/product/tatcha-luminous-dewy-skin-mist']

def productInfo(list_from_scroll):
    """ gets item link, brand, name, ph, ingredients, and product image """

    with open('Reissue_{}.csv'.format(date.today()), 'w') as f:
        file_csv = csv.writer(f)
        file_csv.writerow(['Brand', 'Product Name', 'pH', 'Ingredients', 'Image Link', 'Item Link'])

        for each in list_from_scroll:
            driver.get(each)
            print(each, '')

            time.sleep(10)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(10)
            
            # item, brand, title, ph
            item_link = driver.current_url
            product_brand = driver.find_element_by_class_name('productPage__brand').text
            product_title = driver.find_element_by_class_name('productPage__name').text
            ph_level = driver.find_element_by_xpath("//text()[. = 'PH Level']/following::p").text

            # ingredients
            try:
                driver.find_element_by_class_name("notableIngredients__view-all").click()
                #driver.find_element_by_class_name('notableIngredients__view-all').send_keys(Keys.RETURN)
                time.sleep(10)
                ingredients = driver.find_element_by_xpath("//text()[. = 'Full ingredients']/following::p").text 
            
            except NoSuchElementException:
                ingredients = ""
                pass

            # image
            image_link = driver.find_element_by_class_name('productPage__img').get_attribute('src')

            print(item_link, product_brand, product_title, ph_level, ingredients, image_link, "")

            file_csv.writerow([product_brand, product_title, ph_level, ingredients, image_link, item_link])

productInfo(list)

print('File created: ', 'Reissue_{}.csv'.format(date.today()))