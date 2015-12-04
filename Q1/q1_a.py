import re
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONValueProtocol
class MRWordCount1(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def steps(self):
        return [
        MRStep(mapper=self.mapper_get,
                reducer=self.reducer_count_rep),
        MRStep(reducer=self.reducer_count_norep)
    ]

    def mapper_get(self,key,post):
        for item in post:
            text = item['text']
            new_text = re.sub(r'[^A-Za-z\s]+','',text)\
                         .lower()
            if re.match('michael kors',new_text):
                yield ('mk','post'),1
                yield ('mk',item['user']['id']),1
            if re.match('kate spade',new_text):
                yield ('ks','post'),1
                yield ('ks',item['user']['id']),1

    # note that Some users may mentioned MK and KS more than once
    def reducer_count_rep(self,key,counts):
        if key[0]=='mk':
            if key[1]=='post':
                yield ('mk','post'),sum(counts)
            else:
                yield ('mk','user'),1
        elif key[0]=='ks':
            if key[1]=='post':
                yield ('ks','post'),sum(counts)
            else:
                yield ('ks','user'),1

    def reducer_count_norep (self,key,counts):
        yield None,(key,sum(counts))

if __name__=='__main__':
    MRWordCount1.run()
