### use Natural Language API
### Author: Nicole

#!/usr/bin/python
# -*- coding: UTF-8 -*-
from google.cloud import language
import pandas as pd
import numpy as np

def nlp(contenttext):
    client = language.LanguageServiceClient()
    document = language.types.Document(
        content = contenttext,
        type=language.enums.Document.Type.PLAIN_TEXT,
    )

    response = client.analyze_entities(
       document=document,
       encoding_type='UTF8',
    )

    TYPE = {
        '0':'UNKNOWN',
        '1':'PERSON',
        '2':'LOCATION',
        '3':'ORGANIZATION',
        '4':'EVENT',
        '5':'WORK_OF_ART',
        '6':'CONSUMER_GOOD',
        '7':'OTHER'
    }

    names = [entity.name for entity in response.entities]
    types = [TYPE[str(entity.type)] for entity in response.entities]
    saliences = [entity.salience for entity in response.entities]
    out = pd.DataFrame({"keywords":names,"type":types,"salience":saliences})
    return(out)


if __name__ == '__main__':
    article = '在美國三大指數中（納斯達克指數、標普500指數、道瓊指數），那斯達克指數一向被視為最能代表科技股的關鍵指數，投資人若想參與科技股的成長，只要投資納斯達克100指數ETF-QQQ就可簡單達成。目前QQQ前五大持股分別為蘋果（11.93%）、亞馬遜（9.88%）、微軟（9.59%）、臉書（5.68%）、谷哥（4.88%），合計占比超過4成，每家公司都是全球知名且深刻影響世界生活的公司，投資人只要透過QQQ就可以將這些公司一籃子買下來，統計過去5年投資QQQ的年化報酬率高達20.37%，比起投資個股一點都不遜色，並可有效分散風險。'
    df = nlp(article)
    print(df)
