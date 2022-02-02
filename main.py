import flyer_template

if __name__ == '__main__':
    food_basics_bot = flyer_template.FlyerBot('https://www.foodbasics.ca/flyer.en.html')
    food_basics_data = food_basics_bot.run()
    print(len(food_basics_data))

    metro_bot = flyer_template.FlyerBot('https://www.metro.ca/en/flyer')
    metro_data = metro_bot.run()
    print(len(metro_data))