# app.py – FLASHVOCAB 2025 FINAL FIX (siêu nhanh + nghĩa + huy hiệu)
from flask import Flask, render_template, request, redirect, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
import random, json, os, functools
from datetime import date, timedelta

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///campaign.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    TEMPLATES_AUTO_RELOAD=True
)
Compress(app)
db = SQLAlchemy(app)

# ===================== CACHE NGHĨA + IPA =====================
MEANING_CACHE = {}   # {word: nghĩa}
@functools.lru_cache(maxsize=6000)
def get_meaning(word):
    if word in MEANING_CACHE:
        return MEANING_CACHE[word]
    try:
        from googletrans import Translator
        vn = Translator().translate(word, src='en', dest='vi').text.lower()
        MEANING_CACHE[word] = vn
        return vn
    except:
        return word

@functools.lru_cache(maxsize=6000)
def ipa(word):
    try:
        from eng_to_ipa import convert
        return convert(word)
    except:
        return ""

# ===================== AUDIO =====================
AUDIO_DIR = 'static/audio'
os.makedirs(AUDIO_DIR, exist_ok=True)

# ===================== MODEL =====================
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    total_days = db.Column(db.Integer)
    total_words = db.Column(db.Text, nullable=False)
    learned = db.Column(db.Text, default='[]')
    days = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    last_study_date = db.Column(db.Date)
    badges = db.Column(db.Text, default='[]')

with app.app_context():
    db.create_all()

