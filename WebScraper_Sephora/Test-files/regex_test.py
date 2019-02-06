import re

html = """
<div class="css-1vwy1pm">
    <b>Which skin type is it good for?</b>
    <br/>✔ Normal
    <br/>✔ Oily
    <br/>✔ Combination
    <br/>✔ Dry
    <br/>
    <br/>
    <b>What it is:</b>
    <br/>A daily anti-aging AHA/BHA extra strength peel that combats common signs of aging to reveal radiant, smooth skin.
    <br/>
    <br/>
    <b>Solutions for:</b>
    <br/>- Dullness and uneven texture
    <br/>- Fine lines and wrinkles
    <br/>- Acne and blemishes
    <br/>- Pores
    <br/>
    <br/>
    <b>If you want to know more…</b>
    <br/> Achieve  smooth, beautiful skin in two minutes with this extra-strength version of the peel Dr. Dennis Gross uses on patients at his NYC practice.  The patented two-step formula contains seven acids, is easy and safe to use at home, and does not require any recovery time. Step one is packed with rejuvenating, powerful, yet gentle exfoliating acids. Step two controls the alpha hydroxy acid activity, delivers anti-aging actives, nourishes, and keeps skin balanced, smooth, and radiant. Skin immediately looks refreshed and perfectly prepped for a more effective skin care routine. Expect to see improved texture and diminished fine lines with continued use. 
    <br/>
    <br/>
    <b>What it is formulated WITHOUT:</b>
    <br/>- Parabens
    <br/>- Sulfates
    <br/>- Phthalates
    <br/>
    <br/>
    <b>What else you need to know:</b>
    <br/>This product is vegan and cruelty-free.
</div>
"""

html2 = """


"""

def remove_html_tags(text):
    # remove <br/>
    clean = re.compile('<br/>')
    new = re.sub(clean, '', text)
    #print(new, type(new))

    # remove bold tags and added commas
    no_front_b = new.replace("<b>", ",")
    no_end_b = no_front_b.replace("</b>", ",")
    #print(no_end_b, type(no_end_b))

    clean = re.compile('<.*?>')
    no_html_tags = re.sub(clean, '', no_end_b) 
    #print(no_html_tags, type(no_html_tags))

    no_ws = no_html_tags.replace("\n", "")
    #print(no_ws, type(no_ws))

    split = no_ws.split(",")
    # remove first blank value
    del split[0]
    return split
    #print(split, type(split))

content = remove_html_tags(html)
print(content)

########################

def what_it_is():
    if "What it is:" in content:
        what_it_is_header = content.index("What it is:")
        print(content[what_it_is_header + 1])
    else:
        print("what it is not found")

def solutions_for():
    if "Solutions for:" in content:
        solutions_for_header = content.index("Solutions for:")
        print(content[solutions_for_header + 1])
    else:
        print("solutions for not found")

def if_you_want_to_know_more():
    if "If you want to know more…" in content:
        if_you_want_to_know_more_header = content.index("If you want to know more…")
        print(content[if_you_want_to_know_more_header + 1])
    else:
        print("if you want to know more not found")

what_it_is()
solutions_for()
if_you_want_to_know_more()

####################

# 1. state start index
what_it_is_header = text.index("What it is:")
solutions_for_header = text.index("Solutions for:")
if_you_want_to_know_more_header = text.index("If you want to know more…")
# need headers for next categories
# what it is formulated without (if in and)
# what else you need to know (if in and )

what_it_is_desc_2 = []
if what_it_is_header in content:
    for each in range(what_it_is_header + 1, solutions_for_header):
        print(each)
        what_it_is_desc_2.append(each)
else:
    print("what it is not found")

what_it_is_desc_2 = []
if what_it_is_header in content:
    for each in range(what_it_is_header + 1, solutions_for_header):
        print(each)
        what_it_is_desc_2.append(each)
else:
    print("what it is not found")

# do this for other categories
# make sure last category 




what_it_is_desc = what_it_is(content)

def solutions_for(text):
    if "Solutions for:" in text:
        solutions_for_header = text.index("Solutions for:")

        # make for loop read from first index after header until 
        # index of next header

            for each in range(solutions_for_header, # index of next header)
        print(text[solutions_for_header + 1])
        solutions_desc = text[solutions_for_header + 1]
        return solutions_desc
    else:
        print("solutions for not found")
    
solutions_desc = solutions_for(content)

def if_you_want_to_know_more(text):
    if "If you want to know more…" in content:
        if_you_want_to_know_more_header = text.index("If you want to know more…")
        print(text[if_you_want_to_know_more_header + 1])
        if_you_want_to_know_more_desc = text[if_you_want_to_know_more_header + 1]
        return if_you_want_to_know_more_desc
    else:
        print("if you want to know more not found")
    
if_you_want_to_know_more_desc = if_you_want_to_know_more(content)





