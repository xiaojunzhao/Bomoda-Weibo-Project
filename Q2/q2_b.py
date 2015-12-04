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
        MRStep(mapper=self.mapper_getpost,reducer=self.reducer_counthourpost),
        MRStep(reducer = self.reducer_find_max)
        ]

    def mapper_getpost(self,key,post_list):
        for post in post_list:
            creationDate = post['created_at']
            # create date tuple (month,day,year,hour) and reconstruct the time string
            dateTuple = parser.parse(creationDate).timetuple()
            hour = str(dateTuple[3])
            yield (hour,1)

    def reducer_counthourpost(self,key,counts):
        yield None,(key,sum(counts))

    def reducer_find_max(self,key,post_count_pairs):
        yield None,max(post_count_pairs,key=lambda i: i[1])

if __name__=='__main__':
    MRWordCount2_1.run()
