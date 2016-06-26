#!/usr/bin/env python
# coding=utf-8

"""
Avalance allocation method:
Apply all extra princial to the highest interest rate loan
"""

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



if __name__ == '__main__':
    from mortgage import Fixed
    import copy

    budget = 1000 # monthly budget

    # a simple sim of one loan (to shoq proof of concept)
    # ex = Fixed(loan=110000.0, r=.0375, months=360)
    # while ex.loan_complete() == False:
    #     amt = budget - ex.payment
    #     ex.makePayment(amt)

    # can we optimize payments to multiple loans?
    loan1 = Fixed(loan=8742.83, r=0.085, months=240)
    loan2 = Fixed(loan=5511.13, r=0.068, months=240)
    loan3 = Fixed(loan=9682.62, r=0.068, months=240)
    loan4 = Fixed(loan=5511.13, r=0.068, months=240)
    loan5 = Fixed(loan=9144.04, r=0.068, months=240)
    loan6 = Fixed(loan=6761.26, r=0.085, months=240)
    loan7 = Fixed(loan=5562.55, r=0.068, months=240)
    loan8 = Fixed(loan=8661.62, r=0.068, months=240)
    loan9 = Fixed(loan=13114.05, r=0.079, months=240)

    loan_list = [loan1,loan2,loan3,loan4,loan5,loan6,loan7,loan8,loan9]

    loan_list_a = copy.deepcopy(loan_list)
    loan_list_b = copy.deepcopy(loan_list)

    #===========================================================================
    # simulations
    #===========================================================================

    # avalanche using select_loan_rate
    print('='*10,'avalanche method','='*10)
    ava = avalanche(loan_list_a,budget,select_loan_rate)
    avalanche_summary(ava)
    print('Total Payments\t\tInterest Paid')
    print(totals(ava))

    # avalanche using select_loan_pmt
    print('='*10,'interest payment method','='*10)
    int_pmt = avalanche(loan_list_b,budget,select_loan_pmt)
    avalanche_summary(int_pmt)
    print('Total Payments\t\tInterest Paid')
    print(totals(int_pmt))
