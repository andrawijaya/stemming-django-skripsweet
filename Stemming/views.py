import csv, io
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .models import Instagram_comment, Stemming
from django.db.models.functions import Lower
import re
import string
import nltk
import io
import textwrap
import time

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# from pprint import pprint

import json

import logging

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

def index(request):

	return render(request,'index.html')

# def angkacoba():

#     iterasi = 1
#     iterasi+=1
#     return iterasi

# def test():
#     global str
#     Colors = ["Red", "Orange", "Yellow", "Green", "Blue"]
#     b = Colors(sep='/n')

    # for temp in subdata:
    #     return temp
    # c = print(*Colors, sep='\n')
    # return c
    # a = print('09','12','2016', sep='-')
    # return b

def post(request):
    global str
    context = None

    if request.method == 'POST':
        text = request.POST['input_text']
        # huruf_kecil = text.lower()
        # angka = re.sub(r"\d+", "", huruf_kecil)
        # tanda_baca = angka.translate(str.maketrans("","",string.punctuation))
        # karakter_kosong = tanda_baca.strip()
        # emoji = remove_emoji(karakter_kosong)

        tokens = word_tokenize(text)
        listStopword =  set(stopwords.words('indonesian'))

        removed = []
        for t in tokens:
            if t not in listStopword:
                removed.append(t)

        kemunculan = nltk.FreqDist(removed)
        most = kemunculan.most_common()
        obj = [str(elem) for elem in list(kemunculan.most_common())]
        most =  str(obj)

        angka2 = re.sub(r"\d+", "", most)
        tanda_baca3 = most.translate(str.maketrans("","",string.punctuation))
        angka3 = re.sub(r"\d+", "", tanda_baca3)

        # create stemmer
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        output   = stemmer.stem(angka2)

        tokens2 = word_tokenize(output)
        output3 = sorted(tokens2)
        output4 = ' '.join([str(e) for e in output3])
        kata = ["mete","tengok",'ate',"ambo","ase","buli","cak","luan","buek","kecek","peci","pandir","ancak","ota","suruk","gelak","cogok","tangkok","tobo","leme","padek","kucak","elok","litak","maro","mekak","rengam","pekaro","pai","sele","bawok","cangok","melalar","jolok","male","ciek","pane","ceme","lago","sangai","cakmano","selop","amek","pede","idup","bengak","bigal","buyan","tempek","gerot","letoi","angek","kipeh","asok","ulo","sadai","telampin","tibo","tekok","didik","madar","kucak","sengak","apik","ndak","pesong","berapo","tawo","kendak","basing","bere","berek","kecik","balak","ajo","gulo","kiro","apo","cando","kek","gaek","muko","warno","sudem","jele","benak","jugo","raso","pecayo","pakek","kito","mato","iko","segak","ado","baco","samo","kato","ngapo","lemak","lanang","dimano","celano","bukak","kerjo","cerito","pakso","kaco","gele","pacak","ingek","omong","dapek","punyo","kelak","ceriek","mertuo","rato","sano","icak","purak","upek","sikok","acik","sengajo","dekek","tanyo","keno","besak","dewek","galak","lupo","gilo","pakam","siko","jago","kalo","suko","nian","pucek","dang","uncu","donga","kemano","bak","nang","cam","keq","pangkeq","ubeq","pangkugh","dagheq","sikeq","isoq","ambiq","ibaq","lonceq","panggang","cepak","mueq","keciq","gedang","begheq","keghe","dekeq","saluagh","tekeloq","jambeqan","pangsiun","umpamo","jelepoq","lamo","sayit","baoq","kegheq","doghong","lipeq","rawaq","ghasan","ibo","dendang","gayut","tukagh","angkeq","kebeq","ibeq","jegheq","bueq","gelegh","gaut","kuweq","oloq","usigh","aghi","linte","bua","bate","atoq","limo","tigo","duo","tokoq","sileq","genti","dengagh","pukeq","basu","ciloq","sesa","cebum","getagh","gughuh","ghato","piagho","ughus","tempeq","ghatoq","pikigh","ikurh","anteq","keceq","baliq","benagh","ghaso","wancik","cepeq","segalo","dapeq","lelegh","aghoq","kelam","sanjo","panjeq","sintung","jau","gelimpang","kigho","ghami","lieq","lompeq","lebeq","oto","geghak","ghama","kutak","ghuma","gogheng","koghsi","laki","ceghai","lawu","tino","mudo","ghimbo","tikagh","aigh","oghang","kemaghin","daghi","nyo","pasagh","dapugh","empeq","sikugh","kini","jawo","njalo","cupaq","jeghek","ikugh","luso","suda","dusun","bughung","teghbang","elogi","cubo","mak","makcik","mbeli","sighih","keghno","lapagh","belanjo","alaman","beghsi","lepau","lapiq","lembagh","limau","pasigh","geghobak","mbaoq","piti","seghibu","datuk","sebghang","naghik","buluh","koghan","sugheq","cabiq","banjigh","anyut","gempo","ancugh","seghing","kighim","adiah","ghoboh","kejagh","jeghing","nokoq","badoq","baghu","mbueq","kabad","beghangkeq","nanam","coghet","aghang","pado","paghang","inga","tioq","sureq","pagagh","soghe","laghi","ajagh","ghajin","mendok","mbasuh","geghulun","ujan","idak","lape","sepeghti","njaig","teghus","keghjo","namo","beghe","taun","tiok","bungo","siapo","palaq","macemano","caro","kebilo","tangkoq","beghapo","ghego","cumpuk","beghankeq","ikeq","magholah","mbadoq","tetanggo","metik","kayo","ketiko","bahwo","pintagh","pulo","mbuka","pinggan","cinto","geghot","hanyo","susa","padohal","sakiq","juagho","peghna","selamo","mbaduq","ngighim","ngola","bembam","nggulai","nangkoq","eloq","dughian","bangso","sederhano","tidugh","mejo","kantogh","beghas","ari","biliq","begodoqan","lugha","geghobaq","jereq","naghiq","talang","njait","boli"]
        kata5 = ["ate"]
        kata6 = ["ate"]

        kata2 = sorted(kata)
        # print(kata2)
        # print(kata5)
        # print(type(tokens2))
        tambah = []
        # if angka2 in kata:
        #     print('berhasil')
        if 'acik' in tokens2:
            tambah.append('mendekati')
        if 'ari' in tokens2:
            tambah.append('hari')
        if 'anyut' in tokens2:
            tambah.append('hanyut')
        if 'adiah' in tokens2:
            tambah.append('hadiah')
        if 'ajagh' in tokens2:
            tambah.append('belajar')
        if 'aghang' in tokens2:
            tambah.append('arang')
        if 'aigh' in tokens2:
            tambah.append('air')
        if 'ancugh' in tokens2:
            tambah.append('hancur')
        if 'aghi' in tokens2:
            tambah.append('hari')
        if 'angkeq' in tokens2:
            tambah.append('angkat')
        if 'ado' in tokens2:
            tambah.append('ada')
        if 'ajo' in tokens2:
            tambah.append('aja')
        if 'apo' in tokens2:
            tambah.append('apa')
        if 'ambiq' in tokens2:
            tambah.append('ambil')
        if 'ambo' in tokens2:
            tambah.append('saya')
        if 'amek' in tokens2:
            tambah.append('nian')
        if 'apik' in tokens2:
            tambah.append('perhatikan')
        if 'asok' in tokens2:
            tambah.append('asap')
        if 'ancak' in tokens2:
            tambah.append('pamer')
        if 'aghoq' in tokens2:
            tambah.append('harap')
        if 'angek' in tokens2:
            tambah.append('marah')
        if 'anteq' in tokens2:
            tambah.append('antaran')
        if 'alaman' in tokens2:
            tambah.append('halaman')
        if 'ase' in tokens2:
            tambah.append('olok')
        if 'ate' in tokens2:
            tambah.append('atas')
        if 'atoq' in tokens2:
            tambah.append('atap')
        if 'baco' in tokens2:
            tambah.append('baca')
        if 'bahwo' in tokens2:
            tambah.append('bahwa')
        if 'balak' in tokens2:
            tambah.append('petaka')
        if 'begodoqan' in tokens2:
            tambah.append('berjualan')
        if 'bembam' in tokens2:
            tambah.append('mangga')
        if 'beghankeq' in tokens2:
            tambah.append('berangkat')
        if 'boli' in tokens2:
            tambah.append('boleh')
        if 'baliq' in tokens2:
            tambah.append('pulang')
        if 'badoq' in tokens2:
            tambah.append('pukul')
        if 'bak' in tokens2:
            tambah.append('ayah')
        if 'baoq' in tokens2:
            tambah.append('bawa')
        if 'bate' in tokens2:
            tambah.append('batas')
        if 'benak' in tokens2:
            tambah.append('tenggelam')
        if 'beghapo' in tokens2:
            tambah.append('berapo')
        if 'begheq' in tokens2:
            tambah.append('berat')
        if 'beghsi' in tokens2:
            tambah.append('bersih')
        if 'besak' in tokens2:
            tambah.append('besar')
        if 'basing' in tokens2:
            tambah.append('sembarang')
        if 'bangso' in tokens2:
            tambah.append('bangsa')
        if 'basu' in tokens2:
            tambah.append('cuci')
        if 'biliq' in tokens2:
            tambah.append('kamar')
        if 'bughung' in tokens2:
            tambah.append('burung')
        if 'bawok' in tokens2:
            tambah.append('bawa')
        if 'beghe' in tokens2:
            tambah.append('beras')
        if 'bengak' in tokens2:
            tambah.append('bodoh')
        if 'baghu' in tokens2:
            tambah.append('baru')
        if 'berapo' in tokens2:
            tambah.append('berapa')
        if 'bere' in tokens2:
            tambah.append('beras')
        if 'benagh' in tokens2:
            tambah.append('benar')
        if 'berek' in tokens2:
            tambah.append('berat')
        if 'bungo' in tokens2:
            tambah.append('bunga')
        if 'banjigh' in tokens2:
            tambah.append('banjir')
        if 'beghas' in tokens2:
            tambah.append('beras')
        if 'beghangkeq' in tokens2:
            tambah.append('berangkat')
        if 'buluh' in tokens2:
            tambah.append('bambu')
        if 'bigal' in tokens2:
            tambah.append('bodoh')
        if 'bua' in tokens2:
            tambah.append('buah')
        if 'buek' in tokens2:
            tambah.append('buat')
        if 'belanjo' in tokens2:
            tambah.append('belanja')
        if 'bueq' in tokens2:
            tambah.append('buat')
        if 'bukak' in tokens2:
            tambah.append('buka')
        if 'buli' in tokens2:
            tambah.append('boleh')
        if 'buyan' in tokens2:
            tambah.append('bodoh')
        if 'cak' in tokens2:
            tambah.append('seperti')
        if 'cakmano' in tokens2:
            tambah.append('bagaimana')
        if 'celano' in tokens2:
            tambah.append('celana')
        if 'caro' in tokens2:
            tambah.append('cara')
        if 'cebum' in tokens2:
            tambah.append('cebur')
        if 'ceme' in tokens2:
            tambah.append('cemas')
        if 'cumpuk' in tokens2:
            tambah.append('tumpuk')
        if 'cerito' in tokens2:
            tambah.append('cerita')
        if 'ceriek' in tokens2:
            tambah.append('curang')
        if 'cepak' in tokens2:
            tambah.append('sepak')
        if 'coghet' in tokens2:
            tambah.append('mencoreti')
        if 'cabiq' in tokens2:
            tambah.append('sobek')
        if 'cinto' in tokens2:
            tambah.append('cinta')
        if 'cepeq' in tokens2:
            tambah.append('cepat')
        if 'ceghai' in tokens2:
            tambah.append('cerai')
        if 'cam' in tokens2:
            tambah.append('macam')
        if 'cando' in tokens2:
            tambah.append('canda')
        if 'ciek' in tokens2:
            tambah.append('curang')
        if 'ciloq' in tokens2:
            tambah.append('curi')
        if 'cangok' in tokens2:
            tambah.append('rakus')
        if 'cogok' in tokens2:
            tambah.append('tunggu')
        if 'cupaq' in tokens2:
            tambah.append('kaleng')
        if 'cubo' in tokens2:
            tambah.append('coba')
        if 'dagheq' in tokens2:
            tambah.append('darat')
        if 'dekeq' in tokens2:
            tambah.append('dekat')
        if 'dang' in tokens2:
            tambah.append('kakak')
        if 'dapek' in tokens2:
            tambah.append('dapat')
        if 'dapeq' in tokens2:
            tambah.append('dapat')
        if 'dapugh' in tokens2:
            tambah.append('dapur')
        if 'dekek' in tokens2:
            tambah.append('dekat')
        if 'daghi' in tokens2:
            tambah.append('dari')
        if 'dendang' in tokens2:
            tambah.append('nyanyi')
        if 'dughian' in tokens2:
            tambah.append('durian')
        if 'dengagh' in tokens2:
            tambah.append('dengar')
        if 'dewek' in tokens2:
            tambah.append('sendiri')
        if 'didik' in tokens2:
            tambah.append('bodoh')
        if 'datuk' in tokens2:
            tambah.append('kakek')
        if 'doghong' in tokens2:
            tambah.append('dorong')
        if 'dimano' in tokens2:
            tambah.append('dimana')
        if 'duo' in tokens2:
            tambah.append('dua')
        if 'dusun' in tokens2:
            tambah.append('desa')
        if 'donga' in tokens2:
            tambah.append('kakak (perempuan)')
        if 'elok' in tokens2:
            tambah.append('bagus')
        if 'eloq' in tokens2:
            tambah.append('bagus')
        if 'elogi' in tokens2:
            tambah.append('maaf')
        if 'empeq' in tokens2:
            tambah.append('empat')
        if 'gaek' in tokens2:
            tambah.append('bapak')
        if 'gedang' in tokens2:
            tambah.append('besar')
        if 'geghot' in tokens2:
            tambah.append('hebat')
        if 'ghato' in tokens2:
            tambah.append('rata')
        if 'ghaso' in tokens2:
            tambah.append('rasa')
        if 'galak' in tokens2:
            tambah.append('mau')
        if 'ghimbo' in tokens2:
            tambah.append('rimba')
        if 'gayut' in tokens2:
            tambah.append('gantung')
        if 'ghatoq' in tokens2:
            tambah.append('ratap')
        if 'geghobak' in tokens2:
            tambah.append('gerobak')
        if 'geghulun' in tokens2:
            tambah.append('pakaian')
        if 'ghama' in tokens2:
            tambah.append('ramah')
        if 'ghami' in tokens2:
            tambah.append('rami')
        if 'ghasan' in tokens2:
            tambah.append('runding')
        if 'gelak' in tokens2:
            tambah.append('tawa')
        if 'gelimpang' in tokens2:
            tambah.append('guling')
        if 'gele' in tokens2:
            tambah.append('gelas')
        if 'gelegh' in tokens2:
            tambah.append('gilir')
        if 'geghak' in tokens2:
            tambah.append('gerak')
        if 'getagh' in tokens2:
            tambah.append('getar')
        if 'geghobaq' in tokens2:
            tambah.append('gerobak')
        if 'gughuh' in tokens2:
            tambah.append('guruh')
        if 'ghoboh' in tokens2: 
            tambah.append('roboh')
        if 'genti' in tokens2:
            tambah.append('ganti')
        if 'ghajin' in tokens2:
            tambah.append('rajin')
        if 'gempo' in tokens2:
            tambah.append('gempa')
        if 'gogheng' in tokens2:
            tambah.append('goreng')
        if 'gaut' in tokens2:
            tambah.append('garuk')
        if 'ghuma' in tokens2:
            tambah.append('rumah')
        if 'gerot' in tokens2:
            tambah.append('kuat')
        if 'gilo' in tokens2:
            tambah.append('gila')
        if 'ghego' in tokens2:
            tambah.append('harga')
        if 'gulo' in tokens2:
            tambah.append('gula')
        if 'hanyo' in tokens2:
            tambah.append('hanya')
        if 'njaig' in tokens2:
            tambah.append('jahit')
        if 'ibaq' in tokens2:
            tambah.append('bungkus')
        if 'idak' in tokens2:
            tambah.append('tidak')
        if 'ibeq' in tokens2:
            tambah.append('bungkus')
        if 'ibo' in tokens2:
            tambah.append('iba')
        if 'ikurh' in tokens2:
            tambah.append('ekor')
        if 'ikugh' in tokens2:
            tambah.append('ikur')
        if 'ikeq' in tokens2:
            tambah.append('ikat')
        if 'idup' in tokens2:
            tambah.append('hidup')
        if 'iko' in tokens2:
            tambah.append('ini')
        if 'icak' in tokens2:
            tambah.append('pura-pura')
        if 'ingek' in tokens2:
            tambah.append('ingat')
        if 'inga' in tokens2:
            tambah.append('kakak')
        if 'isoq' in tokens2:
            tambah.append('hisap')
        if 'jambeqan' in tokens2:
            tambah.append('jembatan')
        if 'jau' in tokens2:
            tambah.append('jauh')
        if 'jegheq' in tokens2:
            tambah.append('jerat')
        if 'jele' in tokens2:
            tambah.append('jelas')
        if 'juagho' in tokens2:
            tambah.append('juara')
        if 'jawo' in tokens2:
            tambah.append('jawa')
        if 'jelepoq' in tokens2:
            tambah.append('terjatuh')
        if 'jeghek' in tokens2:
            tambah.append('ikat')
        if 'jolok' in tokens2:
            tambah.append('hendak')
        if 'jereq' in tokens2:
            tambah.append('jaringan')
        if 'jago' in tokens2:
            tambah.append('jaga')
        if 'jeghing' in tokens2:
            tambah.append('jengkol')
        if 'kaco' in tokens2:
            tambah.append('kaca')
        if 'kejagh' in tokens2:
            tambah.append('kejar')
        if 'kato' in tokens2:
            tambah.append('kata')
        if 'kebeq' in tokens2:
            tambah.append('ikat')
        if 'kebilo' in tokens2:
            tambah.append('kapan')
        if 'kelak' in tokens2:
            tambah.append('nanti')
        if 'kayo' in tokens2:
            tambah.append('kaya')
        if 'kalo' in tokens2:
            tambah.append('kalau')
        if 'koghan' in tokens2:
            tambah.append('koran')
        if 'kendak' in tokens2:
            tambah.append('mau')
        if 'keno' in tokens2:
            tambah.append('kena')
        if 'keghno' in tokens2:
            tambah.append('karena')
        if 'keceq' in tokens2:
            tambah.append('kata')
        if 'kemano' in tokens2:
            tambah.append('kemana')
        if 'kantogh' in tokens2:
            tambah.append('kantor')
        if 'kecek' in tokens2:
            tambah.append('bicara')
        if 'kelam' in tokens2:
            tambah.append('gelap')
        if 'kabad' in tokens2:
            tambah.append('lemari')
        if 'kecik' in tokens2:
            tambah.append('kecil')
        if 'keciq' in tokens2:
            tambah.append('kecil')
        if 'koghsi' in tokens2:
            tambah.append('kursi')
        if 'kek' in tokens2:
            tambah.append('dengan')
        if 'kerjo' in tokens2:
            tambah.append('kerja')
        if 'ketiko' in tokens2:
            tambah.append('ketika')
        if 'kemaghin' in tokens2:
            tambah.append('kemarin')
        if 'kutak' in tokens2:
            tambah.append('kerja')
        if 'kegheq' in tokens2:
            tambah.append('potong')
        if 'keq' in tokens2:
            tambah.append('dengan')
        if 'kipeh' in tokens2:
            tambah.append('kipas')
        if 'keghjo' in tokens2:
            tambah.append('kerja')
        if 'kigho' in tokens2:
            tambah.append('kira')
        if 'kiro' in tokens2:
            tambah.append('kira')
        if 'kito' in tokens2:
            tambah.append('kita')
        if 'keghe' in tokens2:
            tambah.append('keras')
        if 'kighim' in tokens2:
            tambah.append('kirim')
        if 'kucak' in tokens2:
            tambah.append('ganggu')
        if 'kuweq' in tokens2:
            tambah.append('kuat')
        if 'lawu' in tokens2:
            tambah.append('laku')
        if 'luso' in tokens2:
            tambah.append('lusa')
        if 'lapiq' in tokens2:
            tambah.append('tikar')
        if 'naghiq' in tokens2:
            tambah.append('tarik')
        if 'lembagh' in tokens2:
            tambah.append('lembar')
        if 'limau' in tokens2:
            tambah.append('jeruk')
        if 'lapagh' in tokens2:
            tambah.append('lapar')
        if 'lanang' in tokens2:
            tambah.append('laki-laki')
        if 'lago' in tokens2:
            tambah.append('berkelahi')
        if 'laki' in tokens2:
            tambah.append('suami')
        if 'lipeq' in tokens2:
            tambah.append('lipat')
        if 'lieq' in tokens2:
            tambah.append('lihat')
        if 'lugha' in tokens2:
            tambah.append('lurah')
        if 'lemak' in tokens2:
            tambah.append('sedap')
        if 'lelegh' in tokens2:
            tambah.append('alir')
        if 'lamo' in tokens2:
            tambah.append('lama')
        if 'leme' in tokens2:
            tambah.append('lemas')
        if 'laghi' in tokens2:
            tambah.append('lari')
        if 'lepau' in tokens2:
            tambah.append('warung')
        if 'lebeq' in tokens2:
            tambah.append('lebat')
        if 'letoi' in tokens2:
            tambah.append('lesu')
        if 'litak' in tokens2:
            tambah.append('letih')
        if 'limo' in tokens2:
            tambah.append('lima')
        if 'linte' in tokens2:
            tambah.append('lintas')
        if 'luan' in tokens2:
            tambah.append('mendahului')
        if 'lupo' in tokens2:
            tambah.append('lupa')
        if 'lape' in tokens2:
            tambah.append('lapar')
        if 'lonceq' in tokens2:
            tambah.append('loncat')
        if 'lompeq' in tokens2:
            tambah.append('lompat')
        if 'madar' in tokens2:
            tambah.append('santai')
        if 'mudo' in tokens2:
            tambah.append('muda')
        if 'male' in tokens2:
            tambah.append('malas')
        if 'maro' in tokens2:
            tambah.append('tegur')
        if 'mato' in tokens2:
            tambah.append('mata')
        if 'mendok' in tokens2:
            tambah.append('tinggal')
        if 'mbaduq' in tokens2:
            tambah.append('pukul')
        if 'mbaoq' in tokens2:
            tambah.append('bawa')
        if 'mejo' in tokens2:
            tambah.append('meja')
        if 'mekak' in tokens2:
            tambah.append('berisik')
        if 'melalar' in tokens2:
            tambah.append('layap')
        if 'magholah' in tokens2:
            tambah.append('marilah')
        if 'mertuo' in tokens2:
            tambah.append('mertua')
        if 'mak' in tokens2:
            tambah.append('ibu')
        if 'mbadoq' in tokens2:
            tambah.append('pukul')
        if 'mbuka' in tokens2:
            tambah.append('buka')
        if 'makcik' in tokens2:
            tambah.append('bibi')
        if 'mbeli' in tokens2:
            tambah.append('beli')
        if 'mete' in tokens2:
            tambah.append('pacar')
        if 'mueq' in tokens2:
            tambah.append('muat')
        if 'metik' in tokens2:
            tambah.append('petik')
        if 'mbasuh' in tokens2:
            tambah.append('mencuci')
        if 'mbueq' in tokens2:
            tambah.append('buat')
        if 'muko' in tokens2:
            tambah.append('muka')
        if 'macemano' in tokens2:
            tambah.append('bagaimana')
        if 'nang' in tokens2:
            tambah.append('yang')
        if 'njait' in tokens2:
            tambah.append('menjahit')
        if 'ndak' in tokens2:
            tambah.append('mau')
        if 'nggulai' in tokens2:
            tambah.append('gulai')
        if 'nangkoq' in tokens2:
            tambah.append('tangkap')
        if 'njalo' in tokens2:
            tambah.append('mencala')
        if 'nanam' in tokens2:
            tambah.append('tanam')
        if 'ngola' in tokens2:
            tambah.append('garap')
        if 'nian' in tokens2:
            tambah.append('sungguh')
        if 'nyo' in tokens2:
            tambah.append('dia')
        if 'ngapo' in tokens2:
            tambah.append('kenapa')
        if 'nokoq' in tokens2:
            tambah.append('pukul')
        if 'ngighim' in tokens2:
            tambah.append('kirim')
        if 'naghik' in tokens2:
            tambah.append('menarik')
        if 'namo' in tokens2:
            tambah.append('nama')
        if 'omong' in tokens2:
            tambah.append('cakap')
        if 'oloq' in tokens2:
            tambah.append('ganggu')
        if 'ota' in tokens2:
            tambah.append('bual')
        if 'oto' in tokens2:
            tambah.append('mobil')
        if 'oghang' in tokens2:
            tambah.append('orang')
        if 'pacak' in tokens2:
            tambah.append('bisa')
        if 'pakso' in tokens2:
            tambah.append('paksa')
        if 'pasigh' in tokens2:
            tambah.append('pasir')
        if 'pangkeq' in tokens2:
            tambah.append('pangkat')
        if 'pagagh' in tokens2:
            tambah.append('pagar')
        if 'panggang' in tokens2:
            tambah.append('bakar')
        if 'pecayo' in tokens2:
            tambah.append('percaya')
        if 'peghna' in tokens2:
            tambah.append('pernah')
        if 'padek' in tokens2:
            tambah.append('hebat')
        if 'pai' in tokens2:
            tambah.append('pergi')
        if 'pakam' in tokens2:
            tambah.append('hebat')
        if 'paghang' in tokens2:
            tambah.append('parang')
        if 'palaq' in tokens2:
            tambah.append('kepala')
        if 'pinggan' in tokens2:
            tambah.append('piring')
        if 'pakek' in tokens2:
            tambah.append('pakai')
        if 'pado' in tokens2:
            tambah.append('pada')
        if 'pandir' in tokens2:
            tambah.append('sombong')
        if 'pangkugh' in tokens2:
            tambah.append('cangkul')
        if 'pasagh' in tokens2:
            tambah.append('pasar')
        if 'pintagh' in tokens2:
            tambah.append('pintar')
        if 'pangsiun' in tokens2:
            tambah.append('pensiun')
        if 'pulo' in tokens2:
            tambah.append('pula')
        if 'piagho' in tokens2:
            tambah.append('piara')
        if 'pikigh' in tokens2:
            tambah.append('pikir')
        if 'pane' in tokens2:
            tambah.append('panas')
        if 'peci' in tokens2:
            tambah.append('lanjut')
        if 'pede' in tokens2:
            tambah.append('pedas')
        if 'padohal' in tokens2:
            tambah.append('padahal')
        if 'panjeq' in tokens2:
            tambah.append('panjat')
        if 'pekaro' in tokens2:
            tambah.append('masalah')
        if 'pesong' in tokens2:
            tambah.append('gila')
        if 'pucek' in tokens2:
            tambah.append('pucat')
        if 'piti' in tokens2:
            tambah.append('uang')
        if 'pukeq' in tokens2:
            tambah.append('pukat')
        if 'punyo' in tokens2:
            tambah.append('punya')
        if 'purak' in tokens2:
            tambah.append('pura-pura')
        if 'raso' in tokens2:
            tambah.append('rasa')
        if 'rato' in tokens2:
            tambah.append('rata')
        if 'rawaq' in tokens2:
            tambah.append('duga')
        if 'rengam' in tokens2:
            tambah.append('kesal')
        if 'sadai' in tokens2:
            tambah.append('tunggu')
        if 'samo' in tokens2:
            tambah.append('sama')
        if 'sureq' in tokens2:
            tambah.append('surat')
        if 'sano' in tokens2:
            tambah.append('sana')
        if 'sebghang' in tokens2:
            tambah.append('seberang')
        if 'saluagh' in tokens2:
            tambah.append('celana')
        if 'seghing' in tokens2:
            tambah.append('sering')
        if 'sederhano' in tokens2:
            tambah.append('sederhana')
        if 'sangai' in tokens2:
            tambah.append('menunggu lama')
        if 'sanjo' in tokens2:
            tambah.append('kunjung')
        if 'suda' in tokens2:
            tambah.append('sudah')
        if 'sayit' in tokens2:
            tambah.append('iris')
        if 'segak' in tokens2:
            tambah.append('bentak')
        if 'segalo' in tokens2:
            tambah.append('segala')
        if 'soghe' in tokens2:
            tambah.append('sore')
        if 'seghibu' in tokens2:
            tambah.append('seribu')
        if 'sesa' in tokens2:
            tambah.append('cuci')
        if 'siapo' in tokens2:
            tambah.append('siapa')
        if 'selop' in tokens2:
            tambah.append('sendal')
        if 'sele' in tokens2:
            tambah.append('kurang')
        if 'selamo' in tokens2:
            tambah.append('selama')
        if 'sighih' in tokens2:
            tambah.append('sirih')
        if 'sepeghti' in tokens2:
            tambah.append('seperti')
        if 'sengak' in tokens2:
            tambah.append('sombong')
        if 'susa' in tokens2:
            tambah.append('susah')
        if 'sengajo' in tokens2:
            tambah.append('sengaja')
        if 'sikeq' in tokens2:
            tambah.append('sikat')
        if 'sugheq' in tokens2:
            tambah.append('surat')
        if 'kini' in tokens2:
            tambah.append('sekarang')
        if 'sikugh' in tokens2:
            tambah.append('seekor')
        if 'sejegheg' in tokens2:
            tambah.append('seikat')
        if 'sileq' in tokens2:
            tambah.append('silat')
        if 'sakiq' in tokens2:
            tambah.append('sakit')
        if 'siko' in tokens2:
            tambah.append('sini')
        if 'sintung' in tokens2:
            tambah.append('sentuh')
        if 'sikok' in tokens2:
            tambah.append('satu')
        if 'sudem' in tokens2:
            tambah.append('sudah')
        if 'suko' in tokens2:
            tambah.append('suka')
        if 'suruk' in tokens2:
            tambah.append('sembunyi')
        if 'tempek' in tokens2:
            tambah.append('tempat')
        if 'tempeq' in tokens2:
            tambah.append('tempat')
        if 'tanyo' in tokens2:
            tambah.append('tanya')
        if 'tidugh' in tokens2:
            tambah.append('tidur')
        if 'tetanggo' in tokens2:
            tambah.append('tetangga')
        if 'tangkok' in tokens2:
            tambah.append('tangkap')
        if 'talang' in tokens2:
            tambah.append('pagar')
        if 'tawo' in tokens2:
            tambah.append('tawa')
        if 'tekeloq' in tokens2:
            tambah.append('tertidur')
        if 'tekok' in tokens2:
            tambah.append('tebak')
        if 'tangkoq' in tokens2:
            tambah.append('tangkap')
        if 'tioq' in tokens2:
            tambah.append('tiap')
        if 'telampin' in tokens2:
            tambah.append('kena imbas')
        if 'tengok' in tokens2:
            tambah.append('lihat')
        if 'tiok' in tokens2:
            tambah.append('tiap')
        if 'teghbang' in tokens2:
            tambah.append('terbang')
        if 'tibo' in tokens2:
            tambah.append('tiba')
        if 'tikagh' in tokens2:
            tambah.append('tikar')
        if 'tukagh' in tokens2:
            tambah.append('tukar')
        if 'tobo' in tokens2:
            tambah.append('mereka')
        if 'tokoq' in tokens2:
            tambah.append('pukul')
        if 'teghus' in tokens2:
            tambah.append('terus')
        if 'tigo' in tokens2:
            tambah.append('tiga')
        if 'taun' in tokens2:
            tambah.append('tahun')
        if 'tino' in tokens2:
            tambah.append('gadis')
        if 'ubeq' in tokens2:
            tambah.append('obat')
        if 'ulo' in tokens2:
            tambah.append('bedagang')
        if 'umpamo' in tokens2:
            tambah.append('umpama')
        if 'uncu' in tokens2:
            tambah.append('tante')
        if 'upek' in tokens2:
            tambah.append('gunjing')
        if 'ujan' in tokens2:
            tambah.append('hujan')
        if 'usigh' in tokens2:
            tambah.append('usir')
        if 'ughus' in tokens2:
            tambah.append('urusi')
        if 'warno' in tokens2:
            tambah.append('warna')
        if 'wancik' in tokens2:
            tambah.append('paman')
        if  not output in kata:
            tambah.append(output)
        # else:
        #     if 'ambo' in tokens2:
        #         tambah.append('saya')
        #     if 'ancak' in tokens2:
        #         tambah.append('lihat')
        #     if 'ase' in tokens2:
        #         tambah.append('atas')
        #     if 'ate' in tokens2:
        #         tambah.append('atas')
        #     if 'buek' in tokens2:
        #         tambah.append('buek')
        #     if 'buli' in tokens2:
        #         tambah.append('atas')
        #     if 'cak' in tokens2:
        #         tambah.append('seperti')
        #     if 'cogok' in tokens2:
        #         tambah.append('atas')
        #     if 'gelak' in tokens2:
        #         tambah.append('tawa')
        #     if 'kecek' in tokens2:
        #         tambah.append('bicara')
        #     if 'kicu' in tokens2:
        #         tambah.append('bohong')
        #     if 'leme' in tokens2:
        #         tambah.append('lemas')
        #     if 'luan' in tokens2:
        #         tambah.append('atas')
        #     if 'male' in tokens2:
        #         tambah.append('malas')
        #     if 'mete' in tokens2:
        #         tambah.append('pacar')
        #     if 'ota' in tokens2:
        #         tambah.append('atas')
        #     if 'padek' in tokens2:
        #         tambah.append('hebat')
        #     if 'pandir' in tokens2:
        #         tambah.append('sombong')
        #     if 'peci' in tokens2:
        #         tambah.append('atas')
        #     if 'suruk' in tokens2:
        #         tambah.append('sembunyi')
        #     if 'tangkok' in tokens2:
        #         tambah.append('tangkap')
        #     if 'tengok' in tokens2:
        #         tambah.append('lihat')
        #     if 'tobo' in tokens2:
        #         tambah.append('mereka')

        print(tambah)
            # if output == 'tengok':
            #     tambah.append('lihat')
            # if output == 'ambo':
            #     tambah.append('saya')
            # if output == 'ase':
            #     tambah.append('neh')
            # if output == 'buli':
            #     tambah.append('boleh')
            # if output == 'cak':
            #     tambah.append('seperti')
            # if output == 'luan':
            #     tambah.append('duluan')
            # if output == 'buek':
            #     tambah.append('buat')
            # if output == 'kecek':
            #     tambah.append('bicara')
            # if output == 'peci':
            #     tambah.append('duluan')
            # if output == 'pandir':
            #     tambah.append('sombong')
            # if output == 'ancak':
            #     tambah.append('duluan')
            # if output == 'ota':
            #     tambah.append('bohong')
            # if output == 'suruk':
            #     tambah.append('sembunyi')
            # if output == 'gelak':
            #     tambah.append('tawa')
            # if output == 'cogok':
            #     tambah.append('tunggu')
            # if output == 'tangkok':
            #     tambah.append('tangkap')
            # if output == 'tobo':
            #     tambah.append('mereka')
            # if output == 'leme':
            #     tambah.append('lesu')
            # if output == 'padek':
            #     tambah.append('hebat')


        # obj = [str(elem) for elem in list(tambah)]
        # yes = str(obj)
        # no = re.sub(r"\d+", "", yes)
        objek = ' '.join([str(elem) for elem in tambah])

        output1 = 'kata dasar:' +' '+ output4
        output2 = 'arti:' + ' '+ objek
        # testnian = stemmer.get_dictionary(huruf_kecil)

