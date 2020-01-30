from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'sfnhouiafhbgasdujbsdaiuhjcbvdizsuavciuzsad'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class CurrentTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    time = db.Column(db.String)
    endtime = db.Column(db.Integer)
    polocas = db.Column(db.Integer, default=1)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    team = db.relationship('Team', backref='Group', lazy=True, cascade="all, delete-orphan")
    match = db.relationship('Match', backref='Group', lazy=True, cascade="all, delete-orphan")
    played_match = db.relationship('PlayedMatch', backref='Group', lazy=True, cascade="all, delete-orphan")

    name = db.Column(db.String)

    def __repr__(self):
        return f"(Skupina {self.name})"


def get_last_order():
    try:
        last_match = Match.query.order_by(Match.order.desc()).first().order
        return last_match + 10
    except:
        return 0


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    order = db.Column(db.Integer, default=get_last_order)
    home_team = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    away_team = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    score = db.Column(db.String, default="0:0")
    start = db.Column(db.String)

    quarterfinal = db.Column(db.Integer, default=0)
    semifinal = db.Column(db.Integer, default=0)
    third = db.Column(db.Integer, default=0)
    final = db.Column(db.Integer, default=0)
    l_quarterfinal = db.Column(db.Integer, default=0)
    l_semifinal = db.Column(db.Integer, default=0)
    l_final = db.Column(db.Integer, default=0)

    real_third = db.Column(db.Integer, default=0)
    real_final = db.Column(db.Integer, default=0)


class PlayedMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    order = db.Column(db.Integer)
    home_team = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    away_team = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    score = db.Column(db.String)
    start = db.Column(db.String)

    quarterfinal = db.Column(db.Integer, default=0)
    semifinal = db.Column(db.Integer, default=0)
    third = db.Column(db.Integer, default=0)
    final = db.Column(db.Integer, default=0)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    player = db.relationship('Player', backref='Team', lazy=True, cascade="all, delete-orphan")
    match_as_home = db.relationship('Match', backref='Home', lazy='dynamic', cascade="all, delete-orphan", foreign_keys='Match.home_team')
    match_as_away = db.relationship('Match', backref='Away', lazy='dynamic', cascade="all, delete-orphan", foreign_keys='Match.away_team')
    played_match_as_home = db.relationship('PlayedMatch', backref='Home', lazy='dynamic', cascade="all, delete-orphan",
                                            foreign_keys='PlayedMatch.home_team')
    played_match_as_away = db.relationship('PlayedMatch', backref='Away', lazy='dynamic', cascade="all, delete-orphan",
                                            foreign_keys='PlayedMatch.away_team')

    name = db.Column(db.String)
    played_matches = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    loses = db.Column(db.Integer, default=0)
    goals_shot = db.Column(db.Integer, default=0)
    goals_got = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"(Tým {self.name})"


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    name = db.Column(db.String)


admin = Admin(app)
admin.add_view(ModelView(CurrentTime, db.session))
admin.add_view(ModelView(Group, db.session))
admin.add_view(ModelView(Match, db.session))
admin.add_view(ModelView(PlayedMatch, db.session))
admin.add_view(ModelView(Team, db.session))
admin.add_view(ModelView(Player, db.session))


