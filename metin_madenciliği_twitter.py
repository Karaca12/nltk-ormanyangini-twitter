

import tweepy as tw

################# veri toplama   ##################

consumer_key="lütfen twitter api alınız"
consumer_secret="lütfen twitter api alınız"
access_token="lütfen twitter api alınız"
access_token_secret="lütfen twitter api alınız"




auth = tw.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth)


başlangıç_zaman="2021-08-06"
bitiş_zaman="2021-08-07"

enlem_boylam_kapsam="37.2154,28.3636,50km"

tweet= tw.Cursor( api.search,
                           q="#yangın",
                           rpp=100,
                           result_type="recent",
                           include_entities=True,
                           lang="tr",geocode=enlem_boylam_kapsam,
                           since=başlangıç_zaman,
                           until=bitiş_zaman).items(1000)

########### veri biçimlendirme ##################
import pandas as pd

liste=list()

zaman_liste=list()


lokasyonlar=list()

for i in tweet:
    
    liste.append(i.text)
    zaman_liste.append(i.created_at )
    lokasyonlar.append(i.user.location)
    
    



import nltk
from nltk import pos_tag
from nltk.probability import FreqDist
from nltk.corpus import treebank
from nltk.corpus import stopwords

import nltk
nltk.download('punkt')



genelKelimeler = nltk.word_tokenize(str(liste))

küçük_harf=[i.lower() for i in genelKelimeler]

türkçe_dolgular = set(stopwords.words('turkish'))


t_kelimeler=[i for i in küçük_harf if i.isalpha()]

dolgu_temizliği=[kelime for kelime in t_kelimeler if kelime not in türkçe_dolgular]



###### frame oluşturma ##################
temizlenmiş_kelimeler=list()

lokal_dolgular=["https","ve","veya","bir","bi","için","gibi","bir","mugla","gundem"
                ,"yok","kadar","artık","a","ben","var","göre","m","olsun","allah","bile","sen","değil"
                ,"mi","türkiyeyanıyor","alevler","yangın","yangin","yanan","devam","yangını"]
for i in dolgu_temizliği:
    
    if i in lokal_dolgular:
        pass
    
    else:
        temizlenmiş_kelimeler.append(i)
       
        

dataf=pd.DataFrame({"tweetler":liste,"tarih":zaman_liste,"yer":lokasyonlar})

kelime_frekansları=FreqDist(temizlenmiş_kelimeler)    
en_çok_10_frekans=kelime_frekansları.most_common(10)



