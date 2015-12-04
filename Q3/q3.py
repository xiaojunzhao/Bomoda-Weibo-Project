import re
import jieba as jb
import time
import heapq
from chinese_stop_words import stop_words
from mrjob.job import MRJob
from mrjob.job import MRStep
from mrjob.protocol import JSONValueProtocol

class MRWordCount3(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol


    def steps(self):
        return [
        MRStep(mapper=self.mapper_getterm,reducer=self.reducer_countterm),
        MRStep(mapper_init= self.init_get_10,
               mapper=self.mapper_term_gettop10,
               mapper_final=self.mapper_final_term_gettop10,
               reducer_init=self.reducer_init,
               reducer=self.reducer_get_top10,
               reducer_final=self.reducer_final)
        ]

    def mapper_getterm(self,key,comment_list):
        for comment in comment_list:
            try:
                status_text = comment['status']['text']

                filtered_status_text = re.sub(r'[^A-Za-z\s]+','',status_text)\
                                       .lower()
                comment_text = comment['text']
                if re.match('michael kors',filtered_status_text):
                    for word in jb.tokenize(unicode(comment_text)):
                            # filter Chinese terms and remove the stopwords
                            cond1 = re.match(ur'[\u4e00-\u9fff]+',word[0])
                            cond2 = word[0] not in stop_words
                            if cond1 and cond2:
                                yield ('michael',word[0]),1
                if re.match('kate spade',filtered_status_text):
                    for word in jb.tokenize(unicode(comment_text)):
                            # filter Chinese terms and remove the stopwords
                            cond1 = re.match(ur'[\u4e00-\u9fff]+',word[0])
                            cond2 = word[0] not in stop_words
                            if cond1 and cond2:
                                yield ('kate',word[0]),1
            except:
                pass

    def reducer_countterm(self,key,counts):
        yield key[0], (sum(counts),key[1])

    def init_get_10(self):
        self.mk_term = []
        self.ks_term = []

    def mapper_term_gettop10(self,key,term_count_pairs):
        if key=='michael':
            heapq.heappush(self.mk_term,term_count_pairs)
        elif key=='kate':
            heapq.heappush(self.ks_term,term_count_pairs)

    def mapper_final_term_gettop10(self):
        mk_term_largest = heapq.nlargest(10,self.mk_term)
        ks_term_largest = heapq.nlargest(10,self.ks_term)
        for count,key in mk_term_largest:
            yield ('mk_heap',(count,key))
        for count,key in ks_term_largest:
            yield ('ks_heap',(count,key))

    def reducer_init(self):
        self.mk_top10_termlist = []
        self.ks_top10_termlist = []

    def reducer_get_top10(self,key,top10):
        if key=='mk_heap':
            for term_count in top10:
                heapq.heappush(self.mk_top10_termlist,(term_count[0],term_count[1]))
        elif key=='ks_heap':
            for term_count in top10:
                heapq.heappush(self.ks_top10_termlist,(term_count[0],term_count[1]))

    def reducer_final(self):
        mk_term_largest = heapq.nlargest(10,self.mk_top10_termlist)
        mk_top10term = [(key,int(count)) for count,key in mk_term_largest]
        ks_term_largest = heapq.nlargest(10,self.ks_top10_termlist)
        ks_top10term = [(key,int(count)) for count,key in ks_term_largest]
        yield None,('mk',mk_top10term)
        yield None,('ks',ks_top10term)


if __name__=='__main__':
    MRWordCount3.run()
