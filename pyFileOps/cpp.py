#!/usr/bin/python

def skipTo(s,i0,c='}'):
    for i in xrange(i0,len(s)):
        #print "|",s[i],"|",i
        if(s[i]==c): break
    return i

def tillToken(s,i0):
    for i in xrange(i0,len(s)):
        c=s[i]
        if( not(c.isalnum() or c=='_') ): return i

whiteChars      = set([' ','\n','\t'])
identifierChars = set([c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz012345678'])
specialChars    = set([c for c in '.:,;#+/-*%^!&|=<>{}[]()'])

bindingOps = set( ['.',"->",'::'] )

keywords=[
"alignas","alignof","and","and_eq","asm","atomic_cancel","atomic_commit","atomic_noexcept","auto","bitand","bitor","bool","break","case","catch","char","char16_t","char32_t","class","compl","concept","const","constexpr",
"const_cast","continue","co_await","co_return","co_yield","decltype","default","delete","do","double","dynamic_cast","else","enum","explicit","export","extern","false","float","for","friend","goto","if","import","inline",
"int","long","module","mutable","namespace","new","noexcept","not","not_eq","nullptr","operator","or","or_eq","private","protected","public","register","reinterpret_cast","requires","return","short","signed","sizeof",
"static","static_assert","static_cast","struct","switch","synchronized","template","this","thread_local","throw","true","try","typedef","typeid","typename","union","unsigned","using","virtual","void","volatile","wchar_t",
"while","xor","xor_eq",
"NULL",
"ifndef","include", "endif"
]

class CppCrawler:
    iid0       = -1 # start of current identifier
    iid1       = -1 # start of current operator
    scopeLevel = 0
    #iid1=0
    prevId = ""
    
    def load(self,fname):
        with open(fname,'r') as f:
            self.sfile =  f.read()
        #print self.sfile
    
    def isIdentifier(self, s ):
        return not ( ( s in keywords) or s[0].isdigit() )
        
    def finishIdentifier(self,i):
        if self.iid0>0:
            s = self.sfile[self.iid0:i]
            if( self.isIdentifier( s ) ):
                #print s
                lastOp = self.sfile[self.iid1:self.iid0].strip()
                #if lastOp != "":
                #    print lastOp,s
                if lastOp in bindingOps:
                    print lastOp,s
                #if self.prevId=="class":
                #    print "class", s
            self.prevId = s
            self.iid1   = i
        self.iid0 = -1
    
    def crawl(self):
        i=0
        s = self.sfile
        while i<len(s):
            c=s[i]
            #print c
            if c in identifierChars:
               if(self.iid0<0):
                    self.iid0=i
            elif c in  whiteChars:
                self.finishIdentifier(i)
            elif c in specialChars:
                self.finishIdentifier(i)
                if c=='#':
                    i=skipTo(self.sfile,i,c='\n'); continue
                elif   c=='{':
                    self.scopeLevel+=1
                elif c=='}':
                    self.scopeLevel-=1
            i+=1


if __name__ == "__main__":
    crawler = CppCrawler()
    #crawler.load("../../SimpleSimulationEngine/cpp/common/dynamics/DynamicOpt.h")
    crawler.load("/home/prokop/git/SimpleSimulationEngine/cpp/common/dynamics/Molecular/MoleculeType.cpp")
    #crawler.load("/home/prokop/git/SimpleSimulationEngine/cpp/common/dynamics/DynamicOpt.h")
    crawler.crawl()

