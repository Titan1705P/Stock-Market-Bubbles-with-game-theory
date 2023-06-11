import matplotlib.pyplot as plt
import numpy as np
class Market:
    def __init__(self,init_mom=90,init_con = 10 ):
        self.init_mom = init_mom
        self.init_con = init_con
        self.perc_val = 1000;#the hype price target
        self.CMP = 100;# CMP
        self.fundm = 100; #assuming the market is initially trading at the fundamental value
        self.p_crash = self.fundm/10 #later when the crash starts coming, pessimists feel stock value will be nearly wiped out
        self.peakprice = 0
        self.mom = self.init_mom #number of momentum and cont traders at any time
        self.con = self.init_con
        self.demand_excess = self.mom/self.con #assuming all momentum traders buy and contr sell, no of
        self.payoff_b_m = self.perc_val - self.CMP #replication factor = payoff B,S for a buyer of momentum strategy
        self.payoff_s_c = self.CMP-self.fundm #replication factor for a seller of contrarian strategy
        self.payoff_b_c = 0 #payoff of contrarian buyer, will be assigned later
        self.pess = 0
        self.init_pess =0
        self.prices = []
        self.timesteps = []
        self.moms = []
        self.cons = []
        self.pesses = []


    def time_step_boom(self):
        self.mom = int(self.mom*(1+0.01*self.payoff_b_m/self.CMP))#the incentive to become M relative to the fundamental val
        self.con = int(self.con*(1+0.3*self.payoff_s_c/self.CMP))
        self.demand_excess = self.mom/self.con
        #updating the measures
        

        

        markup = min(1.2,1+0.2*(self.demand_excess/10))#upper circuit limit is 20%, max markup of 20% for demand excess of 10
        self.CMP = self.CMP*markup
        
        self.perc_val = self.perc_val*self.mom/self.init_mom  #the percieved value scales directly with relative increase in buyers

        #nextstep replication factors
        self.payoff_b_m = self.perc_val - self.CMP #replication factor = payoff B,S for a buyer of momentum strategy
        self.payoff_s_c = self.CMP-self.fundm 
        print(self.CMP)

    def time_step_bust(self):
        
        self.payoff_s_p = max(self.CMP-self.p_crash,0)#payoff of a pessimist seller,incentive to sell
        
                
        self.payoff_b_c = max(self.CMP - self.peakprice/2,0) #contrarian buyer short sold at an avg price of
        self.pess = int(self.pess*(1+0.01*self.payoff_s_p/self.CMP))#the incentive to become M relative to the fundamental val
        self.con = int(self.con*(1+0.3*self.payoff_b_c/self.CMP))
        self.supply_excess = self.pess/self.con
        #updating the measures
        

        

        markdown = max(0.8,1-0.2*(self.supply_excess/10))#lower circuit limit is 20%, max markdown of 20% for supply excess of 10
        self.CMP = self.CMP*markdown
        
        self.p_crash = self.p_crash*self.init_pess/self.pess  #the percieved final value of pessimists decreases directly with relative increase in pessimists

        
        print(self.CMP)    
    def run_model(self):
        
        #the boom phase
        for i in range(10):
            self.prices.append(self.CMP)
            self.timesteps.append(i)
            self.moms.append(self.mom)
            self.cons.append(self.con)
            self.time_step_boom()
            self.pesses.append(0)
        self.pess = int(self.mom*0.1)
        self.init_pess = self.pess
        self.peakprice = self.CMP
        #the burst phase
        for i in range(10,141):
            self.time_step_bust()
            self.timesteps.append(i)
            self.pesses.append(self.pess)
            self.prices.append(self.CMP)
            self.cons.append(self.con)


       
        


model = Market(90,10)
model.run_model()
#print(model.cons)
plt.plot(model.timesteps,model.prices)
#plt.plot(model.timesteps,model.moms)
#plt.plot(model.timesteps,model.cons)


#plt.title("Number of Contrarians")
#plt.title("Number of Optimists")
plt.title("Stock Price")



plt.grid()
plt.xticks(np.arange(min(model.timesteps), max(model.timesteps)+1, 10))
plt.yticks(np.arange(min(model.prices), max(model.prices)+1, 20))

plt.show()