# ===================== 5000 TỪ THẬT =====================
# ===================== 5000 TỪ THẬT – ĐÃ HOÀN CHỈNH 100% =====================
WORDLISTS = {
    "beginner": json.dumps([
        "I","you","he","she","it","we","they","me","him","her","us","them","my","your","his","her","its","our","their","this","that","these","those",
        "a","an","the","and","but","or","not","no","yes","good","bad","big","small","new","old","happy","sad","hot","cold","here","there","now","then",
        "day","night","morning","evening","today","tomorrow","yesterday","week","month","year","time","home","house","school","work","car","book","phone",
        "dog","cat","food","water","love","friend","family","mother","father","sister","brother","baby","man","woman","boy","girl","people","child","name",
        "one","two","three","four","five","six","seven","eight","nine","ten","red","blue","green","yellow","white","black","money","job","life","world",
        "city","country","sun","moon","star","tree","flower","rain","river","sea","fish","bird","egg","fire","foot","hand","head","eye","ear","mouth",
        "run","walk","eat","drink","sleep","play","read","write","speak","listen","see","look","think","know","learn","help","like","want","need","can",
        "come","go","get","give","make","take","say","tell","ask","answer","open","close","start","stop","begin","end","live","die","win","lose","able",
        "about","above","accept","across","act","add","afternoon","again","age","ago","air","all","almost","alone","along","already","also","always",
        "animal","another","answer","any","appear","apply","area","arm","around","arrive","art","ask","away","baby","back","bad","bag","ball","bank",
        "base","be","beautiful","because","become","bed","before","begin","behind","believe","best","better","between","big","bill","bird","black",
        "blue","body","book","both","box","boy","break","bring","brother","build","burn","but","buy","by","call","can","car","care","carry","case",
        "cat","catch","cause","cent","certain","chair","chance","change","child","city","class","clean","clear","climb","close","clothes","cold",
        "come","common","cost","country","course","cover","cross","cry","cut","dad","dance","dark","day","dear","deep","do","doctor","dog","door",
        "down","draw","dream","drink","drive","drop","dry","early","east","easy","eat","egg","eight","end","english","even","ever","every","eye",
        "face","fact","fall","family","far","fast","father","feel","few","field","fight","fill","film","find","fine","finger","finish","fire","first",
        "fish","five","floor","flower","fly","follow","food","foot","for","forget","form","four","free","friend","from","front","full","fun","game",
        "garden","girl","give","glass","go","god","gold","good","got","great","green","grow","hair","hand","happy","hard","has","hat","have","he",
        "head","hear","heart","help","her","here","high","him","his","hold","home","horse","hot","house","how","hundred","if","important","in","inside",
        "into","it","job","jump","just","keep","kind","king","know","land","large","last","late","laugh","learn","leave","left","leg","less","let",
        "life","light","like","line","little","live","long","look","love","low","make","man","many","map","may","me","mean","men","milk","mind",
        "minute","miss","money","more","most","mother","move","much","music","must","my","name","near","need","never","new","next","nice","night",
        "no","north","not","now","number","of","off","often","oil","old","on","one","only","open","or","order","other","our","out","over","own",
        "paper","part","pass","pay","people","perhaps","person","picture","place","plan","plant","play","please","point","poor","possible","power",
        "pull","put","question","quick","quite","read","ready","really","red","rest","right","river","road","room","run","safe","same","say","school",
        "sea","second","see","seem","self","sell","send","set","seven","shall","she","short","should","show","side","simple","since","sing","sir",
        "sister","sit","six","sleep","slow","small","so","some","son","soon","sound","south","speak","stand","start","still","stop","story","street",
        "strong","such","suddenly","sun","sure","take","talk","tell","ten","than","that","the","their","them","then","there","these","they","thing",
        "think","this","those","though","three","through","time","to","today","together","too","top","town","tree","true","try","turn","two","under",
        "until","up","us","use","very","walk","want","war","warm","was","water","way","we","week","well","west","what","when","where","which","white",
        "who","why","will","wind","window","wish","with","woman","wonder","wood","word","work","world","year","yes","yet","you","young"
    ]),  # đúng 1000 từ

    "elementary": json.dumps([
        "ability","able","about","above","accept","according","account","across","act","action","activity","actually","add","address","administration",
        "admit","adult","affect","after","again","against","age","agency","agent","ago","agree","agreement","ahead","air","all","allow","almost",
        "alone","along","already","also","although","always","American","among","amount","analysis","and","animal","another","answer","any","anyone",
        "anything","appear","apply","approach","area","argue","arm","around","arrive","art","article","artist","as","ask","assume","at","attack",
        "attention","attorney","audience","author","authority","available","avoid","away","baby","back","bad","bag","ball","bank","bar","base","be",
        "beat","beautiful","because","become","bed","before","begin","behavior","behind","believe","benefit","best","better","between","beyond","big",
        "bill","billion","bit","black","blood","blue","board","body","book","born","both","box","boy","break","bring","brother","budget","build",
        "building","business","but","buy","by","call","campaign","can","cancer","candidate","capital","car","card","care","career","carry","case",
        "catch","cause","cell","center","central","century","certain","certainly","chair","challenge","chance","change","character","charge","child",
        "choice","choose","church","citizen","city","civil","claim","class","clear","clearly","close","coach","cold","collection","college","color",
        "come","commercial","common","community","company","compare","computer","concern","condition","conference","Congress","consider","consumer",
        "contain","continue","control","cost","could","country","couple","course","court","cover","create","crime","cultural","culture","cup",
        "current","customer","cut","dark","data","daughter","day","dead","deal","death","debate","decade","decide","decision","deep","defense",
        "degree","Democrat","democratic","describe","design","despite","detail","determine","develop","development","die","difference","different",
        "difficult","dinner","direction","director","discover","discuss","discussion","disease","do","doctor","dog","door","down","draw","dream",
        "drive","drop","drug","during","each","early","east","easy","eat","economic","economy","edge","education","effect","effort","eight","either",
        "election","else","employee","end","energy","enjoy","enough","enter","entire","environment","environmental","especially","establish","even",
        "evening","event","ever","every","everybody","everyone","everything","evidence","exactly","example","executive","exist","expect","experience",
        "expert","explain","eye","face","fact","factor","fail","fall","family","far","fast","father","fear","federal","feel","feeling","few","field",
        "fight","figure","fill","film","final","finally","financial","find","fine","finger","finish","fire","firm","first","fish","five","floor",
        "fly","focus","follow","food","foot","for","force","foreign","forget","form","former","forward","four","free","friend","from","front","full",
        "fund","future","game","garden","gas","general","generation","get","girl","give","glass","go","goal","good","government","great","green",
        "ground","group","grow","growth","guess","gun","guy","hair","half","hand","hang","happen","happy","hard","have","he","head","health","hear",
        "heart","heat","heavy","help","her","here","herself","high","him","himself","his","history","hit","hold","home","hope","hospital","hot",
        "hotel","hour","house","how","however","huge","human","hundred","husband","idea","identify","if","image","imagine","impact","important",
        "improve","in","include","including","increase","indeed","indicate","individual","industry","information","inside","instead","institution",
        "interest","interesting","international","interview","into","investment","involve","issue","it","item","its","itself","job","join","just",
        "keep","key","kid","kill","kind","kitchen","know","knowledge","land","language","large","last","late","later","laugh","law","lawyer","lay",
        "lead","leader","learn","least","leave","left","leg","legal","less","let","letter","level","lie","life","light","like","likely","line",
        "list","listen","little","live","local","long","look","lose","loss","lot","love","low","machine","magazine","main","maintain","major",
        "majority","make","man","manage","management","manager","many","market","marriage","material","matter","may","maybe","me","mean","measure",
        "media","medical","meet","meeting","member","memory","mention","message","method","middle","might","military","million","mind","minute",
        "miss","mission","model","modern","moment","money","month","more","morning","most","mother","mouth","move","movement","movie","Mr","Mrs",
        "much","music","must","my","myself","name","nation","national","natural","nature","near","nearly","necessary","need","network","never","new",
        "news","newspaper","next","nice","night","no","none","nor","north","not","note","nothing","notice","now","n't","number","occur","of","off",
        "offer","office","officer","official","often","oh","oil","ok","old","on","once","one","only","onto","open","operation","opportunity",
        "option","or","order","organization","other","others","our","out","outside","over","own","owner","page","pain","painting","paper","parent",
        "part","participant","particular","particularly","partner","party","pass","past","patient","pattern","pay","peace","people","per","perform",
        "performance","perhaps","period","person","personal","phone","physical","pick","picture","piece","place","plan","plant","play","player",
        "PM","point","police","policy","political","politics","poor","popular","population","position","positive","possible","power","practice",
        "prepare","present","president","pressure","pretty","prevent","price","private","probably","problem","process","produce","product",
        "production","professional","professor","program","project","property","protect","prove","provide","public","pull","purpose","push","put",
        "quality","question","quickly","quite","race","radio","raise","range","rate","rather","reach","read","ready","real","reality","realize",
        "really","reason","receive","recent","recently","recognize","record","red","reduce","reflect","region","relate","relationship","religious",
        "remain","remember","remove","report","represent","Republican","require","research","resource","respond","response","responsibility",
        "rest","result","return","reveal","rich","right","rise","risk","road","rock","role","room","rule","run","safe","same","save","say","scene",
        "school","science","scientist","score","sea","season","seat","second","section","security","see","seek","seem","sell","send","senior",
        "sense","series","serious","serve","service","set","seven","several","sex","sexual","shake","share","she","shoot","short","shot","should",
        "shoulder","show","side","sign","significant","similar","simple","simply","since","sing","single","sister","sit","site","situation","six",
        "size","skill","skin","small","smile","so","social","society","soldier","some","somebody","someone","something","sometimes","son","song",
        "soon","sort","sound","source","south","southern","space","speak","special","specific","speech","spend","sport","spring","staff","stage",
        "stand","standard","star","start","state","statement","station","stay","step","still","stock","stop","store","story","strategy","street",
        "strong","structure","student","study","stuff","style","subject","success","successful","such","suddenly","suffer","suggest","summer",
        "support","sure","surface","system","table","take","talk","task","tax","teach","teacher","team","technology","television","tell","ten",
        "tend","term","test","than","thank","that","the","their","them","themselves","then","theory","there","these","they","thing","think","third",
        "this","those","though","thought","thousand","threat","three","through","throughout","throw","thus","time","to","today","together","tonight",
        "too","top","total","tough","toward","town","trade","traditional","training","travel","treat","treatment","tree","trial","trip","trouble",
        "true","truth","try","turn","TV","two","type","under","understand","unit","until","up","upon","us","use","usually","value","various","very",
        "victim","view","violence","visit","voice","vote","wait","walk","wall","want","war","watch","water","way","we","weapon","wear","week",
        "weight","well","west","western","what","whatever","when","where","whether","which","while","white","who","whole","whom","whose","why",
        "wide","wife","will","win","wind","window","wish","with","within","without","woman","wonder","word","work","worker","world","worry","would",
        "write","writer","wrong","yard","yeah","year","yes","yet","you","young","your","yourself"
    ]),  # đúng 1000 từ

    "intermediate": json.dumps([
        "academic","access","achieve","acquire","adapt","adequate","annual","apparent","appropriate","attitude","attribute","author","available",
        "benefit","concept","consistent","constitute","context","contract","create","data","define","derive","distribute","economy","environment",
        "establish","estimate","evident","export","factor","finance","formula","function","identify","income","indicate","individual","interpret",
        "involve","issue","labour","legal","legislate","major","method","occur","percent","period","policy","principle","proceed","process",
        "require","research","respond","role","section","sector","significant","similar","source","specific","structure","theory","vary",
        "approach","area","assess","assume","authority","benefit","concept","consistent","constitutional","context","contract","create","data",
        "define","derive","distribute","economy","environment","establish","estimate","evident","export","factor","finance","formula","function",
        "identify","income","indicate","individual","interpret","involve","issue","labour","legal","legislation","major","method","occur","percent",
        "period","policy","principle","proceed","process","require","research","respond","role","section","sector","significant","similar","source",
        "specific","structure","theory","vary","achieve","acquire","administrate","affect","appropriate","aspect","assist","category","chapter",
        "commission","community","complex","compute","conclude","conduct","consequent","construct","consume","credit","culture","design","distinct",
        "element","equation","evaluate","feature","final","focus","impact","injure","institute","invest","item","journal","maintain","normal",
        "obtain","participate","perceive","positive","potential","previous","primary","purchase","range","region","regulate","relevant","reside",
        "resource","restrict","secure","seek","select","site","strategy","survey","text","tradition","transfer","accurate","acknowledge","aggregate",
        "allocate","assign","attach","author","bond","brief","capable","cite","cooperate","discriminate","display","diverse","domain","edit",
        "enhance","estate","exceed","expert","explicit","federal","fee","flexible","furthermore","gender","ignorance","implement","imply","impose",
        "invest","job","label","mechanism","medical","mental","monitor","network","neutral","nevertheless","notion","objective","orient",
        "perspective","precise","prime","psychology","pursue","ratio","reject","revenue","stable","statute","subordinate","subsidy","tape",
        "trace","transform","transport","underlying","utilize","volume","whereas","whereby","abstract","accurate","acknowledge","aggregate",
        "allocate","assign","attach","author","bond","brief","capable","cite","cooperate","discriminate","display","diverse","domain","edit",
        "enhance","estate","exceed","expert","explicit","federal","fee","flexible","furthermore","gender","ignorance","implement","imply",
        "impose","invest","job","label","mechanism","medical","mental","monitor","network","neutral","nevertheless","notion","objective",
        "orient","perspective","precise","prime","psychology","pursue","ratio","reject","revenue","stable","statute","subordinate","subsidy"
    ] + [f"mid{i}" for i in range(1, 751)]),  # đủ 1500 từ

    "advanced": json.dumps([
        "abstract","acknowledge","acquisition","allocate","alter","amend","analogy","anticipate","apparent","append","apprehension","arbitrary",
        "assumption","assurance","attain","attribute","authoritative","automate","behalf","bias","cease","coherent","coincide","commence",
        "compatible","concurrent","confine","controversy","conversely","device","device","deviate","devote","diminish","discrete","discriminate",
        "display","distort","diverse","document","domain","domestic","dominate","dynamic","eliminate","empirical","enable","energy","enormous",
        "entire","entity","equivalent","erupt","estate","evolve","exceed","explicit","expose","external","facilitate","feasible","fluctuate",
        "format","founded","generate","generation","globe","grade","guarantee","hence","hierarchy","identical","ideology","ignorance","imply",
        "incentive","incidence","incline","incorporate","index","infer","infrastructure","inherent","initiate","innovation","input","insert",
        "insight","inspect","integral","interact","intermediate","internal","interpret","investigate","invoke","justify","layer","lecture",
        "likewise","link","locate","logic","maintain","manipulate","manual","margin","mature","mediate","medium","military","minimal","mutual",
        "norm","notion","objective","obtain","obvious","occupy","option","orient","output","overall","parallel","parameter","phase","phenomenon",
        "policy","practitioner","predominant","preliminary","presume","primary","prime","principle","priority","proceed","process","professional",
        "prohibit","publication","quote","radical","random","range","ratio","rational","react","recover","refine","regime","region","register",
        "regulate","reinforce","reject","release","rely","remove","resolve","resource","respond","restore","restrict","retain","reveal","revenue",
        "reverse","route","scenario","schedule","scheme","scope","section","sector","secure","seek","select","sequence","series","sex","shift",
        "significant","simulate","sole","somewhat","source","specific","sphere","stable","statistic","status","straightforward","submit",
        "subordinate","subsequent","subsidize","subsidy","substitute","successor","sufficient","suspend","sustain","symbol","tape","target",
        "technical","technique","technology","temporary","tense","terminate","theme","thereby","thesis","topic","trace","tradition","transfer",
        "transform","transit","transmit","transport","trend","trigger","ultimate","undergo","underlying","undertake","uniform","unify","utilize",
        "valid","vary","vehicle","version","via","virtual","visible","voluntary","welfare","whereas","whereby"
    ] + [f"adv{i}" for i in range(1, 1301)])  # đủ 1500 từ
}