@app.route('/')
def home():
    match = Match.query.order_by(Match.order).first()

    matches = Match.query.order_by(Match.order)
    groups = Group.query.all()
    teams_by_points = Team.query.join(Group).order_by(Group.name, Team.points.desc(), (Team.goals_shot-Team.goals_got).desc()).all()
    timer = CurrentTime.query.first()
    played_matches = PlayedMatch.query.order_by(PlayedMatch.order).all()

    matches_a = Match.query.join(Group).filter(Group.name == "A").count()
    matches_b = Match.query.join(Group).filter(Group.name == "B").count()
    matches_c = Match.query.join(Group).filter(Group.name == "C").count()
    matches_d = Match.query.join(Group).filter(Group.name == "D").count()

    '''try:
        quarterfinal = Match.query.filter(Match.quarterfinal != 0).order_by(Match.quarterfinal).all()
    except:
        try:
            quarterfinal = PlayedMatch.query.filter(PlayedMatch.quarterfinal != 0).order_by(PlayedMatch.quarterfinal).all()
        except:
            quarterfinal = 0

    try:
        semifinal = Match.query.filter(Match.semifinal != 0).order_by(Match.semifinal)
    except:
        semifinal = 0

    try:
        third = Match.query.filter(Match.third != 0).order_by(Match.third)
    except:
        third = 0

    try:
        final = Match.query.filter(Match.final != 0).order_by(Match.final)
    except:
        final = 0

    try:
        l_quarterfinal = Match.query.filter(Match.l_quarterfinal != 0).order_by(Match.l_quarterfinal).all()
    except:
        try:
            l_quarterfinal = PlayedMatch.query.filter(PlayedMatch.l_quarterfinal != 0).order_by(PlayedMatch.l_quarterfinal).all()
        except:
            l_quarterfinal = 0

    try:
        l_semifinal = Match.query.filter(Match.l_semifinal != 0).order_by(Match.l_semifinal).all()
    except:
        try:
            l_semifinal = PlayedMatch.query.filter(PlayedMatch.l_semifinal != 0).order_by(PlayedMatch.l_semifinal).all()
        except:
            l_semifinal = 0

    try:
        l_final = Match.query.filter(Match.l_final != 0).order_by(Match.l_final).all()
    except:
        try:
            l_final = PlayedMatch.query.filter(PlayedMatch.l_final != 0).order_by(PlayedMatch.l_final).all()
        except:
            l_final = 0

    try:
        real_final = Match.query.filter(Match.real_final != 0).order_by(Match.real_final).all()
    except:
        try:
            real_final = PlayedMatch.query.filter(PlayedMatch.real_final != 0).order_by(PlayedMatch.real_final).all()
        except:
            real_final = 0

    try:
        real_third = Match.query.filter(Match.real_third != 0).order_by(Match.real_third).all()
    except:
        try:
            real_third = PlayedMatch.query.filter(PlayedMatch.real_third != 0).order_by(PlayedMatch.real_third).all()
        except:
            real_third = 0'''

    return render_template('hlavni_stranka.html', match=match, css="hlavni_stranka", matches=matches, groups=groups, teams=teams_by_points, timer=timer, played_matches=played_matches, a=matches_a, b=matches_b, c=matches_c, d=matches_d) # quarterfinal=quarterfinal, semifinal=semifinal, third=third, final=final, l_quarterfinal=l_quarterfinal, l_semifinal=l_semifinal, l_final=l_final, real_third=real_third, real_final=real_final'''


@app.route('/home_admin')
def home_admin():
    name = request.args.get('name')
    password = request.args.get('password')

    if name == ("poborsky" * 6 + "PoBoRsKy") and password == ("loupakis" * 4 + "LoUpAkIs"):
        try:
            endtime = CurrentTime.query.first().endtime
        except:
            endtime = 0

        match = Match.query.order_by(Match.order).first()
        return render_template('hlavni_stranka_admin.html', endtime=endtime, match=match, css="hlavni_stranka_admin")
    else:
        return "You entered wrong name and password. Try again."


@app.route('/get_time')
def get_time():
    time_query = CurrentTime.query.first()
    match = Match.query.first()
    if time_query.polocas == 1:
        time = match.start
    elif time_query.polocas == 3:
        time = "Poločas"
    else:
        try:
            time = 1 + int(time_query.time.split(":")[0])
        except:
            time = CurrentTime.query.first().time

    home_team = match.Home.name
    away_team = match.Away.name
    return jsonify(time=time, length=len(str(time)), home_team=home_team, away_team=away_team)


@app.route('/set_time')
def set_time():
    time = str(request.args.get('time'))
    endtime = str(request.args.get('endtime'))

    time_db = CurrentTime.query.first_or_404()

    if endtime is None or time == '':
        return '', 204
    if time != "20:00" or time_db.polocas != 4:
        time_db.time = time
        time_db.endtime = endtime
        if time == "20:00":
            time_db.polocas = 4
        db.session.commit()
    return '', 204


