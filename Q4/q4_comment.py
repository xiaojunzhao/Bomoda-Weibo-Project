import re
import time
from dateutil import parser
from mrjob.job import MRJob
from mrjob.job import MRStep
from mrjob.protocol import JSONValueProtocol


class MRWordCount4(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def steps(self):
        return [
        MRStep(mapper=self.mapper_getcomment,reducer=self.reducer_countcomment),
        MRStep(reducer=self.reducer_sort)
        ]

    def mapper_getcomment(self,key,comment_list):
        for comment in comment_list:
            try:
                creationDate = comment['created_at']
                dateTuple = parser.parse(creationDate).timetuple()
                date = dateTuple[0:3]
                newCreationDate = '/'.join([str(x) for x in date])
                status_text = comment['status']['text']
                filtered_status_text = re.sub(r'[^A-Za-z\s]+','',status_text)\
                                        .lower()
                if re.match('michael kors',filtered_status_text):
                    yield ('mk',newCreationDate),1
                if re.match('kate spade',filtered_status_text):
                    yield ('ks',newCreationDate),1
            except:
                pass

    def reducer_countcomment(self,key,counts):
        yield None,(key,sum(counts))

    def reducer_sort(self,_,count_pairs):
        count_pairs = sorted(count_pairs,key=lambda x:(x[0][0],x[0][1]))
        yield None,count_pairs

if __name__=='__main__':
    MRWordCount4.run()
