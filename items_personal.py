import helpers, user



class Items():


    def __init__(self):
        pass

    def get_item_info(self):

        item_results = []
        #set data frame and make column list
        df = helpers.pd.read_csv(r'C:\Users\rford\Desktop\items.csv')
        #stops pandas from reading csv as floats
        data = df.fillna(0)
        item_ids = data['Item Numbers'].astype(int).tolist()
        #get saleManager.php
        for item_id in item_ids:
            #Navigate to item    
            helpers.driver.get("https://www.####.com/manager/entry.php?area=general&id={}".format(item_id))
            helpers.WebDriverWait(helpers.driver,10)
            try:
                #Click 'Yes' on 'Are you sure you want to continue' view
                helpers.driver.find_element_by_css_selector('#form1 > div > input[type=submit]:nth-child(2)').click()
                helpers.WebDriverWait(helpers.driver, 5)
            except helpers.NoSuchElementException:
                pass
            #Get Name
            name = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[1]/td[1]/textarea').text
            #Get Quick Book Name
            qb_name = helpers.driver.find_element_by_name('items[qbname]').get_attribute('value') or " N/A"
            # Get Inventory availability
            qty_available = helpers.driver.find_element_by_xpath('/html/body/form/div/table/tbody/tr[2]/td[1]/b').text[-5:]
            #Parse qty_available to pull only integers
            available = ''.join(filter(lambda i: i.isdigit(), qty_available))
            # Get MSRP
            msrp = helpers.driver.find_element_by_name('items[retail]').get_attribute('value') or " N/A "
            # Get cost depending on what type of Element displays it
            try:
                cost = helpers.driver.find_element_by_name('items[cost]').get_attribute('value') or " N/A "
            except helpers.NoSuchElementException:
                cost = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[4]/td[2]').text or " N/A "
            except helpers.NoSuchElementException:
                cost = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[4]/td[2]/input').text or " N/A "
            #Get FSP
            fsp =  helpers.driver.find_element_by_name('items[salecost]').get_attribute('value') or " N/A "
            #Get Price
            price = helpers.driver.find_element_by_name('items[price]').get_attribute('value') or " N/A "
            # Grab list of product Length Options & Set Length
            product_length_options = helpers.Select(helpers.driver.find_element_by_name('items[clen]'))
            length = product_length_options.first_selected_option.text
            # Grab list of product Gauge Options & Set Gauge
            gauge_length_options = helpers.Select(helpers.driver.find_element_by_name('items[cdiam]'))
            gauge = gauge_length_options.first_selected_option.text
            # Grab list of product Packaging Types & Set Type
            packaging_type_options = helpers.Select(helpers.driver.find_element_by_name('items[cpack]'))
            packaging_type = packaging_type_options.first_selected_option.text
            # Grab list of product Box Count & Set Count
            stick_count_options = helpers.Select(helpers.driver.find_element_by_name('items[ccount]'))
            stick_count = stick_count_options.first_selected_option.text
            #Grab list of Availabilities & Set Availability
            availability_options = helpers.Select(helpers.driver.find_element_by_name('items[availid]'))
            availability = availability_options.first_selected_option.text
            #get Variety Pack timing and status
            try:
                variety_pack_status = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[2]/td[3]/div/p[2]').text
                variety_pack_expiration = helpers.driver.find_element_by_id('varietyPackTimer').text
            except helpers.NoSuchElementException:
                variety_pack_expiration = "N/A"
                variety_pack_status = "N/A"
            #Add data to results list
            item_results.append([item_id, name, qb_name, available, cost, price, msrp, fsp, length, gauge, packaging_type, stick_count, availability, variety_pack_expiration, variety_pack_status])
            #print info gathered into Terminal
            print(str(item_id) + " " + str(name) + " " + str(qb_name) + " " + str(available) + " " +  str(cost) + " " +  str(price) + " " + str(msrp) + " " + str(fsp) + " " + str(length) + " " + str(gauge) + " " + str(packaging_type) + " " + str(stick_count) + " " + str(availability + " " + str(variety_pack_expiration + " " + str(variety_pack_status))))
        print('Item Info Data Gathered!')
        helpers.driver.quit()
        #Write items list to csv
        with open(r'C:\Users\rford\Desktop\item_info.csv', 'w+', newline='', encoding="utf-8") as file:
                writer = helpers.csv.writer(file) 
                writer.writerows(item_results)
                print('Finished Item_Info.csv')
        #Set Columns for CSV
        df = helpers.pd.read_csv(r'C:\Users\rford\Desktop\item_info.csv', header=None, index_col=None)
        df.columns = ['ID', 'Name', 'QB Name', 'Inventory', 'Cost', 'Retail', 'MSRP', 'FSP', 'Length', 'Gauge', 'Packaging', 'Stick Count', 'Availability', "V-Pack Exp", "V-Pack Status"]
        df.to_csv(r'C:\Users\rford\Desktop\item_info.csv', index=False)

    def set_free_ship(self):
        #set data frame and make column list
        df = helpers.pd.read_csv(r'C:\Users\rford\Desktop\items.csv')
        #stops pandas from reading csv as floats
        data = df.fillna(0)
        item_ids = data['Item Numbers'].astype(int).tolist()
        #for each id in list of ids
        for item_id in item_ids:
            helpers.WebDriverWait(helpers.driver, 5)  
            #Navigate to item    
            helpers.driver.get("https://www.####.com/manager/entry.php?area=general&id={}".format(item_id))
            helpers.WebDriverWait(helpers.driver, 10)
            try:
                #Click 'Yes' on 'Are you sure you want to continue' view
                helpers.driver.find_element_by_css_selector('#form1 > div > input[type=submit]:nth-child(2)').click()
                helpers.WebDriverWait(helpers.driver, 5)
            except helpers.NoSuchElementException:
                pass
            #Get Name
            helpers.WebDriverWait(helpers.driver, 5)  
            name = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[1]/td[1]/textarea').text
            is_free_ship = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[2]/td[1]/input[16]')
            save = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/input[6]')
            #check free ship if not checked
            if is_free_ship.is_selected():
                pass
            else:
                is_free_ship.click()
            save.click()
            print(name + ' has been set to Free Shipping')
        print('All Items have been set Successfully!')

    def set_to_online(self):
        #set data frame and make column list
        df = helpers.pd.read_csv(r'C:\Users\rford\Desktop\items.csv')
        #stops pandas from reading csv as floats
        data = df.fillna(0)
        item_ids = data['Item Numbers'].astype(int).tolist()
        #for each id in list of ids
        for item_id in item_ids:
            helpers.WebDriverWait(helpers.driver, 5)  
            #Navigate to item    
            helpers.driver.get("https://www.####.com/manager/entry.php?area=general&id={}".format(item_id))
            helpers.WebDriverWait(helpers.driver, 10)
            try:
                #Click 'Yes' on 'Are you sure you want to continue' view
                helpers.driver.find_element_by_css_selector('#form1 > div > input[type=submit]:nth-child(2)').click()
                helpers.WebDriverWait(helpers.driver, 5)
            except helpers.NoSuchElementException:
                pass
            #Get Name
            name = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[1]/td[1]/textarea').text
            helpers.WebDriverWait(helpers.driver, 5)  
            #get check box inputs
            is_sold_online = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[2]/td[1]/input[8]')
            is_sellable = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[2]/td[1]/input[10]')
            save = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/input[6]')
            #check box if box is not checked
            if is_sold_online.is_selected():
                pass
            else:
                is_sold_online.click()
            if is_sellable.is_selected():
                pass
            else:
                is_sellable.click()
            save.click()
            print(name + ' has been put online')
        print('All Items have been put online!')

    def append_to_name(self):
        #set data frame and make column list
        df = helpers.pd.read_csv(r'C:\Users\rford\Desktop\items.csv')
        #stops pandas from reading csv as floats
        data = df.fillna(0)
        item_ids = data['Item Numbers'].astype(int).tolist()
        #for each id in list of ids
        for item_id in item_ids:
            helpers.WebDriverWait(helpers.driver, 5)  
            #Navigate to item    
            helpers.driver.get("https://www.####.com/manager/entry.php?area=general&id={}".format(item_id))
            helpers.WebDriverWait(helpers.driver, 10)
            try:
                #Click 'Yes' on 'Are you sure you want to continue' view
                helpers.driver.find_element_by_css_selector('#form1 > div > input[type=submit]:nth-child(2)').click()
                helpers.WebDriverWait(helpers.driver, 5)
            except helpers.NoSuchElementException:
                pass
            #Get Name
            textbox = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[1]/td[1]/textarea')
            name = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[1]/td[1]/textarea').text
            helpers.WebDriverWait(helpers.driver, 5)  
            text_being_added = input("Enter the Text that will be appended to Item Name: \n ")
            textbox.clear()
            textbox.send_keys(name + " - " + text_being_added)
            save = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/input[6]')
            save.click()
            helpers.WebDriverWait(helpers.driver, 5)
            print(name + ' has been updated to ' + name + " - " + text_being_added)
        print('All Item Names have been updated')
        helpers.driver.quit()
 
    def get_flavor_type(self):
            item_results = []
            #set data frame and make column list
            df = helpers.pd.read_csv(r'C:\Users\rford\Desktop\items.csv')
            #stops pandas from reading csv as floats
            data = df.fillna(0)
            item_ids = data['Item Numbers'].astype(int).tolist()
            #for each id in list of ids
            for item_id in item_ids:
                helpers.WebDriverWait(helpers.driver, 5)  
                #Navigate to item    
                helpers.driver.get("https://www.####.com/manager/entry.php?area=general&id={}".format(item_id))
                helpers.WebDriverWait(helpers.driver, 10)
                try:
                    #Click 'Yes' on 'Are you sure you want to continue' view
                    helpers.driver.find_element_by_css_selector('#form1 > div > input[type=submit]:nth-child(2)').click()
                    helpers.WebDriverWait(helpers.driver, 5)
                except helpers.NoSuchElementException:
                    pass
                #Get Name
                name = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[1]/td[1]/textarea').text
                helpers.WebDriverWait(helpers.driver, 5)  
                is_coffee = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td[2]/select/option[11]')
                is_mocha = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td[2]/select/option[20]')
                is_mocha_mint = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td[2]/select/option[21]')
                is_cap = helpers.driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td[2]/select/option[7]')
                #if coffee get name
                if is_coffee.is_selected():
                    print(item_id)
                    flavor = "coffee"
                    item_results.append([item_id, name, flavor])
                else:
                    pass
                if is_mocha.is_selected():
                    print(item_id)
                    flavor = "mocha"
                    item_results.append([item_id, name, flavor])
                else:
                    pass
                
                if is_mocha_mint.is_selected():
                    print(item_id)
                    flavor = "Mocha Mint"
                    item_results.append([item_id, name, flavor])
                else:
                    pass

                if is_cap.is_selected():
                    print(name + " is cap")
                    flavor = "Cappucino"
                    item_results.append([item_id, name, flavor])
                else:
                    pass

            print('All Items checked for flavor')
            print(item_results)
            with open(r'C:\Users\rford\Desktop\item_flavor_info.csv', 'w+', newline='', encoding="utf-8") as file:
                writer = helpers.csv.writer(file) 
                writer.writerows(item_results)
                print('Finished Item_flavor_Info.csv')
            df = helpers.pd.read_csv(r'C:\Users\rford\Desktop\item_flavor_info.csv', header=None, index_col=None)
            df.columns = ['ID', 'Name', 'Flavor']
            df.to_csv(r'C:\Users\rford\Desktop\item_flavor_info.csv', index=False)

items = Items()

while True:
    try:
        answer = int(input("Choose function: \n1: Get Item Info \n2: Set Free Shipping \n3: Set Items Online \n4: Append Text To Name \n\n"))
        if answer == 1:
            items.get_item_info()
            continue
        elif answer == 2:
            items.set_free_ship()
            continue
        elif answer == 3:
            items.set_to_online()
            continue
        elif answer == 4:
            items.append_to_name()
            continue
    except ValueError:
        print("Please enter correct command")
        continue