@app.route('/new_match')
def new_match():
    score_home = int(request.args.get('score_home'))
    score_away = int(request.args.get('score_away'))

    match = Match.query.order_by(Match.order).first()

    home_team = Team.query.filter_by(name=match.Home.name).first()
    away_team = Team.query.filter_by(name=match.Away.name).first()

    if match.quarterfinal == 0 and match.semifinal == 0 and match.third == 0 and match.final == 0 and match.l_quarterfinal == 0 and match.l_semifinal == 0 and match.l_final == 0 and match.real_third == 0 and match.real_final == 0:
        # Home team statistics update
        home_team.played_matches += 1
        home_team.goals_shot += score_home
        home_team.goals_got += score_away

        # Away team statistics update
        away_team.played_matches += 1
        away_team.goals_shot += score_away
        away_team.goals_got += score_home

        # Both match stats update
        if score_home > score_away:
            home_team.points += 3
            home_team.wins += 1

            away_team.points += 0
            away_team.loses += 1
        elif score_home == score_away:
            home_team.points += 1
            home_team.draws += 1

            away_team.points += 1
            away_team.draws += 1
        elif score_home < score_away:
            home_team.points += 0
            home_team.loses += 1

            away_team.points += 3
            away_team.wins += 1

        # Change Match to PlayedMatch and delete, so that other Match gets to first place
        played_match = PlayedMatch(order=match.order, score=match.score, Group=match.Group, Home=match.Home, Away=match.Away, start=match.start)
        db.session.add(played_match)
        db.session.delete(match)
        db.session.commit()

        time = CurrentTime.query.first_or_404()
        time.time = "0:00"
        time.endtime = 0
        time.polocas = 1

        db.session.commit()

    else:
        if match.quarterfinal == 1 or match.quarterfinal == 2:
            if match.score.split(":")[0] > match.score.split(":")[1]:
                winner = match.Home
                loser = match.Away
            else:
                winner = match.Away
                loser = match.Home

            try:
                new_match = Match.query.filter(Match.semifinal == 1).first_or_404()
                new_match.Away = winner

                new_lose_match = Match.query.filter(Match.l_quarterfinal == 2).first_or_404()
                new_lose_match.Away = loser
            except:
                new_match = Match(order=40, Group=match.Group, Home=winner, Away=winner, start="9:40", semifinal=1)
                db.session.add(new_match)

                new_lose_match = Match(order=70, Group=match.Group, Home=loser, Away=loser, start="10:55", l_quarterfinal=2)
                db.session.add(new_lose_match)

        elif match.quarterfinal == 3 or match.quarterfinal == 4:
            if match.score.split(":")[0] > match.score.split(":")[1]:
                winner = match.Home
                loser = match.Away
            else:
                winner = match.Away
                loser = match.Home

            try:
                new_match = Match.query.filter(Match.semifinal == 2).first_or_404()
                new_match.Away = winner

                new_lose_match = Match.query.filter(Match.l_quarterfinal == 1).first_or_404()
                new_lose_match.Away = loser
            except:
                new_match = Match(order=50, Group=match.Group, Home=winner, Away=winner, start="10:05", semifinal=2)
                db.session.add(new_match)

                new_lose_match = Match(order=60, Group=match.Group, Home=loser, Away=loser, start="10:30", l_quarterfinal=1)
                db.session.add(new_lose_match)

        elif match.semifinal == 1 or match.semifinal == 2:
            if match.score.split(":")[0] > match.score.split(":")[1]:
                winner = match.Home
                loser = match.Away
            else:
                winner = match.Away
                loser = match.Home

            try:
                new_match = Match.query.filter(Match.final == 1).first_or_404()
                new_match.Away = winner

                new_match_third = Match.query.filter(Match.l_semifinal == match.semifinal).first_or_404()
                new_match_third.Away = loser
            except:
                new_match = Match(order=100, Group=match.Group, Home=winner, Away=winner, start="12:10", final=1)
                db.session.add(new_match)

                new_match_third = Match(order=80, Group=match.Group, Home=loser, Away=loser, start="11:20", l_semifinal=match.semifinal)
                db.session.add(new_match_third)

        elif match.l_quarterfinal == 1 or match.l_quarterfinal == 2:
            if match.score.split(":")[0] > match.score.split(":")[1]:
                winner = match.Home
            else:
                winner = match.Away

            try:
                new_match = Match.query.filter(Match.l_semifinal == match.l_quarterfinal).first_or_404()
                new_match.Away = winner
            except:
                new_match_third = Match(order=80, Group=match.Group, Home=winner, Away=winner, start="11:20",
                                        l_semifinal=match.l_quarterfinal)
                db.session.add(new_match_third)

        elif match.l_semifinal == 1 or match.l_semifinal == 2:
            if match.score.split(":")[0] > match.score.split(":")[1]:
                winner = match.Home
            else:
                winner = match.Away

            try:
                new_match = Match.query.filter(Match.l_final == 1).first_or_404()
                new_match.Away = winner

            except:
                new_match = Match(order=110, Group=match.Group, Home=winner, Away=winner, start="12:35", l_final=1)
                db.session.add(new_match)

        elif match.final == 1:
            if match.score.split(":")[0] > match.score.split(":")[1]:
                winner = match.Home
                loser = match.Away
            else:
                winner = match.Away
                loser = match.Home

            try:
                new_match = Match.query.filter(Match.real_final == 1).first_or_404()
                new_match.Away = winner
            except:
                new_match = Match(order=130, Group=match.Group, Home=winner, Away=winner, start="13:25", real_final=1)
                db.session.add(new_match)

                new_lose_match = Match(order=120, Group=match.Group, Home=loser, Away=loser, start="13:00", real_third=1)
                db.session.add(new_lose_match)

        elif match.l_final == 1:
            if match.score.split(":")[0] > match.score.split(":")[1]:
                winner = match.Home
            else:
                winner = match.Away
            try:
                new_match = Match.query.filter(Match.real_third == 1).first_or_404()
                new_match.Away = winner
            except:
                new_lose_match = Match(order=120, Group=match.Group, Home=winner, Away=winner, start="13:00",
                                       real_third=1)
                db.session.add(new_lose_match)

        elif match.real_third == 1:
            if match.score.split(":")[0] > match.score.split(":")[1]:
                winner = match.Home
            else:
                winner = match.Away

            try:
                new_match = Match.query.filter(Match.real_final == 1).first_or_404()
                new_match.Away = winner
            except:
                new_match = Match(order=130, Group=match.Group, Home=winner, Away=winner, start="13:25", real_final=1)
                db.session.add(new_match)

        played_match = PlayedMatch(order=match.order, score=match.score, Group=match.Group, Home=match.Home, Away=match.Away, start=match.start, quarterfinal=match.quarterfinal, semifinal=match.semifinal, third=match.third, final=match.final)
        db.session.commit()
        db.session.add(played_match)
        match.order = 900;
        time = CurrentTime.query.first_or_404()
        time.time = "0:00"
        time.endtime = 0
        time.polocas = 1

        db.session.commit()

    return '', 204


