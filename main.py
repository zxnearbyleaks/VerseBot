import asyncio
import textwrap
import time

import discord
from discord.ext import commands
from discord import client
import json
import urllib.request
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import random
import sched
import re

Active = [False, False, False, False, False, False, True, True, True, True]

token = "MTAwNDM4NTUzMTg3MTg5MTUxNg.Gstr-j.5M8fA7qFdxt6QyoktDWN4tk4kWm4PLAe9frv6E"
client = commands.Bot(command_prefix="?h")

API = "https://lunar-api-backend-host.herokuapp.com/api/v1/"
APIList = ["allCosmetics", "newCosmetics", "search/", "aes/keys"]
CharacterIcons = ["https://cdn.multiversus.com/roster/lebron-lg.webp", "https://cdn.multiversus.com/roster/shaggy-lg.webp", "https://cdn.multiversus.com/roster/velma-lg.webp", "https://cdn.multiversus.com/roster/batman-lg.webp", "https://cdn.multiversus.com/roster/wonder-woman-t.webp", "https://cdn.multiversus.com/roster/superman-lg.webp", "https://cdn.multiversus.com/roster/taz-lg.webp", "https://cdn.multiversus.com/roster/garnet-lg.webp", "https://cdn.multiversus.com/roster/steven-lg.webp", "https://cdn.multiversus.com/roster/jake-lg.webp", "https://cdn.multiversus.com/roster/reindog-lg.webp", "https://cdn.multiversus.com/roster/finn-lg.webp", "https://cdn.multiversus.com/roster/arya-lg.webp", "https://cdn.multiversus.com/roster/bugs-lg.webp", "https://cdn.multiversus.com/roster/harley-lg.webp", "https://cdn.multiversus.com/roster/tom-and-jerry-lg.webp", "https://cdn.multiversus.com/roster/rick-lg.webp", "https://raw.githubusercontent.com/zxnearbyleaks/VerseBot/main/ninja.png", "https://cdn.multiversus.com/roster/morty-lg.webp"]
AllCosmetics = {"LebronJames":{"id":"character_C016","DisplayName":"Lebron James","image":"https://cdn.multiversus.com/roster/lebron-t.webp","variants":[True]},"Shaggy":{"id":"character_shaggy","DisplayName":"Shaggy","image":"https://cdn.multiversus.com/roster/shaggy-t.webp","variants":[True]},"Velma":{"id":"character_velma","DisplayName":"Velma","image":"https://cdn.multiversus.com/roster/velma-t.webp","variants":[True]},"Batman":{"id":"character_batman","DisplayName":"Batman","image":"https://cdn.multiversus.com/roster/batman-t.webp","variants":[True]},"WonderWoman":{"id":"character_wonder_woman","DisplayName":"Wonder Woman","image":"https://cdn.multiversus.com/roster/wonder-woman-t.webp","variants":[True]},"Superman":{"id":"character_superman","DisplayName":"Superman","image":"https://cdn.multiversus.com/roster/superman-t.webp","variants":[True]},"Taz":{"id":"character_taz","DisplayName":"Taz","image":"https://cdn.multiversus.com/roster/taz-t.webp","variants":[True]},"Garnet":{"id":"character_garnet","DisplayName":"Garnet","image":"https://cdn.multiversus.com/roster/garnet-t.webp","variants":[True]},"Steven":{"id":"character_steven","DisplayName":"Steven Universe","image":"https://cdn.multiversus.com/roster/steven-t.webp","variants":[True]},"Jake":{"id":"character_jake","DisplayName":"Jake","image":"https://cdn.multiversus.com/roster/jake-t.webp","variants":[True]},"ReinDog":{"id":"character_creature","DisplayName":"Rein Dog","image":"https://cdn.multiversus.com/roster/rein-dog-t.webp","variants":[True]},"Finn":{"id":"character_finn","DisplayName":"Finn the Human","image":"https://cdn.multiversus.com/roster/finn-the-human-t.webp","variants":[True]},"AryaShark":{"id":"character_arya","DisplayName":"Arya Stark","image":"https://cdn.multiversus.com/roster/arya-shark-t.webp","variants":[True]},"BugsBunny":{"id":"character_bugs_bunny","DisplayName":"Bugs Bunny","image":"https://cdn.multiversus.com/roster/bugs-bunny-t.webp","variants":[True]},"HarleyQuinn":{"id":"character_harleyquinn","DisplayName":"Harley Quinn","image":"https://cdn.multiversus.com/roster/harley-quinn-t.webp","variants":[True]},"TomAndJerry":{"id":"character_tom_and_jerry","DisplayName":"Tom and Jerry","image":"https://cdn.multiversus.com/roster/tom-and-jerry-t.webp","variants":[True]},"Rick":{"id":"character_C020","DisplayName":"Rick Sanchez","image":"https://cdn.multiversus.com/roster/rick-t.webp","variants":[True]},"Ninja":{"id":"character_ninja","DisplayName":"Ninja","image":"https://raw.githubusercontent.com/zxnearbyleaks/VerseBot/main/ninja.png","variants":[]}, "Morty":{"id":"character_?","DisplayName":"Morty","image":"https://cdn.multiversus.com/roster/morty-t.webp","variants":[]}}
NewCosmetics = {"Rick":{"id":"character_C020","DisplayName":"Rick Sanchez","image":"https://cdn.multiversus.com/roster/rick-t.webp","variants":[]}, "Morty":{"id":"character_?","DisplayName":"Morty","image":"https://cdn.multiversus.com/roster/morty-t.webp","variants":[]}}
FounderPacks = ["https://cdn.multiversus.com/retail/foundersStandard/en/pack.jpg", "https://cdn.multiversus.com/retail/foundersDeluxe/en/pack.jpg", "https://cdn.multiversus.com/retail/foundersPremium/en/pack.jpg"]
CharacterDescriptions = {"LebronJames": "Campione. Icona. Compagno di squadra. Padre. Filantropo.\n \nSuperare le avversità e potenziare gli alleati è uno stile di vita per Lebron James: vincitore di diversi titoli NBA, di medaglie d'oro alle Olimpiadi e riconosciuto come giocatore di maggior valore e migliore compagno di squadra in tutto il mondo. Tuttavia, persino uno dei migliori giocatori di basket non avrebbe mai potuto prevedere le conseguenze del suo rifiuto nei confronti dell'egocentrica intelligenza artificiale nota come “Al-G Rhytmo”. Scaraventato in un’avventura tra mondi diversi attraverso il “Server-Verso”, LeBron si è alleato con Bugs Bunny per guidare la leggendaria Tune Squad e salvare sui figlio dalle grinfie di Al-G in uno Space Jam all’ultimo canestro. Ora, di fronte a una nuova minaccia, LeBron conta sulle sue abilità da giocatore di fama mondiale per aiutare i suoi nuovi amici a difendere i loro mondi.", "AryaStark": "Ha rifiutato il suo retaggio nobiliare ed è diventata letale.\n \n Arya, terzogenita di Eddard e Catelyn Stark, non ha mai desiderato diventare una lady o sprecare tempo nelle formalità richieste dal suo rango nobiliare, le considerava un compito noioso che era meglio lasciare ai suoi fratelli. Ma quando suo padre fu giustiziato e la sua famiglia destituita, la giovane Arya si ritrovò a intraprendere un nuovo viaggio che la portò attraverso il Continente Occidentale e a raggiungere infine le coste del Continente Orientale. Qui seguì l'addestramento per entrare a far parte degli “Uomini senza volto” e divenne un'abile spadaccina e una letale assassina. Fu una trasformazione che avrebbe cambiato per sempre il corso della sua vita e il destino di tutto il Continente Occidentale.", "Batman": "È il Più Grande Detective del Mondo. È la notte. È Batman.\n \n Il Crociato Incappucciato, difensore di Gotham City, noto solo come Batman, è nato la notte in cui il giovane Bruce Wayne assistette alla morte dei propri genitori, uccisi a colpi di pistola proprio davanti ai suoi occhi. Da quel giorno Bruce ha giurato di combattere il crimine e proteggere la gente di Gotham City. Nonostante non possieda superpoteri o abilità fuori dall'ordinario, la sua dedizione, volontà e intelligenza gli hanno permesso di combattere al fianco dei più grandi eroi dell'universo. Anche avere a disposizione un arsenale di dispositivi all'avanguardia, creati grazie al patrimonio di famiglia, lo ha aiutato non poco.", "BugsBunny": "Il coniglio più scaltro e birbante da questa parte dell'universo.\n \n Bugs, icona della cultura pop tra le più celebri e durature, è una star dei film, un eroe d'azione e una leggenda dello sport con una carriera lunga mezzo secolo. Grazie alla sua esperienza nel gioco di squadra e nel Multiverso, Bugs Bunny è senza dubbio uno dei combattenti meno turbati dal caos multi universale. Sebbene non lo dia a vedere, questo coniglio astuto e saputello se la ride sugli schermi grandi e piccoli da molto prima che la maggior parte degli altri combattenti diventasse uno schizzo su un pezzo di carta. Armato di battute di spirito e diversi oggetti marchiati ACME, è pronto a scatenare il caos con il suo tipico atteggiamento flemmatico.", "FinnTheHuman": "Combattere e annientare la malvagità, è questo il suo forte!\n \n Finn, uno degli ultimi umani della Terra di Ooo, è un giovane guerriero che passa la maggior parte della sua vita ad affrontare missioni e ad aiutare le forze del bene nell'infinita battaglia contro il male. Grazie alla sua spada, a un'immaginazione senza limiti e al suo amico/fratello adottivo Jake il cane, non c'è nessun cattivo che Finn non possa sconfiggere. Quando non è occupato ad annientare i malvagi, adora rilassarsi e giocare ai videogame insieme a BMO", "Garnet": "Protettrice della Terra e ballerina dal ritmo impareggiabile.\n \n Garnet è la leader delle Crystal Gem: un gruppo di extraterrestri ribelli che ha trovato rifugio sulla Terra; insieme alle altre gemme (e a Steven) ha giurato di proteggere la sua nuova casa da qualsiasi invasore. Garnet è in realtà la fusione di due gemme: Rubino e Zaffiro, e potrebbe essere la fusione più stabile esistente. Sebbene appaia fredda e stoica, Garnet ha un grande cuore ed è pronta a tutto per proteggere coloro che ama.", "HarleyQuinn": "Ha provato a essere buona, ma essere cattivi è molto più divertente.\n \n Harleen Quinzel lavorava come psichiatra al Manicomio di Arkham, sino al fatidico incontro con lo psicotico criminale chiamato Joker… da allora tutto cambiò per sempre per la dottoressa Quinzel. Dopo anni come spalla e amante principale del Joker, Harley Quinn ha trovato finalmente il coraggio di lasciarlo ed essere la fautrice del proprio destino. La sua ascesa al potere non è passata inosservata a Batman, che ha notato il potenziale di Harley di diventare una dei criminali più pericolosi non solo di Gotham City ma del mondo intero.", "IronGiant": "Eroe robotico venuto dalle stelle.\n \n L'enigmatica meraviglia meccanica soprannominata 'Il Gigante di ferro' precipitò sulle coste di Rockwell, nel Maine, dopo il lancio dello Sputnik nel 1957. Senza alcun ricordo del proprio passato e senza un chiaro obiettivo da seguire, fu ritrovato da un ragazzino di nome Hogarth Hughes, che divenne ben presto il suo migliore amico. Leale e coraggioso, il Gigante di ferro è un difensore degli innocenti e ha giurato di emulare sempre colui che considera il suo eroe, Superman", "Jake": "Quei poteri elastici sono una forza, amico.\n \n Jake non era a conoscenza dell'origine dei suoi poteri elastici, ha scoperto solo molto tempo dopo che erano dovuti al padre biologico, un mutaforma di nome Warren Ampersand. Tuttavia, non importa quale sia il suo pianeta natale, Jake ha una vita felice come eroe e avventuriero insieme al suo migliore amico Finn l'umano. Quando non è fuori a pestare le chiappette dei super cattivi, Jake ama passare del tempo con la sua adorata Lady Iridella e i loro cinque cuccioli ibridi di cane/iridelli/mutaforma.", "Morty": "Oh cavoli, è un picchiaduro. \n \n In molti hanno un rapporto stretto con i propri nonni… e poi c’è il legame tra Morty e suo nonno Rick. Sotto la 'supervisione' di Rick, Morty è stato trascinato attraverso tutto l’universo. Sebbene abbia visto innumerevoli line temporali e varie dimensioni alternative (non sempre in modo legale), Morty rimane ottimista nonostante la devastante realtà.", "ReinDog": "Guardia morbidosa della famiglia reale di Zanifeer e sesto possessore della gemma del potere! \n \n Il mondo di Zanifeer fu una delle prime vittime del Nulla, durante il grande cataclisma dimensionale. Secondo la maggior parte dei resoconti non vi furono sopravvissuti… eccetto uno. Rendog è una guardia reale, un longevo difensore della famiglia reale di Zanifeer, assegnato alla loro protezione. Sotto quella scorza dolce e morbidosa di metà cane e metà renna, batte un cuore da guerriero e Rendog è pronto a tutto per proteggere coloro che ama. Grazie ai fantastici poteri della sua gemma, spera di trovare un modo per riportare indietro la sua amata famiglia reale.", "Rick": "Fammi fare il f*ttuto deus ex machina della situazione e andiamo a casa! \n \n Lo scienziato Rick Sanchez, super genio nichilista e uno degli uomini più ricercati in tutte le galassie, ha visto quasi tutto ciò che la realtà ha da offrire. Quasi sempre in compagnia di suo nipote Morty, i due hanno salvato la galassia e il continuum spazio-temporale dozzine di volte", "Shaggy": "Solo un normale ragazzo che ama abbuffarsi di sandwich e risolvere misteri grazie a poteri illimitati di origine ignota. \n \n L'ultima cosa che Shaggy ricorda prima del Cambiamento è che si trovava nell'ennesima vecchia villa con il suo amico Scoob, proprio come qualsiasi altro giorno insieme alla squadra. Ricorda di aver trovato un cristallo brillante e di avergli dato un morso, pensando fosse una caramella. C'era stato un LAMPO di luce… e poi l'oscurità. Quando ha ripreso i sensi si è ritrovato con questi incredibili poteri. Non sa da dove vengano o come funzionino, ma ha giurato di usarli per il bene e per proteggere il piccoletto… tutto questo dopo aver mangiato qualcosa naturalmente.", "Steven": "Metà umano, metà gemma, tutto eroe. \n \n Steven, unico ibrido di umano e gemma conosciuto, era da sempre destinato a essere speciale. Ha passato la maggior parte della sua infanzia con tre gemme che si nascondevano sulla Terra, ma solo durante l'adolescenza ha iniziato a mostrare il suo vero potenziale da eroe. Grazie a un grande cuore, un ottimismo contagioso e degli incredibili poteri da gemma, Steven risolve sempre la situazione.", "Superman": "Membro fondatore della Justice League e uno degli eroi più potenti della Terra.\n \n Il disastro colpì Krypton, il pianeta natale di Kal-El, quando lui era solo un neonato. I suoi genitori non ebbero altra scelta che inviarlo tra le stelle per salvargli la vita. Il razzo con dentro il piccolo Kal-El atterrò sulla Terra, dove fu trovato da Martha e Jonathan Kent, che decisero di crescerlo come loro figlio. Con il passare degli anni, la luce solare gialla della Terra attivò i poteri kryptoniani di Kal-El, e lui giurò di usarli per proteggere l'umanità, la giustizia e la verità. Come uno dei membri fondatori della Justice League, è stato un'ispirazione per innumerevoli generazioni di eroi nella sua continua lotta contro il male e tutte le sue forme.", "Taz": "(Non preoccuparti. Neanche noi capiamo cosa dice.)\n \n Il Diavolo della Tasmania è una burbera palla frenetica di energia, tanto da sembrare l'incrocio tra un tornado e un rasoio elettrico particolarmente irritato. Si dice che se si riesce a farlo calmare diventa gentile e docile come un gattino, ma è un grosso 'se'. Il temperamento di Taz è eguagliato solo dalla sua fame e fidati, non vuoi vedere il Diavolo della Tasmania affamato.", "TomAndJerry": "Quando questi amici-nemici mettono da parte le loro differenze, scatenano un caos irrefrenabile. \n \n Sin dal loro primo incontro, la relazione tra Tom e Jerry è stata complicata. Come gatto e topo dovrebbero essere nemici mortali, tuttavia i due hanno collaborato innumerevoli volte nel corso degli anni. Come molti 'cartoni', Tom e Jerry hanno uno stile di combattimento bizzarro e folle, con un livello di resistenza quasi indistruttibile. Saranno dei grandi campioni nella lotta contro il Nulla, sempre che riescano a non bisticciare tra di loro.", "Velma": "Perdinci! Abbiamo un mistero da risolvere! \n \n Velma risolve misteri da tempi immemori. Grazie alla sua costante ricerca di risposte e alla sua grande conoscenza, è la perfetta macchina risolvi misteri. È la super detective indiscussa della Mystery Inc., sempre in viaggio con i suoi amici per smascherare criminali e svelare truffe ovunque vada. A volte, quando è troppo concentrata sui libri, finisce per cacciarsi nei guai, ma non sottovalutatela, se necessario Velma Dinkley se la sa cavare bene in una scazzottata.", "WonderWoman": "Principessa Amazzone. Figlia di Zeus. Membro fondatore della Justice League. \n \n Il nome 'Wonder Woman', eroina tra le più potenti della realtà, è temuto e amato in tutto il Multiverso. Diana è una guerriera fiera, una comandante orgogliosa e una leader gentile. È stata inviata nel mondo degli uomini dalle Amazzoni come campionessa della pace. Ha sconfitto miriadi di criminali, sia da sola che come membro della Justice League. È stata d'ispirazione per una generazione interamente nuova di eroi.", "Ninja": "TBD"}
PlayerSearchAPI = "https://api.multiversustracker.com/search/"
PlayerAPI = "https://api.multiversustracker.com/player/"
ProfileIcons = "https://raw.githubusercontent.com/zxnearbyleaks/VerseBot/main/Game/Panda_Main/Blueprints/Rewards/ProfileIcons/"

