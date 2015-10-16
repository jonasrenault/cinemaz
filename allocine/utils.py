import random


class AndroidUserAgentSelector:
    
    def __init__(self):
        self.USER_AGENTS = list()

        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android {v}; fr-fr; Nexus One Build/FRF91) AppleWebKit/5{b}.{c} (KHTML, like Gecko) Version/{a}.{a} Mobile Safari/5{b}.{c}")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android {v}; fr-fr; Dell Streak Build/Donut AppleWebKit/5{b}.{c}+ (KHTML, like Gecko) Version/3.{a}.2 Mobile Safari/ 5{b}.{c}.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android 4.{v}; fr-fr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android 4.{v}; fr-fr; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android {v}; en-gb) AppleWebKit/999+ (KHTML, like Gecko) Safari/9{b}.{a}")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android {v}.5; fr-fr; HTC_IncredibleS_S710e Build/GRJ{b}) AppleWebKit/5{b}.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/5{b}.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android 2.{v}; fr-fr; HTC Vision Build/GRI{b}) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android {v}.4; fr-fr; HTC Desire Build/GRJ{b}) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android 2.{v}; fr-fr; T-Mobile myTouch 3G Slide Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android {v}.3; fr-fr; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android 2.{v}; fr-fr; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android 2.{v}; fr-fr; HTC Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/5{b}.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android 2.{v}; fr-fr; LG-LU3000 Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/5{b}.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android 2.{v}; fr-fr; HTC_DesireS_S510e Build/GRI{a}) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/{c}.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android 2.{v}; fr-fr; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android {v}.3; fr-fr; HTC Desire Build/GRI{a}) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android 2.{v}; fr-fr; HTC Desire Build/FRF{a}) AppleWebKit/533.1 (KHTML, like Gecko) Version/{a}.0 Mobile Safari/533.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android {v}; fr-lu; HTC Legend Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/{a}.{a} Mobile Safari/{c}.{a}")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android {v}; fr-fr; HTC_DesireHD_A9191 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android {v}.1; fr-fr; HTC_DesireZ_A7{c} Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/{c}.{a}")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android {v}.1; en-gb; HTC_DesireZ_A7272 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/{c}.1")
        self.USER_AGENTS.append("Mozilla/5.0 (Linux; U; Android {v}; fr-fr; LG-P5{b} Build/FRG83) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1")

    def get_user_agent(self):
        return random.choice(self.USER_AGENTS)