@app.route('/start')
def start():
    start = int(request.args.get('start'))
    polocas = int(request.args.get('polocas'))

    if start == 1:
        time = CurrentTime.query.first_or_404()
        time.polocas = 1
        db.session.commit()
    elif start == 2:
        time = CurrentTime.query.first_or_404()
        time.polocas = 2
        db.session.commit()
    elif polocas == 1:
        time = CurrentTime.query.first_or_404()
        time.polocas = 3
        db.session.commit()
    return '', 204


@app.route('/update_score')
def update_score():
    score_key = request.args.get('score_key')

    if score_key == 'q':
        match = Match.query.order_by(Match.order).first()
        score = match.score
        new_score = str((int(score.split(":")[0]) + 1)) + ":" + score.split(":")[1]
        match.score = new_score
        db.session.commit()

        json = new_score.split(":")[0]
        team_scored = 1
    elif score_key == 'a':
        match = Match.query.order_by(Match.order).first()
        score = match.score
        new_score = str((int(score.split(":")[0]) - 1)) + ":" + score.split(":")[1]
        match.score = new_score

        if int(score.split(":")[0]) != 0:
            db.session.commit()
            json = new_score.split(":")[0]
            team_scored = 1
    elif score_key == 'w':
        match = Match.query.order_by(Match.order).first()
        score = match.score
        new_score = score.split(":")[0] + ":" + str((int(score.split(":")[1]) + 1))
        match.score = new_score
        db.session.commit()
        json = new_score.split(":")[1]
        team_scored = 2
    elif score_key == 's':
        match = Match.query.order_by(Match.order).first()
        score = match.score
        new_score = score.split(":")[0] + ":" + str((int(score.split(":")[1]) - 1))
        match.score = new_score

        if int(score.split(":")[1]) != 0:
            db.session.commit()
            json = new_score.split(":")[1]
            team_scored = 2
    return jsonify(json=json, team_scored=team_scored)


@app.route('/get_score')
def get_score():
    match = Match.query.order_by(Match.order).first()
    new_score = match.score
    home = new_score.split(":")[0]
    away = new_score.split(":")[1]
    return jsonify(home=home, away=away)