@client.event

async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="MultiVersus API"))
    print(client.user, "è ora online")



@client.event

async def on_message(message):
    realmessage = message.content.lower()
    wordslist = open("Words.txt", "a+", encoding="utf8")
    wordslistread = open("Words.txt", "a+", encoding="utf8")
    Characters = ""
    print(message.content)
    if message.author.id == client.user.id:
        return
    splitmessage = message.content.split()
    readlist = wordslistread.read()
    with open("Words.txt", "a+") as listtoappend:
        listtoappend.seek(0)
        wordslist.write(message.content + " ")
    if "?personaggi" in realmessage:
        Characters = ">>> "
        Data = urllib.request.urlopen(API + APIList[0])
        jsonified = json.loads(Data.read())
        for x in AllCosmetics:
            Characters = Characters + AllCosmetics[x]["DisplayName"] + "\n"
        print(Characters)
        await message.channel.send(Characters)
    if "?nuovipersonaggi" in realmessage:
        Characters = ">>> "
        Data = urllib.request.urlopen(API + APIList[1])
        jsonified = json.loads(Data.read())
        for x in NewCosmetics:
            Characters = Characters + NewCosmetics[x]["DisplayName"] + "\n"
        await message.channel.send(Characters)
    if "?cerca" in realmessage:
        itemname = ""
        separated = message.content.split()[1].capitalize()
        cosmetic = ""
        for l in AllCosmetics:
            if separated in l:
                cosmetic = l
                print(cosmetic)
                break
        Data = urllib.request.urlopen(API + APIList[2] + cosmetic)
        jsonified = json.loads(Data.read())
        imagelink = ""
        itemname = AllCosmetics[cosmetic]["DisplayName"]
        itemname = itemname.split()
        itemname = itemname[0].lower()
        for g in CharacterIcons:
            if itemname in g:
                print(g)
                imagelink = g
        imagedata = urllib.request.urlopen(imagelink)
        img = Image.open(imagedata).convert("RGBA")
        img.save("Icons/" + AllCosmetics[cosmetic]["DisplayName"] + ".png", "Png")
        #await message.channel.send(Characters, file=discord.File("Icons/" + jsonified[x]["DisplayName"] + ".png"))
        varianti = ""
        if AllCosmetics[cosmetic]["variants"]:
            varianti = "Si"
        else:
            varianti = "No"
        embed = discord.Embed(title=AllCosmetics[cosmetic]["DisplayName"], description=CharacterDescriptions[cosmetic], color=discord.Color.red())
        embed.set_image(url=imagelink)
        embed.add_field(name="Ha varianti:", value=varianti)
        embed.add_field(name="ID", value=AllCosmetics[cosmetic]["id"])
        embed.set_footer(text="VerseBot. Creato da Nearby e SpiritsFish. Informazione richiesta da " + message.author.display_name)
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)
    if "?chiaviaes" in realmessage:
        Characters = ">>> "
        Data = urllib.request.urlopen(API + APIList[3])
        jsonified = json.loads(Data.read())
        for x in jsonified:
            Characters = Characters + jsonified[x]["key"] + " Data Chiave: " + jsonified[x]["date"] + "\n"
        await message.channel.send(Characters)
    if "?giocatore" in realmessage:
        separated = message.content.split()[1]
        request1 = urllib.request.Request(PlayerSearchAPI + separated, headers={"User-Agent":"Mozilla/5.0"})
        response1 = urllib.request.urlopen(request1)
        jsonified = json.loads(response1.read())
        playerid = jsonified["Id"]
        request2 = urllib.request.Request(PlayerAPI + playerid, headers={"User-Agent":"Mozilla/5.0"})
        response2 = urllib.request.urlopen(request2)
        jsonified2 = json.loads(response2.read())
        embed = discord.Embed(title=jsonified["Name"],
                              color=discord.Color.red())
        profileicon = re.split('(?<!\d)[,.]|[,.](?!\d)', ProfileIcons + jsonified2["responses"][3]["body"]["server_data"]["ProfileIcon"]["AssetPath"])
        embed.set_image(
            url=ProfileIcons + profileicon[3] + ".png")
        print(ProfileIcons + jsonified2["responses"][3]["body"]["server_data"]["ProfileIcon"]["AssetPath"] + ".png")
        embed.add_field(name="Maggior danno inflitto", value=jsonified2["responses"][0]["body"]["server_data"]["stat_trackers"]["HighestDamageDealt"])
        embed.add_field(name="Assist totali:", value=jsonified2["responses"][0]["body"]["server_data"]["stat_trackers"]["TotalAssists"])
        embed.add_field(name="Schivate totali:",
                        value=jsonified2["responses"][0]["body"]["server_data"]["stat_trackers"]["TotalAttacksDodged"])
        embed.add_field(name="Fuori ring totali:",
                        value=jsonified2["responses"][0]["body"]["server_data"]["stat_trackers"]["TotalRingouts"])
        embed.add_field(name="Vittorie totali:",
                        value=jsonified2["responses"][0]["body"]["server_data"]["stat_trackers"]["TotalWins"])
        embed.set_footer(
            text="VerseBot. Creato da Nearby e SpiritsFish. Informazione richiesta da " + message.author.display_name)
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)









client.run(token)


