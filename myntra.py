from multiprocessing import Process
from utils import get_hash_key, get_products, get_total_pages, make_request

data = (
        #  {"name": "men-ethnic-wear", "pages":2},
        {"name": "kids", "pages":3},
        # {"name": "fashion-jewellery", "pages":2},

    )
    


for keys in data:
    make_request(keys["name"],keys["pages"])

# def f1():
#        make_request(keys[0]["name"],keys[0]["pages"])

# def f2():
#        make_request(keys[1]["name"],keys[1]["pages"])

# def f3():
#        make_request(keys[2]["name"],keys[2]["pages"])
# # for key in keys:
# #     Process(target=make_request(key["name"],key["pages"])).start()

# Process(target=f1).start()
# Process(target=f2).start()
# Process(target=f3).start()