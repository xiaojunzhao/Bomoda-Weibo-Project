import re
import time
import heapq
from dateutil import parser
from mrjob.job import MRJob
from mrjob.job import MRStep
from mrjob.protocol import JSONValueProtocol


class MRWordCount2_1(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol


    def steps(self):
        return [
        MRStep(mapper=self.mapper_getpost,reducer=self.reducer_countpost),
        MRStep(reducer = self.reducer_find_max)
        ]

    def mapper_getpost(self,key,post_list):
        for post in post_list:
            creationDate = post['created_at']
            # create date tuple (month,day,year,hour) and reconstruct the time string
            dateTuple = parser.parse(creationDate).timetuple()
            date = dateTuple[0:3]
            hour = dateTuple[3]
            newCreationDate = '/'.join([str(x) for x in date])
            #yield (newCreationDate,1)
            text = post['text']
            newText = re.sub(r'[^A-Za-z\s]+','',text)\
                         .lower()
            if re.match('michael kors',newText):
                yield (newCreationDate,'michael kors'),1
            if re.match('kate spade',newText):
                yield (newCreationDate,'kate spade'),1

    def reducer_countpost(self,key,counts):
        yield key[1],(key,sum(counts))

    def reducer_find_max(self,key,post_count_pairs):
        yield None,max(post_count_pairs,key=lambda i: i[1])

if __name__=='__main__':
    MRWordCount2_1.run()
