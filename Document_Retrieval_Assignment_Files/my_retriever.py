import math

class Retrieve:
    d_length = {}#The key is the document id, the value is the denominator of the corresponding similarity calculation before sqrt
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index, termWeighting):
        self.index = index
        self.termWeighting = termWeighting
        self.docu_length()

    def docu_length(self):
        """Record dictionary d_length based on different configurations """
        idf = self.inverse_document_frequency()
        for term,id_count in self.index.items():
            for id,count in id_count.items():
                if self.termWeighting == 'binary':
                    if id not in self.d_length:
                        self.d_length[id] = 1
                    else:
                        self.d_length[id] += 1
                elif self.termWeighting == 'tf':
                    if id not in self.d_length:
                        self.d_length[id] = count**2
                    else:
                        self.d_length[id] += count**2
                else:
                    if id not in self.d_length:
                        self.d_length[id] = (count * idf[term]) ** 2
                    else:
                        self.d_length[id] += (count * idf[term]) ** 2

    # Method performing retrieval for specified query
    def forQuery(self, query):
              
        if self.termWeighting == 'binary':
            return self.termweighting_binary(query)
        elif self.termWeighting == 'tf':
            return self.termweighting_tf(query)
        elif self.termWeighting == 'tfidf':
            return self.termweighting_tfidf(query)
        else:
            print("warning")
    
    
    def candidate_id(self, query):
        """Iterate over the index, return all the document id containing the term in query"""
        C_id = []
        for terms in query:
            for term in self.index:
                if terms == term:
                    id = list(self.index[term].keys())
                    for i in id:
                        C_id.append(i)
        return C_id

    
    def candidate_dict(self, query):
        """Record dictionary C_dict, the values in the dictionary is the number of times 
        that term appears in the document corresponding to a document ID"""
        C_dict = {}
        for term in query:
            if term in self.index:
                for id,count in self.index[term].items():
                    if id not in C_dict:
                        C_dict[id] = {term:count}
                    else:
                        C_dict[id][term] = count
        return C_dict
            
        

    
    def termweighting_binary(self, query):
        """Calculate weights based on Binary term weighting scheme.
        Returns the document ID from high to low related to Query based on similarity calculation"""
        C_id = self.candidate_id(query)
        id_count = {}# Keys is the candidate document id, the corresponding values is the number of the term that appears in both query and index.
        rank = {}#This dictionary record values for the similarity corresponding to the candidate document id.
        rank_list = []#Rank the candidate document id according to the similarity
        for i in C_id:
            if i not in id_count:
                id_count[i] = 1
            else:
                id_count[i] += 1
        for id,count in id_count.items():
            sim = count/ math.sqrt(self.d_length[id])
            rank.update({id:sim})
        order = sorted(rank.items(), key=lambda x: x[1], reverse=True)
        for n in order:
            rank_list.append(n[0])
        return rank_list   
               
     

            
    def termweighting_tf(self, query):
        """Calculate weights based on TF term weighting scheme.
        Returns the document ID from high to low related to Query based on similarity calculation"""
        C_id = set(self.candidate_id(query))
        C_dict = self.candidate_dict(query)
        rank = {}#This dictionary record values for the similarity corresponding to the candidate document id.
        rank_list = []#Rank the candidate document id according to the similarity
        for id in C_id:
            score = 0
            for term in query:
                if term in C_dict[id]:
                    score += C_dict[id][term] * query[term]
            sim = score/ math.sqrt(self.d_length[id])
            rank.update({id:sim})
        order = sorted(rank.items(), key=lambda x: x[1], reverse=True)
        for n in order:
            rank_list.append(n[0])
        return rank_list  

           
        
    def termweighting_tfidf(self, query):
        """Calculate weights based on TFIDF term weighting scheme.
        Returns the document ID from high to low related to Query based on similarity calculation"""
        idf = self.inverse_document_frequency()
        C_id = set(self.candidate_id(query))
        C_dict = self.candidate_dict(query)
        rank = {}#This dictionary record values for the similarity corresponding to the candidate document id.
        rank_list = []#Rank the candidate document id according to the similarity
        for id in C_id:
            score = 0
            for term in query:
                if term in C_dict[id]:
                    score += C_dict[id][term]*idf[term] * query[term]*idf[term]
            sim = score/ math.sqrt(self.d_length[id])
            rank.update({id:sim})
        order = sorted(rank.items(), key=lambda x: x[1], reverse=True)
        for n in order:
            rank_list.append(n[0])
        return rank_list              
        
        
    def inverse_document_frequency(self):
        """Returns the inverse document frequency of term"""
        document_frequency = {}
        idf = {} #This dictionary record the IDF value for each term.
        id = []
        for term in self.index:
            document_frequency.update({term:len(self.index[term])})#number of documents containing terms
            for Did in self.index[term]:
                id.append(Did)
        D = len(set(id)) #total number of documents in collection     
        for terms in self.index:
            count = math.log(D/document_frequency[terms],10)
            idf.update({terms:count})
        return idf
                    
        

