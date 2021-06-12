# RoatpkzMoneyPrinter
 An anonymous, synchronous, mule-ready automatic vote bot for RoatPkz, with support for auto-rotating proxies and captcha solvers.
 
I have been using this script on autopilot for about three years now, but I don't have time to harvest any of the mules or avoid consistant RWT bans anymore, so I'd like to pass it on to whoever else would like to continue wrecking their economy. 


# Features

**Completely Automated**

The bot votes on the required voting websites, then loops back to the Roatpkz website and auto-claims the vote for your mule. No intervention is required.

**Anti-Anti Botting Measures**

Runelocus has 10-second countdown timer before the captcha shows up that slows down the bot significantly. Weirdly though, they download the captcha immiedietly as you load the website. The bot exploits this by ignoring the countdown and sniffing the captcha straight from the chromedriver network requests tab.

RSPS-List rejects normal recaptcha tokens, and decide to change them somewhat to their own "format" by POSTing it to their PHP script and using the response as the token. To work around this, the bot simply encodes it's own 2captcha response through their own channel and submits it just like their actual website does.

**Mule-Ready**

This bot can run concurrently with all of your mules, voting for every one of them all at once, meaning you don't have to risk banning your main/RWTing account. If you have more than 20 bots though, I do reccomend buying a VPS with an AMD Epyc/Threadripper (you only need to rent it for about 10 minutes twice a day, very cheap!) with sufficient RAM to keep all of the chrome tabs running smoothly. Two sites need to be loaded for each bot (roatpkz vote claim and the current voting site), so with 50 bots, you will need to be able to run 100 chrome tabs without paging.


# Profitability Analysis

Each vote gives each mule one vote box and one vote ticket. With 55 mules and voting twice per day (one every 12 hours), each mule gains two vote boxes and two vote tickets every day, stacking in their queue until claimed. Since vote boxes are worth ~900pkp and vote points are worth ~1500pkp, this will be netting a total of 264,000pkp minted out of thin air every day, assuming no bans and no RWT issues.

The current price is about 10m OSRS for every 100k RoatPkz PKP, and the current OSRS GP price is about $0.45 USD per 1m. This amounts to about $11.88 USD per day, all automatic except for harvests. If you have higher quality rotating proxies, more mules, and more time to harvest, you may get much higher profits than mine.

# How To Use

You will need to have very high quality rotating proxies to use the bot. My personal reccomendation is [LinkProxy](https://discord.com/invite/vWc6NkWtbb), his proxies are extremely fast, reliable and cheap, costing about $2.8/GB if you buy 25GB. I am not affiliated with his service, I just haven't found anything nearly as good.

Each vote website requires a captcha to be solved before registering your partial vote. To bypass these automatically, you should sign up to [2captcha](https://2captcha.com/) and paste your API key into the API_KEY variable. Next, you will need to download [chromedriver](https://chromedriver.chromium.org/downloads) and paste the path to the file under path_to_chromedriver. You will also need to manually sign up for as many mule accounts on Roatpkz as you'd like. 


# 2captcha Roadblocks

The workers at 2captcha are great at solving Google's recaptcha and such, but they don't seem to be very good at specifically the custom request for Runelocus's captcha. Here's an example of what they are given:

**How many video game objects are shown over the handwashing image? (1 to 5, objects can overlap)**

![](https://i.gyazo.com/057ab4181b01c4149a7729ad6fae9080.png)

The answer is 4, but workers who aren't very familiar with video game objects might not see the difference between the lamp and the log and therefore answer "3". This happens a lot due to overlapping objects, leading the success rate to be about 40% in my experience. 

The bot will keep trying the captcha after every failed response from the workers, but it does cost you a small amount every time, wastes bandwidth, and most importantly wastes your time. If you can think of a better way to word the captcha for the workers, you'll be able to solve this issue.

If you don't want to deal with this, there is commented code for tkinter that will pop the captcha up in a window and let you manually input the answer to each one, but this will require manual intervention for every vote.