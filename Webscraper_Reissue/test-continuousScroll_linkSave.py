def scrollUntilNoNewElementsWithContinuousSave():
    """ same as scrollUntilNoNewElements() but with continuous save"""

    time.sleep(3)

    SCROLL_PAUSE_TIME = 1
    
    last_height = driver.execute_script("return document.body.scrollHeight")

    old_num_of_links = len(driver.find_elements_by_xpath("//a[contains(@href, \
                                                '/product/')]"))

    list_links = []

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        new_num_of_links = len(driver.find_elements_by_xpath("//a[contains(@href, \
                                            '/product/')]"))

        list_links = []

        if new_height == last_height:
            print('\n', "done scrolling", '\n')

            if new_num_of_links == old_num_of_links:
                print('\n', 'no new links', '\n')
                break

            else:
                list_of_website_links = driver.find_elements_by_xpath("//a[contains(@href, \
                                                '/product/')]")
                                                
                for link in list_of_website_links(old_num_of_links : new_num_of_links + 1):
                    ind_link = link.get_attribute('href')  
                    list_links.append()

        else:
            list_of_website_links = driver.find_elements_by_xpath("//a[contains(@href, \
                                                '/product/')]")

            for link in list_of_website_links(old_num_of_links : new_num_of_links + 1):
                ind_link = link.get_attribute('href')  
                list_links.append()

        last_height = new_height
        old_num_of_links = new_num_of_links

    
        
    