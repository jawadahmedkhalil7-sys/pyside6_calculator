print("=====Welcome Calculator=====")

while True:
    while True:
        try:
            number1=int(input("Enter your number: "))
            break
        except ValueError:
            print("Please ente a valid number!")
    while True:
            operator=input("Enter your operator(+ - * /): ")
            if operator in ["+","-","*","/"]:
                break
            else:
                print("Invalid operator!please enter + - * /")
    while True:
        try:
            number2=int(input("Enter your number: "))
            break
        except ValueError:
            print("Please enter a valid number!")
    if operator=="+":
        print("Result:",number1+number2)
    elif operator=="-":
        print("Result:",number1-number2)
    elif operator=="*":
        print("Result:",number1*number2)
    elif operator=="/":
        if number2==0:
            print("cannot divide by zero!")
        else:
            print("Result:",number1/number2)
    while True:
        again=input("Do you want to calculate again?(yes/no):").lower()
        if again=="yes":
            break
        elif again=="no":
            print("calculator closed")
            exit()
        else:
            print("Please enter yes or no!")