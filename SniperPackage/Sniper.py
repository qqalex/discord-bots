import os
import requests_async as requests   # Need to rewrite using aiohttp, as current package doesn't support proxies + it suxxx ://///
import asyncio
import pause                        # Redundant, can use a simple function instead. == less reliance == more control
                                    # Eventually look into making this all dockerized and using NUMBA

class credentials:

    def __init__(self):
        # Discord verification tokens
        self.verification_bot_token = "MTA2OTE2ODA2OTAyNjUyNTIwNA.Gmj87y.wrLxx0Gm_eZa0BJZ4En55YMC4Q6njGbGqnkamc"
        self.dog_bot_token = "MTA2OTE2ODA2OTAyNjUyNTIwNA.Gmj87y.wrLxx0Gm_eZa0BJZ4En55YMC4Q6njGbGqnkamc"
        
        # Proxy authentication credentials     username:creds@rotating-address
        self.proxy = {'http':'minecat:5d86f4-e1a8a9-a211fd-5f7e38-23741a@usa.rotating.proxyrack.net:9000'}

class watchdog:

    def __init__(self):
        self.watchdog_file_name = 'wd/watchdog'

        if os.path.isfile(self.watchdog_file_name):
            pass
        else:
            open(self.watchdog_file_name, 'w')

        self.watchdog_file_read = open(self.watchdog_file_name, 'r')
        self.watchdog_list = self.__loadList()

    def __loadList(self):
        list = self.watchdog_file_read.readlines()
        for i in range(len(list)-1):
            list[i] = list[i].strip()
        
        return list

    def __checkDuplicates(self, name):
        list = self.watchdog_list

        if name in list:
            return 1
        else:
            return 0

    def __listWrite(self):
        list_string = ''

        file = open(self.watchdog_file_name, 'w')
        list = self.watchdog_list

        last_index = len(list)-1
        for i in list:
            if i == list[last_index]:
                list_string += f'{i}'
            else:
                list_string += f'{i}\n'

        file.write(list_string)

    def Watch(self, name):
        name = name.lower()
        if self.__checkDuplicates(name):
            return 1
        else:
            pass

        self.watchdog_list.append(name)
        self.__listWrite()
        
        return 0

    def Ignore(self, name):
        name = name.lower()
        if self.__checkDuplicates(name):
            pass
        else:
            return 0

        self.watchdog_list.remove(name)
        self.__listWrite()

class nameSniper:

    def __init__(self, dropTime, proxies= None):

        # Request info
        self.nameChangeEndpoint = 'https://api.minecraftservices.com/minecraft/profile/name/'
        self.createProfileEndpoint = 'https://api.minecraftservices.com/minecraft/profile/'
        self.authHeader = None
        self.drop_time = dropTime

        # Proxy information
        self.proxies = proxies

        # Timings
        self.adjustment = -2

    def __defAuthHeader(self, token):

        self.authHeader = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }

    async def __nameChangeRequest(self, username):

        if self.proxies is None:
            if self.gamepassAccount is not None:
                return await requests.post(self.createProfileEndpoint, headers= self.authHeader, json= {"profileName": username}, proxies= self.proxies)
            else:
                return await requests.put(self.nameChangeEndpoint + username, headers= self.authHeader, proxies= self.proxies, verify = False)

        else:
            if self.gamepassAccount is not None:
                print(self.createProfileEndpoint)
                print(self.authHeader)
                print(username)
                print(self.proxies)
                return await requests.post(self.createProfileEndpoint, headers= self.authHeader, json= {"profileName": username}, proxies= self.proxies)
            else:
                return await requests.put(self.nameChangeEndpoint + username, headers= self.authHeader, proxies= self.proxies, verify = False)

    async def __snipeLoop(self, username):
        while True:
            response = await self.__nameChangeRequest(username)
            if response.status_code == 200:
                print(f'Successfully sniped {username}')
            else:
                print(response.text)
                print(response.status_code)

    def snipe(self, username, token, gamepassAccount= None):
        self.gamepassAccount = gamepassAccount

        self.__defAuthHeader(token)

        pause.until(self.drop_time + self.adjustment)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__snipeLoop(username))
        loop.close()