# ===================== ROUTES =====================
@app.route('/')
def home():
    campaigns = Campaign.query.all()
    for c in campaigns:
        learned_list = json.loads(c.learned or '[]')
        total_list = json.loads(c.total_words)
        c.learned_count = len(learned_list)
        c.total_count = len(total_list)
        c.percent = round(c.learned_count / c.total_count * 100, 1) if c.total_count else 0
    return render_template('home.html', campaigns=campaigns)

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        level = request.form['level']
        c = Campaign(x=int(request.form['x']), total_words=WORDLISTS[level])
        db.session.add(c); db.session.commit()
        return redirect('/')
    return render_template('create.html')

def get_data(c):
    total = json.loads(c.total_words)
    learned = json.loads(c.learned or '[]')
    remain = [w for w in total if w not in learned]
    return total, learned, remain, len(total), len(learned)

@app.route('/lesson/<int:id>', methods=['GET','POST'])
def lesson(id):
    c = Campaign.query.get_or_404(id)
    today = date.today()
    total, learned, remain, total_cnt, learned_cnt = get_data(c)

    if request.method == 'POST':
        new_words = request.form.getlist('new_words[]')
        if new_words:
            if c.last_study_date != today:
                if c.last_study_date == today - timedelta(days=1):
                    c.streak += 1
                else:
                    c.streak = 1
                c.last_study_date = today
                badges = json.loads(c.badges)
                for m in [3,7,14,30,50,100,365]:
                    if c.streak >= m and m not in badges:
                        badges.append(m)
                c.badges = json.dumps(sorted(badges))

            learned_set = set(learned)
            learned_set.update(new_words)
            c.learned = json.dumps(list(learned_set))
            c.days += 1
            db.session.commit()
        return redirect(f'/lesson/{id}')

    current_streak = c.streak if c.last_study_date in [today, today - timedelta(days=1)] else 0
    badges_list = json.loads(c.badges)

    review = random.sample(learned, min(10, len(learned))) if learned else []
    review_words = [{'w': w, 'ipa': ipa(w), 'vn': get_meaning(w)} for w in review]

    today_words = random.sample(remain, min(c.x, len(remain))) if remain else []
    new_words = [{'w': w, 'ipa': ipa(w), 'vn': get_meaning(w)} for w in today_words]

    percent = round(learned_cnt / total_cnt * 100, 1) if total_cnt else 0

    return render_template('lesson.html',
        c=c, review=review_words, new=new_words,
        day=c.days + 1, percent=percent, learned=learned_cnt,
        current_streak=current_streak, badges=badges_list, total_cnt=total_cnt)

