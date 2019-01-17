import pandas as pd
import numpy as np
from scipy.stats import norm


class Black_Scholes_model:
    def __init__(self, s, k, vol, r, T):
        if T > 0:
            d1 = (np.log(s/k) + (r+0.5*(vol**2))*T) / (vol*np.sqrt(T))
            d2 = d1 - vol * np.sqrt(T)  
        else:  
            if s >= K:
                d1 = 99999
                d2 = d1 - vol * np.sqrt(T)
            else:
                d1 = -99999
                d2 = d1 - vol * np.sqrt(T)
        
        self.s = s
        self.k = k
        self.vol = vol
        self.r = r
        self.T = T
        self.d1 = d1
        self.d2 = d2
        self.nd1 = norm.cdf(self.d1)
        self.nd2 = norm.cdf(self.d2)
        # n(-d2)
        self.nnd2 = norm.cdf(-self.d2)
    
    def call_price(self):
        call = self.s * norm.cdf(self.d1) - np.exp(-self.r * self.T) * self.k * norm.cdf(self.d2)
        self.call = call
        return self.call
    
    def put_price(self):
        put = self.k * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.s * norm.cdf(-self.d1)
        self.put = put
        return self.put


class Binomial_model:
    '''
    Using Cox-Ross-Rubinstein solution.
    '''
    def __init__(self, s, k, vol, r, T, n_period, american=False):
        self.delta_t = T / n_period
        self.up = np.exp(vol*np.sqrt(self.delta_t))
        self.down = 1 / self.up
        self.probability = (np.exp(r*self.delta_t) - self.down) / (self.up-self.down)
        self.s = s
        self.k = k
        self.vol =vol
        self.r = r
        self.T = T
        self.n_period = n_period
        self.american = american
        
        # build price tree
        price_tree = np.zeros([self.n_period+1, self.n_period+1])
        for i in range(self.n_period+1):
            for j in range(i+1):
                price_tree[j, i] = s * (self.down**j) * (self.up**(i-j))
        self.price_tree = price_tree
        
    def call_price(self):
        '''
        American calls on non-dividend paying stock should never be exercised early.
        Thus, the price of an American call must be equal to European call (under non-dividend payment).
        As a result, parameter "american" won't work while calculating call price.
        -Rangarajan K. Sundaram / Sanjiv R. Das - Derivatives p.274
        '''
        call_tree = np.zeros([self.n_period+1, self.n_period+1])
        call_tree[:, self.n_period] = np.maximum(np.zeros(self.n_period+1),
                                            self.price_tree[:, self.n_period] - self.k)
        
        for i in np.arange(self.n_period-1, -1, -1):
            for j in np.arange(0, i+1):
                call_tree[j, i] = np.exp(-self.r*self.delta_t) * (
                    self.probability*call_tree[j, i+1] + (1-self.probability)*call_tree[j+1, i+1]
                )
        self.call_tree = pd.DataFrame(call_tree)
        self.call = self.call_tree.iloc[0, 0]
        return self.call
    
    def put_price(self):
        put_tree = np.zeros([self.n_period+1, self.n_period+1])
        put_tree[:, self.n_period] = np.maximum(np.zeros(self.n_period+1),
                                           self.k - self.price_tree[:, self.n_period])
        if self.american:
            for i in np.arange(self.n_period-1, -1, -1):
                for j in np.arange(0, i+1):
                    temp_value = np.exp(-self.r*self.delta_t) * (
                        self.probability*put_tree[j, i+1] + (1-self.probability)*put_tree[j+1, i+1]
                    )
                    if temp_value > (self.k - self.price_tree[j, i]):
                        put_tree[j, i] = temp_value
                    else:
                        put_tree[j, i] = self.k - self.price_tree[j, i]
        else:
            for i in np.arange(self.n_period-1, -1, -1):
                for j in np.arange(0, i+1):
                    temp_value = np.exp(-self.r*self.delta_t) * (
                        self.probability*put_tree[j, i+1] + (1-self.probability)*put_tree[j+1, i+1]
                    )
                    put_tree[j, i] = temp_value
        self.put_tree = pd.DataFrame(put_tree)
        self.put = self.put_tree.iloc[0, 0]
        return self.put


class Monte_Carlo_simulation:
    '''
    Price of an asset follows a geometric Brownian motion.
    '''
    def __init__(self, s, k, vol, r, T, n_simulaton):
        self.s = s
        self.k = k
        self.vol =vol
        self.r = r
        self.T =T
        self.n_simulaton = n_simulaton
        self.discount_factor = np.exp(-self.r * self.T)
    
    def generate_s_T(self):
        s_T = self.s * np.exp((self.r - 0.5 * self.vol**2) * self.T + 
                               self.vol * np.sqrt(self.T) * np.random.normal())
        return s_T
    
    def call_price(self):
        def call_payoff(s_T, k):
            return max(s_T-k, 0)
        
        pay_off = []
        for i in range(self.n_simulaton):
            s_T = self.generate_s_T()
            pay_off.append(call_payoff(s_T, self.k))
        
        call = self.discount_factor * (sum(pay_off) / float(self.n_simulaton))
        self.call = call
        return self.call

    def put_price(self):
        def put_payoff(s_T, k):
            return max(k-s_T, 0)
        
        pay_off = []
        for i in range(self.n_simulaton):
            s_T = self.generate_s_T()
            pay_off.append(put_payoff(s_T, self.k))
        
        put = self.discount_factor * (sum(pay_off) / float(self.n_simulaton))
        self.put = put
        return self.put