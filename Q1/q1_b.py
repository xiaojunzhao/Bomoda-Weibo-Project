import re
import heapq
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONValueProtocol
class MRWordCount1_2(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def steps(self):
        return [
        MRStep(mapper=self.mapper_get_posts,
                reducer=self.reducer_count_posts),
        MRStep(mapper_init=self.init_get_10,
               mapper = self.mapper_nation_gettop10,
               mapper_final = self.mapper_final_nation_gettop10,
               reducer_init = self.reducer_init,
               reducer = self.reducer_get_top10,
               reducer_final = self.reducer_final)
    ]    

    # First MRJob
    def mapper_get_posts(self,key,post):
        for item in post:
            userid = item['user']['id']
            provinceid =item['user']['province']
            if provinceid!="400" and provinceid!="100":
                yield ('province',provinceid),1
                yield ('nation','0'),1
            elif provinceid=='400':
                yield ('nation',item['user']['city']),1
            yield ('user',userid),1
  
    def reducer_count_posts(self,key,counts):
        if key[0]=='user':
            yield "user",(sum(counts),key)
        elif key[0]=='province':
            yield "province",(sum(counts),key)
        elif key[0]=='nation':
            yield 'nation',(sum(counts),key)

    # Second MRJob
    def init_get_10(self):
        self.user = []
        self.province = []
        self.nation = []

    def mapper_nation_gettop10(self,key,post_count_pairs):
        if key=='user':
            heapq.heappush(self.user,post_count_pairs)
        elif key=='province':
            heapq.heappush(self.province,post_count_pairs)
        elif key=='nation':
            heapq.heappush(self.nation,post_count_pairs)

    def mapper_final_nation_gettop10(self):
        user_largest = heapq.nlargest(10,self.user)
        province_largest = heapq.nlargest(10,self.province)
        nation_largest = heapq.nlargest(10,self.nation)
        for count, key in user_largest:
            yield ('user_heap',(count,key))
        for count,key in province_largest:
            yield ('province_heap',(count,key))
        for count,key in nation_largest:
            yield ('nation_heap',(count,key))

    def reducer_init(self):
        self.top10_userlist=[]
        self.top10_provincelist=[]
        self.top10_nationlist = []

    def reducer_get_top10(self,key,top10):
        if key=='user_heap':
            for post_count in top10:
                heapq.heappush(self.top10_userlist,(post_count[0],post_count[1]))
        elif key=='province_heap':
            for post_count in top10:
                heapq.heappush(self.top10_provincelist,(post_count[0],post_count[1])) 
        elif key=='nation_heap':
            for post_count in top10:
                heapq.heappush(self.top10_nationlist,(post_count[0],post_count[1]))

    def reducer_final(self):
        user_largest = heapq.nlargest(10,self.top10_userlist)
        user_posts = [(key,int(count)) for count,key in user_largest]
        province_largest = heapq.nlargest(10,self.top10_provincelist)
        province_posts = [(key,int(count)) for count,key in province_largest]
        nation_largest = heapq.nlargest(10,self.top10_nationlist)
        nation_posts = [(key,int(count)) for count,key in nation_largest]

        yield (None,user_posts)
        yield (None,province_posts)
        yield (None,nation_posts)


if __name__=='__main__':
    MRWordCount1_2.run()
    