# -*- coding: utf-8 -*-
"""
This is a very minor modification from the Guttag Object he uses as an
example in his book.

Created on Mon Oct  5 22:42:46 2015
@author: jonbruno
"""
from __future__ import print_function
import numpy as np
import operator


#page 147 plotting mortgages, fig 11.1 and 11.3
def findPayment(loan, r, m):
    """Assumes: loan and r are floats, m an int
       Returns the montly payment for a mortgage of size
       loan at a monthly rate of r and m months"""
    return loan*((r*(1+r)**m)/((1+r)**m-1))

class Mortgage(object):
    """Abstract class for building different kinds of mortgages"""
    def __init__(self, loan, annRate, months):
        """Create a new mortgage"""
        self.loan = loan
        self.rate = annRate/12.0
        self.months = months
        self.paid = [0.0] #
        self.owed = [loan]
        self.payment = findPayment(loan, self.rate, months) #Min Payment
        self.interest = [0.0]
        self.legend = None #description of mortgage
        self.complete = self.loan_complete()
    def makePayment(self, amt=0.0):
        """Make a payment, if amt > 0.0 pay extra towards principal"""
        period_payment = self.payment + amt
        self.paid.append(period_payment)
        reduction = period_payment - self.owed[-1]*self.rate
        self.owed.append(self.owed[-1] - reduction)
        self.interest.append(self.owed[-1]*self.rate)
        self.complete = self.loan_complete()
    def getTotalPaid(self):
        """Return the total amount paid so far"""
        return sum(self.paid)
    def getInterestPaid(self):
        """Return the total interest paid so far"""
        return sum(self.interest)
    def __str__(self):
        return self.legend


    def sim_summary(self):
        annual_rate = self.rate*12.0
        months_paid = len(self.paid)
        total_paid = self.getTotalPaid()
        interest_paid = self.getInterestPaid()
        self.sim_list = [annual_rate,months_paid,total_paid,interest_paid]
        return self.sim_list
    def print_sim_summary(self):
        self.sim_list  = self.sim_summary()
        print('Annual Rate:\t\t {0}'.format(self.sim_list[0]))
        print('Months Paid:\t\t {0}'.format(self.sim_list[1]))
        print('Total Paid:\t\t {0}'.format(self.sim_list[2]))
        print('Total Interest:\t\t {0}'.format(self.sim_list[3]))
        print('\n')

    def sim(self,amt=0.0):
        while self.loan_complete() == False:
            self.makePayment(amt)

    def loan_complete(self):
        if self.owed[-1] <= 0:
            self.complete = True
        else:
            self.complete = False
        return self.complete


class Fixed(Mortgage):
    def __init__(self, loan, r, months):
        Mortgage.__init__(self, loan, r, months)
        self.legend = 'Fixed, ' + str(r*100) + '%'

class FixedWithPts(Mortgage):
    def __init__(self, loan, r, months, pts):
        Mortgage.__init__(self, loan, r, months)
        self.pts = pts
        self.paid = [loan*(pts/100.0)]
        self.legend = 'Fixed, ' + str(r*100) + '%, '\
                        + str(pts) + ' points'

class TwoRate(Mortgage):
    def __init__(self, loan, r, months, teaserRate, teaserMonths):
        Mortgage.__init__(self, loan, teaserRate, months)
        self.teaserMonths = teaserMonths
        self.teaserRate = teaserRate
        self.nextRate = r/12.0
        self.legend = str(teaserRate*100)\
                        + '% for ' + str(self.teaserMonths)\
                        + ' months, then ' + str(r*100) + '%'
    def makePayment(self):
        if len(self.paid) == self.teaserMonths + 1:
            self.rate = self.nextRate
            self.payment = findPayment(self.owed[-1], self.rate,
                                       self.months - self.teaserMonths)
        Mortgage.makePayment(self)


