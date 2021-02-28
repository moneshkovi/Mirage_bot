from __future__ import annotations
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from PIL import Image, ImageOps, ImageDraw
import random
import asyncpg
import ssl
ctx = ssl.create_default_context(cafile='rds-combined-ca-bundle.pem')
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
class Database:
    def __init__(self, loop, user: str, password: str) -> None:
        self.user = user
        self.password = password
        loop.create_task(self.connect())

    async def connect(self) -> None:
        self.conn = await asyncpg.connect(user=self.user, password=self.password, database='d9m1ilmuvnuaka', host='ec2-52-20-66-171.compute-1.amazonaws.com',ssl=ctx)
        await self.conn.close()
        self.conn = await asyncpg.connect(user=self.user, password=self.password, database='d9m1ilmuvnuaka', host='ec2-52-20-66-171.compute-1.amazonaws.com',ssl=ctx)
        await self.conn.fetch('CREATE TABLE IF NOT EXISTS users (id TEXT NOT NULL, rank INT NOT NULL, xp INT NOT NULL)')

    async def fetch(self, sql: str) -> list:
        return await self.conn.fetch(sql)


class Rank:
    def __init__(self) -> None:
        self.font = ImageFont.truetype('arialbd.ttf', 42)
        self.medium_font = ImageFont.truetype('arial.ttf', 34)
        self.medium_bold_font = ImageFont.truetype('arialbd.ttf', 34)
        self.small_font = ImageFont.truetype('arialbd.ttf', 24)
        self.rank_font = ImageFont.truetype('arialbd.ttf', 28)
        self.very_small_font = ImageFont.truetype('arialbd.ttf',22)
    def draw(self, user: str, rank: str, xp: str, profile_bytes: BytesIO) -> BytesIO:
        profile_bytes = Image.open(profile_bytes)
        bg = Image.open('codm.png')
        bg.resize((100,100))


        profile_bytes = profile_bytes.resize((120,120), Image.ANTIALIAS)
        bigsize = (profile_bytes.size[0] * 3, profile_bytes.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(profile_bytes.size, Image.ANTIALIAS)
        profile_bytes.putalpha(mask)
        output = ImageOps.fit(profile_bytes, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        im = Image.new('RGBA', (650, 850), (44, 44, 44, 255))
        im.paste(bg, (0, 0), bg)
        im_draw = ImageDraw.Draw(im)
        w, h = im_draw.textsize(user, font=self.rank_font)
        print(w)
        im_draw.text((250+(200-w)/2, 330), user, font=self.rank_font, fill=(255, 255, 255, 255))

        rank_text = f'RANK {rank}'
        im_draw.text((100, 360), rank_text, font=self.rank_font, fill=(255, 255, 255, 255))

        needed_xp = self.neededxp(rank)
        xp_text = f'{xp}/{needed_xp}'
        im_draw.text((300, 380), xp_text, font=self.small_font, fill=(255, 255, 255, 255))

        im_draw.rectangle((250, 380, 450, 370), fill=(64, 64, 64, 255))
        im_draw.rectangle((250, 380, 250+(int(xp/needed_xp*100))*2, 370), fill=(221, 221, 221, 255))
        im_draw.rectangle((250+(int(xp/needed_xp*100))*2, 380, 250+(int(xp/needed_xp*100))*2+3, 370), fill=(255, 0, 0, 255))
        im_draw.text((0, 480), "Level Role", font=self.font, fill=(255, 255, 255, 255))
        im_draw.text((0, 600), "Next Reward", font=self.font, fill=(255, 255, 255, 255))
        linew = 770
        quotes = ["if you want it, work for it.", "Nothing Lasts forever.", "No guts, no story.", "Stay hungry.Stay foolish", "Dream big.Pray Bigger.", "Fight till the last gasp", " Enjoy the little things", " Keep going. Be all in. ", " Screw it, let's do it. ", " Take the risk or loose the chance. ",  "Feel the fear & do it anyway. ", " Never stop dreaming. "]
        if rank < 5:
            im_draw.text((0, 540), "No Level Reached Yet", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 660), "Enthusiast", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 720), "• Ability to post media in media channel", font=self.very_small_font, fill=(255, 255, 255, 255))
            #im_draw.text((0, 720), "• Reward 2", font=self.medium_font, fill=(255, 255, 255, 255))
        elif rank >= 5 and rank < 15:
            im_draw.text((0, 540), "Enthusiast", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 660), "Rookie", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 720), "• Ability to use External emojies", font=self.very_small_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 750), "• Obtain a coloured name", font=self.very_small_font, fill=(255, 255, 255, 255))
        elif rank >= 15 and rank < 25:
            im_draw.text((0, 540), "Rookie", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 660), "Veterain", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 720), "• Ability to react messages", font=self.very_small_font, fill=(255, 255, 255, 255))
            #im_draw.text((0, 720), "• Reward 2", font=self.very_small_font, fill=(255, 255, 255, 255))
        elif rank >= 25 and rank < 35:
            im_draw.text((0, 540), "Veterain", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 660), "Elite", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 720), "• Ability to share scrren & live stream", font=self.very_small_font, fill=(255, 255, 255, 255))
            #im_draw.text((0, 720), "• Reward 2", font=self.very_small_font, fill=(255, 255, 255, 255))
        elif rank >= 35 and rank < 50:
            im_draw.text((0, 540), "Elite", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 660), "Pro", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 720), "• Ability to change your Nickname", font=self.very_small_font, fill=(255, 255, 255, 255))
            #im_draw.text((0, 720), "• Reward 2", font=self.very_small_font, fill=(255, 255, 255, 255))
        elif rank >= 50 and rank < 65:
            im_draw.text((0, 540), "Pro", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 660), "Master", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 720), "• Ability to share media files in chat", font=self.very_small_font, fill=(255, 255, 255, 255))
            #im_draw.text((0, 720), "• Reward 2", font=self.very_small_font, fill=(255, 255, 255, 255))
        elif rank >= 65 and rank < 75:
            im_draw.text((0, 540), "Master", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 660), "Legendary", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 720), "• Ability to DJ Commands", font=self.very_small_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 750), "• Access to VIP Channels(Giveaways)", font=self.very_small_font, fill=(255, 255, 255, 255))
        elif rank >= 75 and rank < 85:
            im_draw.text((250+(200-w)/2, 330), user, font=self.rank_font, fill=(255, 0, 0, 255))
            im_draw.text((0, 540), "Legendary", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 660), "Mythical", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 720), "• Ability to post GIF links", font=self.very_small_font, fill=(255, 255, 255, 255))
            #im_draw.text((0, 720), "• Reward 2", font=self.very_small_font, fill=(255, 255, 255, 255))
        else:
            im_draw.text((250+(200-w)/2, 330), user, font=self.rank_font, fill=(255, 0, 0, 255))
            im_draw.text((0, 540), "Mythical", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 660), "Highest Reward Reached", font=self.medium_font, fill=(255, 255, 255, 255))
            im_draw.text((0, 720), "• No Reward", font=self.very_small_font, fill=(255, 255, 255, 255))
        im_draw.line((0, 790, 650, 790),fill=(255,255,255,255),width=2)
        quote = random.choice(quotes)
        im_draw.text((20, 810), "“"+quote+"”", font=self.very_small_font, fill=(255, 255, 255, 255))
        im.paste(profile_bytes, (270, 200), profile_bytes)

        buffer = BytesIO()
        im.save(buffer, 'png')
        buffer.seek(0)

        return buffer

    @staticmethod
    def neededxp(level: str) -> int:
        return 100+level*80


class Utilities:
    def __init__(self):
        self.database = Database
        self.rankcard = Rank()


utilities = Utilities()
