from flask import Flask, render_template, request, session, redirect, url_for
import riot_app as ri
from passlib.hash import sha256_crypt as sha
import configparser as cf

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

@app.route('/summoners/', methods=['GET', 'POST'])
def summon():
    #FIXME: If no summoner is found (ri.get_summoner_by_id returns NoneType), just redirect
    if request.method == 'POST' and 'summoner1_input' in request.form.to_dict() and 'summoner2_input' in request.form.to_dict():
        s1 = ri.get_summoner_by_name(request.form['summoner1_input'])
        s2 = ri.get_summoner_by_name(request.form['summoner2_input'])

        if s1 is None or s2 is None:
            return redirect(url_for('home'))

        print(s1.summonerId)
        beta = ri.get_summoner_by_id(s2.summonerId)

        beta.rank = ri.get_summoner_rank(s2.summonerId)
        if isinstance(beta.rank, (list,)):
            for re in beta.rank:
                print(re.queueType)
                if re.queueType == "RANKED_SOLO_5x5":
                    beta.rank = re
        beta.gamesPlayed = beta.rank.wins + beta.rank.losses

        alpha = ri.get_summoner_by_id(s1.summonerId)
        alpha.rank = ri.get_summoner_rank(s1.summonerId)
        if isinstance(alpha.rank, (list,)):
            for ra in alpha.rank:
                print(ra.queueType)
                if ra.queueType == "RANKED_SOLO_5x5":
                    alpha.rank = ra
        alpha.gamesPlayed = alpha.rank.wins + alpha.rank.losses

        s1WinPercent = (alpha.rank.wins) / (alpha.rank.wins + alpha.rank.losses)
        s2WinPercent = (beta.rank.wins) / (beta.rank.wins + beta.rank.losses)

        return render_template('home.html', summoner1 = alpha, summoner2 = beta, s1Wins = s1WinPercent, s2Wins = s2WinPercent)

    else:
        print("REDIRECTING")
        print(request.form.to_dict())
        return redirect(url_for('home'))
    

@app.route('/', methods=['GET'])
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