if __name__ == '__main__':

    #===========================================================================
    # simulations
    #===========================================================================
    # a simple simulation
    ex = Fixed(loan=110000.0, r=.0375, months=360)

    budget = 1000 # monthly budget

    # a simple sim of one loan (to shoq proof of concept)
    # while ex.loan_complete() == False:
    #     amt = budget - ex.payment
    #     ex.makePayment(amt)

    # can we optimize payments to multiple loans
    loan1 = Fixed(loan=8742.83, r=0.085, months=240)
    loan2 = Fixed(loan=5511.13, r=0.068, months=240)
    loan3 = Fixed(loan=9682.62, r=0.068, months=240)
    loan4 = Fixed(loan=5511.13, r=0.068, months=240)
    loan5 = Fixed(loan=9144.04, r=0.068, months=240)
    loan6 = Fixed(loan=6761.26, r=0.085, months=240)
    loan7 = Fixed(loan=5562.55, r=0.068, months=240)
    loan8 = Fixed(loan=8661.62, r=0.068, months=240)
    loan9 = Fixed(loan=13114.05, r=0.079, months=240)


    loan_list = [loan1,loan2,loan3,
                 loan4,loan5,loan6,
                 loan7,loan8,loan9]

    # a = pd.Series(loan_list)
    # loan_list[0].run_sim()
    # b = pd.Series([loan.complete==False for loan in loan_list])
    # final = a[a[b]]

    # we need to know how to allocate the budget
    '''avalance allocation method
       apply all extra princial to the highest interest rate loan '''

    # if loan is not complete add it to the list that we will evaluate
    def check_loan_status(loan_list):
        """check loans to see if they are complete,
           return a list of incomplete loans"""
        incomplete_loans = []
        for loan in loan_list:
            if loan.complete == False:
                incomplete_loans.append(loan)
        return incomplete_loans

    def calculate_prin_pmt(loan_list, budget):
        """return the amount we can put towards the loan principal"""
        # calculate the monthly min
        monthly_min = sum([loan.payment for loan in loan_list])
        # calculate the additional principal payment
        amt = budget - monthly_min
        return amt

    def select_loan_rate(loan_list):
        """select the loan with the highest interest rate
           and lowest outstanding amount,
           return the loan object"""
        # select loans with max interest rate
        _max = max([loan.rate for loan in loan_list])
        output_list = [i for i in loan_list if i.rate == _max]
        # select the remaining loans with the lowest payment amount
        _min = min([loan.loan for loan in output_list])
        final = [i for i in output_list if i.loan == _min]
        return final[0]

    def select_loan_pmt(loan_list):
        """select the loan with the highest interest payment,
           return the loan object

           THIS COULD BE CLEANED UP"""
        # select loans with max interest payment
        _max = max([loan.rate*loan.owed[-1] for loan in loan_list])
        output_list = [i for i in loan_list if i.rate*i.owed[-1] == _max]
        return output_list[0]

    #===========================================================================
    # avalance simulation
    #===========================================================================
    def avalanche(loan_list, budget, select_loan):
        """simulate paying off loans on a budget given
           you have to select the method of selecting the loan to payoff first
        """
        # while at least 1 loan is incomplete
        while len(check_loan_status(loan_list)) > 0:
            # take all incomplete loans
            _loan_list = check_loan_status(loan_list)
            # calculate the amount of principal we can put towards
            amt = calculate_prin_pmt(_loan_list, budget)
            # find which loan to put the principal payment towards
            loan_to_pay = select_loan(_loan_list)
            # while the loan to pay is incomplete... make payments to all loans
            print(loan_to_pay)
            while loan_to_pay.complete == False:
                for _loan in _loan_list:
                    if _loan == loan_to_pay:
                        _loan.makePayment(amt)
                    else:
                        _loan.makePayment()
        return loan_list


    def avalanche_summary(loan_list):
        """prints summary results for the simulation"""
        for loan in loan_list:
            loan.print_sim_summary()

    def totals(loan_list):
        """returns a list of the simulation total paid and interest paid"""
        paid = sum([loan.sim_summary()[2] for loan in loan_list])
        interest = sum([loan.sim_summary()[3] for loan in loan_list])
        return [paid, interest]


    # # some fake loans
    # a = Fixed(1000.0,0.35,12) # credit card
    # b = Fixed(200000.0,0.035,360) # mortgage
    # c = Fixed(25000.0,0.02,60) # car loan
    # d = Fixed(20000.0, 0.04,120) # student loan

    import copy

    # loan_list_a = [a,b,c,d]
    # loan_list_b = copy.deepcopy([a,b,c,d])

    loan_list_a = copy.deepcopy(loan_list)
    loan_list_b = copy.deepcopy(loan_list)

    print('='*10,'avalanche method','='*10)
    ava = avalanche(loan_list_a,budget,select_loan_rate)
    avalanche_summary(ava)
    print(totals(ava))

    #===========================================================================
    # interst payment method
    #===========================================================================

    print('='*10,'interest payment method','='*10)
    int_pmt = avalanche(loan_list_b,budget,select_loan_pmt)
    avalanche_summary(int_pmt)
    print(totals(int_pmt))
