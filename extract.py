import json
import re
import codecs
import threading
import requests
from headers import get_cookies, get_headers
import json2excel
import time

start_time = time.time()

def extract_large_file(page):
    with codecs.open(page + ".txt", "r+", encoding="unicode_escape") as file:
        extracted_data = []
        for line in file:
            threads = []
            # Extracting product names
            product_matches = re.finditer(r'productName"\s*:\s*"([^"]+)"', line)
            brand_matches = re.finditer(r'brand"\s*:\s*"([^"]+)"', line)
            mrp_matches = re.finditer(r'"mrp"\s*:\s*(\d+)', line)
            price_matches = re.finditer(r'"price"\s*:\s*(\d+)', line)
            additional_info_matches = re.finditer(r'"additionalInfo"\s*:\s*"([^"]+)"', line)
            category_matches = re.finditer(r'"category"\s*:\s*"([^"]+)"', line)
            search_image_matches = re.finditer(r'"searchImage"\s*:\s*"([^"]+)"', line)
            landing_page_url_matches = re.finditer(r'"landingPageUrl"\s*:\s*"([^"]+)"', line)
            product_id_matches = re.finditer(r'"productId"\s*:\s*(\d+)', line)
            rating_matches = re.finditer(r'"rating"\s*:\s*(\d+)', line)
            discount_display_label_matches = re.finditer(r'"discountDisplayLabel"\s*:\s*"\(([^"]+)\)"', line)
            sizes_match = re.search(r'"sizes"\s*:\s*"(.*?)"', line)  # Updated regex for sizes

            images_match = re.search(r'"images"\s*:\s*\[({.*?})\]', line)

            cookies = get_cookies()
            headers = get_headers()
            
            def getProductDetails(match):
                print("--------- Iterating on "+match[0].group(1)+ " ---------" )
                productDump = str(requests.get("https://www.myntra.com/" + match[7].group(1).replace("\\u002F", "/"), cookies=cookies, headers=headers).text)
                
                seller_name_matches = re.findall(r'"sellerName"\s*:\s*"([^"]+)"', productDump)
                seller_address_matches = re.findall(r'"address"\s*:\s*"([^"]+)"', productDump)
                description_matches = re.findall(r'"descriptors"\s*:\s*\[\s*{"title"\s*:\s*"description",\s*"description"\s*:\s*"([^"]+)"', productDump)
                article_attributes_matches = re.search(r'"articleAttributes"\s*:\s*({[^}]+})', productDump)
                article_attributes = {}

                if article_attributes_matches:
                      article_attributes_str = article_attributes_matches.group(1)
                      article_attributes = dict(re.findall(r'"([^"]+)"\s*:\s*"([^"]*)"', article_attributes_str))
                
                # Extract sizes
                sizes = sizes_match.group(1).split(",") if sizes_match else []
                    
                data_dict = {
                    "productName": match[0].group(1),
                    "brand": match[1].group(1),
                    "price": match[2].group(1),
                    "offer_price": match[3].group(1),
                    "product_detail": match[4].group(1),
                    "category": match[5].group(1),
                    "searchImage": match[6].group(1).replace("\\u002F", "/"),
                    "landingPageUrl": "https://www.myntra.com/" + match[7].group(1).replace("\\u002F", "/"),
                    "productId": match[8].group(1),
                    "rating": match[9].group(1),
                    "sellerName": seller_name_matches[0],
                    "sellerAddress": seller_address_matches[0].replace("\\u002F4","").replace("\\u002Fp","").replace("\\u002F",""),  # Include sellerAddress in the dictionary
                    "discountDisplayLabel": match[10].group(1),  # Include discountDisplayLabel in the dictionary
                    "description": description_matches[0].replace("\\u003Cp","").replace("\\u003C","").replace("\\u003E",""),  # Include description in the dictionary
                    "sizes": sizes,
                     "specifications": article_attributes,
                }

                # Extract image URLs
                if images_match:
                    images_str = images_match.group(1)
                    image_matches = re.finditer(r'"view"\s*:\s*"([^"]+)",\s*"src"\s*:\s*"([^"]+)"', images_str)
                    image_urls = [view.group(2).replace("\\u002F", "/") for view in image_matches]
                    data_dict["image_urls"] = image_urls
                else:
                    data_dict["image_urls"] = {}
                extracted_data.append(data_dict)
            
            for match in zip(product_matches, brand_matches, mrp_matches, price_matches, additional_info_matches, category_matches, search_image_matches, landing_page_url_matches, product_id_matches, rating_matches, discount_display_label_matches,):
                thread = threading.Thread(target=getProductDetails, args=(match,), name=match[0])
                thread.start()
                threads.append(thread)
            
            for thread in threads:
                thread.join()
                
        # Writing the extracted data to a JSON file
        with open(page + ".json", "w+") as json_file:
            json.dump(extracted_data, json_file, indent=4)
            
        json_filename = page + '.json'
        xlsx_filename = page + '.xlsx'
        json2excel.convert_json_to_xlsx(json_filename, xlsx_filename)