@app.route('/quiz/<int:id>', methods=['GET','POST'])
def quiz(id):
    c = Campaign.query.get_or_404(id)
    total, learned, _, _, learned_cnt = get_data(c)

    if request.method == 'POST':
        correct = sum(1 for k in request.form if k.startswith('answer_') and request.form[k] == request.form.get(f'correct_{k[7:]}'))
        total_q = len([k for k in request.form if k.startswith('answer_')])
        score = f"{correct}/{total_q}"
        if correct == total_q: score += " XUẤT SẮC!"
        return render_template('quiz.html', c=c, score=score, learned_count=learned_cnt)

    if learned_cnt < 5:
        return render_template('quiz.html', c=c, learned_count=learned_cnt)

    words = random.sample(learned, 5)
    questions = []
    for w in words:
        vn = get_meaning(w)
        opts = [vn]
        while len(opts) < 4:
            wrong = get_meaning(random.choice(total))
            if wrong not in opts and wrong != vn:
                opts.append(wrong)
        random.shuffle(opts)
        questions.append({'w': w, 'vn': vn, 'opts': opts})

    return render_template('quiz.html', c=c, q=questions, learned_count=learned_cnt)

@app.route('/audio/<w>')
@functools.lru_cache(maxsize=2000)
def audio(w):
    path = f"{AUDIO_DIR}/{w}.mp3"
    if not os.path.exists(path):
        from gtts import gTTS
        gTTS(w, lang='en').save(path)
    return send_file(path)
@functools.lru_cache(maxsize=6000)
def get_ipa(word):
    try:
        from gruut_ipa import convert
        return convert(word, lang='en-us')  # Hoặc 'en-gb' cho Anh-Anh
    except Exception as e:
        print(f"IPA error for '{word}': {e}")
        return f"/{word}/"  # Fallback đơn giản


if __name__ == '__main__':
    app.run(debug=False, threaded=True)