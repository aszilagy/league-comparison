from flask import Flask, render_template, request, session, redirect, url_for
import riot_app as ri
from passlib.hash import sha256_crypt as sha
import configparser as cf
from pprint import pprint

config = cf.ConfigParser()
config.read('config.ini')

encrypted_pass = config['DEFAULT']['PASSWORD']
encrypted_user = config['DEFAULT']['USER']
port = config['DEFAULT']['PORT']
host = config['DEFAULT']['HOST']
tournieId = ""

blueTeam = []
redTeam = []

app = Flask(__name__)
app.secret_key = b'(0a$li*&$p]/nap993-1z[1'

@app.route('/', methods=['GET', 'POST'])
#FIXME: Should add parameters into URL (127.0.0.1/summoners?user1=Decelx&user2=Plu&champSearch=Graves
def summon():
    searchChampId, search1Name, search_mast_s1, search2Name, search_mast_s2 = None, None, None, None, None
    champDict = ri.make_champion_id_list()
    if request.method == 'POST' and 'summoner1_input' in request.form.to_dict() and 'summoner2_input' in request.form.to_dict():
        s1 = ri.get_summoner_by_name(request.form['summoner1_input'])
        s2 = ri.get_summoner_by_name(request.form['summoner2_input'])

        if 'champion_input' in request.form.to_dict():
            champ = request.form['champion_input']

        if s1 is None or s2 is None:
            s1 = ri.get_summoner_by_name('T1 OK GOOD YES')
            s2 = ri.get_summoner_by_name('lpp user50')

        if champ is not '':
            champion_stats = ri.get_champ_page(champ.capitalize())

            if champion_stats is not None:
                print("FOUND CHAMP KEY")
                searchChampId = champion_stats['key']
                searchChampName = champDict[str(searchChampId)]

    else:
        s1 = ri.get_summoner_by_name('T1 OK GOOD YES')
        s2 = ri.get_summoner_by_name('lpp user50')

    mast_s1 = ri.get_mastery_by_summonerid(s1.summonerId)
    mast_s2 = ri.get_mastery_by_summonerid(s2.summonerId)

    if searchChampId:
        for x in mast_s1:
            if str(x['championId']) == str(searchChampId):
                search_mast_s1 = x
                search1Name = champDict[str(x['championId'])]

        for y in mast_s2:
            if str(y['championId']) == str(searchChampId):
                search_mast_s2 = y
                search2Name = champDict[str(y['championId'])]

    print(search_mast_s2, search_mast_s1)


    s1_champId = mast_s1[0]['championId']
    s2_champId = mast_s2[0]['championId']

    champ1Name = champDict[str(s1_champId)]
    champ2Name = champDict[str(s2_champId)]

    beta = ri.get_summoner_by_id(s2.summonerId)

    beta.rank = ri.get_summoner_rank(s2.summonerId)
    if isinstance(beta.rank, (list,)):
        for re in beta.rank:
            print(re.queueType)
            if re.queueType == "RANKED_SOLO_5x5":
                beta.rank = re


    alpha = ri.get_summoner_by_id(s1.summonerId)
    alpha.rank = ri.get_summoner_rank(s1.summonerId)
    if isinstance(alpha.rank, (list,)):
        for ra in alpha.rank:
            print(ra.queueType)
            if ra.queueType == "RANKED_SOLO_5x5":
                alpha.rank = ra

    alpha.gamesPlayed, beta.gamesPlayed, s1WinPercent, s2WinPercent = None, None, None, None
    if alpha.rank is not None:
        alpha.gamesPlayed = alpha.rank.wins + alpha.rank.losses
        s1WinPercent = (alpha.rank.wins) / (alpha.rank.wins + alpha.rank.losses)

    if beta.rank is not None:
        beta.gamesPlayed = beta.rank.wins + beta.rank.losses
        s2WinPercent = (beta.rank.wins) / (beta.rank.wins + beta.rank.losses)


    return render_template('home.html', summoner1 = alpha, summoner2 = beta, s1Wins = s1WinPercent, s2Wins = s2WinPercent, s1Mast = mast_s1, s2Mast = mast_s2, best1Champ = champ1Name, best2Champ = champ2Name, search1Mast = search_mast_s1, search1Champ = search1Name, search2Champ = search2Name, search2Mast = search_mast_s2)


#FIXME: Can remove this eventually (soon)
@app.route('/tyler-moe', methods=['GET'])
def home():
    beta = ri.get_summoner_by_id('qFPc7K5DPBFildIkrWDXd4W0MfM9H8jW5S82nMfeDxGCrTe3')
    beta.rank = ri.get_summoner_rank('qFPc7K5DPBFildIkrWDXd4W0MfM9H8jW5S82nMfeDxGCrTe3')[0]
    beta.gamesPlayed = beta.rank.wins + beta.rank.losses

    alpha = ri.get_summoner_by_id('zgzqdg9xeHXQ9zZpo4TeprEiQ8eRqWU0c7HVrdyR7FJEVno')
    alpha.rank = ri.get_summoner_rank('zgzqdg9xeHXQ9zZpo4TeprEiQ8eRqWU0c7HVrdyR7FJEVno')[0]
    alpha.gamesPlayed = alpha.rank.wins + alpha.rank.losses
    #print(alpha.__dict__, beta.__dict__)

    s1WinPercent = (alpha.rank.wins) / (alpha.rank.wins + alpha.rank.losses)
    s2WinPercent = (beta.rank.wins) / (beta.rank.wins + beta.rank.losses)

    return render_template('home.html', summoner1 = alpha, summoner2 = beta, s1Wins = s1WinPercent, s2Wins = s2WinPercent)

@app.route('/tyler/', methods=['GET'])
def login():
    beta = ri.get_summoner_by_id('qFPc7K5DPBFildIkrWDXd4W0MfM9H8jW5S82nMfeDxGCrTe3')
    beta.rank = ri.get_summoner_rank('qFPc7K5DPBFildIkrWDXd4W0MfM9H8jW5S82nMfeDxGCrTe3')[0]
    #print(beta.rank.__dict__)

    alpha = ri.get_summoner_by_id('zgzqdg9xeHXQ9zZpo4TeprEiQ8eRqWU0c7HVrdyR7FJEVno')
    alpha.rank = ri.get_summoner_rank('zgzqdg9xeHXQ9zZpo4TeprEiQ8eRqWU0c7HVrdyR7FJEVno')[0]
    #print(alpha.__dict__, beta.__dict__)
    return render_template('tyler.html', t1 = alpha, moe = beta)


if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)
