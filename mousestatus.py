class mousestatus(object):
    # Step1. Process mouse key events and return self.event which indicates the click attempt.
    # Step2. Parent class processes the click attempt and return True/False for success or not.
    # Step3. Process the click.
    def __init__(self, scheme=0):
        self.scheme=scheme
        # click counter for universal use
        # 0: nothing
        # 1-3: left round, right round, middle round
        # 4-9: left fail, left success, right fail, right success, chord fail, chord success
        self.clicks=[0]*13 

        if scheme==0: # left, right, left+right=chord
            # mouse states
            # 0. initial state
            # 1. error
            # 2. left down after initial state
            # 3. left up and pending
            # 4. right down after initial state and pending
            # 5. right down with successful right click or chord up by left
            # 6. right down with failed right click
            # 7. chord down
            # 8. chord up by left and pending
            # 9. chord up by right and pending
            # 10. chord up by right
            #              0 1 2 3 4 5 6 7 8  9 10
            self.LDstatus=[2,1,1,1,1,7,7,1,1, 1, 1]
            self.LUstatus=[1,1,3,1,1,1,1,8,1, 1, 0]
            self.RDstatus=[4,1,7,1,1,1,1,1,1, 1, 7]
            self.RUstatus=[1,1,1,1,1,0,0,9,1, 1, 1]
            self.Tstatus =[1,1,1,0,5,1,1,1,5,10, 1]
            self.Fstatus =[1,1,1,0,6,1,1,1,5,10, 1]
            self.LDcount =[1,0,0,0,0,1,1,0,0, 0, 0]
            self.LUcount =[0,0,0,0,0,0,0,0,0, 0, 0]
            self.RDcount =[1,0,1,0,0,0,0,0,0, 0, 1]
            self.RUcount =[0,0,0,0,0,0,6,0,0, 0, 0]
            self.Tcount  =[0,0,0,5,7,0,0,0,9, 9, 0]
            self.Fcount  =[0,0,0,4,0,0,0,0,8, 8, 0]

            self.event   =[0,1,0,2,3,0,0,0,4, 4, 0]
            # return events
            # 0. nothing
            # 1. error
            # 2. left attempt
            # 3. right attempt
            # 4. chord attempt
            
    def leftdown(self):
        s=self.status
        self.clicks[self.LDcount[s]]+=1
        self.status=self.LDstatus[s]
        return self.event[self.status]
    def leftup(self):
        s=self.status
        self.clicks[self.LUcount[s]]+=1
        self.status=self.LUstatus[s]
        return self.event[self.status]
    def rightdown(self):
        s=self.status
        self.clicks[self.RDcount[s]]+=1
        self.status=self.RDstatus[s]
        return self.event[self.status]
    def rightup(self):
        s=self.status
        self.clicks[self.RUcount[s]]+=1
        self.status=self.RUstatus[s]
        return self.event[self.status]
    def clickresult(self,r):
        s=self.status
        if r:
            self.clicks[self.Tcount[s]]+=1
            self.status=self.Tstatus[s]
        else:
            self.clicks[self.Fcount[s]]+=1
            self.status=self.Fstatus[s]

    def lcl(self):
        return self.clicks[4]+self.clicks[5]
    def lce(self):
        return self.clicks[5]
    def rcl(self):
        return self.clicks[6]+self.clicks[7]
    def rce(self):
        return self.clicks[7]
    def dcl(self):
        return self.clicks[8]+self.clicks[9]
    def dce(self):
        return self.clicks[9]
    def cl(self):
        return self.lcl()+self.rcl()+self.dcl()
    def ce(self):
        return self.lce()+self.rce()+self.dce()