#---------------------------------------------------------------------#
        # # stemming process


        # pprint(text())
        context = {
		"output_text": output1,
        "arti_text":output2,
        "input_text": text,
	    }

    return render(request, 'index.html', context)


@permission_required('admin.can_add_log_entry')
def upload_csv(request):

    Instagram_comment.objects.all().delete()
    csv_file = request.FILES['file']

    if not csv_file.name.endswith('csv'):
        messages.error(request, 'this is not a csv file')
        return redirect('index')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Instagram_comment.objects.update_or_create(
            name=column[0],
            comment=column[1],
        )

    context = {}
    return render(request, 'upload_csv.html', context)

def stemming(request):
    start = time.time()
    global str

    obj = [str(elem) for elem in list(Instagram_comment.objects.all().values_list('comment'))]
    text =  str(obj)
    context = None

    huruf_kecil = text.lower()
    angka = re.sub(r"\d+", "", huruf_kecil)
    tanda_baca = angka.translate(str.maketrans("","",string.punctuation))
    karakter_kosong = tanda_baca.strip()
    emoji = remove_emoji(karakter_kosong)

    tokens = word_tokenize(emoji)
    listStopword =  set(stopwords.words('indonesian'))

    removed = []
    for t in tokens:
        if t not in listStopword:
            removed.append(t)

    kemunculan = nltk.FreqDist(removed)
    most = kemunculan.most_common()
    obj = [str(elem) for elem in list(kemunculan.most_common())]
    obj.sort()
    most =  str(obj)

    angka2 = re.sub(r"\d+", "", most)
    tanda_baca3 = most.translate(str.maketrans("","",string.punctuation))

    resul = [int(s) for s in tanda_baca3.split() if s.isdigit()]
    tanda_baca2 = angka2.translate(str.maketrans("","",string.punctuation))

    testo = tanda_baca2.split()
    testo.sort()
    mamang = str(testo)

    uyo = [(ok) for i,ok in enumerate(testo)]
    uya = [(i) for i,ok in enumerate(testo, 1)]

    zipper = list(zip(uya, uyo))

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    output   = stemmer.stem(mamang)

    out = output.split()
    uy = [(ok) for i,ok in enumerate(out)]
    ay = [(i) for i,ok in enumerate(out, 1)]

    zipper2 = list(zip(ay, uy))
    Stemming.objects.all().delete()
    Stemming.objects.bulk_create([Stemming(**{'tokens' : m,
                                              'stem' : x,
                                              'frek' : y})
                            for m,x,y in zip(uyo,uy,resul)])

    stop = time.time()
    ran = stop-start

    context = {
	"output_text":output,
    'dataset': text,
    'proses' : tanda_baca2,
    'stemming' : zipper,
    'root_word' : zipper2,
    'time' : ran,
    "case_folding": emoji,
    "tokenizing" : tokens,
    "remove_stopword" : removed,
    "corpus" : most,
	}

    return render(request, "base.html", context)

def export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['tokens','stem','frek'])
    for export in Stemming.objects.all().values_list('tokens', 'stem', 'frek'):
        writer.writerow(export)

    response['Content-Disposition'] = 'attachment; filename="stemmings.csv"'
    return response




    # if request.method == 'POST':
	# 	print("ini adalah method post")
	# 	context['nama'] = request.POST['nama']
	# 	context['alamat'] = request.POST['alamat']
	# else:
	# 	print("ini adalah method get")

	# return render(request, 'index.html', context)



def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)
