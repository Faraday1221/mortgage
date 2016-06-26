# Mortgage

This project was created to help evaluate the cost of various mortgages. The mortgage classes in **mortgage.py** are from John Guttag's excellent book *Introduction to Computation and Programing using Python*. The **avalance.py** file contains a host of helper functions used to simulate and evaluate various mortgages based on the Mortgage objects in the mortgage.py file.

It should be noted that this simulation will potentially overpay a final payments. This overpayment can present some confusing end results (e.g. the total sum paid across multiple mortgages will be divisible by the budget amount).

## Other Uses
The loans are all fairly generic, this can be used for mortgages, but also car payments, or student loans.

## Running the simulation
A simple simulation can be performed as follows:


    budget = 1000
    ex = Fixed(loan=110000.0, r=.0375, months=360)
    while ex.loan_complete() == False:
        amt = budget - ex.payment
        ex.makePayment(amt)

A comparison of loans can be performed as follows:

    loan1 = Fixed(loan=25000.0, r=0.03, months=60)
    loan2 = Fixed(loan=2000.0, r=0.24, months=12)

    loan_list = [loan1,loan2]
    budget = 1000

    # avalanche using select_loan_rate
    ava = avalanche(loan_list_a,budget,select_loan_rate)
    avalanche_summary(ava)
    print('Total Payments\t\tInterest Paid')
    print(totals(ava))

## Two Approaches
The avalanche function can take two methods for selecting which loan to pay-off, keeping in mind that the loan will be paid off in its entirety before the algorithm chooses another loan. Examples as follows:

**select_loan_rate**

    ava = avalanche(loan_list_a,budget,select_loan_rate)
    avalanche_summary(ava)

**select_loan_pmt**

    int_pmt = avalanche(loan_list_b,budget,select_loan_pmt)
    avalanche_summary(int_pmt)
