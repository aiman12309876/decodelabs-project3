public class BankAccount {
    private String accountNumber;
    private String accountHolder;
    private double balance;
    private String pin;

    public BankAccount(String accountNumber, String accountHolder, String pin) {
        this.accountNumber = accountNumber;
        this.accountHolder = accountHolder;
        this.pin = pin;
        this.balance = 0.0;
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public String getAccountHolder() {
        return accountHolder;
    }

    public double getBalance() {
        return balance;
    }

    public boolean validatePin(String enteredPin) {
        return this.pin.equals(enteredPin);
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println(" Deposit successful! New balance: $" + balance);
        } else {
            System.out.println(" Invalid deposit amount!");
        }
    }

    public void withdraw(double amount) {
        if (amount <= 0) {
            System.out.println(" Invalid withdrawal amount!");
        } else if (amount > balance) {
            System.out.println(" Insufficient balance! Available: $" + balance);
        } else {
            balance -= amount;
            System.out.println(" Withdrawal successful! New balance: $" + balance);
        }
    }

    public void displayBalance() {
        System.out.println(" Current Balance: $" + balance);
    }

    public void displayAccountInfo() {
        System.out.println("\n Account Information");
        System.out.println("-" * 40);
        System.out.println(" Account Number: " + accountNumber);
        System.out.println(" Account Holder: " + accountHolder);
        System.out.println(" Balance: $" + balance);
        System.out.println("-" * 40);
    }
}