multiples = list(range(48, 1104, 48))
print(multiples)
for each in multiples:
    url = "https://www.ulta.com/skin-care-cleansers?N=2794&No={}&Nrpp=48".format(each)
    print(url)
