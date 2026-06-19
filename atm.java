import java.util.Scanner;

public class ATM {
    private BankAccount account;
    private Scanner scanner;

    public ATM(BankAccount account) {
        this.account = account;
        this.scanner = new Scanner(System.in);
    }

    public void displayMenu() {
        System.out.println("\n" + "=".repeat(50));
        System.out.println("        ATM INTERFACE");
        System.out.println("=".repeat(50));
        System.out.println("1. Check Balance");
        System.out.println("2. Deposit");
        System.out.println("3. Withdraw");
        System.out.println("4. Account Info");
        System.out.println("5. Exit");
        System.out.println("=".repeat(50));
        System.out.print("Enter your choice: ");
    }

    public void run() {
        System.out.println("\n" + "=".repeat(50));
        System.out.println("   WELCOME TO DECODELABS ATM");
        System.out.println("=".repeat(50));

        System.out.print("Enter your PIN: ");
        String pin = scanner.nextLine();

        if (!account.validatePin(pin)) {
            System.out.println(" Invalid PIN! Access denied.");
            return;
        }

        System.out.println(" Access granted. Welcome, " + account.getAccountHolder() + "!");

        while (true) {
            displayMenu();
            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1:
                    System.out.println("\n" + "-".repeat(40));
                    account.displayBalance();
                    System.out.println("-".repeat(40));
                    break;

                case 2:
                    System.out.print("\nEnter deposit amount: $");
                    double depositAmount = scanner.nextDouble();
                    scanner.nextLine();
                    System.out.println("-".repeat(40));
                    account.deposit(depositAmount);
                    System.out.println("-".repeat(40));
                    break;

                case 3:
                    System.out.print("\nEnter withdrawal amount: $");
                    double withdrawAmount = scanner.nextDouble();
                    scanner.nextLine();
                    System.out.println("-".repeat(40));
                    account.withdraw(withdrawAmount);
                    System.out.println("-".repeat(40));
                    break;

                case 4:
                    account.displayAccountInfo();
                    break;

                case 5:
                    System.out.println("\n Thank you for using DecodeLabs ATM!");
                    System.out.println(" Goodbye!");
                    scanner.close();
                    return;

                default:
                    System.out.println("\n Invalid choice! Please try again.");
            }
        }
    }

    public static void main(String[] args) {
        BankAccount account = new BankAccount("DL-1001", "Aiman Zahoor", "1234");
        ATM atm = new ATM(account);
        atm.run();
    }
}